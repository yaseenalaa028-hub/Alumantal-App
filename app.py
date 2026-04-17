import streamlit as st
import pandas as pd
import math

# ==========================================
# إعداد التطبيق
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

page = st.session_state.page


# ==========================================
# إخفاء شكل الـ 0 (حل بصري)
# ==========================================
st.markdown("""
<style>
input[type="number"] {
    color: black;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# الصفحة الرئيسية
# ==========================================
if page == "home":

    st.markdown("""
    <style>
    .logo-box {
        text-align:center;
        margin-top:10%;
    }

    .logo {
        font-size:75px;
        font-weight:bold;
        color:#f1c40f;
    }

    .sub {
        font-size:22px;
        margin-top:10px;
    }

    .footer {
        color:gray;
        margin-top:10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="logo-box">
            <div class="logo">⚡ ضجة سيستم</div>
            <div class="sub">نظام التخصيم الذكي للمطابخ</div>
            <div class="footer">برمجة المهندس / ياسين علاء</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()


# ==========================================
# صفحة التخصيم
# ==========================================
elif page == "calc":

    st.title("🛠️ التخصيم الكامل")

    c1, c2 = st.columns(2)

    if c1.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    if c2.button("🗑️ حذف الكل"):
        st.session_state.project_list = []
        st.rerun()

    # ==========================================
    # الإدخال (بدون 0 ظاهر)
    # ==========================================
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

        st.markdown("### الأدراج 2×8")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", 0)
        dr_w = dr2.number_input("عرض الدرج", step=0.5, value=0.0, format="%.2f")
        dr_d = dr3.number_input("عمق الدرج", step=0.5, value=0.0, format="%.2f")

        submit = st.form_submit_button("حساب")

    # ==========================================
    # تحويل 0 → None (إخفاء منطقي)
    # ==========================================
    def clean(x):
        return x if x and x > 0 else None

    W = clean(W)
    H = clean(H)
    D = clean(D)

    # ==========================================
    # الحساب
    # ==========================================
    if submit:

        if not W or not H or not D:
            st.error("من فضلك أدخل المقاسات الأساسية")
            st.stop()

        if unit_type == "وحدة سفلية":
            h_final = H - 13
        else:
            h_final = H - 5

        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        # المونتال
        if unit_type == "وحدة سفلية":
            alum += [
                ["قائم", h_final, 2, "مفرد"],
                ["قائم", h_final, 2, "متقارب"],
                ["عرض", w_final, 3, "مفرد"],
                ["عرض", w_final, 1, "متقارب"],
                ["عمق", d_final, 2, "مفرد"],
                ["عمق", d_final, 2, "متقارب"],
            ]
        else:
            alum += [
                ["قائم", h_final, 2, "مفرد"],
                ["قائم", h_final, 2, "متقارب"],
                ["عرض", w_final, 2, "مفرد"],
                ["عرض", w_final, 2, "متقارب"],
                ["عمق", d_final, 0, "مفرد"],
                ["عمق", d_final, 4, "متقارب"],
            ]

        # الأرفف
        if sh_n > 0:
            alum.append(["رف", sh_w, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # الفواصل
        if v_n > 0:
            alum.append(["فاصل", v_h, v_n * 4, "مفرد"])
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        # الأدراج
        if dr_n > 0:
            drawer_w = dr_w - 2.5
            alum.append(["درج 2×8", drawer_w, dr_n * 2, "2×8"])
            fiber.append(["درج", drawer_w, dr_d, dr_n])

        # الفيبر الأساسي
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

    # ==========================================
    # الجرد
    # ==========================================
    if st.session_state.project_list:

        muf = 0
        mut = 0
        fib = 0

        for u in st.session_state.project_list:
            for a in u["alum"]:
                if a[3] == "مفرد":
                    muf += a[1] * a[2]
                else:
                    mut += a[1] * a[2]

            for f in u["fiber"]:
                fib += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")

        st.success(f"المفرد: {math.ceil(muf / 600)} عود")
        st.success(f"المتقارب: {math.ceil(mut / 600)} عود")

        panel = 280 * 130
        st.success(f"الفيبر: {math.ceil(fib / panel)} لوح")

        if st.button("💰 الفاتورة"):
            st.session_state.page = "invoice"
            st.rerun()


# ==========================================
# صفحة الفاتورة
# ==========================================
elif page == "invoice":

    st.title("📋 الفاتورة النهائية")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    rows = []

    for u in st.session_state.project_list:
        for a in u["alum"]:
            rows.append({
                "الصنف": f"مونتال - {a[0]}",
                "العدد": a[2],
                "سعر الوحدة": 0.0
            })

        for f in u["fiber"]:
            rows.append({
                "الصنف": f"فيبر - {f[0]}",
                "العدد": f[3],
                "سعر الوحدة": 0.0
            })

    df = pd.DataFrame(rows)

    df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    df["الإجمالي"] = df["العدد"] * df["سعر الوحدة"]

    st.table(df)

    st.markdown(f"## 💰 الإجمالي النهائي: {df['الإجمالي'].sum():.2f}")
