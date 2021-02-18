import RLPy
from PySide2 import QtWidgets
from functools import partial
from PySide2 import QtCore


class SelectionControl(QtWidgets.QWidget):
    def __init__(self, id, label, height=60, parent=None):
        super().__init__()

        self.id = id
        self.list_view = QtWidgets.QListView()

        # self.setStyleSheet("QListView {border:1px solid rgb(72, 72, 72);}")
        # self.list_view.setFixedHeight(height)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(QtWidgets.QLabel(label))
        self.layout().addWidget(QtWidgets.QLineEdit(""))
        # self.layout().addWidget(self.list_view)

        if parent:
            parent.addWidget(self)

    def set_item_label(self, item_idx, text):
        self.layout().itemAt(item_idx).widget().setText(text)




class Vector3Control(QtWidgets.QWidget):
    def __init__(self, label='Vector', span=(-100, 0, 100), checked=[True, True, True], parent=None):
        super().__init__()
        self.__enabled = checked
        self.__value = [span[2], span[2], span[2]]
        self.__vector = {"x": span[2], "y": span[2], "z": span[2]}

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setSpacing(2)
        self.layout().setContentsMargins(0, 0, 0, 0)

        def enable_disable(spinbox, axis, cond):
            spinbox.setEnabled(cond)
            index = {"X": 0, "Y": 1, "Z": 2}[axis]
            self.__enabled[index] = cond > 0

        def change_value(axis, value):
            self.__vector[axis.lower()] = value
            index = {"X": 0, "Y": 1, "Z": 2}[axis]
            self.__value[index] = value

        for axis, checked in {"X": checked[0], "Y": checked[1], "Z": checked[2]}.items():
            layout = QtWidgets.QVBoxLayout()
            top_layout = QtWidgets.QHBoxLayout()

            checkbox = QtWidgets.QCheckBox()
            spinbox = QtWidgets.QDoubleSpinBox(
                minimum=span[0], maximum=span[2], value=span[1])

            top_layout.addWidget(checkbox)
            top_layout.addWidget(QtWidgets.QLabel("%s %s" % (label, axis)))
            top_layout.addStretch() #### I don't understand

            layout.addLayout(top_layout)
            layout.addWidget(spinbox)

            checkbox.setEnabled(checked)
            spinbox.setEnabled(checked)

            checkbox.stateChanged.connect(partial(enable_disable, spinbox, axis))
            spinbox.valueChanged.connect(partial(change_value, axis))

            self.layout().addLayout(layout)

        if parent:
            parent.addWidget(self)


class SliderControl(QtWidgets.QWidget):
    def __init__(self, label="Bar", span=(0, 10, 0), parent=None):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        bot_layout = QtWidgets.QHBoxLayout()

        bar = QtWidgets.QSlider(QtCore.Qt.Horizontal,
                                maximum=span[0], minimum=span[1], value=5)

        spinbox = QtWidgets.QSpinBox(maximum=span[0], minimum=span[1], value=5)
        bot_layout.addWidget(bar)
        bot_layout.addWidget(spinbox)

        layout.addWidget(QtWidgets.QLabel(label))
        layout.addLayout(bot_layout)
        self.setLayout(layout)

        if parent:
            parent.addWidget(self)


class Button(QtWidgets.QPushButton):
    def __init__(self, label="Button", enabled=True, parent=None):
        super(Button, self).__init__(label)

        self.setFixedHeight(25)
        self.setEnabled(enabled)

        if parent:
            parent.addWidget(self)

    def clone_prop(self):
        pass
