import os
import logging


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