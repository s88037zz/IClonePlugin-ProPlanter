import RLPy
import ui_components as uic
from PySide2 import QtWidgets
from PySide2.shiboken2 import wrapInstance
from prop_planter_control import PropPlanterUiControl

ui = {}
all_events, event_callback = [], None
global ui_control


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


def show_dialog():
    global ui, ui_control
    ui["main_dlg"] = RLPy.RUi.CreateRDialog()
    ui["main_dlg"].SetWindowTitle("Prop Planter")

    # # Register Event CallBack
    # dialog_event_callback = DialogEventCallback()
    # ui["main_dlg"].RegisterEventCallback(dialog_event_callback)

    dialog = wrapInstance(int(ui['main_dlg'].GetWindow()), QtWidgets.QDialog)

    ui_control = PropPlanterUiControl(dialog)

    ui["main_dlg"].Show()



def initialize_plugin():
    global all_events, event_callback

    ic_dlg = wrapInstance(int(RLPy.RUi.GetMainWindow()), QtWidgets.QMainWindow)
    plugin_menu = ic_dlg.menuBar().findChild(QtWidgets.QMenu, "pysample_menu")
    if plugin_menu is None:
        plugin_menu = wrapInstance(int(RLPy.RUi.AddMenu(
            "Python Samples", RLPy.EMenu_Plugins)), QtWidgets.QMenu)
        plugin_menu.setObjectName('pysample_menu')

    # init dialog
    menu_action = plugin_menu.addAction("PropPlanter")
    menu_action.triggered.connect(show_dialog)

    # register event
    event_callback = SelectionEventCallback()
    id = RLPy.REventHandler.RegisterCallback(event_callback)
    all_events.append(id)


def run_script():
    initialize_plugin()