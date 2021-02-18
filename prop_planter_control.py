import RLPy
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance
import ui_components as UI


class PropPlanterTabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super(PropPlanterTabWidget, self).__init__()

        self.prop_widget = PropConfigControl()
        self.place_widget = PlaceConfigControl()

        self.addTab(self.prop_widget, "Property")
        self.addTab(self.place_widget, "Place")

    def handle_selected_change_event(self):
        self.currentWidget().handle_selected_change_event()


class PlaceConfigControl(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlaceConfigControl, self).__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        ui = {}
        ui["selection"] = UI.SelectionControl(0, "Place", parent=self.layout)
        self.ui = ui.copy()
        # self.refresh()

        if parent:
            parent.addWidget(self)

    def handle_selected_change_event(self):
        self.refresh()
        try:
            name = self.selected_objects[0].GetName()
            self.ui['selection'].set_item_label(1, name)
        except:
            return

    def refresh(self):
        self.selected_objects = self.__get_selected_objects()

    def __get_selected_objects(self):
        return RLPy.RScene.GetSelectedObjects()


class PropConfigControl(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # ui
        ui = {}
        ui['selection'] = UI.SelectionControl(0, "Property", parent=self.layout)
        ui['size'] = UI.Vector3Control('Size', parent=self.layout)
        ui['clone'] = UI.SliderControl("Clone", parent=self.layout)

        # data
        self.ui = ui.copy()
        # self.refresh()

        if parent:
            parent.addWidget(self)

    def handle_selected_change_event(self):
        self.refresh()
        try:
            name = self.selected_objects[0].GetName()
            self.ui['selection'].set_item_label(1, name)
        except:
            return

    def refresh(self):
        self.selected_objects = self.__get_selected_objects()

    def __get_selected_objects(self):
        return RLPy.RScene.GetSelectedObjects()