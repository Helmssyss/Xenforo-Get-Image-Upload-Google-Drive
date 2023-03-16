from io import BytesIO
from mimetypes import MimeTypes
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

VOID = None

__author__      = "Arif-Helmsys"
__author__      = "Coderx37"

class LoginTHT:
    @classmethod
    @property
    def __getCookies(cls) -> dict[str,str]:
        __config = RawConfigParser()
        __config.read(".cfg")
        cookies = {}
        cookies.update({k:v for k,v in __config["THT_LOGIN_COOKIES"].items()})
        return cookies

    @classmethod
    def getThtHtmlPageContent(cls,url:str) -> bytes:
        """
        Eğer Mechanize tarafında 403 hatası alınırsa ilgili web sayfasının kaynak kodlarını kaydedip, yorum satırına alınan kısmı aktif edin. Mechanize
        tarafını iptal edin
        >>> # response = ''
            # with open("indirilen_kaynak_dosyasi.html","r",encoding="utf-8") as response_file:
            #     response = response_file.read()
            # return response
        """
        try:
            br = Browser()
            br.addheaders = [
                ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                ("cookie",f"xf_user={cls.__getCookies['xf-user']}; xf_tfa_trust={cls.__getCookies['xf-tfa-trust']}; xf_session={cls.__getCookies['xf-session']}")
            ]
            br.set_handle_robots(False)
            br.open(url)
            print(br._ua_handlers['_cookies'].cookiejar)
            return br.response().read()
            # response = ''
            # with open("response6.html","r",encoding="utf-8") as response_file:
            #     response = response_file.read()
            # return response
        except Exception as e:
            print(e)
            

class DriveApi:
    lock = threading.Lock()
    que = queue.Queue()
    def __init__(self,url):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        self.content = LoginTHT.getThtHtmlPageContent(url)
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        # self.service = build('drive', 'v3', credentials=self.creds)
        # results = self.service.files().list(pageSize=100, fields="files(id, name)").execute()
        # items = results.get('files', [])
        # print(*items, sep="\n", end="\n\n")

    def getImages(self) -> Generator:
        try:
            soup = BeautifulSoup(self.content,"lxml")
            for i in soup.find_all("img",attrs={"class":"bbImage"}):
                for j in urlparse(i['data-url']).netloc.split('.'):
                    if j =="hizliresim":
                        yield i['data-url']
        except:
            pass

    def readAllImageContents(self,que:queue.Queue,count:int):
        self.lock.acquire()
        picURL = que.get()
        imgName = ''.join(i for i in random.choices(string.ascii_uppercase,k=20))+'.png'
        try:
            response = requestsGetMethod(picURL)
            imgLoad = BytesIO(response.content)
            file_metadata  = {"name": imgName,"mimeType":'image/png'}
            media_body = MediaIoBaseUpload(imgLoad, resumable=True,mimetype="image/png")
            self.service = build('drive', 'v3', credentials=self.creds)
            self.service.files().create(body=file_metadata, media_body=media_body).execute()
            print(f"[{count}] {imgName} Başarıyla Google Drive'a Kaydedildi",threading.current_thread().name)

        except Exception as e:
            print(f"[{count}] {imgName} Google Drive'a Kaydetme Başarısız!",threading.current_thread().name)
        finally:
            que.task_done()
            self.lock.release()

    def uploadGoogleDrive(self) -> VOID:
        threads:list[threading.Thread] = []
        count = 0
        print("\n")
        for picture in set(self.getImages()):
            try:
                self.que.put(picture)
                print(f"[{count}] {picture} Başarıyla Alındı")
                t = threading.Thread(target=self.readAllImageContents,args=(self.que,count))
                threads.append(t)
            except Exception as e:
                print(f"[{count}] {picture} Alma işlemi başarısız oldu.",e)
            finally:
                count += 1

        print("\n")
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

if __name__ == "__main__":
    print("\n[Config (.cfg) dosyasına Cookieleri yazdığından emin ol]")
    print("Google Drive'a Resimlerin Yüklenme Hızı İnternet Hızı İle Doğru Orantılı\n")
    input("Devam Etmek İçin (Enter) >")
    input = input("Forumdan bir konu linki Gönder > ")
    app = DriveApi(input)
    app.uploadGoogleDrive()
