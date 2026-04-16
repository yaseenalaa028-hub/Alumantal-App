import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيم الألومنيوم - المهندس ياسين علاء", layout="wide")

# كود سحري لإخفاء القطة (GitHub) وأي علامات برمجية
st.markdown("""
    <style>
    /* إخفاء شريط الأدوات العلوي بالكامل بما فيه القطة والقائمة */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* منع المستخدم من عمل Fork أو رؤية الكود */
    .stDeployButton {display:none;}
    
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .main {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .unit-card {
        background-color: #ffffff !important;
        color: #1e272e !important;
        padding: 15px;
        border: 2px solid #27ae60;
        border-radius: 10px;
        margin-bottom: 15px;
        font-family: monospace;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    .header-box {
        background-color: #2f3640;
        color: #fbc531;
        padding: 15px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    div.stButton > button {
        width: 100%;
        background-color: #27ae60 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        height: 3.5em;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>نظام المهندس ياسين علاء</h1><p>مصنع ضد الكسر للألومنيوم</p></div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("📝 إدخال المقاسات")
    unit_title = st.text_input("اسم الوحدة", "وحدة جديدة")
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    w = st.number_input("العرض (سم)", value=0.0)
    h = st.number_input("الارتفاع (سم)", value=0.0)
    d = st.number_input("العمق (سم)", value=0.0)
    
    with st.expander("➕ إضافات (رفوف/أدراج/فواصل)"):
        sh_n = st.number_input("عدد الرفوف", 0)
        sh_w = st.number_input("عرض الرف", 0.0)
        sh_d = st.number_input("عمق الرف", 0.0)
        st.divider()
        dv_n = st.number_input("عدد الفواصل", 0)
        dv_h = st.number_input("ارتفاع الفاصل", 0.0)
        dv_d = st.number_input("عمق الفاصل", 0.0)
        st.divider()
        dr_n = st.number_input("عدد الأدراج", 0)
        dr_w = st.number_input("عرض الدرج", 0.0)
        dr_d = st.number_input("عمق الدرج", 0.0)

    if st.button("💾 إضافة الوحدة"):
        u = {
            'title': unit_title, 'type': unit_type, 'w': w, 'h': h, 'd': d,
            'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
            'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
            'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
        }
        st.session_state.project_storage.append(u)
        st.rerun()

# --- العرض الرئيسي ---
if st.session_state.project_storage:
    st.subheader("📋 تفاصيل التخصيم")
    for idx, u in enumerate(st.session_state.project_storage):
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5

        report_text = f"📦 {u['title']} | {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
        report_text += "-"*40 + "\n"
        report_text += f"📐 ألومنيوم (2*8):\n"
        if u['type'] == "سفلية":
            report_text += f"- ارتفاع {h_baky}: (2 مفرد + 2 متقارب)\n- عرض {w_baky}: (3 مفرد + 1 متقارب)\n- عمق {d_baky}: (2 مفرد + 2 متقارب)\n"
        else:
            report_text += f"- ارتفاع {h_baky}: (2 مفرد + 2 متقارب)\n- عرض {w_baky}: (2 مفرد + 2 متقارب)\n- عمق {d_baky}: (4 متقارب)\n"
        
        report_text += f"\n🪵 تقطيع الفيبر:\n"
        report_text += f"- ضهرية: {w_baky} × {h_baky} (1)\n"
        report_text += f"- أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n"
        report_text += f"- أجناب: {h_baky} × {d_baky} (2)\n"

        if u['sh_n'] > 0:
            report_text += f"\n🧱 الرفوف ({u['sh_n']}): {u['sh_w']-5} × {u['sh_d']-5}\n"
        if u['dr_n'] > 0:
            report_text += f"\n🗄️ الأدراج ({u['dr_n']}): العرض {u['dr_w']-2.5} | العمق {u['dr_d']}\n"

        st.markdown(f'<div class="unit-card"><pre style="white-space: pre-wrap; color: #1e272e;">{report_text}</pre></div>', unsafe_allow_html=True)

    st.divider()
    if st.button("📊 حساب الجرد الكلي للمشروع"):
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
            m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            f_area += (max(0, u['sh_w']-5))*(max(0, u['sh_d']-5))*u['sh_n']
            m_sum += ((max(0, u['dr_w']-2.5))*2 + u['dr_d']*2) * u['dr_n']

        st.success(f"جرد الألومنيوم المفرد: {m_sum/600:.2f} عود | متقارب: {t_sum/600:.2f} عود | فيبر: {f_area/36400:.2f} لوح")

    if st.button("🗑️ مسح كل البيانات"):
        st.session_state.project_storage = []
        st.rerun()
else:
    st.info("أدخل بيانات الوحدة من القائمة الجانبية لبدء التخصيم.")
