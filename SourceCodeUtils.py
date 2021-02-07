import os
import re

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

