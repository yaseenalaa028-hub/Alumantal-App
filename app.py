import streamlit as st
import pandas as pd
import time

# =========================================================
# 1. إعدادات المنظومة الأساسية وحماية مجهود المهندس ياسين
# =========================================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. تهيئة مخزن البيانات (Session State) للحفاظ على المشروع
# =========================================================
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# =========================================================
# 3. نظام الألوان المتغير (الوضع الليلي والنهاري)
# =========================================================
if st.session_state.dark_mode:
    primary_bg = "#1e272e"
    secondary_bg = "#2d3436"
    text_color = "#ffffff"
    accent_color = "#f1c40f"
    table_border = "#f1c40f"
else:
    primary_bg = "#ffffff"
    secondary_bg = "#f8f9fa"
    text_color = "#1e272e"
    accent_color = "#d4ac0d"
    table_border = "#d4ac0d"

# =========================================================
# 4. واجهة المستخدم الرسومية (CSS) - حماية مجهودك من النسخ
# =========================================================
st.markdown(f"""
    <style>
    /* إخفاء القطة (GitHub) وأدوات streamlit الافتراضية */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    /* منع تحديد النصوص وحماية التصميم */
    body {{
        background-color: {primary_bg} !important;
        color: {text_color} !important;
        -webkit-user-select: none;
        user-select: none;
        direction: rtl;
    }}

    /* تنسيق الكروت الاحترافية */
    .unit-card {{
        background-color: {secondary_bg};
        padding: 30px;
        border-radius: 20px;
        border-right: 15px solid {accent_color};
        margin-bottom: 35px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
    }}
    
    /* تنسيق الجداول التفصيلية */
    .stTable td {{ 
        color: {text_color} !important; 
        font-weight: bold !important; 
        font-size: 17px !important;
        border: 1px solid {table_border} !important;
        text-align: center !important;
    }}
    .stTable th {{ 
        background-color: {accent_color} !important; 
        color: #1e272e !important; 
        font-size: 18px !important;
        text-align: center !important;
    }}

    /* صندوق العنوان الرئيسي */
    .header-box {{
        background-color: #1e272e;
        padding: 40px;
        border-radius: 25px;
        border: 4px solid {accent_color};
        border-bottom: 15px solid {accent_color};
        text-align: center;
        margin-bottom: 50px;
    }}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 5. القائمة الجانبية (Sidebar) - مركز التحكم والمخزن
# =========================================================
with st.sidebar:
    st.markdown(f"<h1 style='color:{accent_color}; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{text_color}; font-weight:bold;'>المهندس ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
    
    # أزرار التحكم (الرجوع + تبديل الإضاءة)
    st.subheader("⚙️ أدوات التحكم")
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
    with col_nav2:
        mode_label = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(mode_label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # مخزن المشروع (مكان حساب إجمالي الخامات)
    if st.session_state.project_list:
        st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{accent_color}; text-align:center;'>📦 مخزن الخامات</h3>", unsafe_allow_html=True)
        
        # حسابات الجرد الكلي
        total_mufard = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_motaqareb = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_fiber = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("🪵 إجمالي أعواد مفرد", f"{round(total_mufard, 1)} عود")
        st.metric("🪵 إجمالي أعواد متقارب", f"{round(total_motaqareb, 1)} عود")
        st.metric("💎 إجمالي ألواح فيبر", f"{round(total_fiber, 1)} لوح")
        
        if st.button("🗑️ تفريغ المخزن بالكامل", use_container_width=True):
            with st.spinner("جاري مسح بيانات المشروع..."):
                time.sleep(1)
                st.session_state.project_list = []
                st.rerun()

# =========================================================
# 6. إدارة الشاشات (Navigation Logic)
# =========================================================

# --- شاشة الترحيب (Welcome Screen) ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div class="header-box">
            <h1 style="color:{accent_color}; font-size:4.5em; margin:0; font-weight:900;">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:1.8em; font-weight:bold;">المنظومة الاحترافية لتخصيمات المطابخ</p>
            <p style="color:{accent_color}; font-size:1.4em;">بإشراف المهندس: ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        if st.button("🚀 دخول نظام التخصيم", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق الرئيسية (The App) ---
elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent_color};'>📋 إدخال بيانات المقاسات</h2>", unsafe_allow_html=True)
    
    with st.expander("➕ إضافة وحدة جديدة للمشروع", expanded=True):
        col_in1, col_in2, col_in3 = st.columns(3)
        
        with col_in1:
            u_name = st.text_input("اسم أو كود القطعة")
            u_type = st.selectbox("تصنيف الوحدة", ["سفلية (13سم)", "علوية (5سم)", "دولاب خزين (13سم)"])
            # تم إرجاع الصفر (0.0) كما طلبت يا هندسة
            width = st.number_input("العرض الكلي (سم)", value=0.0)
            height = st.number_input("الارتفاع الكلي (سم)", value=0.0)
            depth = st.number_input("العمق الكلي (سم)", value=0.0)
            
        with col_in2:
            st.markdown(f"<b style='color:{accent_color};'>🧱 الرفوف والفواصل</b>", unsafe_allow_html=True)
            sh_w = st.number_input("عرض الرف الصافي", value=0.0)
            sh_d = st.number_input("عمق الرف الصافي", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
            st.markdown("---")
            # خانات الفواصل كاملة (ارتفاع، عمق، عدد)
            dv_h = st.number_input("ارتفاع الفاصل (H)", value=0.0)
            dv_d = st.number_input("عمق الفاصل (D)", value=0.0)
            dv_n = st.number_input("عدد الفواصل", value=0)
            
        with col_in3:
            st.markdown(f"<b style='color:{accent_color};'>🗄️ الأدراج</b>", unsafe_allow_html=True)
            dr_w = st.number_input("عرض برواز الدرج", value=0.0)
            dr_d = st.number_input("عمق برواز الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج المطلوبة", value=0)
            st.markdown("---")
            notes = st.text_area("ملاحظات إضافية")
            
            if st.button("✅ تنفيذ التخصيم وحفظ", use_container_width=True):
                if width > 0 and height > 0:
                    # تطبيق خوارزمية التخصيم (13 للسفلي/الدولاب و 5 للعالي)
                    deduction = 13 if "13" in u_type else 5
                    h_net = int(height - deduction)
                    w_net, d_net = int(width - 5), int(depth - 5)
                    
                    # إنشاء قائمة تقطيع الألومنيوم التفصيلية
                    alum_data = [
                        {"البيان": "قوايم الارتفاع", "المقاس": h_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العرض", "المقاس": w_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العمق", "المقاس": d_net, "العدد": "4 ق"}
                    ]
                    
                    # إضافة الرفوف والفواصل والأدراج للجداول
                    if sh_n > 0:
                        alum_data.append({"البيان": "عوارض الرف", "المقاس": f"{int(sh_w)}x{int(sh_d)}", "العدد": f"{sh_n*4} ق"})
                    if dv_n > 0:
                        alum_data.append({"البيان": "فواصل داخلية", "المقاس": f"{int(dv_h)}x{int(dv_d)}", "العدد": f"{dv_n*4} ق"})
                    if dr_n > 0:
                        alum_data.append({"البيان": "إطارات أدراج", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{dr_n*4} ق"})

                    # حسابات الفيبر
                    fiber_data = [
                        {"القطعة": "فيبر الظهر", "المقاس": f"{w_net} x {h_net}", "العدد": "1"},
                        {"القطعة": "فيبر الأجناب", "المقاس": f"{h_net} x {d_net}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس": f"{w_net} x {d_net}", "العدد": "1" if "سفلية" in u_type else "2"}
                    ]

                    # حساب أطوال الأعواد للجرد الإجمالي (المخزن)
                    m_mufard = (h_net*4 + w_net*4 + d_net*4) + (sh_w*4*sh_n) + (dr_w*4*dr_n) + (dv_h*4*dv_n)
                    m_motaqareb = (h_net*2 + w_net*2)
                    f_area = (w_net*h_net) + (h_net*d_net*2) + (w_net*d_net*2)

                    # إضافة الوحدة للمخزن
                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{width}x{height}x{depth}",
                        "alum_df": pd.DataFrame(alum_data), "fiber_df": pd.DataFrame(fiber_data),
                        "m_m": m_mufard, "m_t": m_motaqareb, "f_a": f_area, "note": notes
                    })
                    st.success("تم الحفظ في مخزن المشروع!")
                    st.rerun()
                else:
                    st.error("يرجى إدخال العرض والارتفاع بشكل صحيح!")

    # عرض الوحدات المحفوظة وتخصيماتها
    if st.session_state.project_list:
        st.markdown(f"<h3 style='color:{accent_color};'>🧾 كشوف التخصيم والتقطيع</h3>", unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f"""
                <div class="unit-card">
                    <h2 style="color:{accent_color};">#{i+1} {item['name']} ({item['type']})</h2>
                    <p style="font-size:1.1em;">المقاس الكلي للوحدة: <b>{item['dims']} سم</b></p>
                """, unsafe_allow_html=True)
                
                res_col1, res_col2 = st.columns([2, 1])
                with res_col1:
                    st.markdown("<b>⚙️ تخصيم الألومنيوم:</b>", unsafe_allow_html=True)
                    st.table(item['alum_df'])
                with res_col2:
                    st.markdown("<b>🪵 تخصيم الفيبر:</b>", unsafe_allow_html=True)
                    st.table(item['fiber_df'])
                
                if item['note']:
                    st.info(f"📌 ملاحظة: {item['note']}")
                st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 7. التذييل (Footer) - علامة المهندس ياسين التجارية
# =========================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent_color}; font-weight:bold; font-size:1.2em;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء © جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
