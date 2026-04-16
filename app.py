import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QComboBox, QGroupBox, QGridLayout, QMessageBox, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = [] 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام تخصيم الألومنيوم - المهندس ياسين علاء')
        self.setGeometry(30, 30, 1100, 900)
        self.setStyleSheet("background-color: #f5f6fa; font-family: 'Segoe UI';")

        main_layout = QVBoxLayout()

        # العنوان
        header = QLabel("برمجة المهندس ياسين علاء - تخصيم الألومنيوم")
        header.setStyleSheet("background-color: #2f3640; color: #fbc531; font-size: 18pt; font-weight: bold; padding: 15px; border-radius: 10px;")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # منطقة الإدخال
        input_group = QGroupBox("📝 بيانات الوحدة (المقاسات الكلية بالسم)")
        grid = QGridLayout()

        self.unit_title = QLineEdit(); self.unit_title.setPlaceholderText("اسم الوحدة (مثلاً: سفلية حوض)")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين", "أخرى"])
        
        self.w = QLineEdit(); self.w.setPlaceholderText("العرض الكلي")
        self.h = QLineEdit(); self.h.setPlaceholderText("الارتفاع الكلي")
        self.d = QLineEdit(); self.d.setPlaceholderText("العمق الكلي")
        
        # الأرفف والفواصل
        self.sh_n = QLineEdit(); self.sh_n.setPlaceholderText("عدد الأرفف")
        self.sh_w = QLineEdit(); self.sh_w.setPlaceholderText("عرض الرف")
        self.sh_d = QLineEdit(); self.sh_d.setPlaceholderText("عمق الرف")
        
        self.dv_n = QLineEdit(); self.dv_n.setPlaceholderText("عدد الفواصل")
        self.dv_h = QLineEdit(); self.dv_h.setPlaceholderText("ارتفاع الفاصل")
        self.dv_d = QLineEdit(); self.dv_d.setPlaceholderText("عمق الفاصل")

        # الأدراج
        self.dr_n = QLineEdit(); self.dr_n.setPlaceholderText("عدد الأدراج")
        self.dr_w = QLineEdit(); self.dr_w.setPlaceholderText("عرض الدرج المطلوبة")

        grid.addWidget(QLabel("اسم الوحدة:"), 0, 0); grid.addWidget(self.unit_title, 0, 1)
        grid.addWidget(QLabel("نوع الوحدة:"), 0, 2); grid.addWidget(self.unit_type, 0, 3)
        grid.addWidget(QLabel("عرض/ارتفاع/عمق:"), 1, 0)
        grid.addWidget(self.w, 1, 1); grid.addWidget(self.h, 1, 2); grid.addWidget(self.d, 1, 3)
        grid.addWidget(QLabel("الأرفف (ع/ع/ن):"), 2, 0)
        grid.addWidget(self.sh_w, 2, 1); grid.addWidget(self.sh_d, 2, 2); grid.addWidget(self.sh_n, 2, 3)
        grid.addWidget(QLabel("الفواصل (ع/ع/ن):"), 3, 0)
        grid.addWidget(self.dv_h, 3, 1); grid.addWidget(self.dv_d, 3, 2); grid.addWidget(self.dv_n, 3, 3)
        grid.addWidget(QLabel("الأدراج (عرض/عدد):"), 4, 0)
        grid.addWidget(self.dr_w, 4, 1); grid.addWidget(self.dr_n, 4, 2)
        
        input_group.setLayout(grid)
        main_layout.addWidget(input_group)

        # الأزرار
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("💾 إضافة وحساب")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-weight: bold;")
        self.add_btn.clicked.connect(self.process_unit)
        
        self.save_btn = QPushButton("📄 حفظ ملف نصي (فاتورة)")
        self.save_btn.setStyleSheet("background-color: #2980b9; color: white; height: 50px; font-weight: bold;")
        self.save_btn.clicked.connect(self.save_report)
        
        self.clear_btn = QPushButton("🗑️ مسح الكل")
        self.clear_btn.setStyleSheet("background-color: #c0392b; color: white; height: 50px; font-weight: bold;")
        self.clear_btn.clicked.connect(self.clear_data)

        btn_layout.addWidget(self.add_btn); btn_layout.addWidget(self.save_btn); btn_layout.addWidget(self.clear_btn)
        main_layout.addLayout(btn_layout)

        # منطقة النتائج
        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("background-color: #ffffff; border: 2px solid #2ecc71; font-size: 11pt; padding: 10px;")
        main_layout.addWidget(self.result_sheet)

        self.setLayout(main_layout)

    def process_unit(self):
        try:
            u = {
                'title': self.unit_title.text() or "وحدة",
                'type': self.unit_type.currentText(),
                'w': float(self.w.text() or 0),
                'h': float(self.h.text() or 0),
                'd': float(self.d.text() or 0),
                'sh_w': float(self.sh_w.text() or 0), 'sh_d': float(self.sh_d.text() or 0), 'sh_n': int(self.sh_n.text() or 0),
                'dv_h': float(self.dv_h.text() or 0), 'dv_d': float(self.dv_d.text() or 0), 'dv_n': int(self.dv_n.text() or 0),
                'dr_w': float(self.dr_w.text() or 0), 'dr_n': int(self.dr_n.text() or 0)
            }

            # --- حسابات الألومنيوم ---
            # السفلية ودولاب الخزين يشيل 13 سم من الارتفاع
            h_sub = 13 if u['type'] in ["سفلية", "دولاب خزين"] else 5
            h_net = u['h'] - h_sub
            w_net = u['w'] - 5
            d_net = u['d'] - 5

            res = f"📦 {u['title']} ({u['type']}) | {u['w']}x{u['h']}x{u['d']}\n"
            res += "━" * 50 + "\n"
            
            # تفصيل الألومنيوم
            if u['type'] == "سفلية":
                res += f"📐 ألومنيوم:\n- ارتفاع {h_net}: [2 مفرد] [2 متقارب]\n- عرض {w_net}: [3 مفرد] [1 متقارب]\n- عمق {d_net}: [2 مفرد] [2 متقارب]\n"
            else:
                res += f"📐 ألومنيوم:\n- ارتفاع {h_net}: [2 مفرد] [2 متقارب]\n- عرض {w_net}: [2 مفرد] [2 متقارب]\n- عمق {d_net}: [4 متقارب]\n"

            # تفصيل الفيبر
            res += f"🪵 فيبر:\n- ضهرية: {w_net} × {h_net} (1)\n- أرضية: {w_net} × {d_net} (1)\n- أجناب: {h_net} × {d_net} (2)\n"

            # الأرفف والفواصل
            if u['sh_n'] > 0:
                res += f"🧱 أرفف ({u['sh_n']}): ألومنيوم {u['sh_w']}*4 مفرد، {u['sh_d']}*4 مفرد | فيبر {u['sh_w']-5}x{u['sh_d']-5}\n"
            if u['dv_n'] > 0:
                res += f"📐 فواصل ({u['dv_n']}): ألومنيوم {u['dv_h']}*4 مفرد، {u['dv_d']}*4 مفرد | فيبر {u['dv_h']-5}x{u['dv_d']-5}\n"
            
            # الأدراج
            if u['dr_n'] > 0:
                res += f"🗄️ أدراج ({u['dr_n']}): عرض ألومنيوم {u['dr_w']-2.5} | عمق {u['d']} (كما هو)\n"

            res += "━" * 50 + "\n"
            self.result_sheet.append(res)
            self.project_storage.append(u)
            
            # تنظيف جزئي
            for f in [self.w, self.h, self.d, self.unit_title, self.sh_n, self.dr_n, self.dv_n]: f.clear()
            self.unit_title.setFocus()
        except:
            QMessageBox.warning(self, "خطأ", "برجاء مراجعة المقاسات المدخلة")

    def save_report(self):
        if not self.project_storage: return
        path, _ = QFileDialog.getSaveFileName(self, "حفظ التقرير", "", "Text Files (*.txt)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("شيت تخصيمات المهندس ياسين علاء\n\n" + self.result_sheet.toPlainText())
            QMessageBox.information(self, "نجاح", "تم حفظ الفاتورة بنجاح")

    def clear_data(self):
        self.project_storage = []; self.result_sheet.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = AluminumMasterApp(); ex.show(); sys.exit(app.exec_())
