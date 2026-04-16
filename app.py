import streamlit as st
from fpdf import FPDF
import base64

# إعدادات الصفحة وإخفاء أدوات GitHub
st.set_page_config(page_title="نظام تخصيم الألومنيوم - المهندس ياسين علاء", layout="wide")

# تصميم احترافي وإخفاء القطة
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
        font-size: 22pt;
        font-weight: bold;
        padding: 15px;
        text-align: center;
        border-bottom: 4px solid #e1b12c;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .result-sheet {
        background-color: #ffffff;
        color: #1e272e !important;
        border: 2px solid #27ae60;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 11pt;
        border-radius: 8px;
        white-space: pre-wrap;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    div.stButton > button {
        width: 100%;
        background-color: #27ae60 !important;
        color: white !important;
        font-weight: bold;
        height: 3.5em;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-label">نظام المهندس ياسين علاء - مصنع ضد الكسر</div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# وظيفة إنشاء ملف PDF
def create_pdf(data_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Aluminum Master Report - Eng. Yassin Alaa", ln=1, align='C')
    pdf.cell(200, 10, txt="--------------------------------------------------", ln=2, align='C')
    
    for u in data_list:
        h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        line = f"Unit: {u['title']} | Dim: {u['w']}x{u['h']}x{u['d']} | Res: {u['w']-5}x{h_b}x{u['d']-5}"
        pdf.multi_cell(0, 10, txt=line)
        pdf.cell(200, 5, txt="-"*50, ln=1)
        
    return pdf.output(dest='S').encode('latin-1')

# --- القائمة الجانبية (نفس كودك بالظبط) ---
with st.sidebar:
    st.header("📝 إدخال المقاسات")
    u_title = st.text_input("اسم الوحدة / العميل", "وحدة")
    u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    colw, colh, cold = st.columns(3)
    with colw: w = st.number_input("العرض", value=0.0)
    with colh: h = st.number_input("الارتفاع", value=0.0)
    with cold: d = st.number_input("العمق", value=0.0)
    
    with st.expander("🧱 الرفوف والأدراج"):
        sh_n = st.number_input("عدد الرفوف", value=0)
        sh_w = st.number_input("عرض الرف", value=0.0)
        sh_d = st.number_input("عمق الرف", value=0.0)
        st.divider()
        dr_n = st.number_input("عدد الأدراج", value=0)
        dr_w = st.number_input("عرض الدرج", value=0.0)
        dr_d = st.number_input("عمق الدرج", value=0.0)

    if st.button("💾 إضافة للجدول"):
        st.session_state.project_storage.append({
            'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
            'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n, 'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
        })
        st.rerun()

# --- منطقة العرض ---
if st.session_state.project_storage:
    c1, c2, c3 = st.columns([2, 2, 1])
    
    with c1:
        if st.button("📊 جرد الخامات (فاتورة قص)"):
            m, t, f = 0, 0, 0
            for u in st.session_state.project_storage:
                hb = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                wb, db = u['w'] - 5, u['d'] - 5
                if u['type'] == "سفلية":
                    m += (hb*2)+(wb*3)+(db*2); t += (hb*2)+(wb*1)+(db*2)
                else:
                    m += (hb*2)+(wb*2); t += (hb*2)+(wb*2)+(db*4)
                f += (wb*hb) + (wb*db*2) + (hb*db*2) # مساحة تقريبية
            st.success(f"المفرد: {m/600:.2f} عود | المتقارب: {t/600:.2f} عود")

    with c2:
        # زرار تحميل PDF الاحترافي
        pdf_data = create_pdf(st.session_state.project_storage)
        st.download_button(label="📥 تحميل فاتورة PDF", data=pdf_data, file_name=f"Kitchen_Report.pdf", mime="application/pdf")

    with c3:
        if st.button("🗑️ مسح"):
            st.session_state.project_storage = []
            st.rerun()

    for u in st.session_state.project_storage:
        hb = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        wb, db = u['w'] - 5, u['d'] - 5
        
        txt = f"📦 {u['title']} | {u['type']}\n"
        txt += "━" * 40 + "\n"
        txt += f"📐 تخصيم الألومنيوم:\n- ارتفاع: {hb} | عرض: {wb} | عمق: {db}\n"
        
        if u['sh_n'] > 0:
            txt += f"🧱 الرفوف ({u['sh_n']}): {u['sh_w']-5} × {u['sh_d']-5}\n"
        if u['dr_n'] > 0:
            txt += f"🗄️ الأدراج ({u['dr_n']}): {u['dr_w']-2.5} × {u['dr_d']}\n"
        
        st.markdown(f'<div class="result-sheet">{txt}</div>', unsafe_allow_html=True)
else:
    st.info("في انتظار إضافة أول وحدة..")
