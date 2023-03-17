# Authors : Arif-Helmsys , Coderx37

from src import DriveApi

def main() -> None:
    print("\n[Config (.cfg) dosyasına Cookieleri yazdığından emin ol]")
    print(">Google Drive'a Resimlerin Yüklenme Hızı İnternet Hızı İle Doğru Orantılı<")
    print(">Bir veya birden fazla linki 'link_manage.json' dosyasındaki all_link anahtarındaki listenin içerisine ekleyip kaydetmen yeterli.<\n")
    input(">Devam Etmek İçin (Enter)<")
    app = DriveApi()
    return app.run()

if __name__ == "__main__":
    main()