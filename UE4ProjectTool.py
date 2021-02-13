import sys
import os
import FileUtils
import re
import logging
import coloredlogs


def GetModuleNamesOfLayer(basedir):
    dirs = os.listdir(basedir)
    result = []
    for dirname in dirs:
        mdl_build_file = basedir + "/" + dirname + "/" + dirname + ".Build.cs"
        if os.path.exists(mdl_build_file):
            result.append(dirname)
        pass
    pass
    return result


def GenUProjectModuleConfig(mdl_name, type, loading_phase):
    cfg  = "\t\t{\"Name\":\"{0}\",\t\t\"Type\":\"{1}\",\t\t\"LoadingPhase\":\"{2}\"}"
    cfg = cfg.replace("{0}", mdl_name)
    cfg = cfg.replace("{1}", type)
    cfg = cfg.replace("{2}", loading_phase)
    return cfg


def GenUProjectModuleConfigOfLayer(basedir, type, loading_phase):
    names = GetModuleNamesOfLayer(basedir)
    result = ""
    for name in names:
        cfg = GenUProjectModuleConfig(name, type, loading_phase)
        if result == "":
            result = cfg
        else:
            result += ",\n"
            result += cfg
        pass
    pass
    result += "\n"
    logging.info("\n" + result)
    return result




def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    if args[1] == "GenLayer":
        GenUProjectModuleConfigOfLayer(args[2], args[3], args[4])
    pass
    




if __name__ == '__main__':
    #CommandLine(sys.argv)
    CommandLine(["", "GenLayer", r"W:\Project\DFMProj_Refactor\DFM\Source\DFMGameCore", "Runtime", "Default"])
    CommandLine(["", "GenLayer", r"W:\Project\DFMProj_Refactor\DFM\Source\GPFramework", "Runtime", "Default"])
    CommandLine(["", "GenLayer", r"W:\Project\DFMProj_Refactor\DFM\Source\Editor", "Runtime", "Default"])
    
    
    


    