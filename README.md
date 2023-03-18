# THT-GetImage-Link-Upload-To-Google-Drive
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

`link_manage.json` adında json dosyası bulunuyor.. script çalıştğında bu dosya yoksa oluşturur, varsa bu dosyayı okur. Siz bir veya birden fazla link girilmesini istediğinizde, bunlrı `all_link` adındaki anahtarın barındırdığı liste ye eklemeniz gerekli. Ekledikten sonra kayıt edebilirsiniz..



Geliştirilecek...

<img src="https://avatars.githubusercontent.com/u/89170235?v=4" width="90px;" alt="Fenrirsoftware"/>  <img src="https://avatars.githubusercontent.com/u/84701901?s=400&u=159a0e92650378c13f9319b0568e73a206ad4ec0&v=4" width="90px;" alt="Helmsys"/>

