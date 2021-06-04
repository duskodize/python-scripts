#!/usr/bin/env python3

import os
import sys
import shutil
import requests
import keyboard
import webbrowser
from bs4 import BeautifulSoup
from datetime import datetime

gameID = "440900"
steamPath = "E:\Games\SteamLibrary\steamapps"
workshopPath = steamPath + "\workshop\content"
workshopGamePath = workshopPath + "\\" + gameID
modExt = ".pak"
modID = ''
dest = "E:\Games\Conan_Exiles_Mods"
modPath = "E:\Games\SteamLibrary\steamapps\common\Conan Exiles\ConanSandbox\Mods"

acf = ''
modDesc = ''
badChars = '<>:"/\|?*'

with open(r"{}\workshop\appworkshop_{}.acf".format(steamPath, gameID) , 'r') as file:
	acf = file.read().replace('\n', '')

doIt = False

def cleanStr(str):
    for c in badChars:
        str = str.replace(c,'')
    return str

def quote(str):
    return '"{}"'.format(str)

#def robocopy(source, destination, extension=''):
#    os.system("robocopy {} {} {} /xx /njh /copyall /zb".format(quote(source), quote(destination), quote(extension)))

#def robomove(source, destination, extension=''):
#    os.system("robocopy {} {} {} /xx /njh /move /copyall /zb".format(quote(source), quote(destination), quote(extension)))

def copyfiles(srcdir, dstdir,ext = ".*"):
    for basename in os.listdir(srcdir):
        if basename.endswith(ext):
            pathname = os.path.join(srcdir, basename)
            if os.path.isfile(pathname):
                shutil.copy(pathname, dstdir)
                
def movefiles(srcdir, dstdir,ext = ".*"):
    for basename in os.listdir(srcdir):
        if basename.endswith(ext):
            pathname = os.path.join(srcdir, basename)
            if os.path.isfile(pathname):
                shutil.move(pathname, dstdir)
    
def getLastUpdate(id):
    ts = int(acf.partition('"{}"'.format(id))[2].partition('"timeupdated"')[2][:13][3:])
    dt = datetime.fromtimestamp(ts)
    return dt.strftime('%d %h %Y @ %H:%M')

print("This script moves steam workshop mods to conan exile game directory")

print("\nPress Enter to continue or press Esc to exit: ")

if __name__ == "__main__":

    try:
        while True:
            try:
                if keyboard.is_pressed('ENTER'):
                    doIt = True
                    print("Moving mods...\n")
                    break
                
                if keyboard.is_pressed('Esc'):
                    sys.exit(0)
            except:
                break
        if doIt:
            for path, dirs, files in os.walk(workshopGamePath):
                for name in dirs:
                    modID = name
                    modWebPath = 'https://steamcommunity.com/sharedfiles/filedetails/?id='+ modID
                    response = requests.get(modWebPath)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    modDesc = soup.find_all(id='highlightContent')[0].get_text()
                    modName = soup.title.contents[0].partition('Steam Workshop::')[2]
                    cleanModName = cleanStr(modName)
                    if len(modName) == 0:
                        print('Error: Can not get mod name for ' + name)
                        print("moving '{}'...\n".format(modID))
                    else:
                        print("moving '{}'...\n".format(modName))
                    
                    srcDir = os.path.join(workshopGamePath, modID)
                    desDir = os.path.join(dest, modID)
                    os.makedirs(desDir, exist_ok=True)
                    #robomove(srcDir, desDir, modExt)
                    movefiles(srcDir,desDir,modExt)
                    #webbrowser.open(modWebPath, new=2)
                    
                    try:
                        lastUpdate = getLastUpdate(modID)
                        if len(cleanModName) > 0:
                            with open(os.path.join(desDir,"{}.txt".format(cleanModName)), 'w', encoding="utf-8") as f:
                                if len(lastUpdate) > 0:
                                    f.write("{}\n{}\n\n".format(modName,lastUpdate))
                                if len(modDesc) > 0:
                                    f.write(modDesc)
                    except Exception as ex:
                        print(str(ex))
                        print("Error: Can not get details for \"{}\"".format(modName))
                    for root, dir, file in os.walk(desDir):
                        for filename in file:
                            if os.path.splitext(filename)[1].lower() == modExt:
                                try:
                                    linkTarget = os.path.join(root,filename)
                                    linkPath = os.path.join(desDir,filename)
                                    if not linkTarget == linkPath:
                                        os.symlink(linkTarget, linkPath)
                                except Exception as ex:
                                    print(str(ex))
                                    pass
                                
                    
                    #input("Press Enter to continue...")
                    
                    if os.path.isdir(srcDir):
                        shutil.rmtree(srcDir)
            input("\nPress Enter to exit...")
    except Exception as ex:
        print(str(ex))
        input("\nPress Enter to exit...")
