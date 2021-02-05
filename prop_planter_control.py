import RLPy
import ui_components as UI
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance


class PropPlanterUiControl:
    def __init__(self, dialog):
        self.dialog = dialog

        # ui
        ui = {}
        ui['selections'] = [UI.SelectionControl(0, "Selection_0", parent=self.dialog.layout())]
        ui['size'] = UI.Vector3Control('Size', parent=dialog.layout())
        ui["apply"] = UI.Button("apply", parent=self.dialog.layout())

        self.ui = ui

        # data
        self.selected_objects = self.get_selected_objects()


    def get_selected_objects(self):
        return RLPy.RScene.GetSelectedObjects()

    def handle_selected_change_event(self):
        self.refresh()

        for idx, obj in enumerate(self.selected_objects):
            name = obj.GetName()
            if idx < len(self.ui['selections']):
                self.ui['selections'][idx].set_label(name)
            else:
                self.ui['selections'].append(uic.SelectionControl(idx, name, parent=self.dialog.layout()))


    def refresh(self):
        self.selected_objects = self.get_selected_objects()
        print('len of selection:', len(self.selected_objects))




