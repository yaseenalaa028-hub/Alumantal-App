import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QComboBox, QGroupBox, QGridLayout, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام تخصيم المهندس ياسين - الإصدار الكامل')
        self.setGeometry(30, 30, 1200, 950)
        self.setStyleSheet("background-color: #f5f6fa; font-family: 'Segoe UI';")

        main_layout = QVBoxLayout()
        header = QLabel("الورشة الذكية - تخصيم الألومنيوم والفيبر التفصيلي")
        header.setStyleSheet("background-color: #2f3640; color: #fbc531; font-size: 18pt; font-weight: bold; padding: 15px; border-radius: 10px;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # منطقة الإدخال
        input_group = QGroupBox("📝 بيانات الوحدة والمقاسات الكلية")
        grid = QGridLayout()

        self.unit_title = QLineEdit(); self.unit_title.setPlaceholderText("اسم الوحدة")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين"])
        self.w = QLineEdit(); self.w.setPlaceholderText("العرض الكلي")
        self.h = QLineEdit(); self.h.setPlaceholderText("الارتفاع الكلي")
        self.d = QLineEdit(); self.d.setPlaceholderText("العمق الكلي")
        
        # الأرفف والفواصل
        self.sh_n = QLineEdit(); self.sh_n.setPlaceholderText("عدد الرفوف")
        self.sh_w = QLineEdit(); self.sh_w.setPlaceholderText("عرض الرف")
        self.sh_d = QLineEdit(); self.sh_d.setPlaceholderText("عمق الرف")
        
        self.dv_n = QLineEdit(); self.dv_n.setPlaceholderText("عدد الفواصل")
        self.dv_h = QLineEdit(); self.dv_h.setPlaceholderText("ارتفاع الفاصل")
        self.dv_d = QLineEdit(); self.dv_d.setPlaceholderText("عمق الفاصل")

        # الأدراج
        self.dr_n = QLineEdit(); self.dr_n.setPlaceholderText("عدد الأدراج")
        self.dr_w = QLineEdit(); self.dr_w.setPlaceholderText("عرض الدرج")

        grid.addWidget(QLabel("الوحدة:"), 0, 0); grid.addWidget(self.unit_title, 0, 1); grid.addWidget(self.unit_type, 0, 2)
        grid.addWidget(QLabel("المقاسات (عرض/ار/عم):"), 1, 0); grid.addWidget(self.w, 1, 1); grid.addWidget(self.h, 1, 2); grid.addWidget(self.d, 1, 3)
        grid.addWidget(QLabel("الأرفف (عرض/عمق/عدد):"), 2, 0); grid.addWidget(self.sh_w, 2, 1); grid.addWidget(self.sh_d, 2, 2); grid.addWidget(self.sh_n, 2, 3)
        grid.addWidget(QLabel("الفواصل (ار/عم/عدد):"), 3, 0); grid.addWidget(self.dv_h, 3, 1); grid.addWidget(self.dv_d, 3, 2); grid.addWidget(self.dv_n, 3, 3)
        grid.addWidget(QLabel("الأدراج (عرض/عدد):"), 4, 0); grid.addWidget(self.dr_w, 4, 1); grid.addWidget(self.dr_n, 4, 2)
        
        input_group.setLayout(grid)
        main_layout.addWidget(input_group)

        # أزرار العمليات
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("💾 احسب وفصّل القطع")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-weight: bold;")
        self.add_btn.clicked.connect(self.process_unit)
        self.save_btn = QPushButton("📄 حفظ كـ PDF / Text")
        self.save_btn.setStyleSheet("background-color: #2980b9; color: white; height: 50px;")
        
        btn_layout.addWidget(self.add_btn); btn_layout.addWidget(self.save_btn)
        main_layout.addLayout(btn_layout)

        # منطقة عرض النتائج المفصلة
        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("background-color: #ffffff; border: 2px solid #2ecc71; font-size: 11pt; padding: 10px; color: #2c3e50;")
        main_layout.addWidget(self.result_sheet)

        self.setLayout(main_layout)

    def process_unit(self):
        try:
            name = self.unit_title.text() or "وحدة"
            u_type = self.unit_type.currentText()
            w = float(self.w.text()); h = float(self.h.text()); d = float(self.d.text())
            
            # معادلات التخصيم الثابتة
            h_sub = 13 if u_type in ["سفلية", "دولاب خزين"] else 5
            h_net, w_net, d_net = h - h_sub, w - 5, d - 5

            res = f"📍 تقرير الوحدة: {name} ({u_type})\n"
            res += "═" * 70 + "\n"
            
            # --- قسم الألومنيوم (مفرد ومتقارب) ---
            res += "🛠️ [1] جدول تقطيع الألومنيوم (الهيكل):\n"
            if u_type == "سفلية":
                res += f"- الارتفاع ({h_net}): [2 مفرد] + [2 متقارب]\n"
                res += f"- العرض ({w_net}): [3 مفرد] + [1 متقارب]\n"
                res += f"- العمق ({d_net}): [2 مفرد] + [2 متقارب]\n"
            else:
                res += f"- الارتفاع ({h_net}): [2 مفرد] + [2 متقارب]\n"
                res += f"- العرض ({w_net}): [2 مفرد] + [2 متقارب]\n"
                res += f"- العمق ({d_net}): [4 متقارب]\n"

            # تخصيم ألومنيوم الأرفف (العدد * 4 مفرد)
            if self.sh_n.text() and int(self.sh_n.text()) > 0:
                n = int(self.sh_n.text()); sw = self.sh_w.text(); sd = self.sh_d.text()
                res += f"- ألومنيوم الأرفف: {sw} (عدد {n*4} مفرد) | {sd} (عدد {n*4} مفرد)\n"

            # تخصيم ألومنيوم الفواصل (العدد * 4 مفرد)
            if self.dv_n.text() and int(self.dv_n.text()) > 0:
                n = int(self.dv_n.text()); dh = self.dv_h.text(); dd = self.dv_d.text()
                res += f"- ألومنيوم الفواصل: {dh} (عدد {n*4} مفرد) | {dd} (عدد {n*4} مفرد)\n"

            # تخصيم الأدراج
            if self.dr_n.text() and int(self.dr_n.text()) > 0:
                dr_w_final = float(self.dr_w.text()) - 2.5
                res += f"- ألومنيوم الأدراج: العرض {dr_w_final} | العمق {d} (ثابت)\n"

            res += "─" * 40 + "\n"
            
            # --- قسم الفيبر لوحده ---
            res += "🪵 [2] جدول تقطيع الفيبر:\n"
            res += f"- الضهرية: {w_net} × {h_net} (عدد 1)\n"
            res += f"- الأرضية: {w_net} × {d_net} (عدد 1)\n"
            res += f"- الأجناب: {h_net} × {d_net} (عدد 2)\n"
            
            if self.sh_n.text() and int(self.sh_n.text()) > 0:
                fw, fd = float(self.sh_w.text()) - 5, float(self.sh_d.text()) - 5
                res += f"- فيبر الأرفف: {fw} × {fd} (عدد {self.sh_n.text()})\n"

            if self.dv_n.text() and int(self.dv_n.text()) > 0:
                fh, fd = float(self.dv_h.text()) - 5, float(self.dv_d.text()) - 5
                res += f"- فيبر الفواصل: {fh} × {fd} (عدد {self.dv_n.text()})\n"

            res += "═" * 70 + "\n\n"
            self.result_sheet.append(res)
            self.clear_fields()
        except:
            QMessageBox.warning(self, "خطأ", "برجاء مراجعة الأرقام المدخلة")

    def clear_fields(self):
        # تصفير الخانات المهمة فقط لبدء وحدة جديدة
        for f in [self.w, self.h, self.d, self.sh_n, self.dv_n, self.dr_n]: f.clear()
        self.unit_title.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = AluminumMasterApp(); ex.show(); sys.exit(app.exec_())
