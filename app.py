import streamlit as st
import pandas as pd
import datetime

# ==============================================================================
# 1. إعدادات المنظومة الأساسية - م/ ياسين علاء
# ==============================================================================
st.set_page_config(
    page_title="DOGGA SYSTEM 2026",
    page_icon="📐",
    layout="wide",  # فرش الشاشة بالعرض
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. إدارة الحالة (Session State) لضمان استقرار السيستم
# ==============================================================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# ==============================================================================
# 3. محرك التصميم الديناميكي (CSS & Themes) - حل مشكلة "مط" الكلام
# ==============================================================================
if st.session_state.dark_mode:
    main_bg = "#0e1117"
    card_bg = "#161b22"
    text_col = "#ffffff"
    accent = "#f1c40f"  # الذهبي المميز لـ DOGGA
else:
    main_bg = "#ffffff"
    card_bg = "#f0f2f6"
    text_col = "#1e1e1e"
    accent = "#d4ac0d"

st.markdown(f"""
    <style>
    /* أهم جزء: جعل المحتوى يملأ 98% من عرض الشاشة مهما كان الجهاز */
    .block-container {{
        max-width: 98% !important;
        padding-top: 1rem !important;
        padding-right: 1.5rem !important;
        padding-left: 1.5rem !important;
    }}
    
    /* ضبط الاتجاه والخطوط */
    .stApp {{
        background-color: {main_bg} !important;
        color: {text_col} !important;
        direction: rtl !important;
    }}

    /* تصميم الكروت العريضة للوحدات */
    .unit-card {{
        background-color: {card_bg};
        padding: 30px;
        border-radius: 20px;
        border-right: 15px solid {accent};
        margin-bottom: 25px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    }}

    /* تحسين الجداول لتكون واضحة وعريضة */
    .stTable td {{
        font-size: 18px !important;
        font-weight: bold !important;
        border: 1px solid {accent} !important;
        text-align: center !important;
    }}
    
    /* إخفاء عناصر ستريمليت ليكون البرنامج باسمك فقط */
    header, footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    
    /* تنسيق أزرار الإدخال */
    .stButton>button {{
        border-radius: 10px !important;
        font-weight: bold !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. القائمة الجانبية (Sidebar) - لوحة التحكم والمخزن
# ==============================================================================
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center; color:{accent};'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>تطوير المهندس: <b>ياسين علاء</b></p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
    
    # --- تشغيل زرار الـ Dark Mode الحقيقي ---
    label = "☀️ الوضع النهاري" if st.session_state.dark_mode else "🌙 الوضع الليلي"
    if st.button(label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        st.session_state.page = 'welcome'
        st.rerun()

    # --- مخزن جرد الخامات الكلي ---
    if st.session_state.project_list:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{accent};'>📦 جرد المشروع</h3>", unsafe_allow_html=True)
        
        # حسابات الأمتار الطولية الإجمالية
        total_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("أعواد ألومنيوم (6م)", f"{round(total_m, 1)} عود")
        st.metric("ألواح فيبر (لوح)", f"{round(total_f, 1)} لوح")
        
        if st.button("🗑️ مسح المشروع والبدء من جديد", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# ==============================================================================
# 5. إدارة الشاشات والمحتوى الرئيسي
# ==============================================================================

# --- شاشة الترحيب الفخمة ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:120px;">
            <h1 style="color:{accent}; font-size:6em; font-weight:900; margin:0;">DOGGA SYSTEM</h1>
            <h2 style="color:{text_col}; font-size:2.5em;">المنظومة الاحترافية لتخصيمات المطابخ</h2>
            <p style="font-size:1.8em; color:{accent};">برمجة وتطوير م/ ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🚀 دخول لوحة التخصيم", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة العمل الرئيسية (لوحة الإدخال) ---
elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent};'>📋 لوحة إضافة الوحدات والتخصيم الفني</h2>", unsafe_allow_html=True)
    
    with st.expander("🛠️ إدخال بيانات الوحدة (الخانات جاهزة بدون أصفار تعطل الكتابة)", expanded=True):
        # توزيع الخانات بعرض الشاشة لمنع "المط" الطولي
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            st.markdown(f"<b style='color:{accent};'>📏 المقاسات الرئيسية</b>", unsafe_allow_html=True)
            u_name = st.text_input("اسم الوحدة (كود الوحدة)")
            u_type = st.selectbox("نوع التخصيم", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
            # تم إزالة الأصفار باستخدام value=None
            w_val = st.number_input("العرض الكلي (W)", value=None, placeholder="0.0")
            h_val = st.number_input("الارتفاع الكلي (H)", value=None, placeholder="0.0")
            d_val = st.number_input("العمق الكلي (D)", value=None, placeholder="0.0")
            
        with c2:
            st.markdown(f"<b style='color:{accent};'>🧱 الرفوف والفواصل</b>", unsafe_allow_html=True)
            r_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            r_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
            r_n = st.number_input("عدد الرفوف", value=None, placeholder="0")
            st.write("---")
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0.0")
            v_d = st.number_input("عمق الفاصل", value=None, placeholder="0.0")
            v_n = st.number_input("عدد الفواصل", value=None, placeholder="0")

        with c3:
            st.markdown(f"<b style='color:{accent};'>🗄️ الأدراج والملاحظات</b>", unsafe_allow_html=True)
            dr_w = st.number_input("عرض برواز الدرج", value=None, placeholder="0.0")
            dr_d = st.number_input("عمق برواز الدرج", value=None, placeholder="0.0")
            dr_n = st.number_input("عدد الأدراج المطلوبة", value=None, placeholder="0")
            st.write("---")
            tech_note = st.text_area("ملاحظات فنية للتقطيع")
            
            if st.button("✅ تنفيذ التخصيم وجرد الخامات", use_container_width=True):
                if w_val and h_val:
                    # منطق التخصيم (حسب ما تم تعديله من قبل م/ ياسين)
                    deduction = 13 if "13" in u_type else 5
                    h_net = int(h_val - deduction)
                    w_net, d_net = int(w_val - 5), int((d_val or 0) - 5)
                    
                    # جداول التقطيع
                    alum_data = [
                        {"البيان": "قوايم رئيسية", "المقاس": h_net, "العدد": "4 ق"},
                        {"البيان": "عوارض عرض", "المقاس": w_net, "العدد": "4 ق"},
                        {"البيان": "عوارض عمق", "المقاس": d_net, "العدد": "4 ق"}
                    ]
                    # إضافات
                    if r_n: alum_data.append({"البيان": "أعواد رفوف", "المقاس": f"{int(r_w)}x{int(r_d)}", "العدد": f"{int(r_n)*4}"})
                    if v_n: alum_data.append({"البيان": "أعواد فواصل", "المقاس": f"{int(v_h)}x{int(v_d)}", "العدد": f"{int(v_n)*4}"})
                    if dr_n: alum_data.append({"البيان": "إطار درج", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{int(dr_n)*4}"})

                    # حسابات المخزن
                    m_total = (h_net*4 + w_net*4 + d_net*4) + (int(v_h or 0)*4*int(v_n or 0))
                    f_area = (w_net*h_net) + (h_net*d_net*2) + (w_net*d_net*2)

                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w_val}x{h_val}x{d_val}", "type": u_type,
                        "alum_df": pd.DataFrame(alum_data), "m_m": m_total, "f_a": f_area, "note": tech_note
                    })
                    st.rerun()

    # --- عرض الوحدات المحفوظة (بشكل عريض) ---
    st.write("---")
    for i, item in enumerate(st.session_state.project_list):
        st.markdown(f"""
            <div class="unit-card">
                <h2 style="color:{accent}; margin:0;">#{i+1} {item['name']} | مقاس: {item['dims']} | ({item['type']})</h2>
            </div>
        """, unsafe_allow_html=True)
        
        res_c1, res_c2 = st.columns([3, 1])
        with res_c1:
            st.table(item['alum_df'])
        with res_c2:
            st.info(f"📍 ملاحظة: {item['note']}" if item['note'] else "لا يوجد ملاحظات")
            st.metric("أمتار ألومنيوم", f"{round(item['m_m']/100, 2)} متر")

# تذييل المنظومة
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent}; font-weight:bold; font-size:1.5em;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
