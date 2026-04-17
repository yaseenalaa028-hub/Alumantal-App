import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("نظام تخصيم الألومنيوم - نسخة مطورة")
        self.setGeometry(100, 100, 1200, 800)
        self.setFont(QFont("Segoe UI", 10))

        layout = QVBoxLayout()

        # Header
        title = QLabel("نظام تخصيم الألومنيوم - نسخة مطورة")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold; background:#2c3e50; color:white; padding:10px;")
        layout.addWidget(title)

        # Inputs
        form = QGridLayout()

        self.name = QLineEdit(); self.name.setPlaceholderText("اسم الوحدة")
        self.type = QComboBox()
        self.type.addItems(["سفلية", "علوية", "دولاب"])

        self.w = QLineEdit(); self.w.setPlaceholderText("العرض")
        self.h = QLineEdit(); self.h.setPlaceholderText("الارتفاع")
        self.d = QLineEdit(); self.d.setPlaceholderText("العمق")

        self.sh = QLineEdit(); self.sh.setPlaceholderText("عدد الرفوف")
        self.dv = QLineEdit(); self.dv.setPlaceholderText("عدد الفواصل")
        self.dr = QLineEdit(); self.dr.setPlaceholderText("عدد الأدراج")

        form.addWidget(self.name, 0, 0)
        form.addWidget(self.type, 0, 1)

        form.addWidget(self.w, 1, 0)
        form.addWidget(self.h, 1, 1)
        form.addWidget(self.d, 1, 2)

        form.addWidget(self.sh, 2, 0)
        form.addWidget(self.dv, 2, 1)
        form.addWidget(self.dr, 2, 2)

        layout.addLayout(form)

        # Buttons
        btns = QHBoxLayout()

        add_btn = QPushButton("إضافة")
        add_btn.clicked.connect(self.add_item)

        clear_btn = QPushButton("مسح")
        clear_btn.clicked.connect(self.clear_all)

        btns.addWidget(add_btn)
        btns.addWidget(clear_btn)

        layout.addLayout(btns)

        # Output
        self.output = QTextEdit()
        layout.addWidget(self.output)

        self.setLayout(layout)

    def safe_float(self, v):
        try:
            return float(v)
        except:
            return 0

    def add_item(self):
        w = self.safe_float(self.w.text())
        h = self.safe_float(self.h.text())
        d = self.safe_float(self.d.text())

        sh = int(self.sh.text() or 0)
        dv = int(self.dv.text() or 0)
        dr = int(self.dr.text() or 0)

        name = self.name.text() or "وحدة"
        t = self.type.currentText()

        result = f"""
📦 {name}
--------------------
📐 الأبعاد: {w} × {h} × {d}
🪵 رفوف: {sh} | فواصل: {dv} | أدراج: {dr}
🏷️ النوع: {t}

🔧 التخصيم:
- ارتفاع: {h-5 if h > 5 else h}
- عرض: {w-5 if w > 5 else w}
- عمق: {d-5 if d > 5 else d}
--------------------
"""

        self.output.append(result)
        self.project_storage.append((name, w, h, d))

        self.name.clear()
        self.w.clear()
        self.h.clear()
        self.d.clear()
        self.sh.clear()
        self.dv.clear()
        self.dr.clear()

        self.name.setFocus()

    def clear_all(self):
        self.project_storage = []
        self.output.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AluminumMasterApp()
    window.show()
    sys.exit(app.exec_())
