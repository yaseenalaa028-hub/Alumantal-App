import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QComboBox, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGridLayout, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # عنوان البرنامج المعتمد للمهندس ياسين علاء
        self.setWindowTitle('نظام التصنيع المتكامل - ألومنيوم 2*8 (النسخة الاحترافية)')
        self.setGeometry(30, 30, 1100, 900)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()
        
        # --- الجزء الأول: بيانات المشروع ---
        header_group = QGroupBox("👤 بيانات العميل")
        h_layout = QHBoxLayout()
        self.client_name = QLineEdit(); self.client_name.setPlaceholderText("اسم العميل")
        self.color = QLineEdit(); self.color.setPlaceholderText("لون الألومنيوم")
        h_layout.addWidget(QLabel("العميل:")); h_layout.addWidget(self.client_name)
        h_layout.addWidget(QLabel("اللون:")); h_layout.addWidget(self.color)
        header_group.setLayout(h_layout)
        main_layout.addWidget(header_group)

        # --- الجزء الثاني: مدخلات المصنع (نفس ترتيب الصورة) ---
        input_group = QGroupBox("🏗️ مدخلات المقاسات (سم)")
        grid = QGridLayout()
        
        self.w = QLineEdit("200"); self.h = QLineEdit("90"); self.d = QLineEdit("50")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين"])
        
        grid.addWidget(QLabel("العرض الكلي:"), 0, 0); grid.addWidget(self.w, 0, 1)
        grid.addWidget(QLabel("الارتفاع الكلي:"), 0, 2); grid.addWidget(self.h, 0, 3)
        grid.addWidget(QLabel("العمق الكلي:"), 0, 4); grid.addWidget(self.d, 0, 5)
        grid.addWidget(QLabel("نوع الوحدة:"), 0, 6); grid.addWidget(self.unit_type, 0, 7)

        # الرفوف
        self.sh_w = QLineEdit("77"); self.sh_d = QLineEdit("47"); self.sh_n = QLineEdit("2")
        grid.addWidget(QLabel("الرفوف:"), 1, 0); grid.addWidget(self.sh_w, 1, 1); grid.addWidget(QLabel("عرض"), 1, 2)
        grid.addWidget(self.sh_d, 1, 3); grid.addWidget(QLabel("عمق"), 1, 4); grid.addWidget(self.sh_n, 1, 5); grid.addWidget(QLabel("عدد"), 1, 6)

        # الفواصل
        self.dv_h = QLineEdit("77"); self.dv_d = QLineEdit("47"); self.dv_n = QLineEdit("2")
        grid.addWidget(QLabel("الفواصل:"), 2, 0); grid.addWidget(self.dv_h, 2, 1); grid.addWidget(QLabel("ارتفاع"), 2, 2)
        grid.addWidget(self.dv_d, 2, 3); grid.addWidget(QLabel("عمق"), 2, 4); grid.addWidget(self.dv_n, 2, 5); grid.addWidget(QLabel("عدد"), 2, 6)

        # الأدراج
        self.dr_w = QLineEdit("37"); self.dr_d = QLineEdit("45"); self.dr_n = QLineEdit("3")
        grid.addWidget(QLabel("الأدراج (2*8):"), 3, 0); grid.addWidget(self.dr_w, 3, 1); grid.addWidget(QLabel("عرض"), 3, 2)
        grid.addWidget(self.dr_d, 3, 3); grid.addWidget(QLabel("عمق"), 3, 4); grid.addWidget(self.dr_n, 3, 5); grid.addWidget(QLabel("عدد"), 3, 6)

        input_group.setLayout(grid)
        main_layout.addWidget(input_group)

        # زر إصدار الفاتورة التفصيلية
        self.add_btn = QPushButton("💾 إصدار فاتورة التقطيع التفصيلية")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-weight: bold; font-size: 13pt; border-radius: 5px;")
        self.add_btn.clicked.connect(self.process_unit)
        main_layout.addWidget(self.add_btn)

        # --- الجزء الثالث: شيت التشغيل (بالتفصيل الممل) ---
        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("""
            background-color: #ffffff; 
            border: 2px solid #2ecc71; 
            font-family: 'Consolas', 'Courier New'; 
            font-size: 12pt; 
            padding: 20px;
            color: #1e272e;
        """)
        main_layout.addWidget(self.result_sheet)
        
        self.setLayout(main_layout)

    def process_unit(self):
        try:
            # تحويل المدخلات لأرقام
            W, H, D = float(self.w.text()), float(self.h.text()), float(self.d.text())
            sh_w, sh_d, sh_n = float(self.sh_w.text()), float(self.sh_d.text()), int(self.sh_n.text())
            dv_h, dv_d, dv_n = float(self.dv_h.text()), float(self.dv_d.text()), int(self.dv_n.text())
            dr_w, dr_d, dr_n = float(self.dr_w.text()), float(self.dr_d.text()), int(self.dr_n.text())
            u_type = self.unit_type.currentText()

            # 1. تخصيمات الهيكل الأساسي (طرح 13 للسفلية و5 للعلوية)
            h_net = H - 13 if u_type in ["سفلية", "دولاب خزين"] else H - 5
            w_net, d_net = W - 5, D - 5

            # بناء نص الفاتورة التفصيلية
            txt = f"📝 شيت تشغيل تفصيلي | العميل: {self.client_name.text() or 'غير محدد'}\n"
            txt += f"🎨 اللون المطلوب: {self.color.text() or 'غير محدد'}\n"
            txt += f"📦 نوع الوحدة : {u_type} ({W} عرض × {H} ارتفاع × {D} عمق)\n"
            txt += "━" * 75 + "\n"
            
            # [1] تفصيل ألومنيوم الهيكل
            txt += "📐 [1] ألومنيوم الهيكل الأساسي (قطاع 2*8):\n"
            txt += f"  - العرض  ({w_net} سم): قطع (3 قطع مفرد) + (قطعة واحدة متقارب)\n"
            txt += f"  - الارتفاع ({h_net} سم): قطع (قطعتين مفرد) + (قطعتين متقارب)\n"
            txt += f"  - العمق   ({d_net} سم): قطع (قطعتين مفرد) + (قطعتين متقارب)\n"

            # [2] تفصيل فيبر الهيكل (القص الصافي)
            txt += "\n🪵 [2] مقاسات لوح الفايبر (القص الصافي للهيكل):\n"
            txt += f"  - الضهرية : عدد (1) قطعة مقاس ({w_net} × {h_net}) سم\n"
            txt += f"  - الأرضية : عدد (1) قطعة مقاس ({w_net} × {d_net}) سم\n"
            txt += f"  - الأجناب : عدد (2) قطعة مقاس ({h_net} × {d_net}) سم\n"

            # [3] تفصيل الأرفف
            if sh_n > 0:
                txt += f"\n🧱 [3] تفصيل الأرفف (عدد {sh_n}):\n"
                txt += f"  - ألومنيوم العرض: قطع ({sh_n * 4}) قطعة مفرد مقاس {sh_w} سم\n"
                txt += f"  - ألومنيوم العمق : قطع ({sh_n * 4}) قطعة مفرد مقاس {sh_d} سم\n"
                txt += f"  - فايبر الرف (صافي): عدد ({sh_n}) قطعة مقاس {sh_w - 5} × {sh_d - 5} سم\n"
                txt += f"    *(ملاحظة: تم خصم 5 سم من الألومنيوم للفيبر الصافي)*\n"

            # [4] تفصيل الفواصل
            if dv_n > 0:
                txt += f"\n📐 [4] تفصيل الفواصل (عدد {dv_n}):\n"
                txt += f"  - ألومنيوم الارتفاع: قطع ({dv_n * 4}) قطعة مفرد مقاس {dv_h} سم\n"
                txt += f"  - ألومنيوم العمق   : قطع ({dv_n * 4}) قطعة مفرد مقاس {dv_d} سم\n"
                txt += f"  - فايبر الفاصل(صافي): عدد ({dv_n}) قطعة مقاس {dv_h - 5} × {dv_d - 5} سم\n"

            # [5] تفصيل الأدراج (الـ 2.5 سم بتوع المجرى)
            if dr_n > 0:
                txt += f"\n🗄️ [5] تفصيل الأدراج (عدد {dr_n}):\n"
                txt += f"  - ألومنيوم العرض: قطع ({dr_n * 2}) قطعة مفرد مقاس {dr_w - 2.5} سم\n"
                txt += f"  - ألومنيوم العمق : قطع ({dr_n * 2}) قطعة مفرد مقاس {dr_d} سم\n"
                txt += f"    *(ملاحظة: العرض مخصوم منه 2.5 سم لمجرى الدرج)*\n"

            txt += "\n" + "━" * 75 + "\n"
            txt += "✅ تم حساب التخصيمات بدقة وفقاً لمعايير الورشة."
            self.result_sheet.setText(txt)
            
        except:
            QMessageBox.critical(self, "خطأ", "برجاء مراجعة المقاسات المدخلة (يجب أن تكون أرقام)")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AluminumMasterApp()
    ex.show()
    sys.exit(app.exec_())
