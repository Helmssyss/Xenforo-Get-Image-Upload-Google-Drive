# Authors : Arif-Helmsys , Coderx37

from io import BytesIO
from typing import Generator
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload
from mechanize import Browser
from configparser import RawConfigParser
from requests import get as requestsGetMethod

import pickle
import string
import threading
import queue
import random
import os
import json
import time

VOID = None
class LoginTHT:
    contents:list[bytes] = []
    csrfToken = ''
    @classmethod
    @property
    def __getCookies(cls) -> dict[str,str]:
        __config = RawConfigParser()
        __config.read(r".\src\.cfg")
        cookies = {}
        cookies.update({k:v for k,v in __config["THT_LOGIN_COOKIES"].items()})
        return cookies

    @classmethod
    def getThtHtmlPageContent(cls,url:list[str]) -> bytes:
        """
        Eğer Mechanize tarafında 403 hatası alınırsa ilgili web sayfasının kaynak kodlarını kaydedip, yorum satırına alınan kısmı aktif edin. Mechanize
        tarafını iptal edin
        >>> # response = ''
            # with open("indirilen_kaynak_dosyasi.html","r",encoding="utf-8") as response_file:
            #     response = response_file.read()
            # return response
        """
        print("all_link",url)
        if len(url) >= 1:
            for i in url:
                try:
                    print("link:",i)
                    br = Browser()
                    br.addheaders = [
                        ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                        ("cookie",f"xf_user={cls.__getCookies['xf-user']}; xf_tfa_trust={cls.__getCookies['xf-tfa-trust']}; xf_session={cls.__getCookies['xf-session']}")
                    ]
                    br.set_handle_robots(False)
                    br.open(i)
                    print(br._ua_handlers['_cookies'].cookiejar)
                    cls.contents.append(br.response().read())
                except Exception as e:
                    print(e)

class DriveApi:
    lock = threading.Lock()
    que = queue.Queue()
    all_link = []

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        if os.path.exists(r'.\src\token.pickle'):
            with open(r'.\src\token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(r'.\src\credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open(r'.\src\token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def run(self):
        run = True
        sample = {
            "all_link": []
        }
        if not os.path.exists(r".\src\link_manage.json"):
            with open(r".\src\link_manage.json","w",encoding="utf-8") as jfile:
                dumpedJsonObject = json.dumps(sample,indent=4)
                jfile.write(dumpedJsonObject)

        while run:
            try:
                time.sleep(1)
                print("Çalışıyor..")
                with open(r".\src\link_manage.json","r",encoding="utf-8") as jfile:
                    jsonObject = json.load(jfile)

                if len(jsonObject['all_link']) >= 1:
                    print("Link(ler) eklendi!")
                    for i in jsonObject["all_link"]:
                        self.all_link.append(i)
                    
                    jsonObject["all_link"] = []
                    with open(r".\src\link_manage.json","w",encoding="utf-8") as jfile:
                        jfile.write(json.dumps(jsonObject,indent=4))

                    LoginTHT.getThtHtmlPageContent(self.all_link)
                    self.__uploadGoogleDrive()
                    print("Tamamlandı!")

            except Exception as e:
                print(e)
                run = False

            finally:
                self.all_link.clear()
                LoginTHT.contents.clear()

    def getImages(self) -> Generator:
        try:
            for content in LoginTHT.contents:
                soup = BeautifulSoup(content,"lxml")
                for i in soup.find_all("img",attrs={"class":"bbImage"}):
                    for j in urlparse(i['data-url']).netloc.split('.'):
                        if j =="hizliresim":
                            yield i['data-url']
        except Exception as e:
            print(e)

    def readAllImageContents(self,que:queue.Queue):
        picURL = que.get()
        imgName = ''.join(i for i in random.choices(string.ascii_uppercase,k=20))
        try:
            response = requestsGetMethod(picURL)
            imgLoad = BytesIO(response.content)
            file_metadata  = {"name": imgName+'.png',"mimeType":'image/png'}
            media_body = MediaIoBaseUpload(imgLoad, resumable=True,mimetype="image/png")
            self.service = build('drive', 'v3', credentials=self.creds)
            self.service.files().create(body=file_metadata, media_body=media_body).execute()
            self.lock.acquire()
            print(f" {picURL} Başarıyla Google Drive'a Kaydedildi",threading.current_thread().name)
            self.lock.release()
        except Exception as e:
            print(f" {picURL} Google Drive'a Kaydetme Başarısız!",threading.current_thread().name,e,picURL)
            pass

        finally:
            que.task_done()

    def __uploadGoogleDrive(self) -> VOID:
        threads:list[threading.Thread] = []
        print("\n")
        for picture in set(self.getImages()):
            try:
                self.que.put(picture)
                print(f" {picture} Başarıyla Alındı")
                t = threading.Thread(target=self.readAllImageContents,args=(self.que,))
                threads.append(t)

            except Exception as e:
                print(f" {picture} Alma işlemi başarısız oldu.",e)

        print("\n")
        for t in threads:
            t.start()

        for t in threads:
            t.join()