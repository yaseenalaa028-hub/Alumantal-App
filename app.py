import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام تخصيم الألومنيوم - برمجة البرنس", layout="wide")

st.markdown("""
    <style>
    .main-header {text-align: center; color: #fbc531; background-color: #2f3640; padding: 20px; border-radius: 15px; border-bottom: 5px solid #e1b12c;}
    </style>
    <div class="main-header">
        <h1>نظام تخصيم الألومنيوم 🏗️</h1>
        <h2>برمجة البرنس</h2>
    </div>
    """, unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

st.markdown("### 📝 مدخلات المقاسات (برمجة البرنس)")
col1, col2, col3 = st.columns(3)
with col1:
    unit_title = st.text_input("اسم الوحدة", value="وحدة 1")
    w = st.number_input("العرض الكلي", min_value=0.0)
with col2:
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
    h = st.number_input("الارتفاع الكلي", min_value=0.0)
with col3:
    d = st.number_input("العمق الكلي", min_value=0.0)

if st.button("💾 إضافة للجدول", use_container_width=True):
    if w > 0 and h > 0:
        h_baky = h - 13 if unit_type in ["سفلية", "دولاب خزين"] else h - 5
        st.session_state.project_storage.append({'title': unit_title, 'type': unit_type, 'w': w, 'h': h, 'd': d, 'h_b': h_baky})
        st.success("تمت الإضافة يا برنس!")

if st.session_state.project_storage:
    st.table(pd.DataFrame(st.session_state.project_storage)[['title', 'w', 'h', 'd']])
