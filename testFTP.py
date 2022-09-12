# Path ../homes/pascal/Drive/Patrimoine/Appart Pinel/Gestion/QuittanceLoyer

import ftplib
session = ftplib.FTP('192.168.0.100','pdfgenerator','azerty')
session.cwd('../homes/pascal/Drive/Patrimoine/Appart Pinel/Gestion/QuittanceLoyer')
file = open('QuittanceLoyer202208.pdf','rb')                  # file to send
session.storbinary('STOR QuittanceLoyer202208.pdf', file)     # send the file
file.close()                                    # close file and FTP
session.quit()