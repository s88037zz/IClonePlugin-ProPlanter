import RLPy
import ui_components as uic
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance
from prop_planter_control import PropPlanterUiControl, PropPlanterTabWidget

ui = {}
all_events, event_callback = [], None
ui_control = None


class SelectionEventCallback(RLPy.REventCallback):
    def __init__(self):
        RLPy.REventCallback.__init__(self)

    def OnObjectSelectionChanged(self):
        print('selected change')
        global ui_control
        ui_control.handle_selected_change_event()


class DialogEventCallback(RLPy.RDialogCallback):
    def __init__(self):
        RLPy.RDialogCallback.__init__(self)

    def OnDialogHide(self):
        global all_events

        for event in all_events:
            RLPy.REventHandler.UnregisterCallback(event)
        all_events.clear()


def init_dialog():
    global ui, ui_control
    ui['dialog_window'], ui['main_layout'] = set_dock("Prop Planter")

    # # Register Event CallBack
    # dialog_event_callback = DialogEventCallback()
    # ui["main_dlg"].RegisterEventCallback(dialog_event_callback)

    try:
        ui['main_layout'].addWidget(PropPlanterTabWidget())
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


def initialize_plugin():
    global all_events, event_callback

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

    # register event
    event_callback = SelectionEventCallback()
    id = RLPy.REventHandler.RegisterCallback(event_callback)
    all_events.append(id)


def run_script():
    initialize_plugin()