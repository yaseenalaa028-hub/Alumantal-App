
import streamlit as st

# إعدادات الصفحة وحل مشكلة الموبايل
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
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
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

st.markdown('<div class="header-label">نظام تخصيم الألومنيوم - المهندس ياسين علاء</div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False

# زرار الإضافة الرئيسي
if st.button("➕ إضافة مقاسات جديدة"):
    st.session_state.show_inputs = not st.session_state.show_inputs

# --- منطقة المدخلات ---
if st.session_state.show_inputs:
    with st.container():
        st.subheader("📝 بيانات الوحدة الجديدة")
        u_title = st.text_input("اسم الوحدة", placeholder="مثال: وحدة حوض")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        
        c1, c2, c3 = st.columns(3)
        with c1: w = st.number_input("العرض الكلي (W)", value=0.0, placeholder="W")
        with c2: h = st.number_input("الارتفاع الكلي (H)", value=0.0, placeholder="H")
        with c3: d = st.number_input("العمق الكلي (D)", value=0.0, placeholder="D")
        
        with st.expander("🧱 الرفوف"):
            rs1, rs2, rs3 = st.columns(3)
            with rs1: sh_w = st.number_input("عرض الرف", value=0.0, key="shw")
            with rs2: sh_d = st.number_input("عمق الرف", value=0.0, key="shd")
            with rs3: sh_n = st.number_input("عدد الرفوف", value=0, key="shn")
            
        with st.expander("📐 الفواصل"):
            dv1, dv2, dv3 = st.columns(3)
            with dv1: dv_h = st.number_input("ارتفاع الفاصل", value=0.0, key="dvh")
            with dv2: dv_d = st.number_input("عمق الفاصل", value=0.0, key="dvd")
            with dv3: dv_n = st.number_input("عدد الفواصل", value=0, key="dvn")
            
        with st.expander("🗄️ الأدراج"):
            dr1, dr2, dr3 = st.columns(3)
            with dr1: dr_w = st.number_input("عرض الدرج", value=0.0, key="drw")
            with dr2: dr_d = st.number_input("عمق الدرج", value=0.0, key="drd")
            with dr3: dr_n = st.number_input("عدد الأدراج", value=0, key="drn")

        if st.button("💾 اعتماد الإضافة"):
            st.session_state.project_storage.append({
                'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
                'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
            })
            st.session_state.show_inputs = False
            st.rerun()

# --- عرض التقرير المفصل ---
if st.session_state.project_storage:
    st.divider()
    col_x, col_y = st.columns(2)
    with col_x:
        if st.button("📊 جرد خامات المشروع"):
            m_sum, t_sum = 0, 0
            for u in st.session_state.project_storage:
                h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_b, d_b = u['w'] - 5, u['d'] - 5
                if u['type'] == "سفلية":
                    m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                else:
                    m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(w_b*2)+(d_b*4)
            st.warning(f"مفرد: {m_sum/600:.2f} عود | متقارب: {t_sum/600:.2f} عود")

    with col_y:
        if st.button("🗑️ مسح الجدول"):
            st.session_state.project_storage = []
            st.rerun()

    for u in st.session_state.project_storage:
        # حسابات التخصيم الدقيقة
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky = u['w'] - 5
        d_baky = u['d'] - 5
        
        # ترتيب التقرير بشكل احترافي
        report = f"📦 الوحدة: {u['title']} | النوع: {u['type']}\n"
        report += f"📏 المقاس الأصلي: {u['w']} عرض × {u['h']} ارتفاع × {u['d']} عمق\n"
        report += "━" * 50 + "\n"
        
        # 1. تخصيم الألومنيوم
        report += "🛠️ أولاً: تخصيم الألومنيوم (2*8):\n"
        if u['type'] == "سفلية":
            report += f" - الارتفاع {h_baky}: [2 مفرد] | [2 متقارب]\n"
            report += f" - العــــرض {w_baky}: [3 مفرد] | [1 متقارب]\n"
            report += f" - العمــــق {d_baky}: [2 مفرد] | [2 متقارب]\n"
        else:
            report += f" - الارتفاع {h_baky}: [2 مفرد] | [2 متقارب]\n"
            report += f" - العــــرض {w_baky}: [2 مفرد] | [2 متقارب]\n"
            report += f" - العمــــق {d_baky}: [4 متقارب]\n"
            
        # 2. تخصيم الفيبر
        report += f"\n🪵 ثانياً: تقطيع الفيبر:\n"
        report += f" - ضهرية: {w_baky} × {h_baky} (عدد 1)\n"
        report += f" - أرضية: {w_baky} × {d_baky} (عدد {'1' if u['type']=='سفلية' else '2'})\n"
        report += f" - أجناب: {h_baky} × {d_baky} (عدد 2)\n"
        
        # 3. الرفوف (لو موجودة)
        if u['sh_n'] > 0:
            report += f"\n🧱 ثالثاً: الرفوف (عدد {u['sh_n']}):\n"
            report += f" - ألومنيوم: عرض {u['sh_w']} × عمق {u['sh_d']} [مفرد]\n"
            report += f" - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5}\n"
            
        # 4. الفواصل (لو موجودة)
        if u['dv_n'] > 0:
            report += f"\n📐 رابعاً: الفواصل (عدد {u['dv_n']}):\n"
            report += f" - ألومنيوم: ارتفاع {u['dv_h']} × عمق {u['dv_d']}\n"

        # 5. الأدراج (لو موجودة)
        if u['dr_n'] > 0:
            report += f"\n🗄️ خامساً: الأدراج (عدد {u['dr_n']}):\n"
            report += f" - عرض الدرج (صافي): {u['dr_w']-2.5}\n"
            report += f" - عمق الدرج: {u['dr_d']}\n"
            
        st.markdown(f'<div class="result-view">{report}</div>', unsafe_allow_html=True)
