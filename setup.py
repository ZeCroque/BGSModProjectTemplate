import sys
import shutil
import os
from pathlib import Path
from CIScripts import mod_info
from CIScripts import utils
from CIScripts import papyrus_compiler

def StarfieldSetup():
    shutil.move("Data/Starfield.esp", "Data/" + mod_info.config.modName + ".esp")
    os.remove("Data/Fallout4.esp")
    os.remove("Data/Skyrim.esp")
    shutil.rmtree("Data/SEQ/")
    shutil.move("Data/Scripts/" + mod_info.config.modShortName + "/", "Data/Scripts/Source/" + mod_info.config.modShortName + "/")

def Fallout4Setup():
    shutil.move("Data/Fallout4.esp", "Data/" + mod_info.config.modName + ".esp")
    os.remove("Data/Starfield.esp")
    os.remove("Data/Skyrim.esp")
    shutil.rmtree("Data/SEQ/")
    shutil.move("Data/Scripts/" + mod_info.config.modShortName + "/", "Data/Scripts/Source/User/" + mod_info.config.modShortName + "/")

def FlattenNamespaces():
    root = Path("./Data/Source/Scripts")
    for src in list(root.rglob("*")):
        if not src.is_file() or src.parent == root:
            continue
        new_name = "_".join(src.relative_to(root).parts)
        shutil.move(src, root / new_name)
    shutil.rmtree("./Data/Source/Scripts/" + mod_info.config.modShortName + "/")

def SkyrimSetup():
    shutil.move("Data/Skyrim.esp", "Data/" + mod_info.config.modName + ".esp")
    os.remove("Data/Starfield.esp")
    os.remove("Data/Fallout4.esp")
    shutil.move("Data/Scripts/" + mod_info.config.modShortName + "/", "Data/Source/Scripts/" + mod_info.config.modShortName + "/")
    os.remove(mod_info.config.modName + "Debug.ppj")
    os.remove(mod_info.config.modName + "Release.ppj")
    FlattenNamespaces()

def main():   
    match utils.Game(sys.argv[1]):
        case utils.Game.STARFIELD:
            StarfieldSetup()
        case utils.Game.FALLOUT4:
            Fallout4Setup()
        case utils.Game.SKYRIM:
            SkyrimSetup()
        case _:
            print("CONFIGURATION ERROR")
    papyrus_compiler.FillTemplates(papyrus_compiler.CompileMode.DEFAULT)

    #Patch .esp
    with open("./Data/" + mod_info.config.modName + ".esp", "rb") as file:
        patchedFile = file.read()
        patchedFile = patchedFile.replace(b"\0ZEC_", b"\0" + mod_info.config.modShortName.encode() + b"_")
        patchedFile = patchedFile.replace(b"\0ZEC:", b"\0" + mod_info.config.modShortName.encode() + b":")
    with open("./Data/" + mod_info.config.modName + ".esp", "wb") as file:
        file.write(patchedFile)

if __name__ == "__main__":
    main()