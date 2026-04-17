import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


# =========================
# MAIN APP
# =========================
class DoggaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DOGGA SMART SYSTEM")
        self.setGeometry(100, 100, 1000, 700)

        self.projects = []

        self.initUI()

    # =========================
    # UI
    # =========================
    def initUI(self):

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.layout = QVBoxLayout()

        title = QLabel("🛠️ DOGGA SMART SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:30px;font-weight:bold;color:#f1c40f;")

        self.layout.addWidget(title)

        form_layout = QGridLayout()

        # =========================
        # INPUTS
        # =========================
        self.client = QLineEdit()
        self.client.setPlaceholderText("اسم العميل")

        self.unit = QComboBox()
        self.unit.addItems(["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        self.W = QLineEdit()
        self.W.setPlaceholderText("العرض")

        self.H = QLineEdit()
        self.H.setPlaceholderText("الارتفاع")

        self.D = QLineEdit()
        self.D.setPlaceholderText("العمق")

        self.sh_n = QLineEdit()
        self.sh_n.setPlaceholderText("عدد الرفوف")

        self.sh_w = QLineEdit()
        self.sh_w.setPlaceholderText("عرض الرف")

        self.sh_d = QLineEdit()
        self.sh_d.setPlaceholderText("عمق الرف")

        self.v_n = QLineEdit()
        self.v_n.setPlaceholderText("عدد الفواصل")

        self.v_h = QLineEdit()
        self.v_h.setPlaceholderText("ارتفاع الفاصل")

        self.v_d = QLineEdit()
        self.v_d.setPlaceholderText("عمق الفاصل")

        self.dr_n = QLineEdit()
        self.dr_n.setPlaceholderText("عدد الأدراج")

        self.dr_w = QLineEdit()
        self.dr_w.setPlaceholderText("عرض الدرج")

        self.dr_d = QLineEdit()
        self.dr_d.setPlaceholderText("عمق الدرج")

        # =========================
        # ADD TO GRID
        # =========================
        form_layout.addWidget(QLabel("العميل"), 0, 0)
        form_layout.addWidget(self.client, 0, 1)

        form_layout.addWidget(QLabel("الوحدة"), 1, 0)
        form_layout.addWidget(self.unit, 1, 1)

        form_layout.addWidget(QLabel("العرض"), 2, 0)
        form_layout.addWidget(self.W, 2, 1)

        form_layout.addWidget(QLabel("الارتفاع"), 3, 0)
        form_layout.addWidget(self.H, 3, 1)

        form_layout.addWidget(QLabel("العمق"), 4, 0)
        form_layout.addWidget(self.D, 4, 1)

        form_layout.addWidget(QLabel("عدد الرفوف"), 5, 0)
        form_layout.addWidget(self.sh_n, 5, 1)

        form_layout.addWidget(QLabel("عرض الرف"), 6, 0)
        form_layout.addWidget(self.sh_w, 6, 1)

        form_layout.addWidget(QLabel("عمق الرف"), 7, 0)
        form_layout.addWidget(self.sh_d, 7, 1)

        form_layout.addWidget(QLabel("عدد الفواصل"), 8, 0)
        form_layout.addWidget(self.v_n, 8, 1)

        form_layout.addWidget(QLabel("ارتفاع الفاصل"), 9, 0)
        form_layout.addWidget(self.v_h, 9, 1)

        form_layout.addWidget(QLabel("عمق الفاصل"), 10, 0)
        form_layout.addWidget(self.v_d, 10, 1)

        form_layout.addWidget(QLabel("عدد الأدراج"), 11, 0)
        form_layout.addWidget(self.dr_n, 11, 1)

        form_layout.addWidget(QLabel("عرض الدرج"), 12, 0)
        form_layout.addWidget(self.dr_w, 12, 1)

        form_layout.addWidget(QLabel("عمق الدرج"), 13, 0)
        form_layout.addWidget(self.dr_d, 13, 1)

        self.layout.addLayout(form_layout)

        # =========================
        # BUTTONS
        # =========================
        self.calc_btn = QPushButton("💾 حساب")
        self.calc_btn.clicked.connect(self.calculate)

        self.invoice_btn = QPushButton("📋 الفاتورة")
        self.invoice_btn.clicked.connect(self.show_invoice)

        self.layout.addWidget(self.calc_btn)
        self.layout.addWidget(self.invoice_btn)

        # =========================
        # OUTPUT
        # =========================
        self.output = QTextEdit()
        self.layout.addWidget(self.output)

        self.central.setLayout(self.layout)

    # =========================
    # CONVERT
    # =========================
    def num(self, x):
        try:
            return float(x)
        except:
            return 0

    # =========================
    # CALCULATE
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
            self.output.setText("ادخل المقاسات")
            return

        Hf = H - (13 if unit == "وحدة سفلية" else 5)
        Wf = W - 5
        Df = D - 5

        alum = []
        fiber = []

        alum += [
            ("قائم", Hf, 2, "مفرد"),
            ("قائم", Hf, 2, "متقارب"),
            ("عرض", Wf, 3, "مفرد"),
            ("عرض", Wf, 2, "متقارب"),
            ("عمق", Df, 2, "مفرد"),
            ("عمق", Df, 2, "متقارب"),
        ]

        if sh_n > 0:
            alum.append(("رف", Wf, sh_n * 2, "مفرد"))
            fiber.append(("رف", Wf - 5, Df - 5, sh_n))

        if v_n > 0:
            alum.append(("فاصل", Hf, v_n * 4, "مفرد"))
            fiber.append(("فاصل", Hf - 5, Df - 5, v_n))

        if dr_n > 0:
            fiber.append(("درج", dr_w, dr_d, dr_n))

        fiber += [
            ("ضهرية", Wf, Hf, 1),
            ("أرضية", Wf, Df, 1),
            ("أجناب", Hf, Df, 2),
        ]

        self.projects.append({
            "client": self.client.text(),
            "unit": unit,
            "alum": alum,
            "fiber": fiber
        })

        self.output.setText("تم الحساب بنجاح ✅")

    # =========================
    # INVOICE
    # =========================
    def show_invoice(self):

        text = ""

        for p in self.projects:
            text += f"\n👤 {p['client']} - {p['unit']}\n"

            text += "\n-- مونتال --\n"
            for a in p["alum"]:
                text += str(a) + "\n"

            text += "\n-- فيبر --\n"
            for f in p["fiber"]:
                text += str(f) + "\n"

            text += "\n----------------------\n"

        self.output.setText(text)


# =========================
# RUN
# =========================
app = QApplication(sys.argv)
window = DoggaApp()
window.show()
sys.exit(app.exec_())
