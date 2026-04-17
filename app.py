import streamlit as st
import pandas as pd
import math

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="DOGGA SMART ERP", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

if "projects" not in st.session_state:
    st.session_state.projects = []


# =========================
# HOME PAGE
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <style>
    .logo {
        text-align:center;
        font-size:70px;
        font-weight:bold;
        color:#f1c40f;
        margin-top:8%;
    }
    .sub {
        text-align:center;
        font-size:22px;
        margin-top:10px;
    }
    .by {
        text-align:center;
        color:gray;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="logo">ضجة سمارت ERP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">نظام تخصيم المطابخ الاحترافي</div>', unsafe_allow_html=True)
    st.markdown('<div class="by">برمجة المهندس / ياسين علاء</div>', unsafe_allow_html=True)

    if st.button("🚀 بدء النظام", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()


# =========================
# CALC PAGE
# =========================
elif st.session_state.page == "calc":

    st.title("🛠️ شاشة التخصيم")

    if st.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # إدخال كامل بدون Excel
    # =========================
    client = st.text_input("اسم العميل")
    unit = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

    W = st.number_input("العرض", value=None)
    H = st.number_input("الارتفاع", value=None)
    D = st.number_input("العمق", value=None)

    sh = st.number_input("عدد الأرفف", value=0)
    sh_w = st.number_input("عرض الرف", value=0.0)
    sh_d = st.number_input("عمق الرف", value=0.0)

    vf = st.number_input("عدد الفواصل", value=0)
    vf_h = st.number_input("ارتفاع الفاصل", value=0.0)
    vf_d = st.number_input("عمق الفاصل", value=0.0)

    dr = st.number_input("عدد الأدراج", value=0)
    dr_w = st.number_input("عرض الدرج", value=0.0)
    dr_d = st.number_input("عمق الدرج", value=0.0)

    if st.button("💾 حساب التخصيم"):

        if W and H and D:

            # =========================
            # خصم المقاسات
            # =========================
            if unit == "وحدة سفلية":
                Hf = H - 13
            else:
                Hf = H - 5

            Wf = W - 5
            Df = D - 5

            alum = []
            fiber = []

            # =========================
            # مونتال
            # =========================
            alum += [
                ["قائم", Hf, 2, "مفرد"],
                ["قائم", Hf, 2, "متقارب"],
                ["عرض", Wf, 3, "مفرد"],
                ["عرض", Wf, 2, "متقارب"],
                ["عمق", Df, 2, "مفرد"],
                ["عمق", Df, 2, "متقارب"],
            ]

            # =========================
            # أرفف
            # =========================
            if sh > 0:
                alum.append(["رف", Wf, sh * 2, "مفرد"])
                fiber.append(["رف", Wf - 5, Df - 5, sh])

            # =========================
            # فواصل
            # =========================
            if vf > 0:
                alum.append(["فاصل", Hf, vf * 4, "مفرد"])
                fiber.append(["فاصل", Hf - 5, Df - 5, vf])

            # =========================
            # أدراج
            # =========================
            if dr > 0:
                dw = dr_w - 2.5
                fiber.append(["درج", dw, dr_d, dr])

            # =========================
            # فيبر أساسي
            # =========================
            fiber += [
                ["ضهرية", Wf, Hf, 1],
                ["أرضية", Wf, Df, 1],
                ["أجناب", Hf, Df, 2],
            ]

            st.session_state.projects.append({
                "client": client,
                "unit": unit,
                "alum": alum,
                "fiber": fiber
            })

            st.success("تم الحساب بنجاح")

    # =========================
    # جرد الخامات
    # =========================
    if st.session_state.projects:

        muf = mut = fib = 0

        for p in st.session_state.projects:
            for a in p["alum"]:
                if a[3] == "مفرد":
                    muf += a[1] * a[2]
                else:
                    mut += a[1] * a[2]

            for f in p["fiber"]:
                fib += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")

        st.success(f"المفرد: {math.ceil(muf / 600)} عود")
        st.success(f"المتقارب: {math.ceil(mut / 600)} عود")
        st.success(f"الفيبر: {math.ceil(fib / (280*130))} لوح")

        if st.button("💰 الفاتورة"):
            st.session_state.page = "invoice"
            st.rerun()


# =========================
# INVOICE PAGE (CARDS ONLY)
# =========================
elif st.session_state.page == "invoice":

    st.title("📋 الفاتورة النهائية")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    for p in st.session_state.projects:

        st.markdown("---")

        st.markdown(f"## 👤 العميل: {p['client']}")
        st.markdown(f"### 🏷️ نوع الوحدة: {p['unit']}")

        st.markdown("## 🛠️ مونتال")

        for a in p["alum"]:
            st.markdown(f"""
            <div style="
                border:1px solid #ddd;
                padding:10px;
                border-radius:10px;
                margin-bottom:10px;
                background:#f9f9f9;
            ">
                <b>▪ {a[0]}</b><br>
                المقاس: {round(a[1],2)}<br>
                العدد: {a[2]}<br>
                النوع: مونتال
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 🪵 فيبر")

        for f in p["fiber"]:
            st.markdown(f"""
            <div style="
                border:1px solid #ddd;
                padding:10px;
                border-radius:10px;
                margin-bottom:10px;
                background:#f1f1f1;
            ">
                <b>▪ {f[0]}</b><br>
                المقاس: {round(f[1],2)} × {round(f[2],2)}<br>
                العدد: {f[3]}<br>
                النوع: فيبر
            </div>
            """, unsafe_allow_html=True)

        st.success("تم حساب الوحدة بالكامل")

    st.markdown("---")
    st.success("📦 نهاية الفاتورة")
