import os
import FileUtils
import re
import logging
import SourceCodeUtils
import UE4Module
import coloredlogs
import math

class UE4RedirectPair:
    KeyName = ""
    OldName = ""
    NewName = ""
    def __init__(self, keyname):
        self.KeyName = keyname
        self.OldName = ""
        self.NewName = ""


class UE4CoreRedirects:
    Category = ""
    NameMap = {} # KeyName:UE4RedirectPair
    Logger = None

    def __init__(self, category):
        self.Category = category
        self.NameMap = {}
        self.Logger = logging.getLogger(category)
        self.Logger.setLevel(logging.DEBUG)
        

    def AddRedirectOldName(self,keyname, oldname):
        pair = self.NameMap.get(keyname,None)
        if pair == None:
            pair = UE4RedirectPair(keyname)
            pair.OldName = oldname
            self.NameMap[keyname] = pair
        else:
            if not pair.OldName == "":
                self.Logger.error("AddRedirectOldName(%s,%s), The OldName Has Existed = %s", keyname, oldname, pair.OldName)
            else:
                pair.oldname = oldname
            pass
        pass

    
    def AddRedirectNewName(self,keyname, newname):
        pair = self.NameMap.get(keyname,None)
        if pair == None:
            pair = UE4RedirectPair(keyname)
            pair.NewName = newname
            self.NameMap[keyname] = pair
        else:
            if not pair.NewName == "":
                self.Logger.error("AddRedirectNewName(%s,%s), The NewName Has Existed = %s", keyname, newname, pair.NewName)
            else:
                pair.NewName = newname
            pass
        pass        

    def Dump(self, lines):
        self.Logger.warning("Dump() Begin-------")
        pairs = self.NameMap.values()
        
        for pair in pairs:
            n = len(pair.OldName)
            space = ""
            if n < 50:
                space = " "*(50-n)
            else:
                m = 50 + math.ceil((n-50)/10) * 10
                space = " "*(m-n)
            pass
            line = "+{0}=(OldName=\"{1}\", {2}NewName=\"{3}\")".format(self.Category, pair.OldName, space, pair.NewName)
            
            #self.Logger.warning("+%s=(OldName=\"%s\", %sNewName=\"%s\")", self.Category, pair.OldName, space, pair.NewName)
            if lines == None:
                self.Logger.warning(line)
            else:
                lines.append(line + "\n")
            pass
        pass
        self.Logger.warning("Dump() End---------[%d]", len(pairs))
        

    


    

def GetAllModuleDirs(src_dir):
    mdl_build_files = FileUtils.GetAllFiles(src_dir, ".Build.cs")
    mdl_dirs = []
    for filepath in mdl_build_files:
        mdl_dir = os.path.dirname(filepath)
        mdl_dirs.append(mdl_dir)
    pass
    return mdl_dirs


def GetAllModules(src_dir):
    mdl_dirs = GetAllModuleDirs(src_dir)
    mdls = []
    for mdl_dir in mdl_dirs:
        mdl = UE4Module.UE4Module(mdl_dir)
        mdl.ParserSourceCode()
        mdls.append(mdl)
    pass
    return mdls


def GetAllRedirectsFromSrc(src_dir,class_redirects,struct_redirects,enum_redirects):
    mdls = GetAllModules(src_dir)
    for mdl in mdls:
        for name in mdl.UClasses:
            oldname = "/Script/" + mdl.Name + "." + name[1:]
            class_redirects.AddRedirectOldName(name, oldname)
        pass
        for name in mdl.UInterfaces:
            oldname = "/Script/" + mdl.Name + "." + name[1:]
            class_redirects.AddRedirectOldName(name, oldname)
        pass
        for name in mdl.UStructs:
            oldname = "/Script/" + mdl.Name + "." + name[1:]
            struct_redirects.AddRedirectOldName(name, oldname)
        pass
        for name in mdl.UEnums:
            oldname = "/Script/" + mdl.Name + "." + name
            enum_redirects.AddRedirectOldName(name, oldname)
        pass
    pass


def SetAllRedirectsWithDst(dst_dir,class_redirects,struct_redirects,enum_redirects):
    mdls = GetAllModules(dst_dir)
    for mdl in mdls:
        for name in mdl.UClasses:
            newname = "/Script/" + mdl.Name + "." + name[1:]
            class_redirects.AddRedirectNewName(name, newname)
        pass
        for name in mdl.UInterfaces:
            newname = "/Script/" + mdl.Name + "." + name[1:]
            class_redirects.AddRedirectNewName(name, newname)
        pass
        for name in mdl.UStructs:
            newname = "/Script/" + mdl.Name + "." + name[1:]
            struct_redirects.AddRedirectNewName(name, newname)
        pass
        for name in mdl.UEnums:
            newname = "/Script/" + mdl.Name + "." + name
            enum_redirects.AddRedirectNewName(name, newname)
        pass
    pass


def Redirect(src_dir,dst_dir):
    class_redirects = UE4CoreRedirects("ClassRedirects")
    struct_redirects = UE4CoreRedirects("StructRedirects")
    enum_redirects = UE4CoreRedirects("EnumRedirects")
    logging.warning("#"*100)
    GetAllRedirectsFromSrc(src_dir, class_redirects, struct_redirects, enum_redirects)
    logging.warning("#"*100)
    SetAllRedirectsWithDst(dst_dir, class_redirects, struct_redirects, enum_redirects)
    logging.warning("#"*100)
    lines = []
    class_redirects.Dump(lines)
    struct_redirects.Dump(lines)
    enum_redirects.Dump(lines)
    f = open(dst_dir + r"\UE4RedirectDump.ini", mode="w")
    f.writelines(lines)
    f.close()



    

########################################################################
def CommandLine(args):
    logging.getLogger().setLevel(logging.WARN)
    coloredlogs.install(level='WARN')
    logging.info(args)
    Redirect(args[1], args[2])
    



if __name__ == '__main__':
    #CommandLine(sys.argv)
    CommandLine(["",r"E:\Project\DFMProj\DFM\Source",r"E:\Project\DFMProj\DFM\Source"])