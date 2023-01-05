#!/usr/bin/python
# A simple script to compress videos and gain space on your drives
# TODO :
#       window as a class
#       set parameters
#       launch button

import sys
from PyQt5.QtWidgets import QApplication, QWidget

def main_window() :
    app  = QApplication(sys.argv)
    root = QWidget()
    root.resize(320,240)
    root.setWindowTitle('Hello, world!')
    root.show()