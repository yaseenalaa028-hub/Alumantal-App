import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# ===============================
# فاتورة Excel داخل البرنامج
# ===============================
class InvoiceDialog(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("📋 فاتورة الخامات - Excel")
        self.setMinimumSize(900, 600)

        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["القسم", "البيان", "المقاس", "العدد"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        row = 0
        table.setRowCount(1000)

        for u in data:
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b = u['w'] - 5
            d_b = u['d'] - 5

            items = [
                ("مونتال", "ارتفاع", int(h_b), 4),
                ("مونتال", "عرض", int(w_b), 4),
                ("مونتال", "عمق", int(d_b), 4),
                ("فيبر", "ضهرية", f"{int(w_b)}x{int(h_b)}", 1),
                ("فيبر", "أرضية", f"{int(w_b)}x{int(d_b)}", 1),
                ("فيبر", "أجناب", f"{int(h_b)}x{int(d_b)}", 2),
            ]

            for it in items:
                table.setItem(row, 0, QTableWidgetItem(it[0]))
                table.setItem(row, 1, QTableWidgetItem(it[1]))
                table.setItem(row, 2, QTableWidgetItem(str(it[2])))
                table.setItem(row, 3, QTableWidgetItem(str(it[3])))
                row += 1

        table.setRowCount(row)
        layout.addWidget(table)
        self.setLayout(layout)

# ===============================
# نافذة الجرد
# ===============================
class SummaryDialog(QDialog):
    def __init__(self, report):
        super().__init__()
        self.setWindowTitle("📊 جرد تفصيلي")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()
        view = QTextEdit()
        view.setReadOnly(True)
        view.setText(report)
        layout.addWidget(view)
        self.setLayout(layout)

# ===============================
# البرنامج الرئيسي
# ===============================
class AluminumMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.project_storage = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('نظام تخصيم الألومنيوم')
        self.setGeometry(30, 30, 1300, 900)
        self.setFont(QFont("Segoe UI", 11))

        layout = QVBoxLayout()

        # ===== الأزرار =====
        self.total_btn = QPushButton("📊 جرد تفصيلي")
        self.total_btn.clicked.connect(self.show_project_totals)

        self.invoice_btn = QPushButton("📋 فاتورة Excel")
        self.invoice_btn.clicked.connect(self.show_invoice)

        self.export_btn = QPushButton("📥 تصدير Excel")
        self.export_btn.clicked.connect(self.export_excel)

        for b in [self.total_btn, self.invoice_btn, self.export_btn]:
            b.setStyleSheet("height:50px; font-weight:bold;")
            layout.addWidget(b)

        # ===== المدخلات =====
        grid = QGridLayout()

        self.unit_title = QLineEdit()
        self.unit_type = QComboBox()
        self.unit_type.addItems(["سفلية", "علوية", "دولاب خزين"])

        self.w = QLineEdit()
        self.h = QLineEdit()
        self.d = QLineEdit()

        self.sh_w = QLineEdit()
        self.sh_d = QLineEdit()
        self.sh_n = QLineEdit()

        self.dv_h = QLineEdit()
        self.dv_d = QLineEdit()
        self.dv_n = QLineEdit()

        self.dr_w = QLineEdit()
        self.dr_d = QLineEdit()
        self.dr_n = QLineEdit()

        grid.addWidget(self.unit_title,0,0)
        grid.addWidget(self.unit_type,0,1)

        grid.addWidget(self.w,1,0)
        grid.addWidget(self.h,1,1)
        grid.addWidget(self.d,1,2)

        grid.addWidget(self.sh_w,2,0)
        grid.addWidget(self.sh_d,2,1)
        grid.addWidget(self.sh_n,2,2)

        grid.addWidget(self.dv_h,3,0)
        grid.addWidget(self.dv_d,3,1)
        grid.addWidget(self.dv_n,3,2)

        grid.addWidget(self.dr_w,4,0)
        grid.addWidget(self.dr_d,4,1)
        grid.addWidget(self.dr_n,4,2)

        layout.addLayout(grid)

        # ===== أزرار التحكم =====
        btns = QHBoxLayout()
        self.add_btn = QPushButton("إضافة")
        self.add_btn.clicked.connect(self.process_unit)

        self.clear_btn = QPushButton("مسح")
        self.clear_btn.clicked.connect(self.clear_all)

        btns.addWidget(self.add_btn)
        btns.addWidget(self.clear_btn)

        layout.addLayout(btns)

        # ===== العرض =====
        self.result = QTextEdit()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["الوحدة","العرض","الارتفاع","العمق"])

        display = QHBoxLayout()
        display.addWidget(self.result)
        display.addWidget(self.table)

        layout.addLayout(display)
        self.setLayout(layout)

    # ===============================
    # إضافة وحدة
    # ===============================
    def process_unit(self):
        try:
            u = {
                'title': self.unit_title.text(),
                'type': self.unit_type.currentText(),
                'w': float(self.w.text() or 0),
                'h': float(self.h.text() or 0),
                'd': float(self.d.text() or 0),
                'sh_w': float(self.sh_w.text() or 0),
                'sh_d': float(self.sh_d.text() or 0),
                'sh_n': int(self.sh_n.text() or 0),
                'dv_h': float(self.dv_h.text() or 0),
                'dv_d': float(self.dv_d.text() or 0),
                'dv_n': int(self.dv_n.text() or 0),
                'dr_w': float(self.dr_w.text() or 0),
                'dr_d': float(self.dr_d.text() or 0),
                'dr_n': int(self.dr_n.text() or 0)
            }

            self.project_storage.append(u)

            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(u['title']))
            self.table.setItem(row,1,QTableWidgetItem(str(u['w'])))
            self.table.setItem(row,2,QTableWidgetItem(str(u['h'])))
            self.table.setItem(row,3,QTableWidgetItem(str(u['d'])))

        except:
            QMessageBox.critical(self,"خطأ","راجع البيانات")

    # ===============================
    # جرد تفصيلي
    # ===============================
    def show_project_totals(self):
        report = ""
        for u in self.project_storage:
            report += f"{u['title']} - {u['type']}\n"
        SummaryDialog(report).exec_()

    # ===============================
    # فاتورة داخل البرنامج
    # ===============================
    def show_invoice(self):
        InvoiceDialog(self.project_storage).exec_()

    # ===============================
    # تصدير Excel
    # ===============================
    def export_excel(self):
        rows = []
        for u in self.project_storage:
            rows.append({
                "الوحدة": u['title'],
                "العرض": u['w'],
                "الارتفاع": u['h'],
                "العمق": u['d']
            })

        df = pd.DataFrame(rows)
        df.to_excel("report.xlsx", index=False)
        QMessageBox.information(self,"تم","تم إنشاء ملف Excel")

    def clear_all(self):
        self.project_storage=[]
        self.table.setRowCount(0)
        self.result.clear()

# ===============================
# تشغيل البرنامج
# ===============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AluminumMasterApp()
    win.show()
    sys.exit(app.exec_())
