import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والواجهة (بدون شريط جانبي وبكامل العرض)
st.set_page_config(page_title="نظام تخصيم الألومنيوم والفيبر PRO", layout="wide")

# 2. تنسيقات CSS مخصصة لتحسين شكل الواجهة والجدول
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
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
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
        border: none !important;
    }
    th {
        background-color: #2c3e50 !important;
        color: white !important;
        text-align: center !important;
        font-size: 16px !important;
    }
    td {
        text-align: center !important;
        font-weight: bold !important;
        font-size: 15px !important;
        border: 1px solid #dee2e6 !important;
    }
    .total-card {
        background-color: #1e272e;
        color: #f1c40f;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #f1c40f;
        margin-top: 30px;
    }
    .stNumberInput, .stTextInput, .stSelectbox {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة حالة البرنامج (بدأ الشغل أم لا + مخزن البيانات)
if 'is_started' not in st.session_state:
    st.session_state.is_started = False
if 'project_data' not in st.session_state:
    st.session_state.project_data = []

# ---------------------------------------------------------
# الشاشة الأولى: صفحة الترحيب
# ---------------------------------------------------------
if not st.session_state.is_started:
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🏗️ نظام تخصيم الألومنيوم والفيبر")
    st.subheader("نسخة الورشة الاحترافية - حسابات دقيقة وجرد شامل")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
    with col_s2:
        if st.button("🚀 ابدأ التخصيم الآن"):
            st.session_state.is_started = True
            st.rerun()

# ---------------------------------------------------------
# الشاشة الثانية: لوحة العمل الكاملة
# ---------------------------------------------------------
else:
    # هيدر الصفحة
    col_h1, col_h2 = st.columns([8, 2])
    col_h1.title("🛠️ لوحة العمليات والحسابات")
    if col_h2.button("🏠 العودة للرئيسية"):
        st.session_state.is_started = False
        st.rerun()

    st.divider()

    # قسم إدخال البيانات (عرض كامل)
    with st.container():
        st.subheader("📝 إدخال مقاسات الوحدة")
        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([2, 1, 1, 1])
        u_name = row1_col1.text_input("اسم الوحدة (مثلاً: مطبخ علوي زاوية)")
        u_type = row1_col2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        u_width = row1_col3.number_input("العرض الكلي (سم)", min_value=0.0, step=0.1)
        u_height = row1_col4.number_input("الارتفاع الكلي (سم)", min_value=0.0, step=0.1)

        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        u_depth = row2_col1.number_input("العمق الكلي (سم)", min_value=0.0, step=0.1)
        u_shelves = row2_col2.number_input("عدد الرفوف", min_value=0, step=1)
        u_dividers = row2_col3.number_input("عدد الفواصل", min_value=0, step=1)
        u_drawers = row2_col4.number_input("عدد الأدراج", min_value=0, step=1)

        btn_col1, btn_col2 = st.columns(2)
        if btn_col1.button("💾 حفظ الوحدة وإظهار التخصيم في الجدول", type="primary", use_container_width=True):
            if u_width > 0 and u_height > 0:
                st.session_state.project_data.append({
                    'title': u_name or f"وحدة {len(st.session_state.project_data)+1}",
                    'type': u_type, 'w': u_width, 'h': u_height, 'd': u_depth,
                    'sh_n': u_shelves, 'dv_n': u_dividers, 'dr_n': u_drawers
                })
                st.success(f"✅ تم إضافة {u_name or 'الوحدة'} بنجاح")
                st.rerun()
            else:
                st.error("⚠️ يرجى إدخال الطول والعرض للوحدة")
        
        if btn_col2.button("🗑️ مسح وإفراغ المشروع الحالي", use_container_width=True):
            st.session_state.project_data = []
            st.rerun()

    # 4. معالجة البيانات وعرض الجدول الشامل
    if st.session_state.project_data:
        st.divider()
        st.subheader("📋 جدول التخصيم والتقطيع التفصيلي")
        
        display_list = []
        total_mufard, total_mutaqarib, total_fiber = 0, 0, 0

        for unit in st.session_state.project_data:
            # حسابات التخصيم (نفس منطق الكود الأصلي الخاص بك)
            # Baky Calculations
            h_baky = unit['h'] - 13 if unit['type'] in ["سفلية", "دولاب خزين"] else unit['h'] - 5
            w_baky = unit['w'] - 5
            d_baky = unit['d'] - 5
            
            # Aluminum & Fiber Inventory Logic
            if unit['type'] == "سفلية":
                # Aluminum: (H*2)+(W*3)+(D*2) مفرد | (H*2)+(W*1)+(D*2) متقارب
                m_unit = (h_baky * 2) + (w_baky * 3) + (d_baky * 2)
                t_unit = (h_baky * 2) + (w_baky * 1) + (d_baky * 2)
                # Fiber: ضهرية + أرضية + 2 جنب
                f_unit = (w_baky * h_baky) + (w_baky * d_baky) + (h_baky * d_baky * 2)
            else:
                # Aluminum for Upper: (H*2)+(W*2) مفرد | (H*2)+(W*2)+(D*4) متقارب
                m_unit = (h_baky * 2) + (w_baky * 2)
                t_unit = (h_baky * 2) + (w_baky * 2) + (d_baky * 4)
                # Fiber: ضهرية + 2 أرضية + 2 جنب
                f_unit = (w_baky * h_baky) + (w_baky * d_baky * 2) + (h_baky * d_baky * 2)
            
            # Extras (Shelves)
            if unit['sh_n'] > 0:
                m_unit += (unit['w'] * 2 + unit['d'] * 2) * unit['sh_n']
                f_unit += (unit['w'] - 5) * (unit['d'] - 5) * unit['sh_n']

            # Cumulative Totals
            total_mufard += m_unit
            total_mutaqarib += t_unit
            total_fiber += f_unit

            # Add to Display Table
            display_list.append({
                "الوحدة": unit['title'],
                "النوع": unit['type'],
                "ارتفاع الألومنيوم": h_baky,
                "عرض الألومنيوم": w_baky,
                "عمق الألومنيوم": d_baky,
                "الفيبر (الضهر)": f"{w_baky} × {h_baky}",
                "الفيبر (الأرضية)": f"{w_baky} × {d_baky}",
                "الفيبر (الأجناب)": f"{h_baky} × {d_baky}",
                "الرفوف": f"{unit['sh_n']} رف",
                "الأدراج": f"{unit['dr_n']} درج (عرض {unit['w']-2.5})"
            })

        # عرض الجدول الكبير الموحد
        df_final = pd.DataFrame(display_list)
        st.table(df_final)

        # 5. جرد خامات المشروع (فاتورة القص النهائية)
        st.markdown('<div class="total-card">', unsafe_allow_html=True)
        st.subheader("📊 الفاتورة الإجمالية لجرد خامات المشروع")
        col_res1, col_res2, col_res3 = st.columns(3)
        
        # تحويل من سم إلى عود (600 سم) ومن سم2 إلى لوح (36400 سم2)
        col_res1.metric("ألومنيوم مفرد (عود)", f"{total_mufard / 600:.2f}")
        col_res2.metric("ألومنيوم متقارب (عود)", f"{total_mutaqarib / 600:.2f}")
        col_res3.metric("فيبر (2.8 * 1.3) لوح", f"{total_fiber / 36400:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 لا يوجد بيانات لعرضها. يرجى إدخال مقاسات الوحدة بالأعلى والضغط على 'حفظ'.")
