
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
        self._placement_systems = {}

    def add_module(self, scene_module, trigger_update=True):
        """
        Adds a given module to the scene

        :param scene_module: Module instance to add to scene
        :param trigger_update
        """
        self._modules[scene_module.uuid] = scene_module
        if trigger_update:
            self.force_update()

    def delete_modules(self, identifiers, trigger_update=True):
        """
        Deletes  a list of rig modules identified by their UUID.

        This removes all Maya component as forces a UI update.
        """
        for id in identifiers:
            try:
                del self._modules[id]
            except KeyError:
                pass

        if trigger_update:
            self.force_update()

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
        """
        Emits a scene_updated signal.

        Many parts of the UI are hooked into this signal such as the Outliner. This will cause them to update
        to reflect the scenes current state.
        """
        self.scene_updated.emit()