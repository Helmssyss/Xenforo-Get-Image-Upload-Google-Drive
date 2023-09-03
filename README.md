# Xenforo_Image_Scraper

TR
---------------------
Türk Hack Team(https://www.turkhackteam.org/) forum sitesinde, açılmış herhangi bir forum linkinde www.hizliresim.com 'sitesi üzerinden atılmış bütün resimleri alır google drive'a yükler.

Yükleme işlemi, gidilen saf resim linkinden resimin sayfa içeriğini alır bunu byte formatına çevirir ve bu çevrilen formatta drive'a yollar. Drive tarafında bunlar işlenip png uzantılı resimler haline dönüşür. Böylece lokalde tekrardan indirmeye gerek kalmayarak hızdan ve yerden tasarruf etmiş oluruz.


Başlamadan önce
```bash
>> pip install -r requirements.txt
```
Google Drive'dan API'yi aktif etmeniz, aktif ettikten sonra da size verilen json dosyasını indirmeniz gerekli. İndirilen json dosyasının adını "credentials.json" olarak değiştirmeniz gerekli.

Daha sonra Foruma gidip ilgili cookieleri edinmeniz gerekli. Bunları da edinip, ".cfg" dosyasındaki değerlere yazmalısınız.

Çalıştırmak için
```bash
>> python app.py
```

`link_manage.json` adında json dosyası bulunuyor.. script çalıştğında bu dosya yoksa oluşturur, varsa bu dosyayı okur. Siz bir veya birden fazla link girilmesini istediğinizde, bunları `all_link` adındaki anahtarın barındırdığı listeye eklemeniz gerekli. Ekledikten sonra kayıt edebilirsiniz..

EN
---------------------
Türk Hack Team (https://www.turkhackteam.org/) takes all the pictures posted on the forum site, www.hizliresim.com, on any forum link that has been opened, and uploads them to google drive.

The upload process takes the page content of the image from the pure image link, converts it to byte format and sends it to the drive in this converted format. On the Drive side, these are processed and converted into png images. Thus, we save speed and space by not having to download it again locally.


before you start
```bash
>> pip install -r requirements.txt
```
You need to activate the API from Google Drive and download the json file given to you after activating it. You need to rename the downloaded json file to "credentials.json".

Then you need to go to the Forum and obtain the relevant cookies. You should also obtain these and write them to the values ​​in the ".cfg" file.

To make it work
```bash
>> python app.py
```

There is a json file named `link_manage.json`. When the script runs, it creates this file if it does not exist, reads this file if it exists. When you want to enter one or more links, you need to add them to the list hosted by the key named `all_link`. You can save after adding.

<div align="center">
<img src="https://avatars.githubusercontent.com/u/89170235?v=4" width="90px;" alt="Fenrirsoftware"/>  <img src="https://avatars.githubusercontent.com/u/84701901?s=400&u=159a0e92650378c13f9319b0568e73a206ad4ec0&v=4" width="90px;" alt="Helmsys"/>
</div>

