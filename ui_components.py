import RLPy
from PySide2 import QtWidgets


class SelectionControl(QtWidgets.QWidget):
    def __init__(self, id, label, height=60, parent=None):
        super().__init__()

        self.id = id
        self.list_view = QtWidgets.QListView()

        self.setStyleSheet("QListView {border:1px solid rgb(72, 72, 72);}")
        self.list_view.setFixedHeight(height)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(QtWidgets.QLabel(label))
        self.layout().addWidget(QtWidgets.QLineEdit(""))
        # self.layout().addWidget(self.list_view)

        if parent:
            parent.addWidget(self)

    def set_label(self, content):
        self.layout().itemAt(0).widget().setText(content)


class Vector3Control(QtWidgets.QWidget):
    def __init__(self, label='Vector', span=(-100, 0, 100), checked=(True, True, True), parent=None):
        super().__init__()
        self.__enabled = checked
        self.__value = [span[2], span[2], span[2]]
        self.__vector = {"X": span[2], "Y": span[2], "Z": span[2]}

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setSpacing(2)
        self.layout().setContentsMargins(0, 0, 0, 0)

        for axis, checked in {"X": checked[0], "Y": checked[1], "Z": checked[2]}.items():
            layout = QtWidgets.QVBoxLayout()
            top_layout = QtWidgets.QHBoxLayout()

            checkbox = QtWidgets.QCheckBox()
            spinbox = QtWidgets.QDoubleSpinBox(
                minimum=span[0], maximum=span[1], value=span[2])

            top_layout.addWidget(checkbox)
            top_layout.addWidget(QtWidgets.QLabel("%s %s" % (label, axis)))
            top_layout.addStretch() #### I don't understand

            layout.addLayout(top_layout)
            layout.addWidget(spinbox)

            self.layout().addLayout(layout)

        if parent:
            parent.addWidget(self)

class Button(QtWidgets.QPushButton):
    def __init__(self, label="Button", enabled=True, parent=None):
        super(Button, self).__init__(label)

        self.setFixedHeight(25)
        self.setEnabled(enabled)

        if parent:
            parent.addWidget(self)


