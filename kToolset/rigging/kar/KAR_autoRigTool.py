
class KAutoRigger(object):
    def __init__(self):
        self.activeModules = {}
        self.inactiveModules = {}
        self.placement_systems = {}

    ##----------------------------------------------------------------------------------------------------------------##
    ##----------------------------------------------------------------------------------------------------------------##
    ## PLACEMENT SYSTEMS
    ##----------------------------------------------------------------------------------------------------------------##
    ##----------------------------------------------------------------------------------------------------------------##
    def build_placement_systems(self, system = None, all = False):
        """
        Creates an instance of each modules placement system class and runs the function
        to build the base system (i.e geo, joints, controls).

        :param system: UUID of specific module to build
        :param all: Boolean: If true, builds ALL placement systems for all initialized modules
        :return:
        """
        pass

    def assemble_placement_systems(self):
        """
        Parents each placement system in hierarchy as defined by the user.
        :return:
        """
        pass

    def delete_placement_system(self, system = None, all = False):
        """
        Deletes an instance/s of each modules placement system and all related Maya nodes

        :param system: UUID of specific modules placement system to delete
        :param all: Boolean: If True, removes ALL placement systems
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

    def get_placement_position(self, system = None, all = False):
        """
        Returns the positioning information from each placement system

        :param system: UUID of specific modules placement information to retireve
        :param all: Boolean: If True, returns all modules placement information
        :return:
        """
        pass