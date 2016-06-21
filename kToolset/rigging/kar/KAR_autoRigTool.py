class KAutoRigger(object):
    def __init__(self):
        self.modules = {}
        self.placement_systems = {}

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # INTERFACE FUNCTIONS
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def add_module(self, scene_module, trigger_update=True):
        """
        Adds a given module to the scene

        :param scene_module: Module instance to add to scene
        :param trigger_update
        """
        self.modules[scene_module.uuid] = scene_module

    def delete_module(self, identifiers, trigger_update=True):
        """
        Deletes a list of rig modules identified by their UUID.

        This removes all Maya component as forces a UI update.
        """
        if not isinstance(identifiers, list):
            identifiers = [identifiers]

        for _id in identifiers:
            try:
                del self.modules[_id]
            except KeyError:
                pass

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # PLACEMENT SYSTEMS
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    def build_placement_systems(self, system=None, build_all=False):
        """
        Creates an instance of each modules placement system class and runs the function
        to build the base system (i.e geo, joints, controls).

        :param system: UUID of specific module to build
        :param build_all: Boolean: If true, builds ALL placement systems for all initialized modules
        :return:
        """
        pass

    def assemble_placement_systems(self):
        """
        Parents each placement system in hierarchy as defined by the user.
        :return:
        """
        pass

    def delete_placement_system(self, system=None, build_all=False):
        """
        Deletes an instance/s of each modules placement system and all related Maya nodes

        :param system: UUID of specific modules placement system to delete
        :param build_all: Boolean: If True, removes ALL placement systems
        :return:
        """
        pass

    def show_placement_geo(self, val):
        """
        Turns the visibility of all placement geometry off or on. When visbility is off, user is left only with the
        joints and controls visible. This is useful for more accurate placement of joint locations

        :param val: Boolean: If True, all placement geometry is set to visible. If False, all placement geometry
                    is hidden
        :return:
        """
        pass

    def get_placement_position(self, system=None, build_all=False):
        """
        Returns the positioning information from each placement system

        :param system: UUID of specific modules placement information to retireve
        :param build_all: Boolean: If True, returns all modules placement information
        :return:
        """
        pass