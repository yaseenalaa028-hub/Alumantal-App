import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# 1. إعدادات الصفحة وإخفاء القطة (الـ CSS الاحترافي)
st.set_page_config(page_title="نظام تخصيم الألومنيوم - المهندس ياسين علاء", layout="wide")

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
        font-size: 20pt;
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
        font-size: 11pt;
        border-radius: 5px;
        white-space: pre-wrap;
        margin-bottom: 10px;
    }
    div.stButton > button {
        width: 100%;
        font-weight: bold;
        height: 3em;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-label">برمجة المهندس ياسين علاء</div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- منطقة المدخلات (نفس كود الـ PyQt5 بالظبط) ---
with st.sidebar:
    st.header("📝 مدخلات المقاسات")
    unit_title = st.text_input("اسم الوحدة", "وحدة")
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    w = st.number_input("العرض الكلي", value=0.0)
    h = st.number_input("الارتفاع الكلي", value=0.0)
    d = st.number_input("العمق الكلي", value=0.0)
    
    st.subheader("🧱 الرفوف")
    sh_w = st.number_input("الرف (عرض)", value=0.0)
    sh_d = st.number_input("الرف (عمق)", value=0.0)
    sh_n = st.number_input("الرفوف (عدد)", value=0)
    
    st.subheader("📐 الفواصل")
    dv_h = st.number_input("الفاصل (ارتفاع)", value=0.0)
    dv_d = st.number_input("الفاصل (عمق)", value=0.0)
    dv_n = st.number_input("الفواصل (عدد)", value=0)
    
    st.subheader("🗄️ الأدراج")
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

# --- وظيفة إنشاء الـ PDF ---
def download_pdf(storage):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Kitchen Report - Eng. Yassin Alaa", ln=1, align='C')
    for u in storage:
        hb = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        txt = f"Unit: {u['title']} | Type: {u['type']} | W:{u['w']} H:{u['h']} D:{u['d']}\n"
        txt += f"Result: W:{u['w']-5} H:{hb} D:{u['d']-5}"
        pdf.multi_cell(0, 10, txt=txt)
        pdf.cell(200, 5, txt="-"*50, ln=1)
    return pdf.output(dest='S').encode('latin-1')

# --- عرض النتائج والجرد (نفس ترتيب كودك) ---
if st.session_state.project_storage:
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📊 جرد خامات المشروع"):
            m, t, f = 0, 0, 0
            for u in st.session_state.project_storage:
                h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_b, d_b = u['w'] - 5, u['d'] - 5
                if u['type'] == "سفلية":
                    m += (h_b*2)+(w_b*3)+(d_b*2); t += (h_b*2)+(w_b*1)+(d_b*2)
                    f += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
                else:
                    m += (h_b*2)+(w_b*2); t += (h_b*2)+(w_b*2)+(d_b*4)
                    f += (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
                m += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
                m += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
                f += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n'] + (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
                m += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']
            
            st.warning(f"مفرد: {m/600:.2f} عود | متقارب: {t/600:.2f} عود | فيبر: {f/36400:.2f} لوح")

    with col_b:
        pdf_bytes = download_pdf(st.session_state.project_storage)
        st.download_button("💾 حفظ فاتورة PDF", pdf_bytes, "report.pdf", "application/pdf")

    # تفاصيل التخصيم لكل وحدة (نفس الـ Print في كودك)
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
        
        txt += f"\n🪵 [2] تخصيم الفيبر:\n  - ضهرية: {w_baky} × {h_baky} (1)\n  - أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n  - أجناب: {h_baky} × {d_baky} (2)\n"
        
        if u['sh_n'] > 0:
            txt += f"\n🧱 [3] الرفوف ({u['sh_n']}):\n  - ألومنيوم: {u['sh_w']} × {u['sh_n']*2} | {u['sh_d']} × {u['sh_n']*2} [مفرد]\n  - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5}\n"
        
        if u['dr_n'] > 0:
            txt += f"\n🗄️ [5] الأدراج ({u['dr_n']}):\n  - ألومنيوم العرض: {u['dr_w']-2.5} × {u['dr_n']*2} | العمق: {u['dr_d']} × {u['dr_n']*2}\n"
        
        st.markdown(f'<div class="result-view">{txt}</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ مسح الكل"):
        st.session_state.project_storage = []
        st.rerun()
