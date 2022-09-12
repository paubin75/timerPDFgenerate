import logging
import datetime
import locale
import os
import ftplib
from pdfrw import PdfReader, PdfWriter, PdfDict
# ---------------------------------------------------------------------------------
locale.setlocale(locale.LC_ALL, 'fr_FR')
logging.basicConfig(level=logging.INFO)
# ---------------------------------------------------------------------------------
logging.info('Set Dates')
dateActuelle = datetime.datetime.now()
dates = {"Periode": dateActuelle.strftime("%B %Y").capitalize(), "Date_af_date": dateActuelle.strftime("%x")}
# ---------------------------------------------------------------------------------
logging.info('Get Path of PDF Files')
PDFTemplatePath = os.environ['PDFTemplatePath']
logging.debug(PDFTemplatePath)
# TODO: rajouter heure pour test docker CRON
PDFOutPath = os.environ['PDFOutPath'] + dateActuelle.strftime("%Y%m") + ".pdf"
logging.debug(PDFOutPath)
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.info('Reading PDF Template File')
    PDFTemplateFile = PdfReader(PDFTemplatePath)

    logging.info('Parsing Annotations')
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
                    logging.info('Updating Annotations')
                    annotation.update(PdfDict(V='{}'.format(dates[key])))
    # ---------------------------------------------------------------------------------
    logging.info('Writing PDF out File')
    PdfWriter().write(PDFOutPath, PDFTemplateFile)

    logging.info('FTP Connection Start')
    session = ftplib.FTP('192.168.0.100', 'pdfgenerator', 'azerty')
    session.cwd('../homes/pascal/Drive/Patrimoine/Appart Pinel/Gestion/QuittanceLoyer')
    file = open(PDFOutPath, 'rb')  # file to send
    session.storbinary('STOR ' + PDFOutPath, file)  # send the file
    file.close()  # close file and FTP
    session.quit()
