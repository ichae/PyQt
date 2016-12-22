from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from future_builtins import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class NumberFormatDlg(QDialog):
    def __init__(self,format,callback,parent=None):
        super(NumberFormatDlg,self).__init__(parent)

        punctuation_re=QRegExp(r"[ ,:;.]")