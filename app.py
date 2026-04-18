import streamlit as st
import pandas as pd

# -------------------------
# إعداد الصفحة
# -------------------------
st.set_page_config(page_title="Kitchen Pro ERP", layout="wide")

# -------------------------
# CSS احترافي
# -------------------------
st.markdown("""
<style>
body {
    font-family: 'Cairo', sans-serif;
}

.main-box {
    text-align: center;
    padding: 60px;
    background: linear-gradient(90deg,#1e272e,#2c3e50);
    color: white;
    border-radius: 20px;
    margin-top: 50px;
}

.title {
    font-size: 42px;
    font-weight: 900;
    color: #f1c40f;
}

.sub {
    font-size: 20px;
    margin-top: 10px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Session State
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "db" not in st.session_state:
    st.session_state.db = []

# =========================================================
# 🟦 الصفحة الرئيسية
# =========================================================
if st.session_state.page == "home":

    st.markdown("""
    <div class="main-box">
        <div class="title">💎 KITCHEN PRO ERP</div>
        <div class="sub">برمجة المهندس ياسين علاء</div>
        <p>نظام إدارة التخصيم والتقطيع الاحترافي للمطابخ</p>
    </div>
    """, unsafe_allow_html=True)

    # لوجو (غير الرابط براحتك)
    st.image("https://i.imgur.com/8Km9tLL.png", width=180)

    st.write("")

    if st.button("🚀 الدخول إلى نظام التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# =========================================================
# 🟩 صفحة التخصيم
# =========================================================
elif st.session_state.page == "calc":

    st.title("📋 نظام التخصيم الاحترافي للمطابخ")

    if st.button("⬅ الرجوع للرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    st.divider()

    # -------------------------
    # إدخال البيانات
    # -------------------------
    st.subheader("➕ إضافة وحدة جديدة")

    col1, col2, col3, col4 = st.columns(4)

    name = col1.text_input("اسم الوحدة")
    W = col2.number_input("العرض", min_value=0.0)
    H = col3.number_input("الارتفاع", min_value=0.0)
    D = col4.number_input("العمق", min_value=0.0)

    qty = st.number_input("العدد", min_value=1, value=1)

    if st.button("➕ إضافة إلى النظام", use_container_width=True):

        if W > 0 and H > 0:
            st.session_state.db.append({
                "name": name if name else f"UNIT-{len(st.session_state.db)+1}",
                "W": W,
                "H": H,
                "D": D,
                "qty": qty
            })
            st.success("تمت الإضافة ✔")
            st.rerun()

    st.divider()

    # -------------------------
    # جدول التخصيم
    # -------------------------
    if st.session_state.db:

        st.subheader("📊 جدول التخصيم")

        data = []

        for u in st.session_state.db:

            h = u["H"] - 13
            w = u["W"] - 5
            d = u["D"] - 5

            data.append({
                "الوحدة": u["name"],
                "العرض": u["W"],
                "الارتفاع": u["H"],
                "العمق": u["D"],
                "العدد": u["qty"],
                "المقاس بعد التخصيم (H)": h,
                "المقاس بعد التخصيم (W)": w,
                "المقاس بعد التخصيم (D)": d
            })

        df = pd.DataFrame(data)
        st.table(df)

        st.write("---")

        # إجمالي بسيط
        total_units = sum([u["qty"] for u in st.session_state.db])

        st.success(f"📦 إجمالي الوحدات: {total_units}")

        # حذف الكل
        if st.button("🗑️ مسح كل البيانات"):
            st.session_state.db = []
            st.rerun()

    else:
        st.info("لا يوجد بيانات بعد — أضف وحدة لبدء التخصيم")
