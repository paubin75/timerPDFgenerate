from smb.SMBConnection import SMBConnection

file_obj = open('QuittanceLoyer2022août.pdf', 'rb')

connection = SMBConnection('pdfgenerator','azerty', 'ob2nas', 'ob1nas', use_ntlm_v2=True)

connection.connect(ip='192.168.0.100')  # The IP of file server

connection.storeFile(service_name='volume1',  # It's the name of shared folder
                     path='\\volume1\\homes\\pascal\\Drive\\Patrimoine',
                     file_obj=file_obj)
connection.close()