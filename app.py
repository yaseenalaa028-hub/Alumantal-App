import streamlit as st

# 1. إعدادات الصفحة والستايل الاحترافي
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
        margin-bottom: 20px;
    }
    .result-view {
        background-color: #ffffff;
        color: #1e272e !important;
        border: 2px solid #2ecc71;
        padding: 20px;
        font-family: 'Courier New', monospace;
        font-size: clamp(10pt, 3vw, 12pt);
        border-radius: 8px;
        white-space: pre-wrap;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    div.stButton > button {
        width: 100%;
        background-color: #27ae60 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-label">نظام تخصيم الألومنيوم وجرد الخامات<br>برمجة المهندس ياسين علاء</div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False

# زرار الإضافة الرئيسي
if st.button("➕ إضافة مقاسات جديدة"):
    st.session_state.show_inputs = not st.session_state.show_inputs

# --- شاشة الإدخال ---
if st.session_state.show_inputs:
    with st.container():
        st.subheader("📝 إدخال بيانات الوحدة")
        u_name = st.text_input("اسم الوحدة", placeholder="اكتب اسم الوحدة...")
        u_type = st.selectbox("نوع القطعة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        
        c1, c2, c3 = st.columns(3)
        with c1: w = st.number_input("العرض (W)", value=0.0, placeholder="العرض")
        with c2: h = st.number_input("الارتفاع (H)", value=0.0, placeholder="الارتفاع")
        with c3: d = st.number_input("العمق (D)", value=0.0, placeholder="العمق")
        
        with st.expander("🧱 الرفوف"):
            rs1, rs2, rs3 = st.columns(3)
            with rs1: sh_w = st.number_input("عرض الرف", value=0.0, key="shw", placeholder="العرض")
            with rs2: sh_d = st.number_input("عمق الرف", value=0.0, key="shd", placeholder="العمق")
            with rs3: sh_n = st.number_input("عدد الرفوف", value=0, key="shn")
            
        with st.expander("📐 الفواصل"):
            dv1, dv2, dv3 = st.columns(3)
            with dv1: dv_h = st.number_input("ارتفاع الفاصل", value=0.0, key="dvh", placeholder="الارتفاع")
            with dv2: dv_d = st.number_input("عمق الفاصل", value=0.0, key="dvd", placeholder="العمق")
            with dv3: dv_n = st.number_input("عدد الفواصل", value=0, key="dvn")
            
        with st.expander("🗄️ الأدراج"):
            dr1, dr2, dr3 = st.columns(3)
            with dr1: dr_w = st.number_input("عرض الدرج", value=0.0, key="drw", placeholder="العرض")
            with dr2: dr_d = st.number_input("عمق الدرج", value=0.0, key="drd", placeholder="العمق")
            with dr3: dr_n = st.number_input("عدد الأدراج", value=0, key="drn")

        if st.button("💾 حفظ البيانات"):
            st.session_state.project_storage.append({
                'name': u_name, 'type': u_type, 'w': w, 'h': h, 'd': d,
                'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
                'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
            })
            st.session_state.show_inputs = False
            st.rerun()

# --- جرد الخامات والتقرير الفني ---
if st.session_state.project_storage:
    st.divider()
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        if st.button("📊 جرد خامات المشروع (شامل الفيبر)"):
            m_sum, t_sum, f_area = 0, 0, 0
            for u in st.session_state.project_storage:
                h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_b, d_b = u['w'] - 5, u['d'] - 5
                
                # جرد الألومنيوم
                if u['type'] == "سفلية":
                    m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                else:
                    m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                
                # جرد الفيبر (الأساسي)
                f_area += (w_b * h_b) # الضهرية
                f_area += (w_b * d_b * (1 if u['type']=="سفلية" else 2)) # الأرضية/السقف
                f_area += (h_b * d_b * 2) # الأجناب
                
                # جرد الرفوف والفواصل
                m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
                f_area += (u['sh_w']-5) * (u['sh_d']-5) * u['sh_n']
                m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
                f_area += (u['dv_h']-5) * (u['dv_d']-5) * u['dv_n']
                m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']

            st.warning(f"""
            📊 جرد إجمالي المشروع:
            - ألومنيوم مفرد: {m_sum/600:.2f} عود
            - ألومنيوم متقارب: {t_sum/600:.2f} عود
            - ألواح فيبر (2.8*1.3): {f_area/36400:.2f} لوح
            """)

    with col_j2:
        if st.button("🗑️ مسح الكل"):
            st.session_state.project_storage = []
            st.rerun()

    for u in st.session_state.project_storage:
        h_net = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_net, d_net = u['w'] - 5, u['d'] - 5
        
        rep = f"📋 فاتورة تقطيع: {u['name']} | نوع: {u['type']}\n"
        rep += "━" * 50 + "\n"
        rep += f"🛠️ قطعيات الألومنيوم (2*8):\n"
        if u['type'] == "سفلية":
            rep += f" - ارتفاع {h_net}: [2 مفرد] [2 متقارب]\n - عرض {w_net}: [3 مفرد] [1 متقارب]\n - عمق {d_net}: [2 مفرد] [2 متقارب]\n"
        else:
            rep += f" - ارتفاع {h_net}: [2 مفرد] [2 متقارب]\n - عرض {w_net}: [2 مفرد] [2 متقارب]\n - عمق {d_net}: [4 متقارب]\n"

        rep += f"\n🪵 قطعيات الفيبر:\n"
        rep += f" - ضهرية: {w_net} × {h_net} (1)\n"
        rep += f" - أرضية: {w_net} × {d_net} ({'1' if u['type']=='سفلية' else '2'})\n"
        rep += f" - أجناب: {h_net} × {d_net} (2)\n"
        
        if u['sh_n'] > 0:
            rep += f"\n🧱 الرفوف ({u['sh_n']}): فيبر {u['sh_w']-5} × {u['sh_d']-5}\n"
        if u['dr_n'] > 0:
            rep += f"\n🗄️ الأدراج ({u['dr_n']}): عرض {u['dr_w']-2.5} × عمق {u['dr_d']}\n"
            
        st.markdown(f'<div class="result-view">{rep}</div>', unsafe_allow_html=True)
