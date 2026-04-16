import streamlit as st

# إعدادات الصفحة وإخفاء أدوات GitHub (القطة)
st.set_page_config(page_title="نظام تخصيم الألومنيوم - المهندس ياسين علاء", layout="wide")

st.markdown("""
    <style>
    /* إخفاء القطة والشريط العلوي والقوائم تماماً */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* تنسيق الواجهة لتشبه نسخة الكمبيوتر اللي بعتها */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* المربع الأسود اللي كان في الصورة */
    .header-label {
        background-color: #2f3640;
        color: #fbc531;
        font-size: 24pt;
        font-weight: bold;
        padding: 20px;
        text-align: center;
        border-bottom: 4px solid #e1b12c;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    /* صندوق النتائج (زي نسخة PyQt5) */
    .result-sheet {
        background-color: #ffffff;
        color: #1e272e !important;
        border: 2px solid #2ecc71;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 12pt;
        border-radius: 5px;
        white-space: pre-wrap;
        margin-top: 10px;
    }

    /* تحسين الأزرار */
    div.stButton > button {
        width: 100%;
        font-weight: bold;
        height: 3em;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي (نفس النص في كودك)
st.markdown('<div class="header-label">نظام تخصيم الألومنيوم - نسخة المهندس ياسين علاء</div>', unsafe_allow_html=True)

# مخزن البيانات (Project Storage)
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- منطقة المدخلات (نفس الترتيب والأسماء في كودك) ---
with st.sidebar:
    st.header("📝 مدخلات المقاسات")
    unit_title = st.text_input("اسم الوحدة", "وحدة")
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    col_w, col_h, col_d = st.columns(3)
    with col_w: w = st.number_input("العرض", value=0.0)
    with col_h: h = st.number_input("الارتفاع", value=0.0)
    with col_d: d = st.number_input("العمق", value=0.0)
    
    with st.expander("🧱 الرفوف"):
        sh_w = st.number_input("الرف (عرض)", value=0.0)
        sh_d = st.number_input("الرف (عمق)", value=0.0)
        sh_n = st.number_input("الرفوف (عدد)", value=0)
        
    with st.expander("📐 الفواصل"):
        dv_h = st.number_input("الفاصل (ارتفاع)", value=0.0)
        dv_d = st.number_input("الفاصل (عمق)", value=0.0)
        dv_n = st.number_input("الفواصل (عدد)", value=0)
        
    with st.expander("🗄️ الأدراج"):
        dr_w = st.number_input("الدرج (عرض)", value=0.0)
        dr_d = st.number_input("الدرج (عمق)", value=0.0)
        dr_n = st.number_input("الأدراج (عدد)", value=0)

    if st.button("💾 إضافة للجدول (Enter)"):
        u = {
            'title': unit_title, 'type': unit_type, 'w': w, 'h': h, 'd': d,
            'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
            'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
            'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
        }
        st.session_state.project_storage.append(u)
        st.rerun()

# --- أزرار الجرد (نفس الشكل والألوان) ---
c1, c2 = st.columns(2)
with c1:
    if st.button("📊 جرد خامات المشروع (فاتورة قص)"):
        m_sum, t_sum, f_area = 0, 0, 0
        for u in st.session_state.project_storage:
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b, d_b = u['w'] - 5, u['d'] - 5
            if u['type'] == "سفلية":
                m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                f_area += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                f_area += (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
            # إضافات الرفوف والفواصل والأدراج (من كودك بالظبط)
            m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
            f_area += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n'] + (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
            m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']
            
        st.warning(f"""
        📊 جرد خامات المشروع:
        - ألومنيوم مفرد: {m_sum/600:.2f} عود
        - ألومنيوم متقارب: {t_sum/600:.2f} عود
        - فيبر (2.8*1.3): {f_area/36400:.2f} لوح
        """)

with c2:
    if st.button("🗑️ مسح الكل"):
        st.session_state.project_storage = []
        st.rerun()

# --- عرض نتائج التخصيم (نفس التنسيق اللي في الـ result_sheet) ---
if st.session_state.project_storage:
    st.subheader("📋 فاتورة التخصيم")
    full_report = ""
    for u in st.session_state.project_storage:
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5
        
        txt = f"\n📦 {u['title']} | {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
        txt += "━" * 55 + "\n"
        txt += f"📐 [1] تخصيم الألومنيوم (2*8):\n"
        if u['type'] == "سفلية":
            txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n  - عــــرض {w_baky}: [3 مفرد] [1 متقارب]\n  - عمــــق {d_baky}: [2 مفرد] [2 متقارب]\n"
        else:
            txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n  - عــــرض {w_baky}: [2 مفرد] [2 متقارب]\n  - عمــــق {d_baky}: [4 متقارب]\n"
        
        txt += f"\n🪵 [2] تخصيم الفيبر (التقطيع):\n  - ضهرية: {w_baky} × {h_baky} (1)\n  - أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n  - أجناب: {h_baky} × {d_baky} (2)\n"
        
        if u['sh_n'] > 0:
            txt += f"\n🧱 [3] الرفوف ({u['sh_n']}):\n  - ألومنيوم: {u['sh_w']} × {u['sh_n']*2} قطعة | {u['sh_d']} × {u['sh_n']*2} قطعة [مفرد]\n  - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5} ({u['sh_n']} قطعة)\n"
        
        if u['dr_n'] > 0:
            txt += f"\n🗄️ [5] الأدراج ({u['dr_n']}):\n  - ألومنيوم العرض: {u['dr_w']-2.5} × {u['dr_n']*2} | العمق: {u['dr_d']} × {u['dr_n']*2}\n"
        
        txt += "━" * 55 + "\n"
        st.markdown(f'<div class="result-sheet">{txt}</div>', unsafe_allow_html=True)
        full_report += txt

    st.info("💡 للحفظ PDF: استخدم خاصية الطباعة (Print) من المتصفح واختار Save as PDF.")
else:
    st.info("أدخل المقاسات من القائمة الجانبية لبدء الشغل.")
