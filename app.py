import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QComboBox, QGroupBox, QGridLayout, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام التصنيع المتكامل - نسخة الورشة المعتمدة')
        self.setGeometry(50, 50, 1000, 850)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("background-color: #f5f6fa;")

        layout = QVBoxLayout()
        
        # مدخلات المقاسات
        input_group = QGroupBox("🏗️ إدخال مقاسات الوحدة")
        grid = QGridLayout()
        
        self.w = QLineEdit("200"); self.h = QLineEdit("90"); self.d = QLineEdit("50")
        self.u_type = QComboBox(); self.u_type.addItems(["سفلية", "علوية"])
        
        grid.addWidget(QLabel("العرض الكلي:"), 0, 0); grid.addWidget(self.w, 0, 1)
        grid.addWidget(QLabel("الارتفاع الكلي:"), 0, 2); grid.addWidget(self.h, 0, 3)
        grid.addWidget(QLabel("العمق الكلي:"), 0, 4); grid.addWidget(self.d, 0, 5)
        grid.addWidget(QLabel("النوع:"), 0, 6); grid.addWidget(self.u_type, 0, 7)

        # الرفوف (المقاس اللي بتدخله هو اللي بيتحسب عليه)
        self.sh_w = QLineEdit("77"); self.sh_d = QLineEdit("47"); self.sh_n = QLineEdit("2")
        grid.addWidget(QLabel("الرفوف:"), 1, 0); grid.addWidget(self.sh_w, 1, 1); grid.addWidget(QLabel("عرض الرف"), 1, 2)
        grid.addWidget(self.sh_d, 1, 3); grid.addWidget(QLabel("عمق الرف"), 1, 4); grid.addWidget(self.sh_n, 1, 5); grid.addWidget(QLabel("عدد"), 1, 6)

        # الأدراج
        self.dr_w = QLineEdit("37"); self.dr_d = QLineEdit("45"); self.dr_n = QLineEdit("3")
        grid.addWidget(QLabel("الأدراج:"), 2, 0); grid.addWidget(self.dr_w, 2, 1); grid.addWidget(QLabel("عرض الدرج"), 2, 2)
        grid.addWidget(self.dr_d, 2, 3); grid.addWidget(QLabel("عمق الدرج"), 2, 4); grid.addWidget(self.dr_n, 2, 5); grid.addWidget(QLabel("عدد"), 2, 6)

        input_group.setLayout(grid)
        layout.addWidget(input_group)

        self.run_btn = QPushButton("🚀 إصدار التخصيم التفصيلي")
        self.run_btn.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-weight: bold;")
        self.run_btn.clicked.connect(self.calculate)
        layout.addWidget(self.run_btn)

        self.res = QTextEdit(); self.res.setReadOnly(True)
        self.res.setStyleSheet("background-color: white; border: 2px solid #2ecc71; font-family: 'Consolas'; font-size: 12pt; padding: 10px;")
        layout.addWidget(self.res)
        
        self.setLayout(layout)

    def calculate(self):
        try:
            # 1. تخصيم الهيكل (ثابت الورشة)
            W, H, D = float(self.w.text()), float(self.h.text()), float(self.d.text())
            h_net = H - 13 if self.u_type.currentText() == "سفلية" else H - 5
            w_net, d_net = W - 5, D - 5

            # 2. تخصيم الرفوف (بناءً على مقاس الرف المدخل)
            sw, sd, sn = float(self.sh_w.text()), float(self.sh_d.text()), int(self.sh_n.text())
            # الفيبر بيطرح 5 سم من مقاس ألومنيوم الرف
            f_sw, f_sd = sw - 5, sd - 5

            # 3. تخصيم الأدراج (طرح 2.5 من العرض)
            dw, dd, dn = float(self.dr_w.text()), float(self.dr_d.text()), int(self.dr_n.text())
            dw_net = dw - 2.5

            txt = f"📊 فاتورة تقطيع ورشة (المهندس ياسين)\n"
            txt += "━" * 50 + "\n"
            txt += f"1️⃣ [الهيكل]:\n"
            txt += f"   - ألومنيوم ارتفاع: {h_net} (2م / 2ت)\n"
            txt += f"   - ألومنيوم عرض  : {w_net} (3م / 1ت)\n"
            txt += f"   - ألومنيوم عمق   : {d_net} (2م / 2ت)\n"
            txt += f"   - فيبر ضهرية    : {w_net} × {h_net}\n"
            
            if sn > 0:
                txt += f"\n2️⃣ [الرفوف - عدد {sn}]:\n"
                txt += f"   - ألومنيوم: {sw} (عدد {sn*4}) | {sd} (عدد {sn*4})\n"
                txt += f"   - فايبر صافي: {f_sw} × {f_sd}\n"

            if dn > 0:
                txt += f"\n3️⃣ [الأدراج - عدد {dn}]:\n"
                txt += f"   - عرض صافي : {dw_net} (عدد {dn*2})\n"
                txt += f"   - عمق الدرج : {dd} (عدد {dn*2})\n"
            
            txt += "━" * 50
            self.res.setText(txt)
        except: QMessageBox.critical(self, "خطأ", "راجع الأرقام يا هندسة")

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = AluminumMasterApp(); ex.show(); sys.exit(app.exec_())
