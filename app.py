import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AL-PRINCE SYSTEM", layout="wide")

# الستايل الفاخر (أصفر الورشة + أسود ملكي + تصميم مودرن)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 3.8em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; 
        border: 2px solid #2f3640; font-size: 20px; transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #2f3640; color: #fbc531; border: 2px solid #fbc531; }
    
    .report-card {
        background-color: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); direction: rtl; text-align: right;
        border-right: 15px solid #fbc531; margin-bottom: 25px;
    }
    .welcome-card {
        background: linear-gradient(135deg, #2f3640 0%, #1e272e 100%);
        padding: 50px; border-radius: 30px; color: #fbc531; text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3); margin-top: 50px;
    }
    .title-line { font-size: 28px; font-weight: bold; color: #1e3799; border-bottom: 3px solid #fbc531; padding-bottom: 10px; margin-bottom: 20px; }
    .section-label { color: #e84118; font-size: 22px; margin-top: 25px; font-weight: bold; border-right: 6px solid #e84118; padding-right: 12px; }
    .data-line { font-size: 21px; margin: 12px 0; color: #2f3640; font-weight: bold; border-bottom: 1px dashed #dcdde1; padding-bottom: 5px; }
    .header-text { color: #2f3640; font-weight: bold; text-align: center; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة التطبيق
if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- 1. واجهة الترحيب ---
if not st.session_state.started:
    st.markdown("""
        <div class="welcome-card">
            <h1 style='font-size: 45px;'>🏗️ نظام التخصيم الذكي</h1>
            <p style='font-size: 25px; color: #f5f6fa;'>ورشة المهندس ياسين علاء</p>
            <hr style='border: 1px solid #fbc531; width: 50%; margin: 20px auto;'>
            <p style='font-size: 18px;'>دقة في التخصيم .. سرعة في التنفيذ</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 دخول النظام"):
        st.session_state.started = True
        st.rerun()

# --- 2. واجهة العمل ---
else:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>⚙️ التحكم</h2>", unsafe_allow_html=True)
        if st.button("🗑️ مسح الكل والعودة"):
            st.session_state.storage = []
            st.session_state.started = False
            st.rerun()

    st.markdown("<h2 class='header-text'>📝 إدخال بيانات التشغيل</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 🏷️ نوع الوحدة")
        c_title, c_type = st.columns(2)
        with c_title: u_title = st.text_input("اسم الوحدة", "مطبخ سفلي")
        with c_type: u_type = st.selectbox("تصنيف الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
        
        st.markdown("### 📐 المقاسات الكلية (سم)")
        m1, m2, m3 = st.columns(3)
        with m1: w = st.number_input("العرض (W)", value=None)
        with m2: h = st.number_input("الارتفاع (H)", value=None)
        with m3: d = st.number_input("العمق (D)", value=None)

        st.markdown("---")
        st.markdown("### 🧱 تفاصيل الإضافات (أرفف - فواصل - أدراج)")
        
        tab1, tab2, tab3 = st.tabs(["📂 الرفوف", "📂 الفواصل", "📂 الأدراج"])
        
        with tab1:
            r1, r2, r3 = st.columns(3)
            with r1: sh_w_in = st.number_input("عرض الرف (سم)", value=0.0)
            with r2: sh_d_in = st.number_input("عمق الرف (سم)", value=0.0)
            with r3: sh_n_in = st.number_input("عدد الرفوف", value=0, step=1)
            
        with tab2:
            v1, v2, v3 = st.columns(3)
            with v1: dv_h_in = st.number_input("ارتفاع الفاصل (سم)", value=0.0)
            with v2: dv_d_in = st.number_input("عمق الفاصل (سم)", value=0.0)
            with v3: dv_n_in = st.number_input("عدد الفواصل", value=0, step=1)
            
        with tab3:
            d1, d2, d3 = st.columns(3)
            with d1: dr_w_in = st.number_input("عرض الدرج (سم)", value=0.0)
            with d2: dr_d_in = st.number_input("عمق الدرج (سم)", value=0.0)
            with d3: dr_n_in = st.number_input("عدد الأدراج", value=0, step=1)

        if st.button("📝 استخراج شيت القص النهائي"):
            if w and h and d:
                h_c = h - 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else h - 5
                w_c = w - 5
                d_c = d - 5

                unit_entry = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_c': h_c, 'w_c': w_c, 'd_c': d_c,
                    'sh_w': sh_w_in, 'sh_d': sh_d_in, 'sh_n': sh_n_in,
                    'dv_h': dv_h_in, 'dv_d': dv_d_in, 'dv_n': dv_n_in,
                    'dr_w': dr_w_in, 'dr_d': dr_d_in, 'dr_n': dr_n_in
                }
                st.session_state.storage.append(unit_entry)
            else:
                st.error("كمل المقاسات الأساسية الأول يا هندسة!")

    # --- 3. عرض شيت النتائج ---
    if st.session_state.storage:
        st.markdown("<h2 class='header-text'>📋 شيتات القص الجاهزة</h2>", unsafe_allow_html=True)
        for u in st.session_state.storage:
            st.markdown(f"""
            <div class="report-card">
                <div class="title-line">📋 {u['title']} - {u['type']}</div>
                
                <div class="section-label">🪵 تخصيم الفيبر (صافي القص):</div>
                <div class="data-line">📏 الضهرية: {u['w_c']} * {u['h_c']} * 1</div>
                <div class="data-line">📏 الارضية: {u['w_c']} * {u['d_c']} * 1</div>
                <div class="data-line">📏 الاجناب: {u['h_c']} * {u['d_c']} * 2</div>
            """, unsafe_allow_html=True)
            
            if u['sh_n'] > 0:
                st.markdown(f'<div class="data-line">📏 الارفف: {u["sh_w"]-5} * {u["sh_d"]-5} * {u["sh_n"]}</div>', unsafe_allow_html=True)
            if u['dv_n'] > 0:
                st.markdown(f'<div class="data-line">📏 الفواصل: {u["dv_h"]-5} * {u["dv_d"]-5} * {u["dv_n"]}</div>', unsafe_allow_html=True)
            if u['dr_n'] > 0:
                st.markdown(f'<div class="data-line">📏 الادراج: {u["dr_w"]-2.5} عرض * {u["dr_d"]} عمق * {u["dr_n"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">📐 تخصيم الألومنيوم (2*8):</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-line">🛠️ الارتفاع: {u["h_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            
            if u['type'] == "وحدة سفلية":
                st.markdown(f'<div class="data-line">🛠️ العرض: {u["w_c"]} سم (3 مفرد + 1 متقارب)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="data-line">🛠️ العمق: {u["d_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="data-line">🛠️ العرض: {u["w_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="data-line">🛠️ العمق: {u["d_c"]} سم (4 متقارب)</div>', unsafe_allow_html=True)
            
            if u['sh_n'] > 0 or u['dv_n'] > 0:
                count = (u['sh_n'] + u['dv_n']) * 4
                st.markdown(f'<div class="data-line">🛠️ ألومنيا الإضافات: {u["d_c"]} سم ({count} حتة مفرد)</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
