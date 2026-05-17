import json
import shutil
from _versioning import _V

VERSIONS = list(map(_V, ["0.1"])) # add more as needed

# This is for external reference for now
_EXTENSIONS = {"pen", "wedo2", "music", "microbit", "text2speech", "translate", "videoSensing", "makeymakey", "boost", "gdxfor"}

class LibSB3Error(Exception):
    """General Exception for all errors incurred while compiling a scratchblocks program to a Scratch file."""
    pass

class _Target:
    def __init__(self, data):
        self.__dict__.update(data)
        

class sb3writer:
    """Object to implement compilation of scratchblocks programs to Scratch files."""
    def __init__(self, version):
        """sb3writer factory"""
        if not isinstance(version, _V):
            try:
                self.version = _V(version)
            except:
                raise LibSB3Error("bad version: %s" % version)
        else:
            self.version = version
            
        if self.version not in VERSIONS:
                raise LibSB3Error("bad version: %s" % self.version)
        
        self.project = { # a blank slate to start with
                     "targets":[],
                     "monitors":[],
                     "extensions":[],
                     "meta":{              # as per https://en.scratch-wiki.info/wiki/Scratch_File_Format#Metadata
                         "semver":"3.0.0",
                         "vm":"0.2.0", # even though there are no VMs here
                         "agent":"sb3-writer-%s" % self.version
                         }
                    }

    def add_extension(self, extension):
        """Add an extension to the project, based on this extension's identifier. A list of identifiers for
        built-in core extensions comes with _EXTENSIONS.
        """
        if extension in _EXTENSIONS and extension not in self.project["extensions"]:
            self.project["extensions"].append(extension)
        
    def rm_extension(self, extension):
        """Remove an extension in the project, based on this extension's identifier. A list of identifiers
        for built-in core extensions comes with _EXTENSIONS.
        """
        if extension in self.project["extensions"]:
            self.project["extensions"].remove(extension)
        
    def add_target(self, *, isStage=False, name=''):
        """Add a blank target to the JSON.
        Call with exactly one keyword-argument (either isStage:bool
        or name:str)
        """
        if isStage == (name != ''):
            raise LibSB3Error("Specify exactly one of isStage or name")
        self.project["targets"].append({
            "isStage":isStage,
            "name":"Stage" if isStage else name,
            "variables":{},
            "lists":{},
            "broadcasts":{},
            "blocks":{},
            "comments":{},
            "costumes":[],
            "currentCostume":0,
            "sounds":[],
            "layerOrder":0,
            "volume":100
        })
        if isStage:
            self.project["targets"][-1].update({
                "tempo":60, 
                "videoTransparency":50, 
                "textToSpeechLanguage":"en", 
                "videoState":"off"
            })
        else:
            self.project["targets"][-1].update({
                "x":0,
                "y":0,
                "visible":True,
                "size":100,
                "direction":90,
                "draggable":False,
                "rotationStyle":"all around",
            })
    
    def get_target(self, *, isStage=False, name=''):
        """Return a reference to the target identified by name.
        Call with exactly one keyword-argument (either isStage:bool
        or name:str)
        """
        if isStage == (name != ''):
            raise LibSB3Error("Specify exactly one of isStage or name")
        if isStage:
            for di in self.project["targets"]:
                if di["isStage"]:
                    return _Target(di)
        else:
            for di in self.project["targets"]:
                if di["name"] == name:
                    return _Target(di)
        raise LibSB3Error("%s not found in JSON" % name)
