import os


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
def GetAllFiles(dirpath, _extnames = ""):
    files = os.listdir(dirpath)
    result = []
    extnames = []
    if isinstance(_extnames, list):
        extnames = _extnames
    else:
        extnames = _extnames.split("|")
    pass

    for file in files:
        filepath = dirpath + "/" + file;

        if not os.path.isdir(filepath):
            if StringEndswith(filepath, extnames) :
                result.append(filepath)
            pass
        else:
            tmp = GetAllFiles(filepath, extnames)
            result.extend(tmp)
        pass
    pass
    return result
