import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QComboBox, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView, QGridLayout, QMessageBox, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SummaryDialog(QDialog):
    def __init__(self, report):
        super().__init__()
        self.setWindowTitle("📊 فاتورة جرد خامات المشروع")
        self.setMinimumSize(600, 500)
        layout = QVBoxLayout()
        view = QTextEdit()
        view.setReadOnly(True)
        view.setStyleSheet("background-color: #1e272e; color: #f1c40f; font-family: 'Consolas'; font-size: 13pt; padding: 15px;")
        view.setText(report)
        layout.addWidget(view)
        self.setLayout(layout)

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = [] 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام تخصيم الألومنيوم - نسخة الورشة النهائية')
        self.setGeometry(30, 30, 1300, 950)
        self.setFont(QFont("Segoe UI", 11))

        main_layout = QVBoxLayout()

        self.total_btn = QPushButton("📊 جرد خامات المشروع بالكامل (فاتورة قص)")
        self.total_btn.setStyleSheet("background-color: #d35400; color: white; font-weight: bold; height: 60px; font-size: 14pt; border-radius: 10px;")
        self.total_btn.clicked.connect(self.show_project_totals)
        main_layout.addWidget(self.total_btn)

        input_group = QGroupBox("📝 مدخلات المقاسات (تحرك بالأسهم)")
        grid = QGridLayout()

        self.unit_title = QLineEdit(); self.unit_title.setPlaceholderText("اسم الوحدة")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        
        self.w = QLineEdit(); self.w.setPlaceholderText("العرض الكلي")
        self.h = QLineEdit(); self.h.setPlaceholderText("الارتفاع الكلي")
        self.d = QLineEdit(); self.d.setPlaceholderText("العمق الكلي")
        
        self.sh_w = QLineEdit(); self.sh_w.setPlaceholderText("الرف (عرض)")
        self.sh_d = QLineEdit(); self.sh_d.setPlaceholderText("الرف (عمق)")
        self.sh_n = QLineEdit(); self.sh_n.setPlaceholderText("الرفوف (عدد)")
        
        self.dv_h = QLineEdit(); self.dv_h.setPlaceholderText("الفاصل (ارتفاع)")
        self.dv_d = QLineEdit(); self.dv_d.setPlaceholderText("الفاصل (عمق)")
        self.dv_n = QLineEdit(); self.dv_n.setPlaceholderText("الفواصل (عدد)")

        self.dr_w = QLineEdit(); self.dr_w.setPlaceholderText("الدرج (عرض)")
        self.dr_d = QLineEdit(); self.dr_d.setPlaceholderText("الدرج (عمق)")
        self.dr_n = QLineEdit(); self.dr_n.setPlaceholderText("الأدراج (عدد)")

        grid.addWidget(self.unit_title, 0, 0, 1, 2); grid.addWidget(self.unit_type, 0, 2)
        grid.addWidget(self.w, 1, 0); grid.addWidget(self.h, 1, 1); grid.addWidget(self.d, 1, 2)
        grid.addWidget(self.sh_w, 2, 0); grid.addWidget(self.sh_d, 2, 1); grid.addWidget(self.sh_n, 2, 2)
        grid.addWidget(self.dv_h, 3, 0); grid.addWidget(self.dv_d, 3, 1); grid.addWidget(self.dv_n, 3, 2)
        grid.addWidget(self.dr_w, 4, 0); grid.addWidget(self.dr_d, 4, 1); grid.addWidget(self.dr_n, 4, 2)

        input_group.setLayout(grid)
        main_layout.addWidget(input_group)

        self.nav_map = [
            [self.unit_title, self.unit_title, self.unit_type],
            [self.w, self.h, self.d],
            [self.sh_w, self.sh_d, self.sh_n],
            [self.dv_h, self.dv_d, self.dv_n],
            [self.dr_w, self.dr_d, self.dr_n]
        ]

        btns = QHBoxLayout()
        self.add_btn = QPushButton("💾 إضافة للجدول")
        self.add_btn.setStyleSheet("background-color: #27ae60; color: white; height: 50px; font-weight: bold;")
        self.add_btn.clicked.connect(self.process_unit)
        self.clear_btn = QPushButton("🗑️ مسح الكل")
        self.clear_btn.setStyleSheet("background-color: #c0392b; color: white; height: 50px; font-weight: bold;")
        self.clear_btn.clicked.connect(self.clear_all)
        btns.addWidget(self.add_btn); btns.addWidget(self.clear_btn)
        main_layout.addLayout(btns)

        display = QHBoxLayout()
        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("background-color: #ffffff; border: 2px solid #2ecc71; font-family: 'Courier New'; font-size: 11pt; padding: 10px;")
        self.table = QTableWidget(); self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الوحدة", "العرض", "الارتفاع", "العمق"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        display.addWidget(self.result_sheet, 7); display.addWidget(self.table, 3)
        main_layout.addLayout(display)
        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        curr = self.focusWidget()
        r, c = -1, -1
        for row in range(5):
            if curr in self.nav_map[row]: r, c = row, self.nav_map[row].index(curr); break
        if r != -1:
            if event.key() == Qt.Key_Right: self.nav_map[r][min(c+1, 2)].setFocus()
            elif event.key() == Qt.Key_Left: self.nav_map[r][max(c-1, 0)].setFocus()
            elif event.key() == Qt.Key_Down:
                if r < 4: self.nav_map[r+1][c].setFocus()
                else: self.add_btn.setFocus()
            elif event.key() == Qt.Key_Up:
                if r > 0: self.nav_map[r-1][c].setFocus()
            elif event.key() == Qt.Key_Return:
                if r < 4: self.nav_map[r+1][c].setFocus()
                else: self.process_unit()

    def process_unit(self):
        try:
            u = {
                'title': self.unit_title.text() or "وحدة", 'type': self.unit_type.currentText(),
                'w': float(self.w.text() or 0), 'h': float(self.h.text() or 0), 'd': float(self.d.text() or 0),
                'sh_w': float(self.sh_w.text() or 0), 'sh_d': float(self.sh_d.text() or 0), 'sh_n': int(self.sh_n.text() or 0),
                'dv_h': float(self.dv_h.text() or 0), 'dv_d': float(self.dv_d.text() or 0), 'dv_n': int(self.dv_n.text() or 0),
                'dr_w': float(self.dr_w.text() or 0), 'dr_d': float(self.dr_d.text() or 0), 'dr_n': int(self.dr_n.text() or 0)
            }
            if self.project_storage and u == self.project_storage[-1]:
                if QMessageBox.question(self, "تنبيه", "تكرار الوحدة؟", QMessageBox.Yes|QMessageBox.No) == QMessageBox.No: return

            h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_baky, d_baky = u['w'] - 5, u['d'] - 5

            txt = f"\n📦 {u['title']} | النوع: {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
            txt += "━" * 55 + "\n"
            
            txt += "📐 [1] تخصيم الألومنيوم (2*8):\n"
            if u['type'] == "سفلية":
                txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"  - عــــرض {w_baky}: [3 مفرد] [1 متقارب]\n"
                txt += f"  - عمــــق {d_baky}: [2 مفرد] [2 متقارب]\n"
            else:
                txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"  - عــــرض {w_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"  - عمــــق {d_baky}: [4 متقارب]\n"

            txt += "\n🪵 [2] تخصيم الفيبر (التقطيع):\n"
            txt += f"  - ضهرية: {w_baky} × {h_baky} (1)\n"
            txt += f"  - أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n"
            txt += f"  - أجناب: {h_baky} × {d_baky} (2)\n"

            if u['sh_n'] > 0:
                txt += f"\n🧱 [3] الرفوف ({u['sh_n']}):\n"
                txt += f"  - ألومنيوم: {u['sh_w']} × {u['sh_n']*2} قطعة | {u['sh_d']} × {u['sh_n']*2} قطعة [مفرد]\n"
                txt += f"  - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5} ({u['sh_n']} قطعة)\n"

            if u['dv_n'] > 0:
                txt += f"\n📐 [4] الفواصل ({u['dv_n']}):\n"
                txt += f"  - ألومنيوم: {u['dv_h']} × {u['dv_n']*2} قطعة | {u['dv_d']} × {u['dv_n']*2} قطعة [مفرد]\n"
                txt += f"  - فيبر الفاصل: {u['dv_h']-5} × {u['dv_d']-5} ({u['dv_n']} قطعة)\n"

            if u['dr_n'] > 0:
                txt += f"\n🗄️ [5] الأدراج ({u['dr_n']}):\n"
                txt += f"  - ألومنيوم العرض: {u['dr_w']-2.5} × {u['dr_n']*2} | العمق: {u['dr_d']} × {u['dr_n']*2}\n"

            txt += "━" * 55
            self.result_sheet.append(txt); self.project_storage.append(u)
            row = self.table.rowCount(); self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(u['title']))
            self.table.setItem(row, 1, QTableWidgetItem(str(u['w'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(u['h'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(u['d'])))
            
            self.unit_title.clear(); self.w.clear(); self.h.clear(); self.d.clear(); self.unit_title.setFocus()
        except: QMessageBox.critical(self, "خطأ", "برجاء مراجعة المقاسات")

    def clear_all(self):
        if QMessageBox.question(self, "تأكيد", "مسح كل البيانات؟", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.project_storage = []; self.table.setRowCount(0); self.result_sheet.clear()

    def show_project_totals(self):
        if not self.project_storage: return
        m_sum, t_sum, f_area = 0, 0, 0
        for u in self.project_storage:
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b, d_b = u['w'] - 5, u['d'] - 5
            
            if u['type'] == "سفلية":
                m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                f_area += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                f_area += (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
            
            # الرفوف والفواصل (قطعتين لكل ضلع)
            m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
            f_area += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n'] + (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
            # الأدراج
            m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']

        rep = f"📊 جرد الخامات النهائي للمشروع:\n━━━━━━━━━━━━━━━━━━━━━\n"
        rep += f"🔹 ألومنيوم مفرد:   {m_sum/600:.2f} عود\n"
        rep += f"🔹 ألومنيوم متقارب: {t_sum/600:.2f} عود\n"
        rep += f"🔹 فيبر (2.8*1.3):  {f_area/36400:.2f} لوح\n"
        rep += "━━━━━━━━━━━━━━━━━━━━━"
        SummaryDialog(rep).exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = AluminumMasterApp(); ex.show(); sys.exit(app.exec_())
