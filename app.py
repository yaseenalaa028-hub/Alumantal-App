import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيمات ياسين علاء", layout="centered")

# الستايل الاحترافي (أصفر + أسود + واجهة رايقة)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: 2px solid #2f3640; font-size: 18px;
    }
    .report-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); direction: rtl; text-align: right; margin-bottom: 20px;
    }
    .title-line { font-size: 22px; font-weight: bold; color: #1e3799; border-bottom: 2px solid #fbc531; margin-bottom: 15px; }
    .data-line { font-size: 19px; margin: 8px 0; color: #000; font-weight: bold; }
    .section-label { color: #d35400; font-size: 20px; margin-top: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة الواجهة
if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- 1. الواجهة الصافية (البداية) ---
if not st.session_state.started:
    st.markdown("<br><br><h1 style='text-align: center; color: #2f3640;'>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>إشراف المهندس ياسين علاء</h3><br>", unsafe_allow_html=True)
    
    if st.button("🚀 ابدأ التخصيم الآن"):
        st.session_state.started = True
        st.rerun()

# --- 2. واجهة إدخال البيانات والنتائج ---
else:
    st.markdown("<h2 style='text-align: center; color: #2f3640;'>📝 مدخلات المقاسات</h2>", unsafe_allow_html=True)
    
    with st.container():
        u_title = st.text_input("اسم الوحدة", placeholder="مثال: مطبخ")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
        
        # الخانات الأساسية (العرض - الارتفاع - العمق)
        col1, col2, col3 = st.columns(3)
        with col1: w = st.number_input("العرض الكلي", value=None)
        with col2: h = st.number_input("الارتفاع الكلي", value=None)
        with col3: d = st.number_input("العمق الكلي", value=None)

        st.markdown("---")
        # خانات الإضافات (الرفوف والفواصل)
        st.markdown("#### 🧱 أضف الرفوف والفواصل")
        c1, c2 = st.columns(2)
        with c1: 
            sh_n = st.number_input("عدد الرفوف", value=None, step=1)
        with c2: 
            dv_n = st.number_input("عدد الفواصل", value=None, step=1)

        if st.button("💾 احسب المقاسات واعرض النتائج"):
            if w and h and d:
                # قوانين التخصيم الأساسية (باكية الفيبر)
                h_bak = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                w_bak, d_bak = w - 5, d - 5
                
                # تخصيم الرفوف والفواصل (خصم 5 سم إضافية كما في مثالك)
                sh_w, sh_d = w_bak - 5, d_bak - 3
                dv_h, dv_d = h_bak - 5, d_bak - 3

                unit = {
                    'title': u_title, 'type': u_type, 
                    'h_bak': h_bak, 'w_bak': w_bak, 'd_bak': d_bak,
                    'sh_n': int(sh_n) if sh_n else 0, 'sh_w': sh_w, 'sh_d': sh_d,
                    'dv_n': int(dv_n) if dv_n else 0, 'dv_h': dv_h, 'dv_d': dv_d
                }
                st.session_state.storage.append(unit)
            else:
                st.error("أدخل العرض والارتفاع والعمق الأول يا هندسة!")

    # --- عرض النتائج بالصيغة اللي طلبتها ---
    if st.session_state.storage:
        st.markdown("<br><h3 style='text-align: right;'>📋 قائمة القص النهائية:</h3>", unsafe_allow_html=True)
        for u in st.session_state.storage:
            st.markdown(f"""
            <div class="report-card">
                <div class="title-line">📦 {u['title']} - {u['type']}</div>
                
                <div class="section-label">🪵 تخصيم الفيبر:</div>
                <div class="data-line">الضهرية: {u['w_bak']} * {u['h_bak']} * 1</div>
                <div class="data-line">الارضية: {u['w_bak']} * {u['d_bak']} * 1</div>
                <div class="data-line">الاجناب: {u['h_bak']} * {u['d_bak']} * 2</div>
            """, unsafe_allow_html=True)
            
            # إظهار الرفوف لو فيه عدد
            if u['sh_n'] > 0:
                st.markdown(f'<div class="data-line">الارفف: {u["sh_w"]} * {u["sh_d"]} * {u["sh_n"]}</div>', unsafe_allow_html=True)
            
            # إظهار الفواصل لو فيه عدد
            if u['dv_n'] > 0:
                st.markdown(f'<div class="data-line">الفواصل: {u["dv_h"]} * {u["dv_d"]} * {u["dv_n"]}</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="section-label">📐 تخصيم الألومنيوم (2*8):</div>
                <div class="data-line">الارتفاع: {u['h_bak']} سم (2 مفرد + 2 متقارب)</div>
                <div class="data-line">العرض: {u['w_bak']} سم (3 مفرد + 1 متقارب)</div>
                <div class="data-line">العمق: {u['d_bak']} سم (2 مفرد + 2 متقارب)</div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("🔄 مسح السجل والبدء من جديد"):
        st.session_state.started = False
        st.session_state.storage = []
        st.rerun()
