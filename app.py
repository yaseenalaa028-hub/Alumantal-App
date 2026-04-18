import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والواجهة (كامل العرض)
st.set_page_config(page_title="نظام تخصيم الألومنيوم PRO - النسخة الكاملة", layout="wide")

# تنسيق اللغة العربية والشكل العام (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .main-header {
        background-color: #2c3e50;
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stTable { background-color: white; border-radius: 10px; }
    th {
        background-color: #2c3e50 !important;
        color: white !important;
        text-align: center !important;
        font-size: 16px;
    }
    td {
        text-align: center !important;
        font-weight: bold !important;
        font-size: 14px;
        border: 1px solid #dee2e6 !important;
    }
    .total-box {
        background-color: #1e272e;
        color: #f1c40f;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #f1c40f;
        margin-top: 30px;
    }
    .start-btn button {
        background-color: #27ae60 !important;
        color: white !important;
        font-size: 26px !important;
        height: 80px !important;
        width: 100% !important;
        max-width: 400px;
        border-radius: 15px !important;
        margin: 20px auto !important;
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات والتنقل (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- [الشاشة الأولى: صفحة الترحيب] ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🏗️ نظام تخصيم الألومنيوم والفيبر الاحترافي")
    st.subheader("إدارة متكاملة لبيانات المقاسات - جرد الخامات - فواتير القص")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    with col_s2:
        if st.button("🚀 ابدأ التخصيم الآن"):
            st.session_state.page = 'work'
            st.rerun()

# --- [الشاشة الثانية: واجهة العمل الكاملة] ---
else:
    # رأس الصفحة وأزرار التحكم العامة
    col_h1, col_h2 = st.columns([8, 2])
    col_h1.title("🛠️ لوحة إدخال البيانات والتخصيم")
    if col_h2.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

    st.divider()

    # قسم المدخلات (كامل دون نقص)
    with st.container():
        st.subheader("📝 مقاسات الهيكل الأساسي")
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        u_title = c1.text_input("اسم الوحدة (مثل: مطبخ علوي)")
        u_type = c2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        u_w = c3.number_input("العرض الكلي", min_value=0.0, format="%.1f")
        u_h = c4.number_input("الارتفاع الكلي", min_value=0.0, format="%.1f")
        u_d = c5.number_input("العمق الكلي", min_value=0.0, format="%.1f")

        st.markdown("#### 🧱 تفاصيل الإضافات (الرفوف، الفواصل، الأدراج)")
        
        # مدخلات الرفوف
        st.write("➖ **الرفوف:**")
        sc1, sc2, sc3 = st.columns(3)
        sh_n = sc1.number_input("عدد الرفوف", min_value=0, step=1, key="sh_n")
        sh_w = sc2.number_input("عرض الرف", min_value=0.0, format="%.1f", key="sh_w")
        sh_d = sc3.number_input("عمق الرف", min_value=0.0, format="%.1f", key="sh_d")

        # مدخلات الفواصل
        st.write("➖ **الفواصل:**")
        vc1, vc2, vc3 = st.columns(3)
        dv_n = vc1.number_input("عدد الفواصل", min_value=0, step=1, key="dv_n")
        dv_h = vc2.number_input("ارتفاع الفاصل", min_value=0.0, format="%.1f", key="dv_h")
        dv_d = vc3.number_input("عمق الفاصل", min_value=0.0, format="%.1f", key="dv_d")

        # مدخلات الأدراج
        st.write("➖ **الأدراج:**")
        rc1, rc2, rc3 = st.columns(3)
        dr_n = rc1.number_input("عدد الأدراج", min_value=0, step=1, key="dr_n")
        dr_w = rc2.number_input("عرض الدرج", min_value=0.0, format="%.1f", key="dr_w")
        dr_d = rc3.number_input("عمق الدرج", min_value=0.0, format="%.1f", key="dr_d")

        st.write("")
        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("💾 حفظ الوحدة وإضافتها للجدول", type="primary", use_container_width=True):
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
                st.error("⚠️ يرجى إدخال المقاسات الأساسية (العرض والارتفاع)")

        if btn_col2.button("🗑️ مسح كل الوحدات", use_container_width=True):
            st.session_state.project_storage = []
            st.rerun()

    # --- عرض النتائج في جدول شامل وفاتورة جرد ---
    if st.session_state.project_storage:
        st.divider()
        st.subheader("📋 جدول تخصيم الوحدات التفصيلي")
        
        table_rows = []
        sum_mufard, sum_mutaqarib, sum_fiber = 0, 0, 0

        for u in st.session_state.project_storage:
            # 1. تخصيم الهيكل (Baky)
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b = u['w'] - 5
            d_b = u['d'] - 5

            # 2. منطق جرد الخامات (سم طولي و سم مربع)
            if u['type'] == "سفلية":
                m_u = (h_b * 2) + (w_b * 3) + (d_b * 2)
                t_u = (h_b * 2) + (w_b * 1) + (d_b * 2)
                f_u = (w_b * h_b) + (w_b * d_b) + (h_b * d_b * 2)
            else:
                m_u = (h_b * 2) + (w_b * 2)
                t_u = (h_b * 2) + (w_b * 2) + (d_b * 4)
                f_u = (w_b * h_b) + (w_b * d_b * 2) + (h_b * d_b * 2)

            # 3. حساب الإضافات في الجرد
            m_u += (u['sh_w'] * 2 + u['sh_d'] * 2) * u['sh_n']
            m_u += (u['dv_h'] * 2 + u['dv_d'] * 2) * u['dv_n']
            m_u += ((u['dr_w'] - 2.5) * 2 + u['dr_d'] * 2) * u['dr_n']
            f_u += (u['sh_w'] - 5) * (u['sh_d'] - 5) * u['sh_n']
            f_u += (u['dv_h'] - 5) * (u['dv_d'] - 5) * u['dv_n']

            sum_mufard += m_u
            sum_mutaqarib += t_u
            sum_fiber += f_u

            # 4. بناء سطر الجدول
            table_rows.append({
                "اسم الوحدة": u['title'],
                "النوع": u['type'],
                "ارتفاع الألوم": h_b,
                "عرض الألوم": w_b,
                "عمق الألوم": d_b,
                "فيبر ضهر": f"{w_b}×{h_b}",
                "فيبر أرضية": f"{w_b}×{d_b}",
                "فيبر أجناب": f"{h_b}×{d_b}",
                "الرفوف": f"{u['sh_n']} رف ({u['sh_w']}×{u['sh_d']})",
                "الفواصل": f"{u['dv_n']} فاصل ({u['dv_h']}×{u['dv_d']})",
                "الأدراج": f"{u['dr_n']} درج (عرض {u['dr_w']-2.5})"
            })

        # عرض الجدول
        df = pd.DataFrame(table_rows)
        st.table(df)

        # 5. فاتورة الجرد النهائي للمشروع
        st.markdown('<div class="total-box">', unsafe_allow_html=True)
        st.subheader("📊 إجمالي خامات المشروع بالكامل (فاتورة القص)")
        res1, res2, res3 = st.columns(3)
        res1.metric("ألومنيوم مفرد (عـود 6م)", f"{sum_mufard/600:.2f}")
        res2.metric("ألومنيوم متقارب (عـود 6م)", f"{sum_mutaqarib/600:.2f}")
        res3.metric("فيبر (لوح 2.8×1.3)", f"{sum_fiber/36400:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 لم تقم بإضافة أي وحدات بعد. أدخل المقاسات أعلاه واضغط حفظ.")
