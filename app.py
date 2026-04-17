import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام تخصيم الألومنيوم", layout="wide")

# تخزين البيانات
if "data" not in st.session_state:
    st.session_state.data = []

st.title("🧠 نظام تخصيم الألومنيوم - نسخة ويب")

# ===== الإدخالات =====
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("اسم الوحدة")

with col2:
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])

with col3:
    w = st.number_input("العرض", min_value=0.0)
    h = st.number_input("الارتفاع", min_value=0.0)
    d = st.number_input("العمق", min_value=0.0)

col4, col5, col6 = st.columns(3)

with col4:
    shelves = st.number_input("عدد الرفوف", min_value=0)

with col5:
    dividers = st.number_input("عدد الفواصل", min_value=0)

with col6:
    drawers = st.number_input("عدد الأدراج", min_value=0)

# ===== حساب التخصيم =====
def calc(w, h, d, t):
    if t == "سفلية":
        h2 = h - 13
    else:
        h2 = h - 5

    w2 = w - 5
    d2 = d - 5

    return h2, w2, d2

# ===== زر الإضافة =====
if st.button("➕ إضافة وحدة"):
    if name:
        h2, w2, d2 = calc(w, h, d, unit_type)

        item = {
            "اسم": name,
            "نوع": unit_type,
            "عرض": w,
            "ارتفاع": h,
            "عمق": d,
            "تخصيم_ارتفاع": h2,
            "تخصيم_عرض": w2,
            "تخصيم_عمق": d2,
            "رفوف": shelves,
            "فواصل": dividers,
            "أدراج": drawers
        }

        st.session_state.data.append(item)
        st.success("تمت الإضافة بنجاح ✔")

# ===== عرض الجدول =====
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df, use_container_width=True)

    # ===== إجمالي بسيط =====
    st.subheader("📊 إجمالي المشروع")

    total_units = len(st.session_state.data)
    total_shelves = sum(x["رفوف"] for x in st.session_state.data)

    st.write("عدد الوحدات:", total_units)
    st.write("إجمالي الرفوف:", total_shelves)

# ===== مسح البيانات =====
if st.button("🗑️ مسح الكل"):
    st.session_state.data = []
    st.rerun()
