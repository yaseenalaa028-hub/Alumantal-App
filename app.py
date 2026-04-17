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
    # إدخال كامل بدون نقص
    # =========================
    df_input = pd.DataFrame([{
        "العميل": "",
        "نوع الوحدة": "",
        "العرض": "",
        "الارتفاع": "",
        "العمق": "",
        "عدد الأرفف": "",
        "عرض الرف": "",
        "عمق الرف": "",
        "عدد الفواصل": "",
        "ارتفاع الفاصل": "",
        "عمق الفاصل": "",
        "عدد الأدراج": "",
        "عرض الدرج": "",
        "عمق الدرج": ""
    }])

    edited = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

    if st.button("💾 حساب التخصيم"):

        for _, r in edited.iterrows():

            if r["العرض"] == "" or r["الارتفاع"] == "" or r["العمق"] == "":
                continue

            W = float(r["العرض"])
            H = float(r["الارتفاع"])
            D = float(r["العمق"])

            unit = r["نوع الوحدة"]

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
            sh = int(r["عدد الأرفف"] or 0)
            if sh > 0:
                alum.append(["رف", Wf, sh * 2, "مفرد"])
                fiber.append(["رف", Wf - 5, Df - 5, sh])

            # =========================
            # فواصل
            # =========================
            vf = int(r["عدد الفواصل"] or 0)
            if vf > 0:
                alum.append(["فاصل", Hf, vf * 4, "مفرد"])
                fiber.append(["فاصل", Hf - 5, Df - 5, vf])

            # =========================
            # أدراج
            # =========================
            dr = int(r["عدد الأدراج"] or 0)
            if dr > 0:
                dw = float(r["عرض الدرج"] or 0) - 2.5
                dh = float(r["عمق الدرج"] or 0)

                alum.append(["درج 2×8", dw, dr * 2, "2×8"])
                fiber.append(["درج", dw, dh, dr])

            # =========================
            # فيبر أساسي
            # =========================
            fiber += [
                ["ضهرية", Wf, Hf, 1],
                ["أرضية", Wf, Df, 1],
                ["أجناب", Hf, Df, 2],
            ]

            st.session_state.projects.append({
                "client": r["العميل"],
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
# INVOICE PAGE (VERTICAL FULL)
# =========================
elif st.session_state.page == "invoice":

    st.title("📋 الفاتورة التفصيلية")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    for p in st.session_state.projects:

        st.markdown("---")

        # =========================
        # العميل
        # =========================
        st.markdown(f"## 👤 العميل: {p['client']}")
        st.markdown(f"### 🏷️ نوع الوحدة: {p['unit']}")

        # =========================
        # مونتال (رأسي)
        # =========================
        st.markdown("## 🛠️ مونتال")

        for a in p["alum"]:
            st.markdown(
                f"""
                **▪ {a[0]}**
                - المقاس: `{round(a[1],2)}`
                - العدد: `{a[2]}`
                - النوع: مونتال
                ---
                """
            )

        # =========================
        # فيبر (رأسي)
        # =========================
        st.markdown("## 🪵 فيبر")

        for f in p["fiber"]:
            st.markdown(
                f"""
                **▪ {f[0]}**
                - المقاس: `{round(f[1],2)} × {round(f[2],2)}`
                - العدد: `{f[3]}`
                - النوع: فيبر
                ---
                """
            )

        st.markdown("### 💰 تم إنهاء وحدة بالكامل")
        st.success("تم حساب جميع الخامات بنجاح")

    st.markdown("---")
    st.success("📦 نهاية الفاتورة")
