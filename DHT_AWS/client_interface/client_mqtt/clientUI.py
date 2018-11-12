# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project3.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(611, 691)
        self.req_data = QtWidgets.QPushButton(dialog)
        self.req_data.setGeometry(QtCore.QRect(40, 40, 141, 29))
        self.req_data.setObjectName("req_data")
        self.c_to_f = QtWidgets.QPushButton(dialog)
        self.c_to_f.setGeometry(QtCore.QRect(450, 40, 91, 29))
        self.c_to_f.setObjectName("c_to_f")
        self.gen_graph = QtWidgets.QPushButton(dialog)
        self.gen_graph.setGeometry(QtCore.QRect(180, 600, 191, 29))
        self.gen_graph.setObjectName("gen_graph")
        self.display_values = QtWidgets.QTextEdit(dialog)
        self.display_values.setGeometry(QtCore.QRect(40, 140, 511, 411))
        self.display_values.setObjectName("display_values")
        self.clear_data = QtWidgets.QPushButton(dialog)
        self.clear_data.setGeometry(QtCore.QRect(240, 40, 161, 29))
        self.clear_data.setObjectName("clear_data")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.req_data.setText(_translate("dialog", "REQUEST DATA"))
        self.c_to_f.setText(_translate("dialog", "C/F"))
        self.gen_graph.setText(_translate("dialog", "GENERATE GRAPH"))
        self.clear_data.setText(_translate("dialog", "CLEAR DATA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

