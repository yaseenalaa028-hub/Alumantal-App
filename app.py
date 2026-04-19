import streamlit as st
import pandas as pd

st.title("🏭 نظام تخصيم مصنع الألوميتال")

# =========================
# 📐 بيانات الوحدة الأساسية
# =========================
st.header("📐 بيانات الوحدة")

col1, col2, col3 = st.columns(3)

with col1:
    W = st.number_input("العرض الكلي (سم)", value=0.0)

with col2:
    H = st.number_input("الارتفاع الكلي (سم)", value=0.0)

with col3:
    D = st.number_input("العمق الكلي (سم)", value=0.0)

st.divider()

# =========================
# 📚 الرفوف
# =========================
st.header("📚 الرفوف")

col1, col2 = st.columns(2)

with col1:
    shelves_count = st.number_input("عدد الرفوف", value=0)

with col2:
    st.write("فيبر الرف = 67 × 42 (بعد خصم 5 سم)")

st.divider()

# =========================
# 🧱 الفواصل
# =========================
st.header("🧱 الفواصل")

col1, col2 = st.columns(2)

with col1:
    dividers_count = st.number_input("عدد الفواصل", value=0)

with col2:
    st.write("فيبر الفاصل = 72 × 42 (بعد خصم 5 سم)")

st.divider()

# =========================
# 🗄️ الأدراج
# =========================
st.header("🗄️ الأدراج")

col1, col2 = st.columns(2)

with col1:
    drawers_count = st.number_input("عدد الأدراج", value=0)

with col2:
    st.write("فيبر الدرج = 34.5 × 45")

st.divider()

# =========================
# 🚀 التشغيل
# =========================
if st.button("تشغيل التخصيم"):

    if W > 0 and H > 0 and D > 0:

        body_W = W - 5
        body_H = H - 13
        body_D = D - 5

        data = []

        def add(type_, desc, size, qty):
            data.append([type_, desc, size, qty])

        # =========================
        # 🪵 جسم الوحدة
        # =========================
        add("فيبر", "ضهرية", f"{body_W} × {body_H}", 1)
        add("فيبر", "أرضية", f"{body_W} × {body_D}", 1)
        add("فيبر", "أجناب", f"{body_H} × {body_D}", 2)

        # =========================
        # 📚 الرفوف
        # =========================
        if shelves_count > 0:
            add("فيبر", "رف", "67 × 42", shelves_count)
            add("ألوميتال", "رف عرض", 77 * 2, shelves_count * 2)
            add("ألوميتال", "رف عمق", 47 * 2, shelves_count * 2)

        # =========================
        # 🧱 الفواصل
        # =========================
        if dividers_count > 0:
            add("فيبر", "فاصل", "72 × 42", dividers_count)
            add("ألوميتال", "فاصل ارتفاع", 77 * 2, dividers_count * 2)
            add("ألوميتال", "فاصل عمق", 47 * 2, dividers_count * 2)

        # =========================
        # 🗄️ الأدراج
        # =========================
        if drawers_count > 0:
            add("فيبر", "درج", "34.5 × 45", drawers_count)
            add("ألوميتال", "درج عرض", 34.5 * 5, drawers_count)
            add("ألوميتال", "درج عمق", 45 * 6, drawers_count)

        # =========================
        # 📊 عرض الجدول
        # =========================
        df = pd.DataFrame(data, columns=["النوع", "الوصف", "المقاس", "العدد"])
        st.subheader("📊 جدول التخصيم")
        st.dataframe(df)

    else:
        st.error("من فضلك أدخل بيانات الوحدة الأساسية")
