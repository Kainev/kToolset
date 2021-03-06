# Python Imports

# KAR Imports
import module; reload(module)
from module import Module
from ..utils import KAR_uiUtils as kuiUtils; reload(kuiUtils)


class FootModule(Module):
    icon = kuiUtils.get_icon('Biped_Foot')

    def __init__(self):
        super(FootModule, self).__init__()


class _FootPlacementSystem(object):
    """
    ArmPlacementSystem class is responsible for creating all placement geometry and rigging structures for the user
    to place to determine the joint positioning of the final arm rig
    """
    def __init__(self):
        pass

    def show_geometry(self, val):
        """
        showGeometry accepts a boolean parameter which turns the visibility for all geometry pertaining to the
        individual module on or off

        :param val: Accepts a boolean parameter. If True, all geometry will be visible.
               If False, all geometry will be hidden
        :return:
        """
        pass
