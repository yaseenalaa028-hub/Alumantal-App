import streamlit as st
from fpdf import FPDF
import io

# 1. إعدادات الصفحة والستايل لمنع تقطيع الكلام
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
        padding: 15px;
        font-size: clamp(10pt, 3vw, 12pt);
        border-radius: 8px;
        white-space: pre-wrap;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    div.stButton > button {
        width: 100%;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-label">نظام تخصيم الألومنيوم - المهندس ياسين علاء</div>', unsafe_allow_html=True)

if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []
if 'show_inputs' not in st.session_state:
    st.session_state.show_inputs = False

# زرار الإضافة
if st.button("➕ إضافة مقاسات جديدة"):
    st.session_state.show_inputs = not st.session_state.show_inputs

# --- شاشة الإدخال (الخانات فاضية بدون أصفار) ---
if st.session_state.show_inputs:
    with st.container():
        st.subheader("📝 تفاصيل الوحدة")
        u_name = st.text_input("اسم العميل / الوحدة", placeholder="مثال: مطبخ المهندس أحمد")
        u_type = st.selectbox("نوع القطعة", ["سفلية", "علوية", "دولاب خزين"])
        
        c1, c2, c3 = st.columns(3)
        with c1: w = st.number_input("العرض الكلي (W)", value=None, placeholder="أدخل العرض")
        with c2: h = st.number_input("الارتفاع الكلي (H)", value=None, placeholder="أدخل الارتفاع")
        with c3: d = st.number_input("العمق الكلي (D)", value=None, placeholder="أدخل العمق")
        
        with st.expander("🧱 الرفوف"):
            rs1, rs2, rs3 = st.columns(3)
            with rs1: sh_w = st.number_input("عرض الرف", value=None, placeholder="العرض")
            with rs2: sh_d = st.number_input("عمق الرف", value=None, placeholder="العمق")
            with rs3: sh_n = st.number_input("عدد الرفوف", value=0)
            
        with st.expander("📐 الفواصل"):
            dv1, dv2, dv3 = st.columns(3)
            with dv1: dv_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="الارتفاع")
            with dv2: dv_d = st.number_input("عمق الفاصل", value=None, placeholder="العمق")
            with dv3: dv_n = st.number_input("عدد الفواصل", value=0)
            
        with st.expander("🗄️ الأدراج"):
            dr1, dr2, dr3 = st.columns(3)
            with dr1: dr_w = st.number_input("عرض الدرج", value=None, placeholder="العرض")
            with dr2: dr_d = st.number_input("عمق الدرج", value=None, placeholder="العمق")
            with dr3: dr_n = st.number_input("عدد الأدراج", value=0)

        if st.button("💾 حفظ الوحدة"):
            if w and h and d: # التأكد من إدخال المقاسات الأساسية
                st.session_state.project_storage.append({
                    'name': u_name, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'sh_w': sh_w or 0, 'sh_d': sh_d or 0, 'sh_n': sh_n or 0,
                    'dv_h': dv_h or 0, 'dv_d': dv_d or 0, 'dv_n': dv_n or 0,
                    'dr_w': dr_w or 0, 'dr_d': dr_d or 0, 'dr_n': dr_n or 0
                })
                st.session_state.show_inputs = False
                st.rerun()
            else:
                st.error("من فضلك أدخل المقاسات الأساسية (عرض، ارتفاع، عمق)")

# --- وظيفة إنشاء الـ PDF ---
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Kitchen Report - Eng. Yassin Alaa", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    for u in data:
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Unit: {u['name']} ({u['type']})", ln=True)
        pdf.cell(200, 10, txt=f"Dimensions: W:{u['w']} H:{u['h']} D:{u['d']}", ln=True)
        pdf.cell(200, 5, txt="-"*50, ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- النتائج والجرد والـ PDF ---
if st.session_state.project_storage:
    st.divider()
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("📊 جرد الخامات"):
            m_sum, t_sum, f_area = 0, 0, 0
            for u in st.session_state.project_storage:
                h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_b, d_b = u['w'] - 5, u['d'] - 5
                if u['type'] == "سفلية":
                    m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                else:
                    m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                f_area += (w_b*h_b) + (w_b*d_b*(1 if u['type']=="سفلية" else 2)) + (h_b*d_b*2)
            st.warning(f"مفرد: {m_sum/600:.2f} | متقارب: {t_sum/600:.2f} | فيبر: {f_area/36400:.2f}")

    with col_b:
        pdf_file = create_pdf(st.session_state.project_storage)
        st.download_button("💾 تحميل فاتورة PDF", pdf_file, "report.pdf", "application/pdf")

    with col_c:
        if st.button("🗑️ مسح الكل"):
            st.session_state.project_storage = []
            st.rerun()

    for u in st.session_state.project_storage:
        h_net = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_net, d_net = u['w'] - 5, u['d'] - 5
        
        rep = f"📋 فاتورة: {u['name']} | {u['type']}\n"
        rep += "━" * 40 + "\n"
        rep += f"🛠️ ألومنيوم (2*8):\n- ارتفاع: {h_net} | عرض: {w_net} | عمق: {d_net}\n"
        rep += f"🪵 فيبر:\n- ضهرية: {w_net}x{h_net} | أرضية: {w_net}x{d_net} | أجناب: {h_net}x{d_net}\n"
        
        if u['sh_n'] > 0:
            rep += f"🧱 رفوف ({u['sh_n']}): فيبر {u['sh_w']-5}x{u['sh_d']-5}\n"
        if u['dr_n'] > 0:
            rep += f"🗄️ أدراج ({u['dr_n']}): عرض {u['dr_w']-2.5}\n"
            
        st.markdown(f'<div class="result-view">{rep}</div>', unsafe_allow_html=True)
