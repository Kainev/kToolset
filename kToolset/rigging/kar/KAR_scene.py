# KAR Imports
import modules.module; reload(modules.module)
from modules.module import Module
class Scene(object):
    """
    Container class that manages the current modules and the scene hierarchy
    """
    def __init__(self):
        # Stores all currently added modules, using their UUID as the dictionary key
        self._modules = {}

    def add_module(self, scene_module):
        """
        Adds a given module to the scene

        :param scene_module: Module instance to add to scene
        """
        if isinstance(scene_module, Module):
            self._modules[scene_module.uuid] = scene_module
        else:
            print("'%s' is not a valid module.." % scene_module)

    def get_all_modules(self):
        """
        Returns dictionary of all scene modules
        """
        return self._modules

    def get_module(self, identifier):
        """
        Returns a specific module given its UUID

        :param identifier: UUID of module to return
        """
        try:
            scene_module = self._modules[identifier]
            return scene_module
        except KeyError:
            return
