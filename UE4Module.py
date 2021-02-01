import os
import FileUtils
import re
import logging

class UE4TargetRules:
    Type = ""
    Platform = ""


class UE4ModuleRules:
    Target = UE4TargetRules()
    PublicIncludePaths = []
    PrivateIncludePaths = []
    PublicDependencyModuleNames = []
    PrivateDependencyModuleNames = []

    def LoadFromFile(self,path):
        return



class UE4Module:
    Dir = ""
    Name = ""
    Rules = UE4ModuleRules()
    UClasses = []
    UStructs = []
    UEnums = []
    Headers = []

    def __init__(self, dir):
        self.Dir = dir
        self.Name = os.path.basename(dir)
        self.Rules.LoadFromFile(dir + Name + ".Build.cs")
        

    def Parser(self):
        Headers = LogTrackUtils.GetAllFiles(self.Dir, ".h")
        for header in Headers:
            self.__ParserHeader(header)
        pass
            

    def __ParserHeader(self, header):
        f = open(header, "r")
        lines = f.readlines()
        f.close()
        flag = 0
        for line in lines:
            if line.startswith("UCLASS"):
                flag = 1
                continue
            elif line.startswith("USTRUCT"):
                flag = 2
                continue
            elif line.startswith("UENUM"):
                flag = 3
                continue
            pass

            if flag == 1:
                self.__ParserUClass(line)
            elif flag == 2:
                self.__ParserUStruct(line)
            elif flag == 3:
                self.__ParserUEnum(line)
            pass
        
        pass



    def __ParserUClass(self, line):
        line



