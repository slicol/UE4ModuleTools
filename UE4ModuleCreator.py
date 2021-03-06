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
        rule_file_path = self.Dir + "/" + self.Name + ".Build.cs"
        if os.path.exists(rule_file_path):
            self.Logger.warning("RuleFile Is Existed: %s", rule_file_path)
            return
        pass
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
        filepath = self.Dir + "/Public/" + self.Name + "Module.h"
        if os.path.exists(filepath):
            self.Logger.warning("HeaderFile Is Existed: %s", filepath)
            return
        pass
        f = open(r"Templates/{ModuleName}Module.h", "r", encoding="UTF-8")
        text = f.read()
        f.close()
        text = text.replace(r"{ModuleName}", self.Name)
        f = open(filepath, "w", encoding="UTF-8")
        f.write(text)
        f.close()


    def CreateModuleSourceFile(self):
        self.Logger.info("CreateModuleSourceFile")
        filepath = self.Dir + "/Private/" + self.Name + "Module.cpp"
        if os.path.exists(filepath):
            self.Logger.warning("SourceFile Is Existed: %s", filepath)
            return
        pass
        f = open(r"Templates/{ModuleName}Module.cpp", "r", encoding="UTF-8")
        text = f.read()
        f.close()
        text = text.replace(r"{ModuleName}", self.Name)
        f = open(filepath, "w", encoding="UTF-8")
        f.write(text)
        f.close()


def CreateModule(dir):
    if not FileUtils.IsUE4ModuleDir(dir):
        creator = UE4ModuleCreator(dir)
        creator.CreateAll()
    pass

def CreateModulesOfLayer(basedir):
    dirs = os.listdir(basedir)
    for dir in dirs:
        dir = basedir + "/" + dir
        if os.path.isdir(dir):
            CreateModule(dir)
        pass
    pass

def CreateModulesOfPlugin(basedir):
    dirs = os.listdir(basedir + "/Source")
    for dir in dirs:
        dir = basedir + "/Source/" + dir
        if os.path.isdir(dir):
            CreateModule(dir)
        pass
    pass


def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    if args[1].lower() == "CreateModule".lower():
        CreateModule(args[2])
    elif args[1].lower() == "CreateModulesOfLayer".lower():
        CreateModulesOfLayer(args[2])
    elif args[1].lower() == "CreateModulesOfPlugin".lower():
        CreateModulesOfPlugin(args[2])        
    pass



if __name__ == '__main__':
    '''
    python UE4ModuleCreator.py CreateModule {ModuleDir}
    python UE4ModuleCreator.py CreateModulesOfLayer {LayerDir}
    python UE4ModuleCreator.py CreateModulesOfPlugin {PluginDir}
    '''
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    CommandLine(sys.argv)

    


    