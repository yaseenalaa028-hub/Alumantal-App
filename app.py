import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيم الألومنيوم - برمجة البرنس", layout="wide")

# الهيدر الاحترافي باسمك
st.markdown("""
    <style>
    .main-header {
        text-align: center; 
        color: #fbc531; 
        background-color: #2f3640; 
        padding: 20px; 
        border-radius: 15px; 
        border-bottom: 5px solid #e1b12c;
    }
    </style>
    <div class="main-header">
        <h1>نظام تخصيم الألومنيوم 🏗️</h1>
        <h2>برمجة البرنس</h2>
    </div>
    """, unsafe_allow_html=True)

# مخزن البيانات
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# المدخلات الأساسية
st.markdown("### 📝 إدخال المقاسات")
col1, col2, col3 = st.columns(3)
with col1:
    unit_title = st.text_input("اسم الوحدة", value="مطبخ 1")
    w = st.number_input("العرض (W)", min_value=0.0, step=0.1)
with col2:
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
    h = st.number_input("الارتفاع (H)", min_value=0.0, step=0.1)
with col3:
    d = st.number_input("العمق (D)", min_value=0.0, step=0.1)

# زرار الإضافة والحساب
if st.button("💾 حفظ الوحدة وتخصيمها", use_container_width=True):
    if w > 0 and h > 0:
        # معادلاتك "الصح": 13 سم خصم للسفلي و5 سم للعلوي والعرض والعمق
        h_baky = h - 13 if unit_type in ["سفلية", "دولاب خزين"] else h - 5
        w_baky, d_baky = w - 5, d - 5
        
        st.session_state.project_storage.append({
            'الوحدة': unit_title, 
            'النوع': unit_type, 
            'عرض': w, 
            'ارتفاع': h, 
            'عمق': d, 
            'الصافي H': h_baky,
            'الصافي W': w_baky,
            'الصافي D': d_baky
        })
        st.success("تم الحفظ بنجاح يا برنس!")
    else:
        st.error("برجاء إدخال المقاسات الأساسية!")

# عرض النتائج في جدول
if st.session_state.project_storage:
    st.divider()
    st.subheader("📊 جدول التخصيمات")
    df = pd.DataFrame(st.session_state.project_storage)
    st.table(df)
    
    # تفاصيل تقطيع سريعة
    st.subheader("📐 تفاصيل التقطيع السريع")
    for u in st.session_state.project_storage:
        st.info(f"الوحدة **{u['الوحدة']}**: تقطيع الارتفاع على `{u['الصافي H']}` | العرض على `{u['الصافي W']}`")
        
    if st.button("🗑️ مسح الجدول"):
        st.session_state.project_storage = []
        st.rerun()
