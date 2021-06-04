#!/usr/bin/env python3

import os

#this script is for creating symlinks 
#from all files in a path (recursively) 
#with a certain extension.

srcDir="E:\Games\Conan_Exiles_Mods" 
desDir="E:\Games\Conan_Exiles_Mods"
Ext=".pak"

for root, dir, file in os.walk(srcDir):
    for filename in file:
        if os.path.splitext(filename)[1].lower() == Ext:
            try:
                if not os.path.islink(filename):
                    linkTarget = os.path.join(root,filename)
                    linkPath = os.path.join(desDir,filename)
                    if not linkTarget == linkPath:
                        os.symlink(linkTarget, linkPath)
            except Exception as ex:
                print("Error, '{}':\n{}".format(str(ex),filename))
                pass
        
			
			
input("\nPress Enter to exit...")