import RLPy
import ui_components as UI
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance
from random import randrange
from prop_planter_control import PropPlanterTabWidget
from manipulation import local_move
# Global value
ui = {}

# Callback
event_list = []
dialog_event_callback = None
event_callback = None


# ----------------- Event Call Back -----
class PropPlanterEventCallBack(RLPy.REventCallback):
    def __init__(self):
        RLPy.REventCallback.__init__(self)

    def OnObjectSelectionChanged(self):
        print('selected change')
        global ui
        ui['tab_widget'].handle_selected_change_event()


class DialogEventCallback(RLPy.RDialogCallback):
    def __init__(self):
        RLPy.RDialogCallback.__init__(self)

    def OnDialogHide(self):
        global event_list
        for event in event_list:
            RLPy.REventHandler.UnregisterCallback(event)
        event_list.clear()


def regist_event():
    global event_callback
    event_callback = PropPlanterEventCallBack()
    id = RLPy.REventHandler.RegisterCallback(event_callback)
    event_list.append(id)

    global ui
    global dialog_event_callback
    dialog_event_callback = DialogEventCallback()
    ui['dialog_window'].RegisterEventCallback(dialog_event_callback)


# ----- Set Plugin -------
def init_dialog():
    global ui
    global tab_widget
    ui['dialog_window'], ui['main_layout'] = set_dock("Prop Planter")

    try:
        # tab ui
        ui['tab_widget'] = PropPlanterTabWidget()
        ui['main_layout'].addWidget(ui['tab_widget'])

        # apply button
        button = UI.Button("apply", parent=ui['main_layout'])
        button.clicked.connect(apply)
        ui['apply'] = button

    except Exception as e:
        print(e)


def set_dock(title="Prop Planter", width=300, height=400, layout=QtWidgets.QVBoxLayout):
    dock = RLPy.RUi.CreateRDockWidget()
    dock.SetWindowTitle(title)

    qt_dock = wrapInstance(int(dock.GetWindow()), QtWidgets.QDockWidget)
    main_widget = QtWidgets.QWidget()
    qt_dock.setWidget(main_widget)
    qt_dock.setFixedWidth(width)
    qt_dock.setMinimumHeight(height)

    main_layout = layout()
    main_widget.setLayout(main_layout)

    return dock, main_layout


def show_dialog():
    global ui
    ui["dialog_window"].Show()
    regist_event()


def initialize_plugin():
    global event_list, event_callback

    ic_dlg = wrapInstance(int(RLPy.RUi.GetMainWindow()), QtWidgets.QMainWindow)
    plugin_menu = ic_dlg.menuBar().findChild(QtWidgets.QMenu, "pysample_menu")
    if plugin_menu is None:
        plugin_menu = wrapInstance(int(RLPy.RUi.AddMenu(
            "Python Samples", RLPy.EMenu_Plugins)), QtWidgets.QMenu)
        plugin_menu.setObjectName('pysample_menu')

    # dialog
    menu_action = plugin_menu.addAction("PropPlanter")
    init_dialog()
    menu_action.triggered.connect(show_dialog)


def run_script():
    initialize_plugin()


def apply():
    global ui
    property_config_widget, place_config_widget = ui['tab_widget'].widget(0), ui['tab_widget'].widget(1)
    prop = property_config_widget.selection
    place = place_config_widget.selection
    clone_quantity = property_config_widget.clone_quantity

    print("PropName: %s" % prop.GetName())
    print("Clone Quantity: %d" % clone_quantity)
    print("Place Name: %s" % place.GetName())

    x_min, x_max = 0, 1000
    y_min, y_max = 0, 1,
    z_min, z_max = 0, 1

    # get place bounding size
    maxPoint = RLPy.RVector3()
    cenPoint = RLPy.RVector3()
    minPoint = RLPy.RVector3()
    status = place.GetBounds(maxPoint, cenPoint, minPoint)
    bounding = maxPoint - cenPoint

    # populate the four point of bounding box
    # top_left_up =

    for i in range(clone_quantity):
        # Create clone object
        clone = prop.Clone()
        transform = clone.WorldTransform()

        # set min and max
        transform.T().x = randrange(x_min, x_max)
        transform.T().y = randrange(y_min, y_max)
        transform.T().z = randrange(z_min, z_max)

        # set coordination of clone object
        transform_control = clone.GetControl("Transform")
        transform_data_block = transform_control.GetDataBlock()
        transform_data_block.SetData("Position/PositionX", RLPy.RTime(0), RLPy.RVariant(transform.T().x))
        transform_data_block.SetData("Position/PositionY", RLPy.RTime(0), RLPy.RVariant(transform.T().y))
        transform_data_block.SetData("Position/PositionZ", RLPy.RTime(0), RLPy.RVariant(transform.T().z))




