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
        a = 0
        #logging.info("NormalizeIncludeSlash: %s, No Changed", filepath)
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




def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    if args[1] == "NormalizeIncludeSlash":
        NormalizeIncludeSlashAuto(args[2])
    pass
    


if __name__ == '__main__':
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    CommandLine(sys.argv)
    #CommandLine(["", "NormalizeIncludeSlash", r"E:\Project\DFMProj\DFM\Source"])
    