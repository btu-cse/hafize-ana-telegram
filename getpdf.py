import requests
from bs4 import BeautifulSoup
from tabula import read_pdf
from tabula import convert_into

class GetPdf:
    def __init__(self):
        pass

    def get_pdf(self):
        requests.packages.urllib3.disable_warnings()
        url = "https://sks.btu.edu.tr/index.php?sid=235"
        response = requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all("a")
        i = 0
        for link in links:
            i += 1
            if ('.pdf' in link.get('href', []) and i==62):
                print(i ,"Adet Dosya Indiriliyor")
                response = requests.get(link.get('href'),verify=False)
                pdf = open("pdf"+str(i)+".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()
        print("PDF Dosyasi Indirildi")
    def convert_pdf(self):
        df = read_pdf("pdf62.pdf", pages='all')[0]
        convert_into("pdf62.pdf", "yemekhane.csv", output_format="csv", pages='all')
GetPdf().get_pdf()
GetPdf().convert_pdf()