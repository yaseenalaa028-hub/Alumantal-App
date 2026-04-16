import streamlit as st
from fpdf import FPDF

# 1. إعدادات الصفحة وحل مشكلة الموبايل
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
    /* منع تقطيع الكلام في الموبايل */
    .header-label {
        background-color: #2f3640;
        color: #fbc531;
        font-size: clamp(14pt, 5vw, 22pt);
        font-weight: bold;
        padding: 15px;
        text-align: center;
        border-bottom: 4px solid #e1b12c;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .result-view {
        background-color: #ffffff;
        color: #1e272e !important;
        border: 2px solid #2ecc71;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: clamp(9pt, 3vw, 11pt);
        border-radius: 5px;
        white-space: pre-wrap;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-label">نظام تخصيم الألومنيوم - المهندس ياسين علاء</div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- منطقة المدخلات (كاملة كما طلبت) ---
with st.sidebar:
    st.header("📝 إدخال البيانات")
    u_title = st.text_input("اسم الوحدة", "وحدة جديدة")
    u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    w = st.number_input("العرض (W)", value=0.0)
    h = st.number_input("الارتفاع (H)", value=0.0)
    d = st.number_input("العمق (D)", value=0.0)
    
    with st.expander("🧱 تفاصيل الرفوف"):
        sh_w = st.number_input("عرض الرف", value=0.0)
        sh_d = st.number_input("عمق الرف", value=0.0)
        sh_n = st.number_input("عدد الرفوف", value=0)
        
    with st.expander("📐 تفاصيل الفواصل"):
        dv_h = st.number_input("ارتفاع الفاصل", value=0.0)
        dv_d = st.number_input("عمق الفاصل", value=0.0)
        dv_n = st.number_input("عدد الفواصل", value=0)
        
    with st.expander("🗄️ تفاصيل الأدراج"):
        dr_w = st.number_input("عرض الدرج", value=0.0)
        dr_d = st.number_input("عمق الدرج", value=0.0)
        dr_n = st.number_input("عدد الأدراج", value=0)

    if st.button("💾 إضافة الوحدة"):
        st.session_state.project_storage.append({
            'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
            'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
            'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
            'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
        })
        st.rerun()

# --- الحسابات والجرد (نفس كودك بالظبط) ---
if st.session_state.project_storage:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 جرد الخامات"):
            m_total, t_total, f_total = 0, 0, 0
            for u in st.session_state.project_storage:
                # حساب الارتفاع الصافي (التخصيم اللي أنت حددته)
                h_net = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_net, d_net = u['w'] - 5, u['d'] - 5
                
                if u['type'] == "سفلية":
                    m_total += (h_net*2) + (w_net*3) + (d_net*2)
                    t_total += (h_net*2) + (w_net*1) + (d_net*2)
                else:
                    m_total += (h_net*2) + (w_net*2)
                    t_total += (h_net*2) + (w_net*2) + (d_net*4)
                
                # إضافات الرفوف والفواصل والأدراج من كودك
                m_total += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
                m_total += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
                m_total += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']
            
            st.success(f"مفرد: {m_total/600:.2f} عود | متقارب: {t_total/600:.2f} عود")

    # عرض الفاتورة التفصيلية
    for u in st.session_state.project_storage:
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5
        
        report = f"وحدة: {u['title']} ({u['type']})\n"
        report += f"المقاس الكلي: {u['w']} × {u['h']} × {u['d']}\n"
        report += "-"*30 + "\n"
        report += f"✅ هيكل الألومنيوم:\n- الارتفاع: {h_baky}\n- العرض: {w_baky}\n- العمق: {d_baky}\n"
        
        if u['sh_n'] > 0:
            report += f"✅ الرفوف ({u['sh_n']}): ألومنيوم {u['sh_w']}×{u['sh_d']} | فيبر {u['sh_w']-5}×{u['sh_d']-5}\n"
        if u['dv_n'] > 0:
            report += f"✅ الفواصل ({u['dv_n']}): {u['dv_h']} × {u['dv_d']}\n"
        if u['dr_n'] > 0:
            report += f"✅ الأدراج ({u['dr_n']}): العرض {u['dr_w']-2.5} × العمق {u['dr_d']}\n"
            
        st.markdown(f'<div class="result-view">{report}</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ مسح الكل"):
        st.session_state.project_storage = []
        st.rerun()
