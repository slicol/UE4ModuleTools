import os
import logging
import chardet
import re

########################################################################
def StringEndswith(str, suffix):
    if isinstance(suffix,list):
        for tmp in suffix:
            if str.endswith(tmp):
                return True
            pass
        pass
    else:
        return str.endswith(suffix)
    pass
    return False


########################################################################
def GetAllFiles(dirpath, _extnames = "",_mtimescope = []):
    files = os.listdir(dirpath)
    result = []
    extnames = []
    if isinstance(_extnames, list):
        extnames = _extnames
    else:
        extnames = _extnames.split("|")
    pass

    bValidModifyTimeScope = len(_mtimescope) == 2
    mtime_min = 0
    mtime_max = 0
    if bValidModifyTimeScope:
        mtime_min = _mtimescope[0]
        mtime_max = _mtimescope[1]
    pass

    for file in files:
        filepath = dirpath + "/" + file

        if not os.path.isdir(filepath):
            if StringEndswith(filepath, extnames) :
                if bValidModifyTimeScope:
                    st = os.stat(filepath)
                    if st.st_mtime >= mtime_min and st.st_mtime <= mtime_max:
                        result.append(filepath)
                    pass
                else:
                    result.append(filepath)
                pass
            pass
        else:
            tmp = GetAllFiles(filepath, extnames, _mtimescope)
            result.extend(tmp)
        pass
    pass
    return result



def GetAllLines(filepath):
    lines = []
    try:
        f = open(filepath,"r",encoding="UTF-8")
        lines = f.readlines()
        f.close()
    except Exception as e:
        f.close()

        try:
            f = open(filepath, "r")
            lines = f.readlines()
            f.close()
        except Exception as e:
            f.close()
            
            logging.error("GetAllLines: %s", filepath)
            logging.error(e)
            lines = []
        pass
    pass
    return lines


def GetAllUE4ModuleDirs(src_dir):
    mdl_build_files = GetAllFiles(src_dir, ".Build.cs")
    mdl_dirs = []
    for filepath in mdl_build_files:
        mdl_dir = os.path.dirname(filepath)
        mdl_dirs.append(mdl_dir)
    pass
    return mdl_dirs

def IsUE4ModuleDir(dir):
    mdl_name = os.path.basename(dir)
    mdl_rule_file_path = dir + "/" + mdl_name + ".Build.cs"
    return os.path.exists(mdl_rule_file_path)


def IsUtf8File(filepath):
    f = open(filepath,"rb")
    rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    if encoding == None:
        logging.error("%s <encoding = None>!!!", filepath)
        return False
    pass

    if encoding.lower().startswith("utf-8"):
        if result["confidence"] >= 0.99:
            return True
        pass
    pass
    return False

def DetectUtf8FileConfidence(filepath):
    f = open(filepath,"rb")
    rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    if encoding == None:
        logging.error("%s <encoding = None>!!!")
        return 0
    pass    
    if encoding.lower().startswith("utf-8"):
        return result["confidence"]
    pass
    return 0


def EnsureUtf8WithChinese(filepath):
    RE_CheckChinese = re.compile(u'[\u4e00-\u9fa5]+',re.UNICODE)
    if IsUtf8File(filepath):
        return True
    pass
    lines = GetAllLines(filepath)
    flag = 0
    for line in lines:
        match = re.search(RE_CheckChinese, line)
        if match is None:
            continue
        pass
        
        linesize = len(line)
        for i in  range(linesize):
            if flag == 0:
                if ord(line[i]) & 0x80 == 0x00:
                    flag = 0
                elif ord(line[i]) & 0xE0 == 0xC0:
                    flag = 1
                elif ord(line[i]) & 0xF0 == 0xE0:
                    flag = 2
                elif ord(line[i]) & 0xF8 == 0xF0:
                    flag = 3
                else:
                    return False
                pass
            else:
                if not ord(line[i]) & 0xC0 == 0x80:
                    return False
                pass
                flag -= 1
            pass
        pass
    pass
    return True    
    

