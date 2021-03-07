import sys
import os
import FileUtils
import re
import logging
import coloredlogs
import SourceCodeUtils
from UE4Module import UE4Module



class UE4ModuleGraphSide:
    SrcNodeName = ""
    DstNodeName = ""
    def __init__(self, src_node_name,dst_node_name):
        self.SrcNodeName = src_node_name
        self.DstNodeName = dst_node_name


class UE4ModuleGraphNode:
    Name = ""
    LayerName = ""
    NextNodeNames = [] 
    
    def __init__(self, name):
        self.Name = name
        self.LayerName = ""
        self.NextNodeNames = []
        


class UE4ModuleGraphLayer:
    Name = ""
    Nodes = [] 
    Sides = []
    NextLayers = []

    def __init__(self, name):
        self.Name = name
        self.Nodes = []
        self.Sides = []
        self.NextLayers = []



def CollectModuleNode(mdldir, layername:str, modules:{}):
    module = UE4Module(mdldir)
    module.ParserRules()
    node = UE4ModuleGraphNode(module.Name)
    node.NextNodeNames = module.Rules.PublicDependencyModuleNames
    node.NextNodeNames.extend(module.Rules.PrivateDependencyModuleNames)
    node.LayerName = layername
    modules[node.Name] = node
    return node


def CollectLayerNodes(layerdir, layers:{}, modules:{}):
    layer = UE4ModuleGraphLayer(os.path.basename(layerdir))
    mdl_dirs = FileUtils.GetAllUE4ModuleDirs(layerdir)
    for mdl_dir in mdl_dirs:
        node = CollectModuleNode(mdl_dir, layer.Name, modules)
        layer.Nodes.append(node)
    pass
    layers[layer.Name] = layer
    return layer



def CollectLayerSides(layer:UE4ModuleGraphLayer, sides:[], layers:{}, modules:{}):
    for node in layer.Nodes:
        for next_node_name in node.NextNodeNames:
            next_node:UE4ModuleGraphNode = modules.get(next_node_name)
            if not next_node == None:
                if next_node.LayerName == layer.Name or next_node.LayerName == "" :
                    layer.Sides.append(UE4ModuleGraphSide(node.Name, next_node.Name))
                    sides.append(UE4ModuleGraphSide(node.Name, next_node.Name))
                else:
                    next_layer:UE4ModuleGraphLayer = layers.get(next_node.LayerName)
                    if not next_layer == None:
                        if layer.NextLayers.index(next_layer) < 0:
                            layer.NextLayers.append(next_layer)
                            sides.append(UE4ModuleGraphSide(layer.Name, next_layer.Name))
                        pass
                    else:
                        logging.error("Layer Is Not Exist: %s", next_node.LayerName)
                    pass
                pass
            else:
                logging.warning("Module Is Out Of Graph Scope: %s", next_node_name)
            pass
        pass
    pass








def CommandLine(args):
    logging.getLogger().setLevel(logging.DEBUG)
    coloredlogs.install(level='DEBUG')
    logging.info(args)
    basedir = args[1]
    layernames = args[2].split("|")

    modules = {}
    layers = {}
    sides = []

    for layername in layernames:
        CollectLayerNodes(basedir + "/Source/" + layername, layers, modules)    
    pass
    
    for layer in layers.values:
        CollectLayerSides(layer, sides,layers,modules)
    pass

    for side in sides:
        logging.info("%s --> %s", side.SrcNodeName, side.DstNodeName)
    pass






    

if __name__ == '__main__':
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    #CommandLine(sys.argv)
    CommandLine(["", r"I:\Project\DFMProj\DFM", r"Editor|DFMBusiness|DFMGameMode|DFMGameCore|GPFramework"])