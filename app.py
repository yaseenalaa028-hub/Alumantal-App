import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit,
                             QComboBox, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
                             QGridLayout, QMessageBox, QDialog, QFileDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from fpdf import FPDF  # تأكد من عمل pip install fpdf

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = [] 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام تخصيم الألومنيوم - المهندس ياسين علاء')
        self.setGeometry(30, 30, 1300, 950)
        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout()

        # الهيدر المحمي
        header_label = QLabel("نظام تخصيم الألومنيوم - المهندس ياسين علاء")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            background-color: #2f3640; color: #fbc531; font-size: 20pt;
            font-weight: bold; padding: 15px; border-bottom: 4px solid #e1b12c;
            border-radius: 10px; margin-bottom: 10px;
        """)
        main_layout.addWidget(header_label)

        # صف أزرار العمليات (الجرد وحفظ PDF)
        top_btns = QHBoxLayout()
        self.pdf_btn = QPushButton("📄 حفظ كـ PDF")
        self.pdf_btn.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold; height: 55px; font-size: 13pt; border-radius: 10px;")
        self.pdf_btn.clicked.connect(self.save_as_pdf)
        
        self.total_btn = QPushButton("📊 جرد خامات المشروع")
        self.total_btn.setStyleSheet("background-color: #d35400; color: white; font-weight: bold; height: 55px; font-size: 13pt; border-radius: 10px;")
        self.total_btn.clicked.connect(self.show_project_totals)
        
        top_btns.addWidget(self.pdf_btn)
        top_btns.addWidget(self.total_btn)
        main_layout.addLayout(top_btns)

        # مدخلات المقاسات (بدون أصفار - Placeholder فقط)
        input_group = QGroupBox("📝 مدخلات المقاسات")
        grid = QGridLayout()
        self.unit_title = QLineEdit(); self.unit_title.setPlaceholderText("اسم الوحدة")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين"])
        
        self.w = QLineEdit(); self.w.setPlaceholderText("العرض W")
        self.h = QLineEdit(); self.h.setPlaceholderText("الارتفاع H")
        self.d = QLineEdit(); self.d.setPlaceholderText("العمق D")
        
        # مدخلات الأرفف والأدراج
        self.sh_n = QLineEdit(); self.sh_n.setPlaceholderText("عدد الرفوف")
        self.sh_w = QLineEdit(); self.sh_w.setPlaceholderText("عرض الرف")
        self.sh_d = QLineEdit(); self.sh_d.setPlaceholderText("عمق الرف")
        self.dr_n = QLineEdit(); self.dr_n.setPlaceholderText("عدد الأدراج")
        self.dr_w = QLineEdit(); self.dr_w.setPlaceholderText("عرض الدرج")

        grid.addWidget(self.unit_title, 0, 0); grid.addWidget(self.unit_type, 0, 1)
        grid.addWidget(self.w, 1, 0); grid.addWidget(self.h, 1, 1); grid.addWidget(self.d, 1, 2)
        grid.addWidget(self.sh_w, 2, 0); grid.addWidget(self.sh_d, 2, 1); grid.addWidget(self.sh_n, 2, 2)
        grid.addWidget(self.dr_w, 3, 0); grid.addWidget(self.dr_n, 3, 1)
        input_group.setLayout(grid)
        main_layout.addWidget(input_group)

        # زر الإضافة
        self.add_btn = QPushButton("💾 إضافة وحساب التخصيم")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-weight: bold;")
        self.add_btn.clicked.connect(self.process_unit)
        main_layout.addWidget(self.add_btn)

        # عرض النتائج
        display = QHBoxLayout()
        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("background-color: #ffffff; border: 2px solid #2ecc71; font-size: 11pt;")
        display.addWidget(self.result_sheet)
        main_layout.addLayout(display)

        self.setLayout(main_layout)

    def process_unit(self):
        try:
            name = self.unit_title.text() or "وحدة"
            u_type = self.unit_type.currentText()
            w = float(self.w.text()); h = float(self.h.text()); d = float(self.d.text())
            
            # 1. تخصيم الهيكل الأساسي
            h_baky = h - 13 if u_type != "علوية" else h - 5
            w_baky, d_baky = w - 5, d - 5

            res = f"📦 {name} | {u_type} | {w}x{h}x{d}\n"
            res += "━" * 40 + "\n"
            res += f"🛠️ الألومنيوم: H:{h_baky} | W:{w_baky} | D:{d_baky}\n"
            res += f"🪵 الفيبر: ضهرية {w_baky}x{h_baky} | أجناب {h_baky}x{d_baky}\n"

            # 2. تخصيم الأرفف (الدقيق)
            if self.sh_n.text() and float(self.sh_w.text() or 0) > 0:
                sh_w_fib = float(self.sh_w.text()) - 5
                sh_d_fib = float(self.sh_d.text()) - 5
                res += f"🧱 الرفوف ({self.sh_n.text()}): فيبر الرف الصافي {sh_w_fib}x{sh_d_fib}\n"

            # 3. تخصيم الأدراج
            if self.dr_n.text() and float(self.dr_w.text() or 0) > 0:
                dr_w_final = float(self.dr_w.text()) - 2.5
                res += f"🗄️ الأدراج: عرض ألومنيوم الدرج {dr_w_final}\n"

            res += "━" * 40 + "\n"
            self.result_sheet.append(res)
            self.project_storage.append(res)
            
            # تنظيف الخانات
            self.w.clear(); self.h.clear(); self.d.clear(); self.unit_title.setFocus()
        except:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال المقاسات بشكل صحيح")

    def save_as_pdf(self):
        if not self.project_storage: return
        path, _ = QFileDialog.getSaveFileName(self, "حفظ ملف PDF", "", "PDF Files (*.pdf)")
        if path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Kitchen Cutting List - Eng. Yassin Alaa", ln=1, align='C')
            pdf.ln(10)
            for item in self.project_storage:
                # تنظيف النص من الإيموجي لأن FPDF النسخة العادية لا تدعمها جيداً بدون خطوط خاصة
                clean_text = item.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, txt=clean_text)
            pdf.output(path)
            QMessageBox.information(self, "نجاح", "تم حفظ ملف PDF")

    def show_project_totals(self):
        # هنا تضع دالة الجرد النهائية
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AluminumMasterApp()
    ex.show()
    sys.exit(app.exec_())
