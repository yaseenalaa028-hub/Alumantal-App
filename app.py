import streamlit as st
import pandas as pd
import math

# =========================
# إعداد التطبيق
# =========================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

if "show_price" not in st.session_state:
    st.session_state.show_price = False


# =========================
# تحويل آمن
# =========================
def num(x):
    try:
        return float(x) if x != "" else 0
    except:
        return 0


# =========================
# الصفحة الرئيسية
# =========================
if st.session_state.page == "home":

    st.markdown("""
        <style>
        .stApp { background-color: white; color: black; }
        .center { text-align: center; margin-top: 10%; }
        .logo { font-size: 50px; font-weight: bold; color: #f1c40f; }
        .sub { font-size: 20px; margin-top: 10px; }
        .footer { font-size: 16px; color: gray; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="center">
            <div class="logo">ضجة سمارت</div>
            <div class="sub">نحو دقة أعلى في شغل المطابخ 👌</div>
            <div class="footer">برمجة المهندس / ياسين علاء</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()


# =========================
# صفحة التخصيم
# =========================
else:

    st.title("🛠️ التخصيم")

    if st.button("🏠 رجوع"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # الإدخال (فاضي بدون 0.00)
    # =========================
    with st.form("form"):

        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)
        W = d1.text_input("العرض")
        H = d2.text_input("الارتفاع")
        D = d3.text_input("العمق")

        st.markdown("### 🪵 الرفوف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.text_input("عدد الرفوف")
        sh_w = sh2.text_input("عرض الرف")
        sh_d = sh3.text_input("عمق الرف")

        st.markdown("### 🧱 الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.text_input("عدد الفواصل")
        v_h = v2.text_input("ارتفاع الفاصل")
        v_d = v3.text_input("عمق الفاصل")

        st.markdown("### 🧰 الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.text_input("عدد الأدراج")
        dr_w = dr2.text_input("عرض الدرج")
        dr_d = dr3.text_input("عمق الدرج")

        submit = st.form_submit_button("حساب")


    # =========================
    # الحساب
    # =========================
    if submit:

        W = num(W)
        H = num(H)
        D = num(D)

        sh_n = int(num(sh_n))
        sh_w = num(sh_w)
        sh_d = num(sh_d)

        v_n = int(num(v_n))
        v_h = num(v_h)
        v_d = num(v_d)

        dr_n = int(num(dr_n))
        dr_w = num(dr_w)
        dr_d = num(dr_d)

        if W and H and D:

            h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
            w_final = W - 5
            d_final = D - 5

            alum = []
            fiber = []

            # =========================
            # مونتال
            # =========================
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

            # =========================
            # رفوف
            # =========================
            if sh_n > 0:
                alum.append(["رف", w_final, sh_n * 2, "مفرد"])
                fiber.append(["رف", w_final - 5, d_final - 5, sh_n])

            # =========================
            # فواصل
            # =========================
            if v_n > 0:
                alum.append(["فواصل", h_final, v_n * 4, "مفرد"])
                fiber.append(["فواصل", h_final - 5, d_final - 5, v_n])

            # =========================
            # أدراج
            # =========================
            if dr_n > 0:
                dw = dr_w - 2.5
                fiber.append(["درج 2×8", dw, dr_d, dr_n])

            # =========================
            # فيبر
            # =========================
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

            st.success("تم الحساب بنجاح")


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

        st.write(f"🔹 المفرد: {math.ceil(total_muf / 600)} عود")
        st.write(f"🔹 المتقارب: {math.ceil(total_mut / 600)} عود")

        panel_area = 280 * 130
        st.write(f"🔹 الفيبر: {math.ceil(total_fiber / panel_area)} لوح")


    # =========================
    # التفاصيل
    # =========================
    if st.session_state.project_list:

        st.markdown("## 📋 التفاصيل")

        for unit in st.session_state.project_list:

            st.write(f"### {unit['client']} - {unit['unit_type']}")

            st.table(pd.DataFrame(unit["alum"]))
            st.table(pd.DataFrame(unit["fiber"]))
