import streamlit as st
import pandas as pd
import math

# ==========================================
# إعداد الصفحة
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

if 'project_list' not in st.session_state:
    st.session_state.project_list = []

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ==========================================
# الصفحة الرئيسية (بيضاء)
# ==========================================
if st.session_state.page == 'home':
    st.markdown("""
        <style>
        .stApp { background-color: white; color: black; }
        .center-box { text-align: center; margin-top: 10%; }
        .logo { font-size: 50px; font-weight: bold; color: #f1c40f; }
        .sub { font-size: 20px; margin-top: 10px; }
        .footer { font-size: 16px; color: gray; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="center-box">
            <div class="logo">ضجة سمارت</div>
            <div class="sub">نحو دقة أعلى في شغل المطابخ 👌</div>
            <div class="footer">برمجة المهندس / ياسين علاء</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = 'calc'
        st.rerun()

# ==========================================
# صفحة التخصيم
# ==========================================
else:
    st.title("🛠️ صفحة التخصيم")

    if st.button("🏠 رجوع"):
        st.session_state.page = 'home'
        st.rerun()

    # ==========================================
    # الفورم
    # ==========================================
    with st.form("form"):
        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض", value=0.0)
        H = d2.number_input("الارتفاع", value=0.0)
        D = d3.number_input("العمق", value=0.0)

        st.markdown("### الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", 0)
        sh_w = sh2.number_input("عرض الرف", 0.0)
        sh_d = sh3.number_input("عمق الرف", 0.0)

        st.markdown("### الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", 0)
        v_h = v2.number_input("ارتفاع الفاصل", 0.0)
        v_d = v3.number_input("عمق الفاصل", 0.0)

        st.markdown("### الأدراج (2×8)")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", 0)
        dr_w = dr2.number_input("عرض الدرج", 0.0)
        dr_d = dr3.number_input("عمق الدرج", 0.0)

        submit = st.form_submit_button("حساب")

    # ==========================================
    # الحساب
    # ==========================================
    if submit and W > 0 and H > 0 and D > 0:

        # التخصيم الأساسي
        if unit_type in ["وحدة سفلية", "دولاب خزين"]:
            h_final = H - 13
        else:
            h_final = H - 5

        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        # =============================
        # المونتال
        # =============================
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

        # =============================
        # الأرفف
        # =============================
        if sh_n > 0:
            alum.append(["أرفف عرض", sh_w, sh_n * 4, "مفرد"])
            alum.append(["أرفف عمق", sh_d, sh_n * 4, "مفرد"])

            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # =============================
        # الفواصل
        # =============================
        if v_n > 0:
            alum.append(["فواصل ارتفاع", v_h, v_n * 4, "مفرد"])
            alum.append(["فواصل عمق", v_d, v_n * 4, "مفرد"])

            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        # =============================
        # الأدراج (2×8)
        # =============================
        if dr_n > 0:
            drawer_w = dr_w - 2.5

            alum.append(["درج عرض", drawer_w, dr_n * 2, "مفرد"])
            alum.append(["درج عمق", dr_d, dr_n * 2, "مفرد"])

            fiber.append(["قاعدة درج", drawer_w, dr_d, dr_n])
            fiber.append(["جنب درج", 8, dr_d, dr_n * 2])

        # =============================
        # الفيبر الأساسي
        # =============================
        fiber += [
            ["ضهرية", w_final, h_final, 1],
            ["أرضية", w_final, d_final, 1],
            ["أجناب", h_final, d_final, 2]
        ]

        st.session_state.project_list.append({
            "client": client,
            "alum": alum,
            "fiber": fiber
        })

    # ==========================================
    # عرض البيانات
    # ==========================================
    if st.session_state.project_list:

        total_muf = total_mut = total_fiber = 0

        for unit in st.session_state.project_list:
            for a in unit["alum"]:
                if a[3] == "مفرد":
                    total_muf += a[1] * a[2]
                else:
                    total_mut += a[1] * a[2]

            for f in unit["fiber"]:
                total_fiber += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")

        st.write(f"🔹 المفرد: {total_muf/600:.2f} عود")
        st.write(f"🔹 المتقارب: {total_mut/600:.2f} عود")

        panel_area = 280 * 130
        st.write(f"🔹 الفيبر: {total_fiber/panel_area:.2f} لوح")

        st.markdown("## 📋 التفاصيل")

        for unit in st.session_state.project_list:
            st.write("### العميل:", unit["client"])
            st.table(pd.DataFrame(unit["alum"], columns=["البيان", "المقاس", "العدد", "النوع"]))
            st.table(pd.DataFrame(unit["fiber"], columns=["البيان", "العرض", "الارتفاع", "العدد"]))
