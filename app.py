import streamlit as st
import pandas as pd

st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# =========================
# SESSION
# =========================
if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "show_price" not in st.session_state:
    st.session_state.show_price = False

# =========================
# UI
# =========================
st.title("🛠️ DOGGA SMART SYSTEM")

# =========================
# INPUT
# =========================
with st.form("form"):

    client = st.text_input("اسم العميل")
    unit_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

    W = st.number_input("العرض", step=1.0, value=0.0, format="%.0f")
    H = st.number_input("الارتفاع", step=1.0, value=0.0, format="%.0f")
    D = st.number_input("العمق", step=1.0, value=0.0, format="%.0f")

    sh_n = st.number_input("عدد الأرفف", 0)
    sh_w = st.number_input("عرض الرف", step=1.0, value=0.0, format="%.0f")
    sh_d = st.number_input("عمق الرف", step=1.0, value=0.0, format="%.0f")

    v_n = st.number_input("عدد الفواصل", 0)
    v_h = st.number_input("ارتفاع الفاصل", step=1.0, value=0.0, format="%.0f")
    v_d = st.number_input("عمق الفاصل", step=1.0, value=0.0, format="%.0f")

    dr_n = st.number_input("عدد الأدراج 2×8", 0)
    dr_w = st.number_input("عرض الدرج", step=1.0, value=0.0, format="%.0f")
    dr_d = st.number_input("عمق الدرج", step=1.0, value=0.0, format="%.0f")

    submit = st.form_submit_button("حساب")

# =========================
# CALCULATION
# =========================
if submit and W > 0 and H > 0 and D > 0:

    # خصم ثابت
    h_final = H - (13 if unit_type != "وحدة علوية" else 5)
    w_final = W - 5
    d_final = D - 5

    alum = []
    fiber = []

    # =========================
    # MONTAL
    # =========================
    if unit_type == "وحدة سفلية":
        alum += [
            ["قائم", int(h_final), 2, "مفرد"],
            ["قائم", int(h_final), 2, "متقارب"],
            ["عارض", int(w_final), 3, "مفرد"],
            ["عارض", int(w_final), 1, "متقارب"],
            ["عمق", int(d_final), 2, "مفرد"],
            ["عمق", int(d_final), 2, "متقارب"],
        ]
    else:
        alum += [
            ["قائم", int(h_final), 2, "مفرد"],
            ["قائم", int(h_final), 2, "متقارب"],
            ["عارض", int(w_final), 2, "مفرد"],
            ["عارض", int(w_final), 2, "متقارب"],
            ["عمق", int(d_final), 0, "مفرد"],
            ["عمق", int(d_final), 4, "متقارب"],
        ]

    # =========================
    # SHELVES
    # =========================
    if sh_n > 0:
        alum.append(["رف", int(sh_w), sh_n * 2, "مفرد"])
        alum.append(["رف", int(sh_d), sh_n * 2, "مفرد"])
        fiber.append(["رف", int(sh_w - 5), int(sh_d - 5), sh_n])

    # =========================
    # DIVIDERS
    # =========================
    if v_n > 0:
        alum.append(["فاصل", int(v_h), v_n * 4, "مفرد"])
        alum.append(["فاصل", int(v_d), v_n * 4, "مفرد"])
        fiber.append(["فاصل", int(v_h - 5), int(v_d - 5), v_n])

    # =========================
    # DRAWERS 2×8
    # =========================
    if dr_n > 0:
        dw = dr_w - 2.5
        alum.append(["درج 2×8", int(dw), dr_n * 2, "2×8"])
        alum.append(["درج 2×8", int(dr_d), dr_n * 2, "2×8"])
        fiber.append(["قاعدة درج 2×8", int(dw), int(dr_d), dr_n])

    # =========================
    # FIBER BASIC
    # =========================
    fiber += [
        ["ضهرية", int(w_final), int(h_final), 1],
        ["أرضية", int(w_final), int(d_final), 1],
        ["أجناب", int(h_final), int(d_final), 2],
    ]

    st.session_state.project_list.append({
        "client": client,
        "unit": unit_type,
        "alum": alum,
        "fiber": fiber
    })

# =========================
# DISPLAY + INVENTORY
# =========================
if st.session_state.project_list:

    st.markdown("## 📊 الجرد")

    total_m = 0
    total_mt = 0
    total_f = 0

    for u in st.session_state.project_list:
        for a in u["alum"]:
            if a[3] == "مفرد":
                total_m += a[1] * a[2]
            else:
                total_mt += a[1] * a[2]

        for f in u["fiber"]:
            total_f += f[1] * f[2] * f[3]

    st.write("🔹 مفرد:", total_m / 600)
    st.write("🔹 متقارب:", total_mt / 600)
    st.write("🔹 فيبر:", total_f / (280 * 130))

    # =========================
    # INVOICE
    # =========================
    st.markdown("## 💰 الفاتورة")

    rows = []

    for u in st.session_state.project_list:

        for a in u["alum"]:
            rows.append({
                "القسم": "مونتال",
                "النوع": a[0],
                "العدد": a[2],
                "سعر": 0
            })

        for f in u["fiber"]:
            rows.append({
                "القسم": "فيبر",
                "النوع": f[0],
                "العدد": f[3],
                "سعر": 0
            })

    df = pd.DataFrame(rows)

    prices = []

    for i in range(len(df)):
        p = st.number_input(
            f"{df.iloc[i]['القسم']} - {df.iloc[i]['النوع']}",
            value=0.0,
            key=f"p_{i}"
        )
        prices.append(p)

    df["سعر الوحدة"] = prices
    df["الإجمالي"] = df["العدد"] * df["سعر الوحدة"]

    st.table(df)

    st.markdown(f"## 💰 الإجمالي: {df['الإجمالي'].sum():.2f}")

    # =========================
    # RESET
    # =========================
    if st.button("🗑️ مشروع جديد"):
        st.session_state.project_list = []
        st.rerun()
