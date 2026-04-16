import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QComboBox, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGridLayout, QMessageBox, QDialog, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = [] 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام التصنيع المتكامل - ألومنيوم 2*8')
        self.setGeometry(30, 30, 1300, 950)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()
        header_label = QLabel("بيانات العميل والمشروع 👤")
        header_label.setStyleSheet("background-color: #e1e1e1; padding: 5px; font-weight: bold;")
        main_layout.addWidget(header_label)

        # صف العميل واللون
        client_layout = QHBoxLayout()
        self.client_name = QLineEdit(); self.client_name.setPlaceholderText("اسم العميل")
        self.color = QLineEdit(); self.color.setPlaceholderText("اللون")
        client_layout.addWidget(QLabel("العميل:"))
        client_layout.addWidget(self.client_name)
        client_layout.addWidget(QLabel("اللون:"))
        client_layout.addWidget(self.color)
        main_layout.addLayout(client_layout)

        input_group = QGroupBox("🏗️ مدخلات المصنع")
        grid = QGridLayout()
        
        # الصف الأول: المقاسات ونوع الوحدة
        self.w = QLineEdit("200"); self.h = QLineEdit("90"); self.d = QLineEdit("50")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين"])
        
        grid.addWidget(QLabel("العرض الكلي:"), 0, 0); grid.addWidget(self.w, 0, 1)
        grid.addWidget(QLabel("الارتفاع الكلي:"), 0, 2); grid.addWidget(self.h, 0, 3)
        grid.addWidget(QLabel("العمق الكلي:"), 0, 4); grid.addWidget(self.d, 0, 5)
        grid.addWidget(QLabel("نوع الوحدة:"), 0, 6); grid.addWidget(self.unit_type, 0, 7)

        # الصف الثاني: الرفوف
        self.sh_w = QLineEdit("77"); self.sh_d = QLineEdit("47"); self.sh_n = QLineEdit("2")
        grid.addWidget(QLabel("الرفوف:"), 1, 0); grid.addWidget(self.sh_w, 1, 1); grid.addWidget(QLabel("عرض"), 1, 2)
        grid.addWidget(self.sh_d, 1, 3); grid.addWidget(QLabel("عمق"), 1, 4)
        grid.addWidget(self.sh_n, 1, 5); grid.addWidget(QLabel("عدد"), 1, 6)

        # الصف الثالث: الفواصل
        self.dv_h = QLineEdit("77"); self.dv_d = QLineEdit("47"); self.dv_n = QLineEdit("2")
        grid.addWidget(QLabel("الفواصل:"), 2, 0); grid.addWidget(self.dv_h, 2, 1); grid.addWidget(QLabel("ارتفاع"), 2, 2)
        grid.addWidget(self.dv_d, 2, 3); grid.addWidget(QLabel("عمق"), 2, 4)
        grid.addWidget(self.dv_n, 2, 5); grid.addWidget(QLabel("عدد"), 2, 6)

        # الصف الرابع: الأدراج
        self.dr_w = QLineEdit("37"); self.dr_d = QLineEdit("45"); self.dr_n = QLineEdit("3")
        grid.addWidget(QLabel("الأدراج (2*8):"), 3, 0); grid.addWidget(self.dr_w, 3, 1); grid.addWidget(QLabel("عرض"), 3, 2)
        grid.addWidget(self.dr_d, 3, 3); grid.addWidget(QLabel("عمق"), 3, 4)
        grid.addWidget(self.dr_n, 3, 5); grid.addWidget(QLabel("عدد"), 3, 6)

        input_group.setLayout(grid); main_layout.addWidget(input_group)

        self.add_btn = QPushButton("💾 إصدار الشيت التفصيلي وحفظ البيانات")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; height: 45px; font-weight: bold;")
        self.add_btn.clicked.connect(self.process_unit)
        main_layout.addWidget(self.add_btn)

        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("background-color: #ffffff; border: 1px solid #3498db; font-family: 'Courier New'; font-size: 11pt;")
        main_layout.addWidget(self.result_sheet)
        
        self.setLayout(main_layout)

    def process_unit(self):
        try:
            # سحب البيانات
            W, H, D = float(self.w.text()), float(self.h.text()), float(self.d.text())
            sh_w, sh_d, sh_n = float(self.sh_w.text()), float(self.sh_d.text()), int(self.sh_n.text())
            dv_h, dv_d, dv_n = float(self.dv_h.text()), float(self.dv_d.text()), int(self.dv_n.text())
            dr_w, dr_d, dr_n = float(self.dr_w.text()), float(self.dr_d.text()), int(self.dr_n.text())
            u_type = self.unit_type.currentText()

            # معادلات التخصيم بناءً على الصورة
            h_net = H - 13 if u_type == "سفلية" else H - 5
            w_net, d_net = W - 5, D - 5

            txt = f"📄 شيت تشغيل: {self.client_name.text() or 'عميل جديد'} | اللون: {self.color.text() or 'غير محدد'}\n"
            txt += f"📦 الوحدة : {u_type} ({W} × {H} × {D})\n"
            txt += "━" * 60 + "\n"
            
            # 1. تقطيع الألومنيوم
            txt += "📐 [تقطيع الألومنيوم]\n"
            txt += f"- الارتفاع: {h_net} * 2 مفرد / {h_net} * 2 متقارب\n"
            txt += f"- العرض: {w_net} * 3 مفرد / {w_net} * 1 متقارب\n"
            txt += f"- العمق: {d_net} * 2 مفرد / {d_net} * 2 متقارب\n"

            # 2. مقاسات الفيبر
            txt += "\n🪵 [مقاسات الفيبر]\n"
            txt += f"- الضهرية: {w_net} × {h_net} (عدد 1)\n"
            txt += f"- الأرضية: {w_net} × {d_net} (عدد 1)\n"
            txt += f"- الأجناب: {h_net} × {d_net} (عدد 2)\n"

            # 3. الرفوف (مطابق للصورة تماماً)
            if sh_n > 0:
                txt += f"\n🧱 [الأرفف]:\n"
                txt += f"- فيبر: {sh_w - 5} × {sh_d - 5} (عدد {sh_n})\n"
                txt += f"- ألومنيوم: {sh_w} * 8 مفرد / {sh_d} * 8 مفرد\n"

            # 4. الفواصل
            if dv_n > 0:
                txt += f"\n📐 [الفواصل]:\n"
                txt += f"- فيبر: {dv_h - 5} × {dv_d - 5} (عدد {dv_n})\n"
                txt += f"- ألومنيوم: {dv_h} * 8 مفرد / {dv_d} * 8 مفرد\n"

            # 5. الأدراج (مطابق للصورة تماماً)
            if dr_n > 0:
                txt += f"\n🗄️ [الأدراج قطاع 2*8]:\n"
                txt += f"- العرض الصافي: {dr_w - 2.5} × {dr_n * 2} مفرد\n"
                txt += f"- العمق: {dr_d} × {dr_n * 2} مفرد\n"

            self.result_sheet.setText(txt)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"تأكد من الأرقام: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = AluminumMasterApp(); ex.show(); sys.exit(app.exec_())
