import RLPy
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance
import ui_components as UI


class PropPlanterTabWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super(PropPlanterTabWidget, self).__init__()

        self.prop_widget = PropPlanterUiControl()
        self.place_widget = PlaceControl()

        self.addTab(self.prop_widget, "Property")
        self.addTab(self.place_widget, "Place")

    def handle_selected_change_event(self):
        self.prop_widget.handle_selected_change_event()


class PlaceControl(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlaceControl, self).__init__()

        top_layout = QtWidgets.QVBoxLayout()

        bot_layout = QtWidgets.QHBoxLayout()
        bot_layout.setSpacing(0)
        bot_layout.setContentsMargins(0, 0, 3, 0)

        # set the place object label layout
        place_label = QtWidgets.QLineEdit("")
        bot_layout.addWidget(place_label)

        # the button to set the place that prop will be planted on it
        button = QtWidgets.QPushButton("Set Place")
        button.clicked.connect(self.set_place)
        bot_layout.addWidget(button)

        top_layout.addWidget(QtWidgets.QLabel("Place"))
        top_layout.addLayout(bot_layout)

        self.setLayout(top_layout)
        self.place_label = place_label

        if parent:
            parent.addWidget(self)

    def set_place(self):
        selected_objs = RLPy.RScene.GetSelectedObjects()

        if len(selected_objs) == 1:
            self.place_label.setText("")
        elif len(selected_objs) == 0:
            RLPy.RUi.MessageBox("PropPlanter",
                                "You have to select first, ant then a prop to be the place",
                                RLPy.EMsgButton_Ok)

        else:
            RLPy.RUi.MessageBox("PropPlanter",
                                "You can select multiple place",
                                RLPy.EMsgButton_Ok)


class PropPlanterUiControl(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.root_layout = QtWidgets.QVBoxLayout()
        self.prop_layout = QtWidgets.QVBoxLayout()
        self.root_layout.addLayout(self.prop_layout)
        self.setLayout(self.root_layout)

        # ui
        ui = {}
        ui['selections'] = [UI.SelectionControl(0, "Selection_0", parent=self.prop_layout)]
        ui['size'] = UI.Vector3Control('Size', parent=self.root_layout)
        ui['clone'] = UI.SliderControl("Clone", parent=self.root_layout)
        ui["apply"] = UI.Button("apply", parent=self.root_layout)

        # data
        self.ui = ui.copy()
        self.refresh()

        if parent:
            parent.addWidget(self)

    def handle_selected_change_event(self):
        self.refresh()
        for idx, obj in enumerate(self.selected_objects):
            print("GetName: %s" % (obj.GetName()))
            name = obj.GetName()
            if idx < len(self.ui['selections']):
                self.ui['selections'][idx].set_label(name)
            else:
                self.ui['selections'].append(UI.SelectionControl(idx, name, parent=self.prop_layout))

    def refresh(self):
        self.selected_objects = self.__get_selected_objects()

    # def add_place_menu(self):
    #     plugin_menu = wrapInstance(int(RLPy.RUi.AddMenu("Test", self.dialog)), QtWidgets.QMenu)

    def __get_selected_objects(self):
        return RLPy.RScene.GetSelectedObjects()