import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيمات ياسين علاء", layout="wide")

# الستايل الاحترافي
st.markdown("""
    <style>
    .main { background-color: #f1f2f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: 2px solid #2f3640; font-size: 18px;
    }
    .report-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); direction: rtl; text-align: right;
        border-right: 12px solid #fbc531; margin-bottom: 20px;
    }
    .title-line { font-size: 26px; font-weight: bold; color: #1e3799; border-bottom: 3px solid #fbc531; padding-bottom: 5px; }
    .section-label { color: #c0392b; font-size: 22px; margin-top: 20px; font-weight: bold; border-right: 5px solid #c0392b; padding-right: 10px; }
    .data-line { font-size: 20px; margin: 12px 0; color: #2d3436; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'storage' not in st.session_state:
    st.session_state.storage = []

st.markdown("<h1 style='text-align: center;'>🏗️ نظام التخصيم المتكامل - م/ ياسين علاء</h1>", unsafe_allow_html=True)

# --- واجهة إدخال البيانات المفصلة ---
with st.container():
    st.markdown("### 📝 بيانات الوحدة الأساسية")
    u_title = st.text_input("اسم القطعة")
    u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
    
    col1, col2, col3 = st.columns(3)
    with col1: w = st.number_input("العرض الكلي (سم)", value=None, key="w_main")
    with col2: h = st.number_input("الارتفاع الكلي (سم)", value=None, key="h_main")
    with col3: d = st.number_input("العمق الكلي (سم)", value=None, key="d_main")

    st.divider()
    
    # --- خانات الرفوف المفصلة ---
    st.markdown("### 🧱 بيانات الرفوف")
    r1, r2, r3 = st.columns(3)
    with r1: sh_w = st.number_input("عرض الرف", value=None, key="sh_w")
    with r2: sh_d = st.number_input("عمق الرف", value=None, key="sh_d")
    with r3: sh_n = st.number_input("عدد الرفوف", value=0, step=1, key="sh_n")

    # --- خانات الفواصل المفصلة ---
    st.markdown("### 🧱 بيانات الفواصل")
    v1, v2, v3 = st.columns(3)
    with v1: dv_h = st.number_input("ارتفاع الفاصل", value=None, key="dv_h")
    with v2: dv_d = st.number_input("عمق الفاصل", value=None, key="dv_d")
    with v3: dv_n = st.number_input("عدد الفواصل", value=0, step=1, key="dv_n")

    # --- خانات الأدراج المفصلة ---
    st.markdown("### 🧱 بيانات الأدراج")
    dr1, dr2, dr3 = st.columns(3)
    with dr1: drawer_w = st.number_input("عرض الدرج", value=None, key="dr_w")
    with dr2: drawer_d = st.number_input("عمق الدرج", value=None, key="dr_d")
    with dr3: drawer_n = st.number_input("عدد الأدراج", value=0, step=1, key="dr_n")

    if st.button("💾 استخراج شيت القص بالكامل"):
        if w and h and d:
            # تخصيم الارتفاع
            h_clean = h - 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else h - 5
            w_clean = w - 5
            d_clean = d - 5

            unit = {
                'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                'h_c': h_clean, 'w_c': w_clean, 'd_c': d_clean,
                'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
                'dr_w': drawer_w, 'dr_d': drawer_d, 'dr_n': drawer_n
            }
            st.session_state.storage.append(unit)
        else:
            st.error("أدخل المقاسات الأساسية الأول")

# --- عرض النتائج ---
if st.session_state.storage:
    for u in st.session_state.storage:
        st.markdown(f"""
        <div class="report-card">
            <div class="title-line">📄 شيت تفصيل: {u['title']}</div>
            
            <div class="section-label">🪵 تخصيم الفيبر (الخامات):</div>
            <div class="data-line">الضهرية: {u['w_c']} * {u['h_c']} * 1</div>
            <div class="data-line">الارضية: {u['w_c']} * {u['d_c']} * 1</div>
            <div class="data-line">الاجناب: {u['h_c']} * {u['d_c']} * 2</div>
        """, unsafe_allow_html=True)

        if u['sh_n'] > 0:
            st.markdown(f'<div class="data-line">الارفف: {u["sh_w"]-5 if u["sh_w"] else 0} * {u["sh_d"]-5 if u["sh_d"] else 0} * {u["sh_n"]}</div>', unsafe_allow_html=True)
        if u['dv_n'] > 0:
            st.markdown(f'<div class="data-line">الفواصل: {u["dv_h"]-5 if u["dv_h"] else 0} * {u["dv_d"]-5 if u["dv_d"] else 0} * {u["dv_n"]}</div>', unsafe_allow_html=True)
        if u['dr_n'] > 0:
            st.markdown(f'<div class="data-line">الادراج: {u["dr_w"]-2.5 if u["dr_w"] else 0} عرض * {u["dr_d"] if u["dr_d"] else 0} عمق * {u["dr_n"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">📐 تخصيم الألومنيوم (2*8):</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="data-line">الارتفاع: {u["h_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
        
        if u['type'] == "وحدة سفلية":
            st.markdown(f'<div class="data-line">العرض: {u["w_c"]} سم (3 مفرد + 1 متقارب)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-line">العمق: {u["d_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="data-line">العرض: {u["w_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-line">العمق: {u["d_c"]} سم (4 متقارب)</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

if st.button("🔄 مسح السجل"):
    st.session_state.storage = []
    st.rerun()
