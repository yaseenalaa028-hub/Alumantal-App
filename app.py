import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="نظام تخصيم الألومنيوم PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .welcome-box {
        background-color: #2c3e50;
        color: white;
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .start-btn button {
        background-color: #27ae60 !important;
        color: white !important;
        font-size: 24px !important;
        height: 70px !important;
        width: 300px !important;
        border-radius: 15px !important;
        margin-top: 20px;
        border: none;
    }
    .unit-card {
        background-color: #ffffff;
        border-right: 5px solid #3498db;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (Navigation & Storage)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- الصفحة الأولى: الواجهة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown("""
        <div class="welcome-box">
            <h1>🏗️ نظام تخصيم الألومنيوم والفيبر</h1>
            <p style="font-size: 1.2em;">النسخة الاحترافية المخصصة للورش والمصانع</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("🚀 ابدأ التخصيم"):
            st.session_state.page = 'work'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: واجهة الشغل ---
else:
    with st.sidebar:
        if st.button("🏠 العودة للرئيسية"):
            st.session_state.page = 'home'
            st.rerun()
        st.divider()
        st.header("⚙️ إضافة وحدة جديدة")
        u_title = st.text_input("اسم الوحدة")
        u_type = st.selectbox("النوع", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        u_w = st.number_input("العرض الكلي", min_value=0.0)
        u_h = st.number_input("الارتفاع الكلي", min_value=0.0)
        u_d = st.number_input("العمق الكلي", min_value=0.0)
        
        with st.expander("➕ الرفوف والفواصل والأدراج"):
            s_n = st.number_input("عدد الرفوف", min_value=0)
            s_w = st.number_input("عرض الرف", min_value=0.0)
            s_d = st.number_input("عمق الرف", min_value=0.0)
            st.divider()
            v_n = st.number_input("عدد الفواصل", min_value=0)
            v_h = st.number_input("ارتفاع الفاصل", min_value=0.0)
            v_d = st.number_input("عمق الفاصل", min_value=0.0)
            st.divider()
            d_n = st.number_input("عدد الأدراج", min_value=0)
            d_w = st.number_input("عرض الدرج", min_value=0.0)
            d_d = st.number_input("عمق الدرج", min_value=0.0)

        if st.button("💾 حفظ للجدول", use_container_width=True):
            if u_w > 0 and u_h > 0:
                st.session_state.project_storage.append({
                    'title': u_title or f"وحدة {len(st.session_state.project_storage)+1}",
                    'type': u_type, 'w': u_w, 'h': u_h, 'd': u_d,
                    'sh_n': s_n, 'sh_w': s_w, 'sh_d': s_d,
                    'dv_n': v_n, 'dv_h': v_h, 'dv_d': v_d,
                    'dr_n': d_n, 'dr_w': d_w, 'dr_d': d_d
                })
                st.success("تم الحفظ!")
            else:
                st.error("أدخل المقاسات!")

    # عرض النتائج والجرد
    st.header("📊 لوحة تحكم التخصيم")
    
    if st.session_state.project_storage:
        col_act1, col_act2 = st.columns([2, 1])
        with col_act1:
            if st.button("📋 عرض فاتورة جرد خامات المشروع بالكامل", type="primary"):
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
                    m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
                    f_area += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n'] + (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
                    m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']

                st.markdown(f"""
                <div style="background-color:#1e272e; color:#f1c40f; padding:20px; border-radius:10px;">
                    <h3>📊 الجرد النهائي:</h3>
                    • ألومنيوم مفرد: <b>{m_sum/600:.2f}</b> عود<br>
                    • ألومنيوم متقارب: <b>{t_sum/600:.2f}</b> عود<br>
                    • فيبر (2.8*1.3): <b>{f_area/36400:.2f}</b> لوح
                </div>
                """, unsafe_allow_html=True)
        
        with col_act2:
            if st.button("🗑️ مسح المشروع"):
                st.session_state.project_storage = []
                st.rerun()

        st.divider()
        
        # تقسيم الشاشة بين الجدول وبيان التقطيع
        view_l, view_r = st.columns([6, 4])
        
        with view_r:
            st.subheader("📋 جدول الوحدات")
            st.table(pd.DataFrame(st.session_state.project_storage)[['title', 'w', 'h', 'd']])

        with view_l:
            st.subheader("🪚 بيان التقطيع التفصيلي")
            for u in st.session_state.project_storage:
                h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_baky, d_baky = u['w'] - 5, u['d'] - 5
                
                txt = f"📦 {u['title']} | النوع: {u['type']}\n"
                txt += "━" * 40 + "\n"
                txt += f"📐 ألومنيوم الهيكل:\n  - ارتفاع {h_baky} | عرض {w_baky} | عمق {d_baky}\n"
                txt += f"🪵 فيبر التقطيع:\n  - ضهر {w_baky}x{h_baky} | أرضية {w_baky}x{d_baky} | جنب {h_baky}x{d_baky}\n"
                if u['sh_n'] > 0: txt += f"🧱 الرفوف ({u['sh_n']}): {u['sh_w']}x{u['sh_d']}\n"
                if u['dv_n'] > 0: txt += f"📐 الفواصل ({u['dv_n']}): {u['dv_h']}x{u['dv_d']}\n"
                if u['dr_n'] > 0: txt += f"🗄️ الأدراج ({u['dr_n']}): عرض {u['dr_w']-2.5}\n"
                
                st.code(txt, language="text")
    else:
        st.info("أضف وحدات من القائمة الجانبية للبدء")
