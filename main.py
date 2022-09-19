import logging
import datetime
import locale
# import os
import ftplib
from pdfrw import PdfReader, PdfWriter, PdfDict
# ---------------------------------------------------------------------------------
locale.setlocale(locale.LC_ALL, 'fr_FR')
logging.basicConfig(level=logging.INFO)
# ---------------------------------------------------------------------------------
print ('Set Dates')
dateActuelle = datetime.datetime.now()
dates = {"Periode": dateActuelle.strftime("%B %Y").capitalize(), "Date_af_date": dateActuelle.strftime("%x")}
# ---------------------------------------------------------------------------------
print ('Get Path of PDF Files')
# PDFTemplatePath = os.environ['PDFTemplatePath']
PDFTemplatePath = "/app/QuittanceLoyertemplate.pdf"
logging.debug(PDFTemplatePath)

# PDFOutPath = os.environ['PDFOutPath'] + dateActuelle.strftime("%Y%m%H%M%S") + ".pdf"
PDFOutPath = "QuittanceLoyer" + dateActuelle.strftime("%Y%m%H%M%S") + ".pdf"
logging.debug(PDFOutPath)
# ---------------------------------------------------------------------------------

print ('Reading PDF Template File')
PDFTemplateFile = PdfReader(PDFTemplatePath)

print ('Parsing Annotations')
for page in PDFTemplateFile.pages:
    annotations = page['/Annots']
    if annotations is None:
        continue
    for annotation in annotations:
        if annotation['/Subtype'] == '/Widget':
            if annotation['/T']:
                key = annotation['/T'].to_unicode()
                logging.debug(key)
                logging.debug(dates[key])
                print('Updating Annotations')
                annotation.update(PdfDict(V='{}'.format(dates[key])))
# ---------------------------------------------------------------------------------
print ('Writing PDF out File')
PdfWriter().write(PDFOutPath, PDFTemplateFile)

print ('FTP Connection Start')
session = ftplib.FTP('192.168.0.100', 'pdfgenerator', 'azerty')
print ('FTP session Start')
session.cwd('../homes/pascal/Drive/Patrimoine/Appart Pinel/Gestion/QuittanceLoyer')
file = open(PDFOutPath, 'rb')  # file to send
print ('FTP sending')
session.storbinary('STOR ' + PDFOutPath, file)  # send the file
print ('FTP closing')
file.close()  # close file and FTP
session.quit()
