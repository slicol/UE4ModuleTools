import sys
import os
import FileUtils
import re
import logging
import coloredlogs
import SourceCodeUtils




class UE4TargetRules:
    Type = ""
    Platform = ""
    def __init__(self):
        self.Type = ""
        self.Platform = ""



class UE4ModuleRules:
    Name = ""
    Target = UE4TargetRules()
    PublicIncludePaths = []
    PrivateIncludePaths = []
    PublicDependencyModuleNames = []
    PrivateDependencyModuleNames = []
    Logger = None

    def __init__(self, name):
        self.Name = name
        self.Target = UE4TargetRules()
        self.PublicIncludePaths = []
        self.PrivateIncludePaths = []
        self.PublicDependencyModuleNames = []
        self.PrivateDependencyModuleNames = []
        self.Logger = logging.getLogger("UE4ModuleRules<" + self.Name + ">")
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.warning("-"*(100-len(self.Name)))

    def LoadFromBuildFile(self,path):
        text = FileUtils.GetFileString(path)
        text = SourceCodeUtils.TrimCStyleComments(text)
        self.PublicIncludePaths = self.FindList("PublicIncludePaths", text)
        self.PrivateIncludePaths = self.FindList("PrivateIncludePaths", text)
        self.PublicDependencyModuleNames = self.FindList("PublicDependencyModuleNames", text)
        self.PrivateDependencyModuleNames = self.FindList("PrivateDependencyModuleNames", text)
        return


    def FindList(self, VarName, text):
        RE_LIST_ASSIGN_CODE_ADDRANGE = VarName + r"\.AddRange\s*\(.*?\s*\{([\s\S]*?)\}\s*\)"
        RE_LIST_ASSIGN_CODE_ADD      = VarName + r"\.Add\s*\(([\s\S]*?)\)"
        RE_LIST_ASSIGN_CODE_ADDLAYER = VarName + r"\.AddRange\s*\(\s*\w+\s*\(([\s\S]*?)\)\s*\)"

        result = []
        matches = re.findall(RE_LIST_ASSIGN_CODE_ADDRANGE, text)
        for match in matches:
            items = re.findall(r"\"(.+?)\"", match)
            for item in items:
                result.append(item)
            pass
        pass
        matches = re.findall(RE_LIST_ASSIGN_CODE_ADD, text)
        for match in matches:
            items = re.findall(r"\"(.+?)\"", match)
            for item in items:
                result.append(item)
            pass
        pass
        matches = re.findall(RE_LIST_ASSIGN_CODE_ADDLAYER, text)
        for match in matches:
            items = re.findall(r"\"(.+?)\"", match)
            for item in items:
                result.append("[Layer]" + item)
            pass
        pass
        return result


    def Dump(self):
        self.Logger.info("-"*100)
        self.Logger.info("PublicIncludePaths:")
        for item in self.PublicIncludePaths:
            self.Logger.info(item)
        pass
        self.Logger.info("-"*100)
        self.Logger.info("PrivateIncludePaths:")
        for item in self.PrivateIncludePaths:
            self.Logger.info(item)
        pass
        self.Logger.info("-"*100)
        self.Logger.info("PublicDependencyModuleNames:")
        for item in self.PublicDependencyModuleNames:
            self.Logger.info(item)
        pass
        self.Logger.info("-"*100)
        self.Logger.info("PrivateDependencyModuleNames:")
        for item in self.PrivateDependencyModuleNames:
            self.Logger.info(item)
        pass








def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)    
    if len(args) > 2 and args[1].lower() == "dump" and args[2].lower().endswith("build.cs"):
        name = os.path.basename(os.path.dirname(args[2]))
        rules = UE4ModuleRules(name)
        rules.LoadFromBuildFile(args[2])
        rules.Dump()
    else:
        logging.error("args error: " + args)    
    pass
    

if __name__ == '__main__':
    '''
    python UE4ModuleRules.py Dump {ModuleBuildRulesPath}
    '''
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    CommandLine(sys.argv)
    #CommandLine(["", "Dump", r"L:\Project\TFW\Master\TFWeather\FourSeasons\Plugins\TFWeather\Source\TFWeather\TFWeather.Build.cs"])
    