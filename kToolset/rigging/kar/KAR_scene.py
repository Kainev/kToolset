
import PySide.QtCore as qc
# KAR Imports
import modules.module; reload(modules.module)
from modules.module import Module

import modules; reload(modules)

class Scene(qc.QObject):
    """
    Container class that manages the current modules and the scene hierarchy
    """

    scene_updated = qc.Signal()

    # AVAILABLE MODULES
    MODULES = [modules.ArmModule,
               modules.HandModule,
               modules.SpineModule,
               modules.LegModule,
               modules.FootModule,
               modules.JointModule]

    def __init__(self):
        super(Scene, self).__init__()
        # Stores all currently added modules, using their UUID as the dictionary key
        self._modules = {}

    def add_module(self, scene_module, trigger_update=True):
        """
        Adds a given module to the scene

        :param scene_module: Module instance to add to scene
        :param trigger_update
        """
        #if isinstance(scene_module, Module):
        self._modules[scene_module.uuid] = scene_module
        if trigger_update:
            self.scene_updated.emit()
        #else:
            #print("'%s' is not a valid module.." % scene_module)

    def delete_modules(self, identifiers, trigger_update=True):
        for id in identifiers:
            try:
                del self._modules[id]
            except KeyError:
                pass

        if trigger_update:
            self.scene_updated.emit()

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

    def force_update(self):
        self.scene_updated.emit()