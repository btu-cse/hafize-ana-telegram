import requests
from bs4 import BeautifulSoup
from tabula import read_pdf
from tabula import convert_into
import os

class ScrapMenu:
    def __init__(self):
        pass

    def getPdf(self):
        requests.packages.urllib3.disable_warnings()
        url = "https://sks.btu.edu.tr/index.php?sid=235"
        response = requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all("a")
        counter = 0
        for link in links:
            counter += 1
            if ('.pdf' in link.get('href', [])):
                print(counter ,"Adet Dosya Indiriliyor")
                response = requests.get(link.get('href'),verify=False)
                pdf = open("pdf"+str(counter)+".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()
        print("PDF Dosyasi Indirildi")
    def convertPdfToCsv(self):
        df = read_pdf("pdf62(BU KISIM BOT CALISINCA DEGISECEK.pdf", pages='all')[0]
        convert_into("pdf62(BU KISIM BOT CALISINCA DEGISECEK.pdf", "yemekhane.csv", output_format="csv", pages='all')
        os.rename("pdf62(BU KISIM BOT CALISINCA DEGISECEK.pdf", "pdfs/pdf62(BU KISIM BOT CALISINCA DEGISECEK.pdf")
    
