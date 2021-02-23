import sys
import os
import re
import FileUtils
import coloredlogs
import logging


def GetClassNameFromLine(line):
    RE_CLASS_NAME = r"(class|struct|interface)\s+(\w+\s+)?(\w+)\s*(final\s*)?:?"
    match_name = re.search(RE_CLASS_NAME, line)
    if not match_name == None:
        return match_name.group(3)
    pass
    return ""

def GetEnumNameFromLine(line):
    RE_CLASS_NAME = r"(enum|namespace)\s+(class\s+)?(\w+\s+)?(\w+)\s*:?"
    match_name = re.search(RE_CLASS_NAME, line)
    if not match_name == None:
        return match_name.group(4)
    pass
    return ""

def GetStructNameFromLine(line):
    RE_CLASS_NAME = r"(struct)\s+(\w+\s+)?(\w+)\s*:?"
    match_name = re.search(RE_CLASS_NAME, line)
    if not match_name == None:
        return match_name.group(3)
    pass
    return ""



def TrimCStyleComments(text):
    RE_COMMENTS = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(RE_COMMENTS, re.MULTILINE|re.DOTALL)
    
    def _replacer(match):
        if match.group(2) is not None:
            return "" #将注释替换为空
        else:
            return match.group(1) #原样返回
        pass

    return regex.sub(_replacer, text)





def NormalizeIncludeSlash(filepath):
    lines = FileUtils.GetAllLines(filepath)
    num = len(lines)
    changed = False
    for i in range(0, num):
        line = lines[i]
        if line.startswith("#include "):
            if line.find("\\") > 0:
                changed = True
                line = line.replace("\\","/")
                lines[i] = line
            pass
        pass
    pass
    if changed:
        logging.warning("NormalizeIncludeSlash: %s", filepath)
        f = open(filepath, "w", encoding="UTF-8")
        f.writelines(lines)
        f.close()
    else:
        logging.info("NormalizeIncludeSlash: %s, No Changed", filepath)
    pass


def NormalizeIncludeSlashAuto(dir_or_filepath):
    if not os.path.exists(dir_or_filepath):
        logging.error("[%s] Don't Existed!", dir_or_filepath)
        return
    pass
    if os.path.isdir(dir_or_filepath):
        paths = FileUtils.GetAllFiles(dir_or_filepath, ".h|.cpp")
        for filepath in paths:
            NormalizeIncludeSlash(filepath)
        pass
    else:
        NormalizeIncludeSlash(dir_or_filepath)
    pass


def NormalizeModuleAPIMacro(filepath, macro):
    #RE_API_MACRO = r"(class|struct)\s*(\w+_API)\s+\w+"
    RE_API_MACRO = r"\s+([A-Z]+_API)\s+"
    
    if macro == "":
        return
    pass
    lines = FileUtils.GetAllLines(filepath)
    num = len(lines)
    changed = False
    for i in range(0, num):
        line = lines[i]
        match = re.search(RE_API_MACRO, line)
        if not match == None:
            old = match.group(1)
            if not old == macro:
                line = line.replace(old, macro)
                changed = True
                lines[i] = line
            pass
        pass
    pass
    if changed:
        logging.warning("NormalizeModuleAPIMacro: %s", filepath)
        f = open(filepath, "w", encoding="UTF-8")
        f.writelines(lines)
        f.close()
    else:
        logging.info("NormalizeModuleAPIMacro: %s, No Changed", filepath)
    pass


def NormalizeModuleAPIMacroOfUE4(mdl_dir):
    if not FileUtils.IsUE4ModuleDir(mdl_dir):
        logging.error("NormalizeModuleAPIMacroOfUE4() [%s] Is Not UE4Module!!!", mdl_dir)
        return
    pass
    mdl_name = os.path.basename(mdl_dir)
    api_macro = mdl_name.upper() + "_API"
    paths = FileUtils.GetAllFiles(mdl_dir, ".h")
    for path in paths:
        NormalizeModuleAPIMacro(path, api_macro)
    pass


def NormalizeModuleAPIMacroOfUE4Auto(srcdir_or_mdldir):
    if not FileUtils.IsUE4ModuleDir(srcdir_or_mdldir):
        dirs = FileUtils.GetAllUE4ModuleDirs(srcdir_or_mdldir)
        for dir in dirs:
            NormalizeModuleAPIMacroOfUE4(dir)
        pass
    else:
        NormalizeModuleAPIMacroOfUE4(srcdir_or_mdldir)
    pass


def ListNotUtf8SourceFile(srcdir):
    paths = FileUtils.GetAllFiles(srcdir, ".h|.cpp")
    for path in paths:
        if not FileUtils.EnsureUtf8WithChinese(path):
            logging.warning(path)
        pass
    pass



def CommandLine(args):
    logging.getLogger().setLevel(logging.WARN)
    coloredlogs.install(level='WARN')
    logging.info(args)
    if args[1] == "NormalizeIncludeSlash":
        NormalizeIncludeSlashAuto(args[2])
    elif args[1] == "NormalizeModuleAPIMacro":
        NormalizeModuleAPIMacroOfUE4Auto(args[2])
    elif args[1] == "ListNotUtf8SourceFile":
        ListNotUtf8SourceFile(args[2])
    pass
    




if __name__ == '__main__':
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    CommandLine(sys.argv)
    #CommandLine(["", "ListNotUtf8SourceFile", r"E:\Project\DFMProj\DFM\Source"])
    #CommandLine(["", "NormalizeModuleAPIMacro", r"W:\Project\DFMProj_Refactor\DFM\Source"])
    