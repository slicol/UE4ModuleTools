import sys
import os
import FileUtils
import re
import logging
import coloredlogs


class UE4ModuleCreator:
    Dir = "" #这个是完整路径
    ModuleDir = "" #这个是相对于Source的路径 
    Name = ""
    Logger = None

    def __init__(self, dir):
        self.Dir = dir.replace("\\","/")
        self.Name = os.path.basename(self.Dir)
        self.ModuleDir = self.GetModuleDir()
        self.Logger = logging.getLogger("UE4ModuleCreator<" + self.Name + ">")
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.warning("-"*(100-len(self.Name)))

    def GetModuleDir(self):
        i = self.Dir.rfind("Source/")
        if i == -1:
            i = self.Dir.rfind("source/")
        pass
        if i == -1:
            return self.Dir
        pass
        return self.Dir[i + 7:]



    def CreateAll(self):
        self.CreateBuildRuleFile()
        self.CreateDirectories()
        self.CreateModuleHeaderFile()
        self.CreateModuleSourceFile()


    def CreateBuildRuleFile(self):
        self.Logger.info("CreateBuildRuleFile")
        f = open(r"Templates/{ModuleName}.Build.cs", "r", encoding="UTF-8")
        text = f.read()
        f.close()
        text = text.replace(r"{ModuleName}", self.Name)
        text = text.replace(r"{ModuleDirectory}", self.ModuleDir)
        f = open(self.Dir + "/" + self.Name + ".Build.cs", "w", encoding="UTF-8")
        f.write(text)
        f.close()

    def CreateDirectories(self):
        self.Logger.info("CreateDirectories")
        if not os.path.exists(self.Dir + "/Public"):
            os.mkdir(self.Dir + "/Public")
        pass
        if not os.path.exists(self.Dir + "/Private"):
            os.mkdir(self.Dir + "/Private")
        pass

    def CreateModuleHeaderFile(self):
        self.Logger.info("CreateModuleHeaderFile")
        f = open(r"Templates/{ModuleName}Module.h", "r", encoding="UTF-8")
        text = f.read()
        f.close()
        text = text.replace(r"{ModuleName}", self.Name)
        f = open(self.Dir + "/Public/" + self.Name + "Module.h", "w", encoding="UTF-8")
        f.write(text)
        f.close()


    def CreateModuleSourceFile(self):
        self.Logger.info("CreateModuleSourceFile")
        f = open(r"Templates/{ModuleName}Module.cpp", "r", encoding="UTF-8")
        text = f.read()
        f.close()
        text = text.replace(r"{ModuleName}", self.Name)
        f = open(self.Dir + "/Private/" + self.Name + "Module.cpp", "w", encoding="UTF-8")
        f.write(text)
        f.close()


def CreateModule(dir):
    creator = UE4ModuleCreator(dir)
    creator.CreateAll()

def CreateModuleBatch(basedir):
    dirs = os.listdir(basedir)
    for dir in dirs:
        dir = basedir + "/" + dir
        if os.path.isdir(dir):
            CreateModule(dir)
        pass
    pass




def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    if len(args) == 2:
        CreateModule(args[1])
    elif len(args) > 2 and args[2] == "-Batch":
        CreateModuleBatch(args[1])
    pass
    




if __name__ == '__main__':
    #CommandLine(sys.argv)
    CommandLine(["",r"W:\Project\DFMProj_Refactor\DFM\Source\DFMGameCore\DFMVehicle"])
    #CommandLine(["",r"W:\Project\DFMProj_Refactor\DFM\Source\GPFramework","-Batch"])
    #CommandLine(["",r"W:\Project\DFMProj_Refactor\DFM\Source\DFMGameCore","-Batch"])
    


    