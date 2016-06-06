# Python Imports
import uuid


class Module(object):
    """
    Base class of all rig modules.

    Establishes a new UUID.
    """
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.name = ''
        self.parent = None  # UUID of module to be parented to
        self._attachment_point = None  # Maya node of parent to be parented under


