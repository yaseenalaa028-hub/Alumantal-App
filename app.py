import streamlit as st
from fpdf import FPDF

# إعداد الصفحة وحل مشكلة الموبايل
st.set_page_config(page_title="نظام المهندس ياسين علاء", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .header-label {
        background-color: #2f3640;
        color: #fbc531;
        font-size: clamp(14pt, 5vw, 22pt);
        font-weight: bold;
        padding: 15px;
        text-align: center;
        border-bottom: 4px solid #e1b12c;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .result-view {
        background-color: #ffffff;
        color: #1e272e !important;
        border: 2px solid #2ecc71;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: clamp(10pt, 3vw, 12pt);
        border-radius: 5px;
        white-space: pre-wrap;
        margin-bottom: 10px;
    }
    /* تنسيق زرار الإضافة الرئيسي */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-label">نظام تخصيم الألومنيوم - المهندس ياسين علاء</div>', unsafe_allow_html=True)

# إدارة حالة الصفحة (إظهار/إخفاء خانات الإدخال)
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# الزرار الرئيسي لفتح الإدخال
if st.button("➕ إضافة مقاسات جديدة"):
    st.session_state.show_inputs = not st.session_state.show_inputs

# --- شاشة إدخال البيانات (بتظهر لما تدوس على الزرار) ---
if st.session_state.show_inputs:
    with st.container():
        st.subheader("📝 أدخل بيانات الوحدة:")
        u_title = st.text_input("اسم الوحدة", placeholder="مثال: وحدة حوض، وحدة علوية...")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        
        c1, c2, c3 = st.columns(3)
        with c1: w = st.number_input("العرض الكلي (W)", value=0.0, format="%.1f")
        with c2: h = st.number_input("الارتفاع الكلي (H)", value=0.0, format="%.1f")
        with c3: d = st.number_input("العمق الكلي (D)", value=0.0, format="%.1f")
        
        with st.expander("🧱 تفاصيل الرفوف والأدراج"):
            col_sh1, col_sh2, col_sh3 = st.columns(3)
            with col_sh1: sh_w = st.number_input("عرض الرف", value=0.0, placeholder="العرض")
            with col_sh2: sh_d = st.number_input("عمق الرف", value=0.0, placeholder="العمق")
            with col_sh3: sh_n = st.number_input("عدد الرفوف", value=0)
            
            st.divider()
            
            col_dr1, col_dr2 = st.columns(2)
            with col_dr1: dr_w = st.number_input("عرض الدرج", value=0.0, placeholder="العرض - 2.5")
            with col_dr2: dr_n = st.number_input("عدد الأدراج", value=0)

        if st.button("💾 حفظ الوحدة في الجدول"):
            st.session_state.project_storage.append({
                'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                'dr_w': dr_w, 'dr_n': dr_n, 'dr_d': d, # العمق ثابت من عمق الوحدة
                'dv_h': 0, 'dv_d': 0, 'dv_n': 0 # فواصل اختيارية
            })
            st.session_state.show_inputs = False # إخفاء الخانات بعد الحفظ
            st.success("تمت الإضافة بنجاح!")
            st.rerun()

# --- الحسابات وعرض النتائج (نفس معادلات كودك بالظبط) ---
if st.session_state.project_storage:
    st.divider()
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("📊 جرد خامات المشروع"):
            m_total, t_total = 0, 0
            for u in st.session_state.project_storage:
                h_net = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_net, d_net = u['w'] - 5, u['d'] - 5
                if u['type'] == "سفلية":
                    m_total += (h_net*2) + (w_net*3) + (d_net*2); t_total += (h_net*2) + (w_net*1) + (d_net*2)
                else:
                    m_total += (h_net*2) + (w_net*2); t_total += (h_net*2) + (w_net*2) + (d_net*4)
                m_total += ((u['dr_w']-2.5)*2 + u['d']*2) * u['dr_n'] # تخصيم الأدراج
            st.warning(f"مفرد: {m_total/600:.2f} عود | متقارب: {t_total/600:.2f} عود")

    with col_act2:
        if st.button("🗑️ مسح الجدول"):
            st.session_state.project_storage = []
            st.rerun()

    for u in st.session_state.project_storage:
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5
        
        res = f"وحدة: {u['title']} | النوع: {u['type']}\n"
        res += "━" * 45 + "\n"
        res += f"📐 تخصيم الهيكل:\n- ارتفاع: {h_baky} | عرض: {w_baky} | عمق: {d_baky}\n"
        
        if u['sh_n'] > 0:
            res += f"🧱 الرفوف ({u['sh_n']}): {u['sh_w']-5} × {u['sh_d']-5}\n"
        if u['dr_n'] > 0:
            res += f"🗄️ الأدراج ({u['dr_n']}): عرض {u['dr_w']-2.5} × عمق {u['d']}\n"
            
        st.markdown(f'<div class="result-view">{res}</div>', unsafe_allow_html=True)
else:
    if not st.session_state.show_inputs:
        st.info("اضغط على 'إضافة مقاسات جديدة' للبدء.")
