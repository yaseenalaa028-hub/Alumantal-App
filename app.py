import streamlit as st
import pandas as pd

st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# ==============================
# Session
# ==============================
if "data" not in st.session_state:
    st.session_state.data = []

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==============================
# الصفحة الرئيسية
# ==============================
if st.session_state.page == "home":

    st.markdown("<h1 style='text-align:center'>🔥 DOGGA SMART SYSTEM</h1>", unsafe_allow_html=True)

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# ==============================
# صفحة التخصيم
# ==============================
elif st.session_state.page == "calc":

    st.title("🛠️ التخصيم")

    if st.button("📊 عرض الجرد والفاتورة"):
        st.session_state.page = "report"
        st.rerun()

    with st.form("form"):

        name = st.text_input("اسم الوحدة")
        unit_type = st.selectbox("النوع", ["سفلية", "علوية", "دولاب خزين"])

        c1, c2, c3 = st.columns(3)
        w = c1.number_input("عرض", 0.0)
        h = c2.number_input("ارتفاع", 0.0)
        d = c3.number_input("عمق", 0.0)

        st.markdown("### الأرفف")
        sh_n = st.number_input("عدد الأرفف", 0)
        sh_w = st.number_input("عرض الرف", 0.0)
        sh_d = st.number_input("عمق الرف", 0.0)

        st.markdown("### الفواصل")
        dv_n = st.number_input("عدد الفواصل", 0)
        dv_h = st.number_input("ارتفاع الفاصل", 0.0)
        dv_d = st.number_input("عمق الفاصل", 0.0)

        st.markdown("### الأدراج")
        dr_n = st.number_input("عدد الأدراج", 0)
        dr_w = st.number_input("عرض الدرج", 0.0)
        dr_d = st.number_input("عمق الدرج", 0.0)

        submit = st.form_submit_button("💾 إضافة")

    if submit:

        h_b = h - 13 if unit_type in ["سفلية", "دولاب خزين"] else h - 5
        w_b = w - 5
        d_b = d - 5

        alum = []
        fiber = []

        # مونتال
        if unit_type == "سفلية":
            alum += [
                ["ارتفاع", h_b, 2, "مفرد"],
                ["ارتفاع", h_b, 2, "متقارب"],
                ["عرض", w_b, 3, "مفرد"],
                ["عرض", w_b, 1, "متقارب"],
                ["عمق", d_b, 2, "مفرد"],
                ["عمق", d_b, 2, "متقارب"],
            ]
        else:
            alum += [
                ["ارتفاع", h_b, 2, "مفرد"],
                ["ارتفاع", h_b, 2, "متقارب"],
                ["عرض", w_b, 2, "مفرد"],
                ["عرض", w_b, 2, "متقارب"],
                ["عمق", d_b, 4, "متقارب"],
            ]

        # رفوف
        if sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # فواصل
        if dv_n > 0:
            alum.append(["فاصل ارتفاع", dv_h, dv_n * 2, "مفرد"])
            alum.append(["فاصل عمق", dv_d, dv_n * 2, "مفرد"])
            fiber.append(["فاصل", dv_h - 5, dv_d - 5, dv_n])

        # أدراج
        if dr_n > 0:
            alum.append(["درج عرض", dr_w - 2.5, dr_n * 2, "2×8"])
            alum.append(["درج عمق", dr_d, dr_n * 2, "2×8"])

        # فيبر أساسي
        fiber += [
            ["ضهرية", w_b, h_b, 1],
            ["أرضية", w_b, d_b, 1],
            ["جنب", h_b, d_b, 2],
        ]

        st.session_state.data.append({
            "name": name,
            "type": unit_type,
            "alum": alum,
            "fiber": fiber
        })

        st.success("تمت الإضافة ✅")

# ==============================
# صفحة الجرد والفاتورة
# ==============================
elif st.session_state.page == "report":

    st.title("📊 الجرد + 💰 الفاتورة")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    rows = []

    for unit in st.session_state.data:
        for a in unit["alum"]:
            rows.append({
                "الوحدة": unit["name"],
                "النوع": f"مونتال - {a[0]}",
                "المقاس": a[1],
                "العدد": a[2],
                "سعر": 0
            })

        for f in unit["fiber"]:
            rows.append({
                "الوحدة": unit["name"],
                "النوع": f"فيبر - {f[0]}",
                "المقاس": f"{f[1]}x{f[2]}",
                "العدد": f[3],
                "سعر": 0
            })

    df = pd.DataFrame(rows)

    for i in range(len(df)):
        df.at[i, "سعر"] = st.number_input(
            f"سعر {df.iloc[i]['النوع']} - {i}",
            value=0.0,
            key=f"p{i}"
        )

    df["الإجمالي"] = df["العدد"] * df["سعر"]

    st.dataframe(df)

    total = df["الإجمالي"].sum()
    st.markdown(f"## 💰 الإجمالي: {total:.2f}")

    # تحميل Excel
    file = "invoice.xlsx"
    df.to_excel(file, index=False)

    with open(file, "rb") as f:
        st.download_button("📥 تحميل Excel", f, file_name="invoice.xlsx")
