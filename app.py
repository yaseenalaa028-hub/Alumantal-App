import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة كاملة العرض (بدون شريط جانبي)
st.set_page_config(page_title="نظام تخصيم الألومنيوم والفيبر PRO", layout="wide")

# 2. تنسيق الواجهة والجداول (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .main-header { 
        background-color: #2c3e50; color: white; padding: 30px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px; 
    }
    .unit-card {
        background-color: #ffffff;
        border: 2px solid #e0e0e0;
        border-right: 10px solid #2980b9;
        padding: 20px;
        margin-bottom: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .unit-title-text { color: #2c3e50; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    th { background-color: #34495e !important; color: white !important; text-align: center !important; }
    td { text-align: center !important; font-weight: bold !important; font-size: 16px !important; }
    .total-summary { 
        background-color: #1e272e; color: #f1c40f; padding: 25px; 
        border-radius: 15px; text-align: center; border: 2px solid #f1c40f; 
        margin-top: 40px;
    }
    .stNumberInput label, .stTextInput label, .stSelectbox label { font-weight: bold !important; color: #2c3e50 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة الحالة (البيانات والصفحات)
if 'started' not in st.session_state:
    st.session_state.started = False
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- الشاشة الأولى: صفحة الترحيب ---
if not st.session_state.started:
    st.markdown('<div class="main-header"><h1>🏗️ نظام تخصيم الألومنيوم والفيبر</h1><h3>نسخة الورشة الاحترافية - جداول متتالية ودقيقة</h3></div>', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    with col_s2:
        if st.button("🚀 ابدأ التخصيم الآن", use_container_width=True):
            st.session_state.started = True
            st.rerun()

# --- الشاشة الثانية: لوحة العمل ---
else:
    col_h1, col_h2 = st.columns([8, 2])
    col_h1.title("🛠️ إدخال المقاسات والحسابات")
    if col_h2.button("🏠 العودة للرئيسية"):
        st.session_state.started = False
        st.rerun()

    st.divider()

    # 4. قسم المدخلات التفصيلي (كل الخانات)
    with st.expander("📝 إدخال بيانات وحدة جديدة", expanded=True):
        row1_1, row1_2, row1_3, row1_4, row1_5 = st.columns([2, 1, 1, 1, 1])
        u_title = row1_1.text_input("اسم الوحدة")
        u_type = row1_2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        u_w = row1_3.number_input("العرض الكلي (W)", min_value=0.0, step=0.1)
        u_h = row1_4.number_input("الارتفاع الكلي (H)", min_value=0.0, step=0.1)
        u_d = row1_5.number_input("العمق الكلي (D)", min_value=0.0, step=0.1)

        st.markdown("##### 🧱 تفاصيل الإضافات:")
        
        # خانات الرفوف
        st.write("**• الرفوف:**")
        sh_c1, sh_c2, sh_c3 = st.columns(3)
        sh_n = sh_c1.number_input("عدد الرفوف", min_value=0, step=1)
        sh_w = sh_c2.number_input("عرض الرف", min_value=0.0, step=0.1)
        sh_d = sh_c3.number_input("عمق الرف", min_value=0.0, step=0.1)

        # خانات الفواصل
        st.write("**• الفواصل:**")
        dv_c1, dv_c2, dv_c3 = st.columns(3)
        dv_n = dv_c1.number_input("عدد الفواصل", min_value=0, step=1)
        dv_h = dv_c2.number_input("ارتفاع الفاصل", min_value=0.0, step=0.1)
        dv_d = dv_c3.number_input("عمق الفاصل", min_value=0.0, step=0.1)

        # خانات الأدراج
        st.write("**• الأدراج:**")
        dr_c1, dr_c2, dr_c3 = st.columns(3)
        dr_n = dr_c1.number_input("عدد الأدراج", min_value=0, step=1)
        dr_w = dr_c2.number_input("عرض الدرج", min_value=0.0, step=0.1)
        dr_d = dr_c3.number_input("عمق الدرج", min_value=0.0, step=0.1)

        st.write("")
        btn_c1, btn_c2 = st.columns(2)
        if btn_c1.button("💾 حفظ الوحدة وعرض التخصيم", type="primary", use_container_width=True):
            if u_w > 0 and u_h > 0:
                st.session_state.project_storage.append({
                    'title': u_title or f"وحدة {len(st.session_state.project_storage)+1}",
                    'type': u_type, 'w': u_w, 'h': u_h, 'd': u_d,
                    'sh_n': sh_n, 'sh_w': sh_w, 'sh_d': sh_d,
                    'dv_n': dv_n, 'dv_h': dv_h, 'dv_d': dv_d,
                    'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d
                })
                st.rerun()
            else:
                st.error("⚠️ يرجى إدخال الطول والعرض للوحدة!")

        if btn_c2.button("🗑️ مسح كل الوحدات", use_container_width=True):
            st.session_state.project_storage = []
            st.rerun()

    # 5. عرض النتائج (جداول تحت بعضها)
    if st.session_state.project_storage:
        st.divider()
        st.subheader("📋 كشوف التخصيم التفصيلية")

        total_m, total_t, total_f = 0, 0, 0

        for idx, u in enumerate(st.session_state.project_storage):
            # العمليات الحسابية الأصلية
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b = u['w'] - 5
            d_b = u['d'] - 5

            if u['type'] == "سفلية":
                m_u = (h_b*2)+(w_b*3)+(d_b*2); t_u = (h_b*2)+(w_b*1)+(d_b*2)
                f_u = (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_u = (h_b*2)+(w_b*2); t_u = (h_b*2)+(w_b*2)+(d_b*4)
                f_u = (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)

            # إضافات الحسابات للجرد
            m_u += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            m_u += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
            m_u += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']
            f_u += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n']
            f_u += (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']

            total_m += m_u; total_t += t_u; total_f += f_u

            # عرض الكارت لكل وحدة
            st.markdown(f"""
            <div class="unit-card">
                <div class="unit-title-text">📦 {u['title']} | النوع: {u['type']} | المقاس: {u['w']} × {u['h']} × {u['d']}</div>
            """, unsafe_allow_html=True)
            
            # جدول التخصيم
            res_table = {
                "البند": ["ألومنيوم ارتفاع", "ألومنيوم عرض", "ألومنيوم عمق", "فيبر الضهر", "فيبر الأرضية", "فيبر الأجناب", "الرفوف", "الفواصل", "الأدراج"],
                "المقاس التخصيمي": [
                    f"{h_b} سم", f"{w_b} سم", f"{d_b} سم", 
                    f"{w_b} × {h_b}", f"{w_b} × {d_b}", f"{h_b} × {d_b}",
                    f"{u['sh_n']} رف ({u['sh_w']} × {u['sh_d']})",
                    f"{u['dv_n']} فاصل ({u['dv_h']} × {u['dv_d']})",
                    f"{u['dr_n']} درج (عرض {u['dr_w']-2.5})"
                ]
            }
            st.table(pd.DataFrame(res_table))
            st.markdown('</div>', unsafe_allow_html=True)

        # 6. جرد خامات المشروع (الفاتورة الإجمالية)
        st.markdown('<div class="total-summary">', unsafe_allow_html=True)
        st.subheader("📊 إجمالي خامات المشروع بالكامل (فاتورة القص)")
        c1, c2, c3 = st.columns(3)
        c1.metric("ألومنيوم مفرد (عود)", f"{total_m/600:.2f}")
        c2.metric("ألومنيوم متقارب (عود)", f"{total_t/600:.2f}")
        c3.metric("فيبر لوح (2.8*1.3)", f"{total_f/36400:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 لم تقم بإضافة وحدات بعد، استخدم النموذج بالأعلى للبدء.")
