# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_DataCheck(object):
    def setupUi(self, DataCheck):
        if not DataCheck.objectName():
            DataCheck.setObjectName(u"DataCheck")
        DataCheck.resize(800, 800)
        DataCheck.setMinimumSize(QSize(800, 800))
        DataCheck.setMaximumSize(QSize(800, 800))
        self.verticalLayout = QVBoxLayout(DataCheck)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.search_line = QLineEdit(DataCheck)
        self.search_line.setObjectName(u"search_line")
        self.search_line.setMinimumSize(QSize(25, 23))
        self.search_line.setMaximumSize(QSize(16777215, 23))

        self.horizontalLayout.addWidget(self.search_line)

        self.search_button = QPushButton(DataCheck)
        self.search_button.setObjectName(u"search_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy)
        self.search_button.setMinimumSize(QSize(0, 25))
        self.search_button.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout.addWidget(self.search_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.true_proportion = QLabel(DataCheck)
        self.true_proportion.setObjectName(u"true_proportion")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.true_proportion.sizePolicy().hasHeightForWidth())
        self.true_proportion.setSizePolicy(sizePolicy1)
        self.true_proportion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.true_proportion)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.prev_image = QPushButton(DataCheck)
        self.prev_image.setObjectName(u"prev_image")

        self.horizontalLayout_3.addWidget(self.prev_image)

        self.next_image = QPushButton(DataCheck)
        self.next_image.setObjectName(u"next_image")

        self.horizontalLayout_3.addWidget(self.next_image)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(DataCheck)

        QMetaObject.connectSlotsByName(DataCheck)
    # setupUi

    def retranslateUi(self, DataCheck):
        DataCheck.setWindowTitle(QCoreApplication.translate("DataCheck", u"DataCheck", None))
        self.search_button.setText(QCoreApplication.translate("DataCheck", u"Search", None))
        self.true_proportion.setText("")
        self.prev_image.setText(QCoreApplication.translate("DataCheck", u"Prev", None))
        self.next_image.setText(QCoreApplication.translate("DataCheck", u"Next", None))
    # retranslateUi

