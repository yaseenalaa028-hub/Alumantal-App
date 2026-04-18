import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (كامل العرض)
st.set_page_config(page_title="نظام تخصيم الألومنيوم PRO", layout="wide")

# تنسيق CSS مخصص للواجهة الكاملة
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
        padding: 80px;
        border-radius: 20px;
        text-align: center;
        margin: 50px auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .start-btn button {
        background-color: #27ae60 !important;
        color: white !important;
        font-size: 28px !important;
        height: 80px !important;
        width: 100% !important;
        border-radius: 15px !important;
        border: none;
    }
    .main-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة التنقل والبيانات
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- الصفحة الأولى: شاشة الترحيب ---
if st.session_state.page == 'home':
    st.markdown("""
        <div class="welcome-box">
            <h1>🏗️ نظام تخصيم الألومنيوم والفيبر</h1>
            <p style="font-size: 1.5em;">النسخة الاحترافية - إدارة كاملة للمشروعات</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    with col_s2:
        if st.button("🚀 ابدأ العمل"):
            st.session_state.page = 'work'
            st.rerun()

# --- الصفحة الثانية: شاشة العمل الكاملة (بدون شريط جانبي) ---
else:
    # هيدر الصفحة وزر العودة
    col_h1, col_h2 = st.columns([8, 2])
    col_h1.title("🛠️ لوحة عمليات التخصيم")
    if col_h2.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

    st.divider()

    # قسم الإدخال في الشاشة الرئيسية (Main Screen Inputs)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("📝 إدخال بيانات الوحدة")
        
        c_top1, c_top2 = st.columns([3, 1])
        u_title = c_top1.text_input("اسم الوحدة", placeholder="مثال: وحدة مطبخ علوي")
        u_type = c_top2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        
        c_dim1, c_dim2, c_dim3 = st.columns(3)
        u_w = c_dim1.number_input("العرض الكلي (سم)", min_value=0.0, step=0.1)
        u_h = c_dim2.number_input("الارتفاع الكلي (سم)", min_value=0.0, step=0.1)
        u_d = c_dim3.number_input("العمق الكلي (سم)", min_value=0.0, step=0.1)

        with st.expander("🛠️ إضافات (رفوف، فواصل، أدراج)"):
            c_sh1, c_sh2, c_sh3 = st.columns(3)
            s_n = c_sh1.number_input("عدد الرفوف", min_value=0, step=1)
            s_w = c_sh2.number_input("عرض الرف", min_value=0.0)
            s_d = c_sh3.number_input("عمق الرف", min_value=0.0)
            
            st.divider()
            c_dv1, c_dv2, c_dv3 = st.columns(3)
            v_n = c_dv1.number_input("عدد الفواصل", min_value=0, step=1)
            v_h = c_dv2.number_input("ارتفاع الفاصل", min_value=0.0)
            v_d = c_dv3.number_input("عمق الفاصل", min_value=0.0)
            
            st.divider()
            c_dr1, c_dr2, c_dr3 = st.columns(3)
            d_n = c_dr1.number_input("عدد الأدراج", min_value=0, step=1)
            d_w = c_dr2.number_input("عرض الدرج", min_value=0.0)
            d_d = c_dr3.number_input("عمق الدرج", min_value=0.0)

        # أزرار الإضافة والمسح
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("💾 حفظ الوحدة وإضافتها للجدول", type="primary"):
            if u_w > 0 and u_h > 0:
                st.session_state.project_storage.append({
                    'title': u_title or f"وحدة {len(st.session_state.project_storage)+1}",
                    'type': u_type, 'w': u_w, 'h': u_h, 'd': u_d,
                    'sh_n': s_n, 'sh_w': s_w, 'sh_d': s_d,
                    'dv_n': v_n, 'dv_h': v_h, 'dv_d': v_d,
                    'dr_n': d_n, 'dr_w': d_w, 'dr_d': d_d
                })
                st.success("✅ تم حفظ البيانات بنجاح")
            else:
                st.error("⚠️ يرجى إدخال الطول والعرض")
        
        if col_b2.button("🗑️ مسح كل الوحدات"):
            st.session_state.project_storage = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- عرض النتائج والجرد ---
    if st.session_state.project_storage:
        st.divider()
        
        # زر الجرد الإجمالي (فاتورة القص)
        if st.button("📊 إصدار فاتورة جرد خامات المشروع بالكامل", type="secondary"):
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
                <div style="background-color: #1e272e; color: #f1c40f; padding: 25px; border-radius: 15px; border: 2px solid #f1c40f; margin-top: 20px;">
                    <h2 style="text-align: center;">📊 تقرير الجرد النهائي للمشروع</h2>
                    <hr style="border-color: #f1c40f;">
                    <p style="font-size: 1.3em;">📏 ألومنيوم مفرد: <b>{m_sum/600:.2f}</b> عود</p>
                    <p style="font-size: 1.3em;">📏 ألومنيوم متقارب: <b>{t_sum/600:.2f}</b> عود</p>
                    <p style="font-size: 1.3em;">🪵 فيبر (2.8*1.3): <b>{f_area/36400:.2f}</b> لوح</p>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        
        # عرض الجداول والتقطيع
        view_col1, view_col2 = st.columns([6, 4])
        
        with view_col2:
            st.subheader("📋 الوحدات المضافة")
            st.table(pd.DataFrame(st.session_state.project_storage)[['title', 'w', 'h', 'd']])

        with view_col1:
            st.subheader("🪚 تفاصيل التقطيع (كل بند على حدة)")
            for u in st.session_state.project_storage:
                h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_baky, d_baky = u['w'] - 5, u['d'] - 5
                
                with st.expander(f"📌 {u['title']} - تفاصيل القص", expanded=True):
                    txt = f"📐 ألومنيوم الهيكل:\n  - ارتفاع: {h_baky} سم\n  - عرض: {w_baky} سم\n  - عمق: {d_baky} سم\n\n"
                    txt += f"🪵 الفيبر:\n  - ضهر: {w_baky}x{h_baky}\n  - أرضية: {w_baky}x{d_baky}\n  - أجناب: {h_baky}x{d_baky}\n\n"
                    
                    if u['sh_n'] > 0: txt += f"🧱 الرفوف ({u['sh_n']}): {u['sh_w']}x{u['sh_d']}\n"
                    if u['dv_n'] > 0: txt += f"📐 الفواصل ({u['dv_n']}): {u['dv_h']}x{u['dv_d']}\n"
                    if u['dr_n'] > 0: txt += f"🗄️ الأدراج ({u['dr_n']}): عرض {u['dr_w']-2.5}\n"
                    
                    st.code(txt, language="text")
    else:
        st.info("💡 لا توجد وحدات حالياً، ابدأ بإدخال مقاسات أول وحدة بالأعلى.")
