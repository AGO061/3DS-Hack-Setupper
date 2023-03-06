import colorama
from sys import exit
import requests
import wget
import shutil
import os
import json
import glob
from zipfile import ZipFile

### VARS AND CONSTS ###
DOWNLOADDIR="./tmp/"
AVALIABLE=glob.glob("packs/*.json",recursive=True)
REGIONS=["EUR","USA","JPN"]
JSONVERSION="1.0"

### USEFUL FUNCTIONS ###
def CreateFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)


### INITS ###
colorama.init()
CreateFolder(DOWNLOADDIR)





### PROMPT FOR METHOD ###
method=0
while not (method<=len(AVALIABLE) and method>0):
    
    print("Avaliable methods:")
    
    for i,string in enumerate(AVALIABLE):
        workingfile=AVALIABLE[i-1]
        hackdata=json.load(open(workingfile,"r"))
        print(str(i+1)+". "+hackdata["general-data"]["name"]+" (pack by "+hackdata["general-data"]["AUTHOR"]+")")
    
    method=int(input("Choose a method (HOW TO CHOOSE A METHOD: https://3ds.hacks.guide/get-started): "))
    
    if not (method<=len(AVALIABLE) and method>0):
        print(colorama.Fore.RED+"The option "+str(method)+" does not exist!")
        print("The only avaliable options are: "+", ".join([str(x+1) for x in range(len(AVALIABLE))])+colorama.Style.RESET_ALL)

workingfile=AVALIABLE[method-1]

hackdata=json.load(open(workingfile,"r"))

print(f'For reference on how to install hb with {hackdata["general-data"]["name"]} you can check: {colorama.Fore.BLUE}{hackdata["general-data"]["guide-page"]}{colorama.Style.RESET_ALL}')
print(f'{colorama.Fore.BLUE}[INFO] You need {len(hackdata["general-data"]["SDs"])} {"SD" if len(hackdata["general-data"]["SDs"])==1 else "SDs"} to perform this hack{colorama.Style.RESET_ALL}')

appcount=0
workingcard=""

for application in hackdata["downloads"]: # we define application as any file that gets downloaded and installed
    if appcount in hackdata["general-data"]["SDs"].values(): # We run the dir change anytime
        n=list(hackdata["general-data"]["SDs"].keys())[list(hackdata["general-data"]["SDs"].values()).index(appcount)]
        workingcard=input(f"\nPath to the {n} SD Card: ")
        if workingcard=="":
            print(f'{colorama.Fore.RED}No SD card directory inserted!{colorama.Style.RESET_ALL}')
            exit(2)
    print(f"\nDownloading {application}...")
    if hackdata["downloads"][application]["direct"]:
        wget.download(hackdata["downloads"][application]["url"],DOWNLOADDIR)
    else:
        response = requests.get(hackdata["downloads"][application]["url"])
        if response.ok:
            wget.download(response.json()["assets"][hackdata["downloads"][application]["download-index"]]["browser_download_url"],DOWNLOADDIR)
        else:
            print(f'{colorama.Fore.RED}response for: {hackdata["downloads"][application]["url"]} is not OK.{colorama.Style.RESET_ALL}')
            exit(1)
    
    if hackdata["downloads"][application]["iszip"]: # if the app is a zip, we use the zipfile data to unzip it
        print(f"\nUnpacking {application}...")
        for zipf in hackdata["downloads"][application]["zipfiles"]:
            with ZipFile(DOWNLOADDIR+zipf,"r") as zipObj:
                for zipcontent in hackdata["downloads"][application]["zipfiles"][zipf]:
                    zipObj.extract(zipcontent,DOWNLOADDIR+hackdata["downloads"][application]["zipfiles"][zipf][zipcontent])
    
    for f in hackdata["downloads"][application]["files"]:
        if hackdata["downloads"][application]["region-dependent"]: # here we first check for the region and then change the folder according to it
            region=""
            while region not in REGIONS:
                region=input(f"\nIt looks like {colorama.Fore.YELLOW}{application}{colorama.Style.RESET_ALL} needs a region to work (check the guide for more details): ").upper()
                if region not in REGIONS:
                    print(f"the \"{region}\" region does not exist!")
            CreateFolder("/".join(f[region]["destination"].replace("&",workingcard).replace("\\","/").split("/")[:-1]))
            shutil.move(DOWNLOADDIR+f[region]["source"],f[region]["destination"].replace("&",workingcard))
        else:
            CreateFolder("/".join(f["destination"].replace("&",workingcard).replace("\\","/").split("/")[:-1]))
            shutil.move(DOWNLOADDIR+f["source"],f["destination"].replace("&",workingcard)) # here we move the files into the current card
    appcount+=1 # one application was installed

shutil.rmtree(DOWNLOADDIR)