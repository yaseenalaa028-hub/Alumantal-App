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
    # الإدخال (عشري)
    # =========================
    with st.form("form"):

        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)

        W = d1.number_input("العرض", step=0.5, value=0.0, format="%.2f")
        H = d2.number_input("الارتفاع", step=0.5, value=0.0, format="%.2f")
        D = d3.number_input("العمق", step=0.5, value=0.0, format="%.2f")

        st.markdown("### الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", 0)
        sh_w = sh2.number_input("عرض الرف", step=0.5, value=0.0, format="%.2f")
        sh_d = sh3.number_input("عمق الرف", step=0.5, value=0.0, format="%.2f")

        st.markdown("### الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", 0)
        v_h = v2.number_input("ارتفاع الفاصل", step=0.5, value=0.0, format="%.2f")
        v_d = v3.number_input("عمق الفاصل", step=0.5, value=0.0, format="%.2f")

        st.markdown("### الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", 0)
        dr_w = dr2.number_input("عرض الدرج", step=0.5, value=0.0, format="%.2f")
        dr_d = dr3.number_input("عمق الدرج", step=0.5, value=0.0, format="%.2f")

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

        # مونتال
        if unit_type == "وحدة سفلية":
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"],
                ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 3, "مفرد"],
                ["عرض", w_final, 1, "متقارب"],
                ["عمق", d_final, 2, "مفرد"],
                ["عمق", d_final, 2, "متقارب"],
            ]
        else:
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"],
                ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 2, "مفرد"],
                ["عرض", w_final, 2, "متقارب"],
                ["عمق", d_final, 0, "مفرد"],
                ["عمق", d_final, 4, "متقارب"],
            ]

        # أرفف
        if sh_n > 0:
            alum.append(["رف", sh_w, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # فواصل
        if v_n > 0:
            alum.append(["فاصل", v_h, v_n * 4, "مفرد"])
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        # أدراج
        if dr_n > 0:
            drawer_w = dr_w - 2.5
            alum.append(["درج 2×8", drawer_w, dr_n * 2, "2×8"])
            fiber.append(["درج", drawer_w, dr_d, dr_n])

        # فيبر أساسي
        fiber += [
            ["ضهرية", w_final, h_final, 1],
            ["أرضية", w_final, d_final, 1],
            ["أجناب", h_final, d_final, 2],
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
# صفحة الفاتورة (Excel)
# ==========================================
elif st.session_state.page == "invoice":

    st.title("📋 فاتورة الخامات (Excel Style)")

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

    df = pd.DataFrame([
        ["مونتال مفرد", total_muf / 600, 0.0],
        ["مونتال متقارب", total_mut / 600, 0.0],
        ["فيبر", total_fiber / (280 * 130), 0.0],
        ["درج 2×8", 0, 0.0],
    ], columns=["الصنف", "العدد", "سعر الوحدة"])

    st.markdown("## ➕ إضافة صنف جديد")

    c1, c2, c3 = st.columns(3)
    name = c1.text_input("الصنف")
    qty = c2.number_input("العدد", 0)
    price = c3.number_input("سعر الوحدة", 0.0)

    if st.button("إضافة"):
        df.loc[len(df)] = [name, qty, price]

    # Excel editor
    df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    df["الإجمالي"] = df["العدد"] * df["سعر الوحدة"]

    st.table(df)

    st.markdown(f"## 💰 الإجمالي النهائي: {df['الإجمالي'].sum():.2f}")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()
