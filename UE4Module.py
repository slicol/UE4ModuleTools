import sys
import os
import FileUtils
import re
import logging
import coloredlogs
import CPPClassParser


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
    UInterfaces = []
    Headers = []
    Logger = None

    def __init__(self, dir):
        self.Dir = dir
        self.Name = os.path.basename(dir)
        self.Rules = UE4ModuleRules()
        self.Rules.LoadFromFile(dir + self.Name + ".Build.cs")
        self.UClasses = []
        self.UStructs = []
        self.UEnums = []
        self.UInterfaces = []
        self.Headers = []        
        self.Logger = logging.getLogger("UE4Module<" + self.Name + ">")
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.warning("-"*(100-len(self.Name)))

    def Parser(self):
        Headers = FileUtils.GetAllFiles(self.Dir, ".h")
        for header in Headers:
            self.__ParserHeader(header)
        pass
            

    def __ParserHeader(self, header):    
        try:
            f = open(header,"r",encoding="UTF-8")
            lines = f.readlines()
            f.close()
        except Exception as e:
            f.close()

            try:
                f = open(header, "r")
                lines = f.readlines()
                f.close()
            except Exception as e:
                f.close()

                self.Logger.error("__ParserHeader: %s", header)
                self.Logger.error(e)
                return
            pass
        pass

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
            elif line.startswith("UINTERFACE"):
                flag = 4
                continue
            pass

            if flag == 1:
                if self.__ParserUClass(header,line):
                    flag = 0
                pass
            elif flag == 2:
                if self.__ParserUStruct(header,line):
                    flag = 0
                pass
            elif flag == 3:
                if self.__ParserUEnum(header,line):
                    flag = 0
                pass
            elif flag == 4:
                if self.__ParserUInterface(header,line):
                    flag = 0
                pass
            pass
        
        pass



    def __ParserUClass(self, header, line):
        name = CPPClassParser.GetClassNameFromLine(line)
        if name == "" or (not name.startswith("U") and not name.startswith("A")):
            self.Logger.error("__ParserUClass Error: %s", header)
            self.Logger.error("__ParserUClass Error: %s", line)
        else:
            self.Logger.info("__ParserUClass Sucess: %s", name)
            self.UClasses.append(name)
        pass
        return True
        
    def __ParserUStruct(self, header, line):
        name = CPPClassParser.GetStructNameFromLine(line)
        if name == "" or not name.startswith("F"):
            self.Logger.error("__ParserUStruct Error: %s", header)
            self.Logger.error("__ParserUStruct Error: %s", line)
        else:
            self.Logger.info("__ParserUStruct Sucess: %s", name)
            self.UStructs.append(name)
        pass
        return True

    def __ParserUEnum(self, header, line):
        name = CPPClassParser.GetEnumNameFromLine(line)
        if name == "" or not name.startswith("E"):
            self.Logger.error("__ParserUEnum Error: %s", header)
            self.Logger.error("__ParserUEnum Error: %s", line)
        else:
            self.Logger.info("__ParserUEnum Sucess: %s", name)
            self.UEnums.append(name)
        pass
        return True

    def __ParserUInterface(self, header, line):
        name = CPPClassParser.GetClassNameFromLine(line)
        if name == "" or not name.startswith("U"):
            self.Logger.error("__ParserUInterface Error: %s", header)
            self.Logger.error("__ParserUInterface Error: %s", line)
        else:
            self.Logger.info("__ParserUInterface Sucess: %s", name)
            self.UInterfaces.append(name)
        pass
        return True





def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    module = UE4Module(args[1])
    module.Parser()
    




if __name__ == '__main__':
    #CommandLine(sys.argv)
    CommandLine(["",r"W:\Project\DFMProj_PVE\DFM\Source\GameFrameWork"])
    