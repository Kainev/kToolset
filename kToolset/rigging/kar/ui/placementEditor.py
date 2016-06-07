# PySide Imports
import PySide.QtCore as qc
import PySide.QtGui as qg

# KAR Imports
import widgets

from .. import modules; reload(modules)


class PlacementEditor(qg.QDockWidget):
    """
    The ModuleOutliner is a list, similar to the Maya outliner, that shows all currently installed modules
    and allows you to select a module to edit.
    """
    # SIGNALS
    add_module = qc.Signal(list)

    # AVAILABLE MODULES
    MODULES = [modules.ArmModule,
               modules.HandModule,
               modules.SpineModule,
               modules.LegModule,
               modules.FootModule,
               modules.JointModule]

    def __init__(self, scene, parent=None):
        super(PlacementEditor, self).__init__('Placement Editor', parent=parent)
        self.setFloating(False)
        self.setAllowedAreas(qc.Qt.LeftDockWidgetArea | qc.Qt.RightDockWidgetArea)
        self.setMinimumWidth(175)

        self.scene = scene

        self.content_widget = qg.QWidget()
        self.content_widget.setLayout(qg.QVBoxLayout())
        self.content_widget.layout().setContentsMargins(5, 5, 5, 5)
        self.content_widget.layout().setSpacing(2)
        self.content_widget.layout().setAlignment(qc.Qt.AlignTop)
        self.setWidget(self.content_widget)

        # GLOBAL SECTION
        global_widget = qg.QWidget(self)
        global_widget.setLayout(qg.QVBoxLayout())

        global_widget.layout().addWidget(widgets.decorators.Heading('Global'))

        g_lay_create_delete = qg.QHBoxLayout()
        global_widget.layout().addLayout(g_lay_create_delete)

        g_btn_create = qg.QPushButton('Create All', self)
        g_btn_delete = qg.QPushButton('Delete All', self)

        g_lay_create_delete.addWidget(g_btn_create)
        g_lay_create_delete.addWidget(g_btn_delete)

        g_lay_geo_vis = qg.QHBoxLayout()
        global_widget.layout().addLayout(g_lay_geo_vis)

        g_lb_geo_vis = qg.QLabel('Geometry Visibility:', self)
        g_comb_geo_vis = qg.QComboBox(self)

        g_lay_geo_vis.addWidget(g_lb_geo_vis)
        g_lay_geo_vis.addWidget(g_comb_geo_vis)

        g_btn_reset = qg.QPushButton('Reset All', self)
        global_widget.layout().addWidget(g_btn_reset)

        self.content_widget.layout().addWidget(global_widget)

        # SELECTED SECTION
        selected_widget = qg.QWidget(self)
        selected_widget.setLayout(qg.QVBoxLayout())

        selected_widget.layout().addWidget(widgets.decorators.Heading('Selected'))

        s_lay_create_delete = qg.QHBoxLayout()
        selected_widget.layout().addLayout(s_lay_create_delete)

        g_btn_create = qg.QPushButton('Create', self)
        g_btn_delete = qg.QPushButton('Delete', self)

        s_lay_create_delete.addWidget(g_btn_create)
        s_lay_create_delete.addWidget(g_btn_delete)

        s_lay_geo_vis = qg.QHBoxLayout()
        selected_widget.layout().addLayout(s_lay_geo_vis)

        s_lb_geo_vis = qg.QLabel('Geometry Visibility:', self)
        s_comb_geo_vis = qg.QComboBox(self)

        s_lay_geo_vis.addWidget(s_lb_geo_vis)
        s_lay_geo_vis.addWidget(s_comb_geo_vis)

        s_btn_reset = qg.QPushButton('Reset', self)
        selected_widget.layout().addWidget(s_btn_reset)

        self.content_widget.layout().addWidget(selected_widget)


