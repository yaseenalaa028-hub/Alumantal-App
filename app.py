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

if "invoice" not in st.session_state:
    st.session_state.invoice = []


# =========================
# CSS (واجهة شركات)
# =========================
st.markdown("""
<style>
.stApp { background-color: white; }

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
    margin-top:5px;
}

.center-btn {
    display:flex;
    justify-content:center;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown('<div class="logo">ضجة سمارت</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">نظام ERP لتخصيم المطابخ</div>', unsafe_allow_html=True)
    st.markdown('<div class="by">برمجة المهندس / ياسين علاء</div>', unsafe_allow_html=True)

    if st.button("🚀 بدء النظام", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()


# =========================
# CALC PAGE
# =========================
elif st.session_state.page == "calc":

    st.title("🛠️ نظام التخصيم")

    col1, col2 = st.columns(2)

    if col1.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    if col2.button("🗑️ حذف الكل"):
        st.session_state.projects = []
        st.rerun()

    # =========================
    # Excel Input (فاضي فعلياً)
    # =========================
    df_input = pd.DataFrame([{
        "العميل": "",
        "الوحدة": "",
        "عرض": "",
        "ارتفاع": "",
        "عمق": "",
        "أرفف": "",
        "فواصل": "",
        "أدراج": "",
        "عرض درج": "",
        "عمق درج": ""
    }])

    edited = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

    if st.button("💾 حفظ + حساب التخصيم"):

        for _, r in edited.iterrows():

            if r["عرض"] == "" or r["ارتفاع"] == "" or r["عمق"] == "":
                continue

            W = float(r["عرض"])
            H = float(r["ارتفاع"])
            D = float(r["عمق"])

            unit = r["الوحدة"]

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
            sh = int(r["أرفف"] or 0)
            if sh > 0:
                alum.append(["رف", Wf, sh * 2, "مفرد"])
                fiber.append(["رف", Wf - 5, Df - 5, sh])

            # =========================
            # فواصل
            # =========================
            vf = int(r["فواصل"] or 0)
            if vf > 0:
                alum.append(["فاصل", Hf, vf * 4, "مفرد"])
                fiber.append(["فاصل", Hf - 5, Df - 5, vf])

            # =========================
            # أدراج
            # =========================
            dr = int(r["أدراج"] or 0)
            if dr > 0:
                dw = float(r["عرض درج"] or 0) - 2.5
                dh = float(r["عمق درج"] or 0)

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

        st.success("تم الحفظ بنجاح")

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

        st.markdown("## 📊 الجرد")

        st.success(f"المفرد: {math.ceil(muf / 600)} عود")
        st.success(f"المتقارب: {math.ceil(mut / 600)} عود")
        st.success(f"الفيبر: {math.ceil(fib / (280*130))} لوح")

        if st.button("💰 فتح الفاتورة"):
            st.session_state.page = "invoice"
            st.rerun()


# =========================
# INVOICE PAGE
# =========================
elif st.session_state.page == "invoice":

    st.title("📋 الفاتورة النهائية (ERP)")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    rows = []

    for p in st.session_state.projects:
        for a in p["alum"]:
            rows.append({
                "الصنف": f"مونتال - {a[0]}",
                "العدد": a[2],
                "سعر الوحدة": 0.0
            })

        for f in p["fiber"]:
            rows.append({
                "الصنف": f"فيبر - {f[0]}",
                "العدد": f[3],
                "سعر الوحدة": 0.0
            })

    df = st.data_editor(pd.DataFrame(rows), num_rows="dynamic", use_container_width=True)

    df["الإجمالي"] = df["العدد"] * df["سعر الوحدة"]

    st.markdown("## 💰 الإجمالي النهائي")
    st.success(f"{df['الإجمالي'].sum():.2f} جنيه")
