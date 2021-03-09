import os
import zipfile
import datetime
import time

print("============================================")

#============================================
#       RCON code to stop the server
#============================================

print("Stopping the server...")

from rcon import Client

with Client('127.0.0.1', 25575, passwd='testpass') as client:
    response = client.run('stop')

print("Server response: ",response)

time.sleep(15)

print("Server stopped successfuly!")

#============================================
#  Delete world_auto_backup.zip, if present
#============================================

if os.path.exists("world_auto_backup.zip"):
  os.remove("world_auto_backup.zip")
  print("Deleted world_auto_backup.zip")
else:
  print("File not deleted, because it did not exist. Good to go!")
 
#============================================
#            Compression Code
#============================================

print("Starting compression...")
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

# Define the name of the file that will be outputted
zipf = zipfile.ZipFile(r"G:/forge_server/world_auto_backup.zip", 'w', zipfile.ZIP_DEFLATED)
# This is the absolute path that you want to backup. Or you can just include this script in the working directory.
zipdir(r'G:/forge_server/world', zipf)
zipf.close()   

print("Successfully compressed!")

#============================================
#    Rename code to rename file with date
#============================================

print("Renaming...")

Current_Date = datetime.datetime.today().strftime ('%d-%b-%Y')
filepathname = 'world_auto_backup ' + '(' + str(Current_Date) + ')' + '.zip'
os.rename(r'world_auto_backup.zip ', filepathname)

print("Done Renaming!")

#============================================
#         Authenticate google drive
#============================================

print("Starting authentication process...")

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

# Load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there
    # This is what solved the issues!!
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})

    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:
    # Refresh token if expired
    gauth.Refresh()
else:
    # Initialize the saved credentials
    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")  

print("Authentication Successful!")

#============================================
#      Upload the file to google drive
#============================================

print("Starting upload of file...")

drive = GoogleDrive(gauth)

#ID is the folder's ID you want to upload it to, here it is forge-server-backups
gfile = drive.CreateFile({'parents': [{'id': '1zZyNCS-JZBVa3I3odI9uW1MRNLQ8nyea'}]})
# Read file and set it as the content of this instance.
gfile.SetContentFile(filepathname)
gfile.Upload() # Upload the file.

print("File uploaded successfully!")

print("All Done!")
print("============================================")
