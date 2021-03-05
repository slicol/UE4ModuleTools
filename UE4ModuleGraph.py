import sys
import os
import FileUtils
import re
import logging
import coloredlogs
import SourceCodeUtils
from UE4Module import UE4Module



class DFMModuleGraphSide:
    SrcNode = ""
    DstNode = ""
    def __init__(self, src,dst):
        self.SrcNode = src
        self.DstNode = dst


class DFMModuleGraphNode:
    Name = ""
    Layer = ""
    NextNodes = [] 
    
    def __init__(self, name):
        self.Name = name
        self.Layer = ""
        self.NextNodes = []
        


class DFMModuleGraphLayer:
    Name = ""
    Nodes = [] 
    Sides = []
    NextLayers = []

    def __init__(self, name):
        self.Name = name
        self.Nodes = []
        self.Sides = []
        self.NextLayers = []



def CollectModuleNode(mdldir, modules:{}):
    module = UE4Module(mdldir)
    module.ParserRules()
    node = DFMModuleGraphNode(module.Name)
    node.NextNodes = module.Rules.PublicDependencyModuleNames
    node.NextNodes.extend(module.Rules.PrivateDependencyModuleNames)
    modules[node.Name] = node
    return node


def CollectLayerNodes(layerdir, layers:{}, modules:{}):
    layer = DFMModuleGraphLayer(os.path.dirname(layerdir))
    mdl_dirs = FileUtils.GetAllUE4ModuleDirs(layerdir)
    for mdl_dir in mdl_dirs:
        node = CollectModuleNode(mdl_dir, modules)
        node.Layer = layer.Name
        layer.Nodes.append(node)
    pass
    layers[layer.Name] = layer
    return layer


def CollectLayerSides(layer:DFMModuleGraphLayer, sides:[], layers:{}, modules:{}):
    for node in layer.Nodes:
        






def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    basedir = args[1]

    modules = {}
    layers = {}
    sides = []
    CollectModuleNode(basedir + "/Source/DFM", modules)
    CollectLayerNodes(basedir + "/Source/Editor", layers, modules)
    CollectLayerNodes(basedir + "/Source/DFMBusiness", layers, modules)
    CollectLayerNodes(basedir + "/Source/DFMGameMode", layers, modules)
    CollectLayerNodes(basedir + "/Source/DFMGameCore", layers, modules)
    CollectLayerNodes(basedir + "/Source/GPFramework", layers, modules)

    sides.append(DFMModuleGraphSide("DFM","DFMBusiness"))
    sides.append(DFMModuleGraphSide("DFM","DFMGameMode"))
    sides.append(DFMModuleGraphSide("DFM","DFMGameCore"))
    
    sides.append(DFMModuleGraphSide("DFMBusiness","DFMGameCore"))
    sides.append(DFMModuleGraphSide("DFMGameMode","DFMGameCore"))

    sides.append(DFMModuleGraphSide("DFMGameCore","GPFramework"))

    for layer in layers.values:
        CollectLayerSides(layer, sides,layers,modules)
    pass




    

if __name__ == '__main__':
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    CommandLine(sys.argv)
    CommandLine(["", r"I:\Project\DFMProj\DFM"])