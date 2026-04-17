import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


# =========================
# MAIN APP
# =========================
class DoggaSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DOGGA SMART SYSTEM")
        self.setGeometry(100, 100, 1200, 700)

        self.projects = []

        self.build_ui()

    # =========================
    # UI
    # =========================
    def build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        # =========================
        # TITLE
        # =========================
        title = QLabel("🛠️ DOGGA SMART SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px;font-weight:bold;color:#f1c40f;")
        layout.addWidget(title)

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

        fields = [
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
        for name, widget in fields:
            form.addWidget(QLabel(name), row, 0)
            form.addWidget(widget, row, 1)
            row += 1

        layout.addLayout(form)

        # =========================
        # BUTTONS
        # =========================
        self.add_btn = QPushButton("➕ إضافة مشروع")
        self.add_btn.clicked.connect(self.add_project)

        self.invoice_btn = QPushButton("📋 عرض الفاتورة")
        self.invoice_btn.clicked.connect(self.show_invoice)

        layout.addWidget(self.add_btn)
        layout.addWidget(self.invoice_btn)

        # =========================
        # TABLE
        # =========================
        self.table = QTableWidget()
        layout.addWidget(self.table)

        central.setLayout(layout)

    # =========================
    # CONVERT NUMBER
    # =========================
    def num(self, x):
        try:
            return float(x)
        except:
            return 0

    # =========================
    # ADD PROJECT
    # =========================
    def add_project(self):

        W = self.num(self.W.text())
        H = self.num(self.H.text())
        D = self.num(self.D.text())

        if W == 0 or H == 0 or D == 0:
            QMessageBox.warning(self, "خطأ", "ادخل المقاسات")
            return

        unit = self.unit.currentText()

        Hf = H - (13 if unit == "وحدة سفلية" else 5)
        Wf = W - 5
        Df = D - 5

        sh_n = int(self.num(self.sh_n.text()))
        v_n = int(self.num(self.v_n.text()))
        dr_n = int(self.num(self.dr_n.text()))

        alum = []
        fiber = []

        # =========================
        # MONTAGE
        # =========================
        alum += [
            ("قائم", 2, "مفرد"),
            ("عرض", 3, "مفرد"),
            ("عمق", 2, "مفرد"),
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

        QMessageBox.information(self, "تم", "تم إضافة المشروع")

    # =========================
    # SHOW INVOICE
    # =========================
    def show_invoice(self):

        rows = []

        for p in self.projects:

            for a in p["alum"]:
                rows.append([
                    p["client"],
                    p["unit"],
                    "مونتال",
                    a[0],
                    a[1],
                    ""
                ])

            for f in p["fiber"]:
                rows.append([
                    p["client"],
                    p["unit"],
                    "فيبر",
                    f[0],
                    f[1],
                    ""
                ])

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "العميل", "الوحدة", "القسم", "النوع", "العدد", "سعر الوحدة"
        ])

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


# =========================
# RUN APP
# =========================
app = QApplication(sys.argv)
window = DoggaSystem()
window.show()
sys.exit(app.exec())
