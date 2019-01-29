# Just a quick script to easily recompile the interface after you make changes in designer

import os

os.system("pyuic5 mainwindow.ui > mainwindow.py")
