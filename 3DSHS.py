import colorama
import requests
import wget
import shutil
import os
from zipfile import ZipFile

### VARS AND CONSTS ###
AVALIABLE={"1":"kartdlphax"}
REGIONS=["EUR","USA","JPN"]


### INITS ###
colorama.init()

### USEFUL FUNCTIONS ###
def CreateFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)



### PROMPT FOR METHOD ###
method=""
while not method in AVALIABLE:
    print("Avaliable methods:")
    for i in AVALIABLE:
        print(str(i)+". "+str(AVALIABLE[i]))
    method=input("Choose a method (HOW TO CHOOSE A METHOD: https://3ds.hacks.guide/get-started): ")
    if not method in AVALIABLE:
        print(colorama.Fore.RED+"The option "+method+" does not exist!")
        print("The only avaliable options are: "+", ".join(AVALIABLE)+colorama.Style.RESET_ALL)

if method=="1":
    print("Please follow the guide at: https://3ds.hacks.guide/installing-boot9strap-(kartdlphax) for instructions")
    print(colorama.Fore.BLUE+"[INFO] Make sure the game region is correct!"+colorama.Style.RESET_ALL)
    region=""
    while not region in REGIONS:
        region=input("Mario Kart 7 Cartridge or Software Region (EUR,USA,JPN): ").upper()
    print("Region set to: "+colorama.Fore.GREEN+region+colorama.Style.RESET_ALL)
    print(colorama.Fore.BLUE+"[INFO] Make sure to plug in the SOURCE 3DS SD Card!"+colorama.Style.RESET_ALL)
    workingcard=input("SOURCE 3DS SD Card directory: ").replace("\\", "/")
    if not workingcard[-1]=="/":
        workingcard+="/"
    
    print(colorama.Fore.RED+"DO NOT UNPLUG THE SD CARD!"+colorama.Style.RESET_ALL)

    # PLUGIN
    print("Downloading kartdlphax...")
    response = requests.get("https://api.github.com/repos/PabloMK7/kartdlphax/releases/latest")
    wget.download(response.json()["assets"][0]["browser_download_url"],".")
    print("\nMoving kartdlphax...")

    # SETTING FOLDER BY REGION
    if region==REGIONS[0]:
        regpath="luma/plugins/0004000000030700/"
    elif region==REGIONS[1]:
        regpath="luma/plugins/0004000000030800/"
    else:
        regpath="luma/plugins/0004000000030600/"
    
    CreateFolder(workingcard+regpath)
    shutil.move("plugin.3gx",workingcard+regpath+"plugin.3gx")
    print(colorama.Fore.GREEN+"Kartdlphax plugin installed!"+colorama.Style.RESET_ALL+"\n")


    # LUMA 3DS FOR 3GX FILES
    print("Downloading Luma 3DS 3GX Loader...")
    response = requests.get("https://api.github.com/repos/Nanquitas/Luma3DS/releases/latest")
    wget.download(response.json()["assets"][0]["browser_download_url"],".")
    print("\nMoving Luma 3DS 3GX Loader...")
    shutil.move("boot.firm",workingcard+"boot.firm")
    print(colorama.Fore.GREEN+"Luma 3DS 3GX Loader installed!"+colorama.Style.RESET_ALL+"\n")

    # CHANGE WORKING 3DS
    print(colorama.Fore.MAGENTA+"SOURCE 3DS READY TO GO!"+colorama.Style.RESET_ALL)
    print("Now that you are done with the SOURCE 3DS, you can unplug the SD and plug in the TARGET 3DS SD")
    workingcard=input("TARGET 3DS SD Card directory: ").replace("\\", "/")
    if not workingcard[-1]=="/":
        workingcard+="/"
    print(colorama.Fore.BLUE+"[INFO] The TARGET 3DS requires more processing as it uncompresses zips and selects files, do not touch any folders while the process is running"+colorama.Style.RESET_ALL)
    print(colorama.Fore.RED+"DO NOT UNPLUG THE SD CARD!"+colorama.Style.RESET_ALL)
    
    # SAFEB9SInstaller
    print("Downloading SafeB9SInstaller...")
    wget.download("https://github.com/d0k3/SafeB9SInstaller/releases/download/v0.0.7/SafeB9SInstaller-20170605-122940.zip")
    print("\nExtracting SafeB9SInstaller...")
    with ZipFile("SafeB9SInstaller-20170605-122940.zip","r") as zipObj:
        zipObj.extract("SafeB9SInstaller.bin",".")
    print("Moving SafeB9SInstaller...")
    shutil.move("SafeB9SInstaller.bin",workingcard+"SafeB9SInstaller.bin")
    print("Cleaning up SafeB9SInstaller...")
    os.remove("SafeB9SInstaller-20170605-122940.zip")
    print(colorama.Fore.GREEN+"SafeB9SInstaller installed!"+colorama.Style.RESET_ALL+"\n")

    #Luma 3DS
    print("Downloading Luma 3DS...")
    response=requests.get("https://api.github.com/repos/LumaTeam/Luma3DS/releases/latest")
    wget.download(response.json()["assets"][0]["browser_download_url"],".")
    print("\nExtracting Luma 3DS...")
    zips=[x for x in os.listdir() if x[-3:] == 'zip']
    with ZipFile(zips[0],"r") as zipObj:
        zipObj.extract("boot.firm",".")
        zipObj.extract("boot.3dsx",".")
    shutil.move("boot.firm",workingcard+"boot.firm")
    shutil.move("boot.3dsx",workingcard+"boot.3dsx")
    print("Cleaning up Luma 3DS...")
    os.remove(zips[0])
    del zips
    print(colorama.Fore.GREEN+"Luma 3DS installed!"+colorama.Style.RESET_ALL+"\n")

    # boot9strap
    print("Downloading boot9strap...")
    wget.download("https://github.com/SciresM/boot9strap/releases/download/1.4/boot9strap-1.4.zip")
    print("\nExtracting boot9strap...")
    with ZipFile("boot9strap-1.4.zip","r") as zipObj:
        zipObj.extract("boot9strap.firm",".")
        zipObj.extract("boot9strap.firm.sha",".")
    print("Moving boot9strap...")
    CreateFolder(workingcard+"boot9strap/")
    shutil.move("boot9strap.firm",workingcard+"boot9strap/boot9strap.firm")
    shutil.move("boot9strap.firm.sha",workingcard+"boot9strap/boot9strap.firm.sha")
    print("Cleaning up boot9strap...")
    os.remove("boot9strap-1.4.zip")
    print(colorama.Fore.GREEN+"boot9strap installed!"+colorama.Style.RESET_ALL+"\n")

    # unSAFE_MODE
    print("Downloading unSAFE_MODE...")
    response=requests.get("https://api.github.com/repos/zoogie/unSAFE_MODE/releases/latest")
    wget.download(response.json()["assets"][0]["browser_download_url"],".")
    print("\nExtracting unSAFE_MODE...")
    zips=[x for x in os.listdir() if x[-3:] == 'zip']
    with ZipFile(zips[0],"r") as zipObj:
        zipObj.extract("usm.bin",".")
        zipObj.extract("slotTool/slotTool.xml",".")
        zipObj.extract("slotTool/slotTool.3dsx",".")
    shutil.move("usm.bin",workingcard+"usm.bin")
    CreateFolder(workingcard+"3ds/slotTool/")
    shutil.move("slotTool/slotTool.xml",workingcard+"3ds/slotTool/slotTool.xml")
    shutil.move("slotTool/slotTool.3dsx",workingcard+"3ds/slotTool/slotTool.3dsx")
    print("Cleaning up unSAFE_MODE...")
    os.remove(zips[0])
    os.removedirs("slotTool")
    del zips
    print(colorama.Fore.GREEN+"unSAFE_MODE installed!"+colorama.Style.RESET_ALL+"\n")

    print("DEFAULT APPS COMING SOON, THE TARGET 3DS IS READY!")
