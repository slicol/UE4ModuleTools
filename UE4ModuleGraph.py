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

    def GetSortKey(side):
        return side.SrcNodeName + side.DstNodeName


class UE4ModuleGraphNode:
    Name = ""
    LayerName = ""
    NextNodeNames = [] 
    NextLayerNames = []
    
    def __init__(self, name):
        self.Name = name
        self.LayerName = ""
        self.NextNodeNames = []
        self.NextLayerNames = []
        


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



def CollectLayerSides(layer:UE4ModuleGraphLayer, sides:[], layers:{}, modules:{}, enable_module_to_layer = False):
    for node in layer.Nodes:
        node_is_standalone = True
        for next_node_name in node.NextNodeNames:
            next_node:UE4ModuleGraphNode = modules.get(next_node_name)
            if not next_node == None:
                if next_node.LayerName == layer.Name or next_node.LayerName == "" :
                    layer.Sides.append(UE4ModuleGraphSide(node.Name, next_node.Name))
                    sides.append(UE4ModuleGraphSide(node.Name, next_node.Name))
                    node_is_standalone = False
                else:
                    next_layer:UE4ModuleGraphLayer = layers.get(next_node.LayerName)
                    if not next_layer == None:
                        if not next_layer in layer.NextLayers:
                            layer.NextLayers.append(next_layer)
                            sides.append(UE4ModuleGraphSide("[Layer]" + layer.Name, "[Layer]" + next_layer.Name))
                            node_is_standalone = False
                        pass
                        if not next_layer.Name in node.NextLayerNames:
                            node.NextLayerNames.append(next_layer.Name)
                            if enable_module_to_layer:
                                sides.append(UE4ModuleGraphSide(node.Name, "[Layer]" + next_layer.Name))
                                node_is_standalone = False
                            pass
                        pass    
                    else:
                        logging.error("Layer Is Not Exist: %s", next_node.LayerName)
                    pass
                pass
            else:
                if next_node_name.startswith("[Layer]"):
                    next_layer_name = next_node_name[len("[Layer]"):]
                    next_layer:UE4ModuleGraphLayer = layers.get(next_layer_name)
                    if not next_layer == None:
                        if not next_layer in layer.NextLayers:
                            layer.NextLayers.append(next_layer)
                            sides.append(UE4ModuleGraphSide("[Layer]" + layer.Name, "[Layer]" + next_layer.Name))
                            node_is_standalone = False
                        pass
                        if not next_layer.Name in node.NextLayerNames:
                            node.NextLayerNames.append(next_layer.Name)
                            if enable_module_to_layer:
                                sides.append(UE4ModuleGraphSide(node.Name, "[Layer]" + next_layer.Name))
                                node_is_standalone = False
                            pass
                        pass    
                    else:
                        logging.error("Layer Is Not Exist: %s", next_node.LayerName)
                    pass
                else:
                    logging.warning("Module Is Out Of Graph Scope: %s -> %s", node.Name, next_node_name)
                pass
            pass
        pass
        if node_is_standalone :
            sides.append(UE4ModuleGraphSide(node.Name, ""))
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
        CollectLayerNodes(basedir + "/" + layername, layers, modules)    
    pass
    
    for layer in layers.values():
        CollectLayerSides(layer, sides,layers,modules,True)
    pass

    sides.sort(key=UE4ModuleGraphSide.GetSortKey)

    dump_file_name = "UE4ModuleGraphDump.csv"
    if len(args) > 3:
        dump_file_name = args[3]
    pass

    f = open(basedir + "/" + dump_file_name, mode="w")
    for side in sides:
        logging.info("%s --> %s", side.SrcNodeName, side.DstNodeName)
        f.write("{0},{1}\n".format(side.SrcNodeName, side.DstNodeName))
    pass
    f.close()



if __name__ == '__main__':
    '''
    python UE4ModuleGraph.py {ProjectSourcePath} {Layer1|Layer2|...} [DumpFileName]
    '''
    curdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(curdir)
    CommandLine(sys.argv)
    #CommandLine(["", r"I:\Project\DFMProj\DFM\Source", r"Editor|DFMBusiness|DFMGameMode|DFMGameCore|GPFramework"])