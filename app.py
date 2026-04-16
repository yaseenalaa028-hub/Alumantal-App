import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QComboBox, QGroupBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QGridLayout, QMessageBox, QDialog, QFileDialog)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt

class SummaryDialog(QDialog):                                                 
    def __init__(self, report):
        super().__init__()
        self.setWindowTitle("📊 فاتورة جرد خامات المشروع")
        self.setMinimumSize(600, 500)
        layout = QVBoxLayout()
        view = QTextEdit()
        view.setReadOnly(True)
        # ستايل شاشة الجرد
        view.setStyleSheet("""
            background-color: #1e272e; 
            color: #f1c40f; 
            font-family: 'Consolas', 'Segoe UI'; 
            font-size: 14pt; 
            padding: 20px;
            border-radius: 10px;
        """)
        view.setText(report)
        layout.addWidget(view)
        self.setLayout(layout)

class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = [] 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام الألومنيوم الاحترافي - م/ ياسين علاء')
        self.setGeometry(50, 50, 1300, 900)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("background-color: #ecf0f1;")

        main_layout = QVBoxLayout()

        # --- الهيدر (العنوان العلوي) ---
        header_label = QLabel("نظام التخصيم الفني | إدارة المهندس ياسين علاء")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            background-color: #2c3e50; color: #f1c40f;
            font-size: 24pt; font-weight: bold; padding: 20px;
            border-bottom: 5px solid #f1c40f;
            border-radius: 15px; margin-bottom: 15px;
        """)
        main_layout.addWidget(header_label)

        # --- أزرار العمليات الكبرى ---
        top_btns = QHBoxLayout()
        
        self.total_btn = QPushButton("📊 جرد خامات المشروع (فاتورة قص)")
        self.total_btn.setStyleSheet("""
            QPushButton { background-color: #e67e22; color: white; font-weight: bold; height: 65px; font-size: 15pt; border-radius: 12px; }
            QPushButton:hover { background-color: #d35400; }
        """)
        self.total_btn.clicked.connect(self.show_project_totals)

        self.save_btn = QPushButton("💾 حفظ التخصيم والجرد (PDF/Text)")
        self.save_btn.setStyleSheet("""
            QPushButton { background-color: #2980b9; color: white; font-weight: bold; height: 65px; font-size: 15pt; border-radius: 12px; }
            QPushButton:hover { background-color: #2471a3; }
        """)
        self.save_btn.clicked.connect(self.save_project_report)

        top_btns.addWidget(self.total_btn)
        top_btns.addWidget(self.save_btn)
        main_layout.addLayout(top_btns)

        # --- منطقة المدخلات ---
        input_container = QHBoxLayout()
        
        # مجموعة المقاسات الأساسية
        basic_group = QGroupBox("📏 المقاسات الأساسية")
        basic_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 10px; margin-top: 10px; padding-top: 20px; }")
        basic_grid = QGridLayout()
        
        self.unit_title = QLineEdit(); self.unit_title.setPlaceholderText("اسم الوحدة")
        self.unit_type = QComboBox(); self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        self.w = QLineEdit(); self.w.setPlaceholderText("العرض الكلي (W)")
        self.h = QLineEdit(); self.h.setPlaceholderText("الارتفاع الكلي (H)")
        self.d = QLineEdit(); self.d.setPlaceholderText("العمق الكلي (D)")

        # استايل موحد لكل الـ LineEdit
        input_style = "QLineEdit { padding: 8px; font-size: 12pt; border: 1px solid #bdc3c7; border-radius: 5px; background: white; } QLineEdit:focus { border: 2px solid #f1c40f; }"
        for widget in [self.unit_title, self.w, self.h, self.d]: widget.setStyleSheet(input_style)
        self.unit_type.setStyleSheet("QComboBox { padding: 8px; font-size: 12pt; }")

        basic_grid.addWidget(QLabel("اسم الوحدة:"), 0, 0); basic_grid.addWidget(self.unit_title, 0, 1)
        basic_grid.addWidget(QLabel("النوع:"), 0, 2); basic_grid.addWidget(self.unit_type, 0, 3)
        basic_grid.addWidget(QLabel("العرض:"), 1, 0); basic_grid.addWidget(self.w, 1, 1)
        basic_grid.addWidget(QLabel("الارتفاع:"), 1, 2); basic_grid.addWidget(self.h, 1, 3)
        basic_grid.addWidget(QLabel("العمق:"), 2, 0); basic_grid.addWidget(self.d, 2, 1)
        basic_group.setLayout(basic_grid)

        # مجموعة الإضافات (أرفف، فواصل، أدراج)
        extra_group = QGroupBox("🧱 الإضافات الفنية")
        extra_group.setStyleSheet("QGroupBox { font-weight: bold; color: #c0392b; border: 2px solid #bdc3c7; border-radius: 10px; margin-top: 10px; padding-top: 20px; }")
        extra_grid = QGridLayout()

        self.sh_w = QLineEdit(); self.sh_w.setPlaceholderText("الرف (ع)")
        self.sh_d = QLineEdit(); self.sh_d.setPlaceholderText("الرف (ق)")
        self.sh_n = QLineEdit(); self.sh_n.setPlaceholderText("العدد")
        self.dv_h = QLineEdit(); self.dv_h.setPlaceholderText("الفاصل (ت)")
        self.dv_d = QLineEdit(); self.dv_d.setPlaceholderText("الفاصل (ق)")
        self.dv_n = QLineEdit(); self.dv_n.setPlaceholderText("العدد")
        self.dr_w = QLineEdit(); self.dr_w.setPlaceholderText("الدرج (ع)")
        self.dr_d = QLineEdit(); self.dr_d.setPlaceholderText("الدرج (ق)")
        self.dr_n = QLineEdit(); self.dr_n.setPlaceholderText("العدد")

        for w_ex in [self.sh_w, self.sh_d, self.sh_n, self.dv_h, self.dv_d, self.dv_n, self.dr_w, self.dr_d, self.dr_n]: w_ex.setStyleSheet(input_style)

        extra_grid.addWidget(QLabel("الرفوف:"), 0, 0); extra_grid.addWidget(self.sh_w, 0, 1); extra_grid.addWidget(self.sh_d, 0, 2); extra_grid.addWidget(self.sh_n, 0, 3)
        extra_grid.addWidget(QLabel("الفواصل:"), 1, 0); extra_grid.addWidget(self.dv_h, 1, 1); extra_grid.addWidget(self.dv_d, 1, 2); extra_grid.addWidget(self.dv_n, 1, 3)
        extra_grid.addWidget(QLabel("الأدراج:"), 2, 0); extra_grid.addWidget(self.dr_w, 2, 1); extra_grid.addWidget(self.dr_d, 2, 2); extra_grid.addWidget(self.dr_n, 2, 3)
        extra_group.setLayout(extra_grid)

        input_container.addWidget(basic_group, 5)
        input_container.addWidget(extra_group, 5)
        main_layout.addLayout(input_container)

        # خريطة التنقل (نفس منطقك الأصلي)
        self.nav_map = [
            [self.unit_title, self.unit_title, self.unit_type],
            [self.w, self.h, self.d],
            [self.sh_w, self.sh_d, self.sh_n],
            [self.dv_h, self.dv_d, self.dv_n],
            [self.dr_w, self.dr_d, self.dr_n]
        ]

        # أزرار الإضافة والمسح
        btns = QHBoxLayout()
        self.add_btn = QPushButton("✅ إضافة الوحدة (Enter)")
        self.add_btn.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; height: 55px; font-weight: bold; font-size: 14pt; border-radius: 10px; }
            QPushButton:hover { background-color: #219150; }
        """)
        self.add_btn.clicked.connect(self.process_unit)

        self.clear_btn = QPushButton("🗑️ تفريغ البيانات")
        self.clear_btn.setStyleSheet("""
            QPushButton { background-color: #c0392b; color: white; height: 55px; font-weight: bold; font-size: 14pt; border-radius: 10px; }
            QPushButton:hover { background-color: #a93226; }
        """)
        self.clear_btn.clicked.connect(self.clear_all)

        btns.addWidget(self.add_btn, 7); btns.addWidget(self.clear_btn, 3)
        main_layout.addLayout(btns)

        # منطقة عرض النتائج والجدول
        display = QHBoxLayout()
        self.result_sheet = QTextEdit(); self.result_sheet.setReadOnly(True)
        self.result_sheet.setStyleSheet("""
            background-color: white; 
            border: 3px solid #2c3e50; 
            border-radius: 10px;
            font-family: 'Consolas', 'Courier New'; 
            font-size: 12pt; 
            padding: 15px;
        """)

        self.table = QTableWidget(); self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الوحدة", "العرض", "الارتفاع", "العمق"])
        self.table.setStyleSheet("QTableWidget { background-color: white; border-radius: 10px; border: 1px solid #bdc3c7; }")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; }")

        display.addWidget(self.result_sheet, 6)
        display.addWidget(self.table, 4)
        main_layout.addLayout(display)

        self.setLayout(main_layout)

    # --- (باقي الميثودز زي ما هي بالظبط عشان منطق الحساب ميتغيرش) ---

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
            h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_baky, d_baky = u['w'] - 5, u['d'] - 5

            txt = f"\n📦 {u['title']} | {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
            txt += "━" * 55 + "\n"
            txt += "📐 [1] تخصيم الألومنيوم (2*8):\n"
            if u['type'] == "سفلية":
                txt += f"   - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"   - عــــرض {w_baky}: [3 مفرد] [1 متقارب]\n"
                txt += f"   - عمــــق {d_baky}: [2 مفرد] [2 متقارب]\n"
            else:
                txt += f"   - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"   - عــــرض {w_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"   - عمــــق {d_baky}: [4 متقارب]\n"

            txt += "\n🪵 [2] تخصيم الفيبر (التقطيع):\n"
            txt += f"   - ضهرية: {w_baky} × {h_baky} (1)\n"
            txt += f"   - أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n"
            txt += f"   - أجناب: {h_baky} × {d_baky} (2)\n"

            if u['sh_n'] > 0:
                txt += f"\n🧱 [3] الرفوف ({u['sh_n']}):\n"
                txt += f"   - ألومنيوم: {u['sh_w']} × {u['sh_n']*2} قطعة | {u['sh_d']} × {u['sh_n']*2} قطعة [مفرد]\n"
                txt += f"   - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5} ({u['sh_n']} قطعة)\n"

            if u['dv_n'] > 0:
                txt += f"\n📐 [4] الفواصل ({u['dv_n']}):\n"
                txt += f"   - ألومنيوم: {u['dv_h']} × {u['dv_n']*2} قطعة | {u['dv_d']} × {u['dv_n']*2} قطعة [مفرد]\n"
                txt += f"   - فيبر الفاصل: {u['dv_h']-5} × {u['dv_d']-5} ({u['dv_n']} قطعة)\n"

            if u['dr_n'] > 0:
                txt += f"\n🗄️ [5] الأدراج ({u['dr_n']}):\n"
                txt += f"   - ألومنيوم العرض: {u['dr_w']-2.5} × {u['dr_n']*2} | العمق: {u['dr_d']} × {u['dr_n']*2}\n"

            txt += "━" * 55
            self.result_sheet.append(txt); self.project_storage.append(u)
            row = self.table.rowCount(); self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(u['title']))
            self.table.setItem(row, 1, QTableWidgetItem(str(u['w'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(u['h'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(u['d'])))
            
            self.unit_title.clear(); self.w.clear(); self.h.clear(); self.d.clear(); self.unit_title.setFocus()
        except: QMessageBox.critical(self, "خطأ", "برجاء مراجعة المقاسات")

    def calculate_project_data(self):
        m_sum, t_sum, f_area = 0, 0, 0
        for u in self.project_storage:
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b, d_b = u['w'] - 5, u['d'] - 5
            if u['type'] == "سفلية":
                m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                f_area += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_sum += (h_b*2)+(w_b*2); t_sum += (
