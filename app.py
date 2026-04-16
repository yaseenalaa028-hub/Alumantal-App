import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيم ياسين علاء", layout="centered")

# الستايل: أصفر وأسود، واضح ومباشر
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: 2px solid #2f3640;
    }
    .report-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); direction: rtl; text-align: right; margin-bottom: 20px;
    }
    .title-line { font-size: 22px; font-weight: bold; color: #1e3799; border-bottom: 2px solid #fbc531; margin-bottom: 15px; }
    .data-line { font-size: 19px; margin: 8px 0; color: #000; font-weight: bold; }
    .section-label { color: #d35400; font-size: 20px; margin-top: 15px; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

if 'storage' not in st.session_state:
    st.session_state.storage = []

st.markdown("<h1 style='text-align: center;'>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)

# --- مدخلات البيانات ---
with st.container():
    u_title = st.text_input("اسم الوحدة", "مطبخ")
    u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
    
    col1, col2, col3 = st.columns(3)
    with col1: w = st.number_input("العرض الكلي", value=None)
    with col2: h = st.number_input("الارتفاع الكلي", value=None)
    with col3: d = st.number_input("العمق الكلي", value=None)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: sh_n = st.number_input("عدد الرفوف", value=None, step=1)
    with c2: dv_n = st.number_input("عدد الفواصل", value=None, step=1)
    with c3: dr_n = st.number_input("عدد الأدراج", value=None, step=1)

    if st.button("✅ عرض التخصيم النهائي"):
        if w and h and d:
            # قوانين التخصيم الأساسية
            h_bak = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
            w_bak, d_bak = w - 5, d - 5
            
            # تخصيم الرفوف والفواصل (خصم 5 سم إضافية من الباكية كما في مثالك)
            # مثالك: الباكية كانت 77*45 والرف طلع 72*42 (خصم 5 من الارتفاع/العرض و 3 من العمق)
            # سنعتمد الخصم الموحد 5 سم للرفوف والفواصل لتسهيل القص
            sh_w, sh_d = w_bak - 5, d_bak - 3
            dv_h, dv_d = h_bak - 5, d_bak - 3

            unit = {
                'title': u_title, 'type': u_type, 
                'h_bak': h_bak, 'w_bak': w_bak, 'd_bak': d_bak,
                'sh_n': sh_n if sh_n else 0, 'sh_w': sh_w, 'sh_d': sh_d,
                'dv_n': dv_n if dv_n else 0, 'dv_h': dv_h, 'dv_d': dv_d
            }
            st.session_state.storage.append(unit)
        else:
            st.error("أدخل المقاسات الأساسية")

# --- عرض النتائج بالصيغة اللي طلبتها ---
if st.session_state.storage:
    for u in st.session_state.storage:
        st.markdown(f"""
        <div class="report-card">
            <div class="title-line">📦 {u['title']} - {u['type']}</div>
            
            <div class="section-label">🪵 تخصيم الفيبر:</div>
            <div class="data-line">الضهرية: {u['w_bak']} * {u['h_bak']} * 1</div>
            <div class="data-line">الارضية: {u['w_bak']} * {u['d_bak']} * 1</div>
            <div class="data-line">الاجناب: {u['h_bak']} * {u['d_bak']} * 2</div>
        """, unsafe_allow_html=True)
        
        if u['sh_n'] > 0:
            st.markdown(f'<div class="data-line">الارفف: {u["sh_w"]} * {u["sh_d"]} * {u["sh_n"]}</div>', unsafe_allow_html=True)
        
        if u['dv_n'] > 0:
            st.markdown(f'<div class="data-line">الفواصل: {u["dv_h"]} * {u["dv_d"]} * {u["dv_n"]}</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="section-label">📐 تخصيم الألومنيوم (2*8):</div>
            <div class="data-line">الارتفاع: {0} سم (2 مفرد + 2 متقارب)</div>
            <div class="data-line">العرض: {1} سم (3 مفرد + 1 متقارب)</div>
            <div class="data-line">العمق: {2} سم (2 مفرد + 2 متقارب)</div>
        </div>
        """.format(u['h_bak'], u['w_bak'], u['d_bak']), unsafe_allow_html=True)

if st.button("🗑️ مسح السجل"):
    st.session_state.storage = []
    st.rerun()
