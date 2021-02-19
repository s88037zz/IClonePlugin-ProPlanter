import RLPy
import ui_components as UI
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance
from random import randrange
from prop_planter_control import PropConfigControl, PropPlanterTabWidget

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

    # skeleton = prop.GetSkeletonComponent()
    # root_bone = skeleton.GetRootBone()
    # prop_wold_transform = root_bone.WorldTransform()
    # print("Prop World Transform:", prop_wold_transform)

    # Create clone object
    clone = prop.Clone()
    transform_control = clone.GetControl("Transform")
    transform_key = RLPy.RTransformKey()
    transform_control.GetTransformKey(RLPy.RTime(0), transform_key)
    transform = transform_key.GetTransform()

    local_pos = RLPy.RVector3(300, 0, 0)
    local_move(clone, local_pos)


    first_clone_move = {
        "x": 0, "y": 0, 'z': 0
    }

    first_clone_scale = {
        'x': 1, 'y': 1, "z": 0
    }


def local_to_world_translate(obj, local_pos):
    transform = obj.WorldTransform()
    transform_matrix = transform.Matrix()
    transform_matrix.SetTranslate(RLPy.RVector3.ZERO)

    local_matrix = RLPy.RMatrix4()
    local_matrix.MakeIdentity()
    local_matrix.SetTranslate(local_pos)

    # Get world-space position by multiplying local-space with the transform-space
    world_matrix = local_matrix * transform_matrix

    return world_matrix.GetTranslate()


def local_move(obj, local_pos):
    world_position = local_to_world_translate(obj, local_pos)
    current_time = RLPy.RGlobal.GetTime()

    # Set positional keys
    t_control = obj.GetControl("Transform")
    t_data_block = t_control.GetDataBlock()
    t_data_block.SetData("Position/PositionX", current_time, RLPy.RVariant(world_position.x))
    t_data_block.SetData("Position/PositionY", current_time, RLPy.RVariant(world_position.y))
    t_data_block.SetData("Position/PositionZ", current_time, RLPy.RVariant(world_position.z))

    # Force update iClone native UI
    RLPy.RGlobal.SetTime(RLPy.RGlobal.GetTime() + RLPy.RTime(1))
    RLPy.RGlobal.SetTime(RLPy.RGlobal.GetTime() - RLPy.RTime(1))