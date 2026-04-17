import streamlit as st
import pandas as pd

# ==========================================
# إعداد التطبيق
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

if "extra_items" not in st.session_state:
    st.session_state.extra_items = []


# ==========================================
# الصفحة الرئيسية
# ==========================================
if st.session_state.page == "home":

    st.markdown("""
        <style>
        .stApp { background-color: white; color: black; }
        .center { text-align: center; margin-top: 10%; }
        .logo { font-size: 50px; font-weight: bold; color: #f1c40f; }
        .sub { font-size: 20px; margin-top: 10px; }
        .footer { font-size: 16px; color: gray; }
        </style>
    """)

    st.markdown("""
        <div class="center">
            <div class="logo">ضجة سمارت</div>
            <div class="sub">نحو دقة أعلى في شغل المطابخ 👌</div>
            <div class="footer">برمجة المهندس / ياسين علاء</div>
        </div>
    """)

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()


# ==========================================
# صفحة التخصيم
# ==========================================
elif st.session_state.page == "calc":

    st.title("🛠️ التخصيم")

    if st.button("🏠 رجوع"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # الإدخال
    # =========================
    with st.form("form"):

        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض", step=1.0, value=0.0, format="%.0f")
        H = d2.number_input("الارتفاع", step=1.0, value=0.0, format="%.0f")
        D = d3.number_input("العمق", step=1.0, value=0.0, format="%.0f")

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
    # الحساب
    # =========================
    if submit and W > 0 and H > 0 and D > 0:

        h_final = H - (13 if unit_type != "وحدة علوية" else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        if unit_type == "وحدة سفلية":
            alum += [
                ["ارتفاع", int(h_final), 2, "مفرد"],
                ["ارتفاع", int(h_final), 2, "متقارب"],
                ["عرض", int(w_final), 3, "مفرد"],
                ["عرض", int(w_final), 1, "متقارب"],
                ["عمق", int(d_final), 2, "مفرد"],
                ["عمق", int(d_final), 2, "متقارب"],
            ]
        else:
            alum += [
                ["ارتفاع", int(h_final), 2, "مفرد"],
                ["ارتفاع", int(h_final), 2, "متقارب"],
                ["عرض", int(w_final), 2, "مفرد"],
                ["عرض", int(w_final), 2, "متقارب"],
                ["عمق", int(d_final), 0, "مفرد"],
                ["عمق", int(d_final), 4, "متقارب"],
            ]

        if sh_n > 0:
            alum.append(["رف عرض", int(sh_w), sh_n * 2, "مفرد"])
            alum.append(["رف عمق", int(sh_d), sh_n * 2, "مفرد"])
            fiber.append(["رف", int(sh_w - 5), int(sh_d - 5), sh_n])

        if v_n > 0:
            alum.append(["فواصل ارتفاع", int(v_h), v_n * 4, "مفرد"])
            alum.append(["فواصل عمق", int(v_d), v_n * 4, "مفرد"])
            fiber.append(["فاصل", int(v_h - 5), int(v_d - 5), v_n])

        if dr_n > 0:
            drawer_w = dr_w - 2.5
            alum.append(["درج 2×8 عرض", int(drawer_w), dr_n * 2, "2×8"])
            alum.append(["درج 2×8 عمق", int(dr_d), dr_n * 2, "2×8"])
            fiber.append(["قاعدة درج 2×8", int(drawer_w), int(dr_d), dr_n])

        fiber += [
            ["ضهرية", int(w_final), int(h_final), 1],
            ["أرضية", int(w_final), int(d_final), 1],
            ["أجناب", int(h_final), int(d_final), 2],
        ]

        st.session_state.project_list.append({
            "client": client,
            "unit_type": unit_type,
            "alum": alum,
            "fiber": fiber
        })

    # =========================
    # الجرد
    # =========================
    if st.session_state.project_list:

        total_muf = 0
        total_mut = 0
        total_fiber = 0

        for unit in st.session_state.project_list:
            for a in unit["alum"]:
                if a[3] == "مفرد":
                    total_muf += a[1] * a[2]
                else:
                    total_mut += a[1] * a[2]

            for f in unit["fiber"]:
                total_fiber += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")

        st.write(f"🔹 المفرد: {total_muf / 600:.2f} عود")
        st.write(f"🔹 المتقارب: {total_mut / 600:.2f} عود")
        st.write(f"🔹 الفيبر: {total_fiber / (280 * 130):.2f} لوح")

        if st.button("🧾 فتح الفاتورة"):
            st.session_state.page = "invoice"
            st.rerun()


# ==========================================
# صفحة الفاتورة (Excel Style)
# ==========================================
elif st.session_state.page == "invoice":

    st.title("📋 فاتورة الخامات (Excel Style)")

    # حساب الخامات
    total_muf = 0
    total_mut = 0
    total_fiber = 0

    for unit in st.session_state.project_list:
        for a in unit["alum"]:
            if a[3] == "مفرد":
                total_muf += a[1] * a[2]
            else:
                total_mut += a[1] * a[2]

        for f in unit["fiber"]:
            total_fiber += f[1] * f[2] * f[3]

    muf = int(total_muf / 600)
    mut = int(total_mut / 600)
    fiber = int(total_fiber / (280 * 130))

    df = pd.DataFrame([
        ["مونتال مفرد", muf, 0.0],
        ["مونتال متقارب", mut, 0.0],
        ["فيبر", fiber, 0.0],
        ["درج 2×8", 0, 0.0],
    ], columns=["الصنف", "العدد", "سعر الوحدة"])

    st.markdown("## ➕ إضافة صنف جديد")

    c1, c2, c3 = st.columns(3)
    name = c1.text_input("الصنف")
    qty = c2.number_input("العدد", 0)
    price = c3.number_input("سعر الوحدة", 0.0)

    if st.button("إضافة"):
        df.loc[len(df)] = [name, qty, price]

    # Excel style edit
    df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    df["الإجمالي"] = df["العدد"] * df["سعر الوحدة"]

    st.markdown("## 📊 الفاتورة")
    st.table(df)

    st.markdown(f"## 💰 الإجمالي النهائي: {df['الإجمالي'].sum():.2f}")

    if st.button("⬅️ رجوع للتخصيم"):
        st.session_state.page = "calc"
        st.rerun()
