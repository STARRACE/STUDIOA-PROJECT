from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client import file, client, tools
from httplib2 import Http
import argparse

parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("-n","--name", help="enter name of file to be uploaded")
args = parser.parse_args()

upload_file_list = [args.name]

''' SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    try:
    	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    	creds = tools.run_flow(flow, store)
    except:
        print("error secrets")
service = build('drive', 'v3', http=creds.authorize(Http()))
'''

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)   

for upload_file in upload_file_list:
	F=open("vidname.txt","r")
	val=F.read(1)
	valint=int(val)+1
	F.close
	F=open("vidname.txt","w")
	F.write(str(valint))
	F.close
	namefile=val+".mp4"
	gfile = drive.CreateFile({'parents': [{'id': '1eZPmwebhEKB91bU30OKERjhbq-JZE1LX'}],'title': namefile})
	# Read file and set it as the content of this instance.
	gfile.SetContentFile(upload_file)
 
	gfile.Upload() # Upload the file.
 