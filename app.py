import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


# =========================
# MAIN WINDOW
# =========================
class DoggaSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DOGGA SMART SYSTEM")
        self.setGeometry(100, 100, 1200, 700)

        self.projects = []

        self.init_ui()

    # =========================
    # UI
    # =========================
    def init_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()

        # =========================
        # TITLE
        # =========================
        title = QLabel("🛠️ DOGGA SMART SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:28px;font-weight:bold;color:#f1c40f;")
        main_layout.addWidget(title)

        # =========================
        # FORM
        # =========================
        form = QGridLayout()

        self.client = QLineEdit()
        self.client.setPlaceholderText("اسم العميل")

        self.unit = QComboBox()
        self.unit.addItems(["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        self.W = QLineEdit(); self.W.setPlaceholderText("العرض")
        self.H = QLineEdit(); self.H.setPlaceholderText("الارتفاع")
        self.D = QLineEdit(); self.D.setPlaceholderText("العمق")

        self.sh_n = QLineEdit(); self.sh_n.setPlaceholderText("عدد الأرفف")
        self.sh_w = QLineEdit(); self.sh_w.setPlaceholderText("عرض الرف")
        self.sh_d = QLineEdit(); self.sh_d.setPlaceholderText("عمق الرف")

        self.v_n = QLineEdit(); self.v_n.setPlaceholderText("عدد الفواصل")
        self.v_h = QLineEdit(); self.v_h.setPlaceholderText("ارتفاع الفاصل")
        self.v_d = QLineEdit(); self.v_d.setPlaceholderText("عمق الفاصل")

        self.dr_n = QLineEdit(); self.dr_n.setPlaceholderText("عدد الأدراج")
        self.dr_w = QLineEdit(); self.dr_w.setPlaceholderText("عرض الدرج")
        self.dr_d = QLineEdit(); self.dr_d.setPlaceholderText("عمق الدرج")

        inputs = [
            ("العميل", self.client),
            ("الوحدة", self.unit),
            ("العرض", self.W),
            ("الارتفاع", self.H),
            ("العمق", self.D),
            ("عدد الأرفف", self.sh_n),
            ("عرض الرف", self.sh_w),
            ("عمق الرف", self.sh_d),
            ("عدد الفواصل", self.v_n),
            ("ارتفاع الفاصل", self.v_h),
            ("عمق الفاصل", self.v_d),
            ("عدد الأدراج", self.dr_n),
            ("عرض الدرج", self.dr_w),
            ("عمق الدرج", self.dr_d),
        ]

        row = 0
        for label, widget in inputs:
            form.addWidget(QLabel(label), row, 0)
            form.addWidget(widget, row, 1)
            row += 1

        main_layout.addLayout(form)

        # =========================
        # BUTTONS
        # =========================
        self.calc_btn = QPushButton("💾 حساب")
        self.calc_btn.clicked.connect(self.calculate)

        self.invoice_btn = QPushButton("📋 الفاتورة")
        self.invoice_btn.clicked.connect(self.show_invoice)

        main_layout.addWidget(self.calc_btn)
        main_layout.addWidget(self.invoice_btn)

        # =========================
        # OUTPUT TABLE
        # =========================
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        central.setLayout(main_layout)

    # =========================
    # CONVERT
    # =========================
    def num(self, x):
        try:
            return float(x)
        except:
            return 0

    # =========================
    # CALCULATION
    # =========================
    def calculate(self):

        W = self.num(self.W.text())
        H = self.num(self.H.text())
        D = self.num(self.D.text())

        sh_n = int(self.num(self.sh_n.text()))
        sh_w = self.num(self.sh_w.text())
        sh_d = self.num(self.sh_d.text())

        v_n = int(self.num(self.v_n.text()))
        v_h = self.num(self.v_h.text())
        v_d = self.num(self.v_d.text())

        dr_n = int(self.num(self.dr_n.text()))
        dr_w = self.num(self.dr_w.text())
        dr_d = self.num(self.dr_d.text())

        unit = self.unit.currentText()

        if not W or not H or not D:
            QMessageBox.warning(self, "خطأ", "ادخل المقاسات")
            return

        Hf = H - (13 if unit == "وحدة سفلية" else 5)
        Wf = W - 5
        Df = D - 5

        alum = []
        fiber = []

        # =========================
        # MONTAL
        # =========================
        alum += [
            ("قائم", 2, "مفرد"),
            ("قائم", 2, "متقارب"),
            ("عرض", 3, "مفرد"),
            ("عرض", 2, "متقارب"),
        ]

        if sh_n > 0:
            alum.append(("رف", sh_n * 2, "مفرد"))
            fiber.append(("رف", sh_n))

        if v_n > 0:
            alum.append(("فاصل", v_n * 4, "مفرد"))
            fiber.append(("فاصل", v_n))

        if dr_n > 0:
            fiber.append(("درج", dr_n))

        fiber += [
            ("ضهرية", 1),
            ("أرضية", 1),
            ("أجناب", 2),
        ]

        self.projects.append({
            "client": self.client.text(),
            "unit": unit,
            "alum": alum,
            "fiber": fiber
        })

        QMessageBox.information(self, "نجاح", "تم الحساب بنجاح")

    # =========================
    # INVOICE TABLE
    # =========================
    def show_invoice(self):

        all_rows = []

        for p in self.projects:

            for a in p["alum"]:
                all_rows.append([p["client"], p["unit"], "مونتال", a[0], a[1], a[2]])

            for f in p["fiber"]:
                all_rows.append([p["client"], p["unit"], "فيبر", f[0], f[1], ""])

        self.table.setRowCount(len(all_rows))
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "العميل", "الوحدة", "القسم", "النوع", "العدد", "سعر الوحدة"
        ])

        for i, row in enumerate(all_rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


# =========================
# RUN APP
# =========================
app = QApplication(sys.argv)
window = DoggaSystem()
window.show()
sys.exit(app.exec())
