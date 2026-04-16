import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. إعدادات المنظومة وحماية مجهود المهندس ياسين
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. تهيئة مخزن البيانات (Session State)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# ==========================================
# 3. نظام الألوان المتغير (Dark/Light Mode)
# ==========================================
if st.session_state.dark_mode:
    primary_bg = "#1e272e"
    secondary_bg = "#2d3436"
    text_color = "#ffffff"
    accent_color = "#f1c40f"
    table_bg = "#2d3436"
else:
    primary_bg = "#ffffff"
    secondary_bg = "#f8f9fa"
    text_color = "#1e272e"
    accent_color = "#d4ac0d"
    table_bg = "#ffffff"

# ==========================================
# 4. واجهة المستخدم الرسومية (CSS) - حماية كاملة
# ==========================================
st.markdown(f"""
    <style>
    /* إخفاء شعار GitHub (القطة) وأدوات streamlit الافتراضية */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    /* منع تحديد النصوص لحماية خوارزمية التخصيم */
    body {{
        background-color: {primary_bg} !important;
        color: {text_color} !important;
        -webkit-user-select: none;
        user-select: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* تنسيق الكروت الاحترافية */
    .unit-card {{
        background-color: {secondary_bg};
        padding: 30px;
        border-radius: 20px;
        border-right: 15px solid {accent_color};
        margin-bottom: 35px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
        transition: 0.3s;
    }}
    
    /* تنسيق الجداول التفصيلية */
    .stTable td {{ 
        color: {text_color} !important; 
        font-weight: bold !important; 
        font-size: 17px !important;
        border: 1px solid {accent_color} !important;
        text-align: center !important;
    }}
    .stTable th {{ 
        background-color: {accent_color} !important; 
        color: #1e272e !important; 
        font-size: 18px !important;
        text-align: center !important;
    }}

    /* صندوق العناوين */
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

# ==========================================
# 5. القائمة الجانبية (Sidebar) - مركز التحكم والمخزن
# ==========================================
with st.sidebar:
    st.markdown(f"<h1 style='color:{accent_color}; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{text_color}; font-size:1.2em;'>المهندس ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
    
    # أزرار التحكم الرئيسية
    st.subheader("⚙️ أدوات التحكم")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
    with c2:
        icon = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(icon, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # مخزن المشروع (حساب الخامات التراكمي الشامل)
    if st.session_state.project_list:
        st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{accent_color}; text-align:center;'>📦 مخزن الخامات</h3>", unsafe_allow_html=True)
        
        total_mufard = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_motaqareb = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_fiber = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("🪵 أعواد مفرد", f"{round(total_mufard, 1)}")
            st.metric("💎 ألواح فيبر", f"{round(total_fiber, 1)}")
        with col_m2:
            st.metric("🪵 أعواد متقارب", f"{round(total_motaqareb, 1)}")
        
        if st.button("🗑️ تفريغ مخزن المشروع", use_container_width=True):
            with st.spinner("جاري مسح البيانات..."):
                time.sleep(1)
                st.session_state.project_list = []
                st.rerun()

# ==========================================
# 6. إدارة الشاشات (Navigation Logic)
# ==========================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div class="header-box">
            <h1 style="color:{accent_color}; font-size:4.5em; margin:0; font-weight:900;">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:1.8em; font-weight:bold;">المنظومة الاحترافية لتخصيمات المطابخ</p>
            <p style="color:{accent_color}; font-size:1.4em;">بإشراف المهندس: ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    c_w1, c_w2, c_w3 = st.columns([1, 2, 1])
    with c_w2:
        if st.button("🚀 ابدأ العمل الآن (دخول النظام)", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق الرئيسية (التخصيم) ---
elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent_color};'>📋 إدخال بيانات المقاسات</h2>", unsafe_allow_html=True)
    
    with st.expander("➕ إضافة وحدة جديدة للمشروع", expanded=True):
        col_in1, col_in2, col_in3 = st.columns(3)
        
        with col_in1:
            name = st.text_input("اسم/كود القطعة", placeholder="مثال: وحدة حوض")
            u_type = st.selectbox("تصنيف الوحدة", ["سفلية (13سم)", "علوية (5سم)", "دولاب خزين (13سم)"])
            width = st.number_input("العرض الكلي (W)", value=0.0, format="%.1f")
            height = st.number_input("الارتفاع الكلي (H)", value=0.0, format="%.1f")
            depth = st.number_input("العمق الكلي (D)", value=0.0, format="%.1f")
            
        with col_in2:
            st.markdown(f"<b style='color:{accent_color};'>🧱 تفاصيل الرفوف</b>", unsafe_allow_html=True)
            sh_w = st.number_input("عرض الرف الصافي", value=0.0)
            sh_d = st.number_input("عمق الرف الصافي", value=0.0)
            sh_n = st.number_input("عدد الرفوف داخل القطعة", value=0)
            st.markdown("---")
            st.markdown(f"<b style='color:{accent_color};'>📏 تفاصيل الفواصل</b>", unsafe_allow_html=True)
            dv_h = st.number_input("ارتفاع الفاصل (H)", value=0.0)
            dv_d = st.number_input("عمق الفاصل (D)", value=0.0)
            dv_n = st.number_input("عدد الفواصل", value=0)
            
        with col_in3:
            st.markdown(f"<b style='color:{accent_color};'>🗄️ تفاصيل الأدراج</b>", unsafe_allow_html=True)
            dr_w = st.number_input("عرض برواز الدرج", value=0.0)
            dr_d = st.number_input("عمق برواز الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج المطلوبة", value=0)
            st.markdown("---")
            notes = st.text_area("ملاحظات فنية إضافية")
            
            if st.button("✅ تنفيذ التخصيم وحفظ بالخزنة", use_container_width=True):
                if width > 0 and height > 0:
                    # تطبيق خوارزمية التخصيم (13 للسفلي و 5 للعالي)
                    deduction = 13 if "13" in u_type else 5
                    h_net = int(height - deduction)
                    w_net, d_net = int(width - 5), int(depth - 5)
                    
                    # إنشاء كشف تقطيع الألومنيوم
                    alum_list = [
                        {"البيان": "قوايم الارتفاع الرئيسية", "المقاس": h_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العرض الأفقية", "المقاس": w_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العمق الجانبية", "المقاس": d_net, "العدد": "4 ق"}
                    ]
                    
                    # دمج إضافات الرفوف والفواصل
                    if sh_n > 0:
                        alum_list.append({"البيان": "عوارض الرفوف الداخلية", "المقاس": f"{int(sh_w)}x{int(sh_d)}", "العدد": f"{sh_n*4} ق"})
                    if dv_n > 0:
                        alum_list.append({"البيان": "قوايم الفواصل الداخلية", "المقاس": f"{int(dv_h)}x{int(dv_d)}", "العدد": f"{dv_n*4} ق"})
                    if dr_n > 0:
                        alum_list.append({"البيان": "إطارات الأدراج (خصم 2.5سم)", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{dr_n*4} ق"})

                    # كشف الفيبر
                    fiber_list = [
                        {"القطعة": "فيبر الظهر", "المقاس": f"{w_net} x {h_net}", "العدد": "1"},
                        {"القطعة": "فيبر الأجناب", "المقاس": f"{h_net} x {d_net}", "العدد": "2"},
                        {"القطعة": "فيبر الأرضية/السقف", "المقاس": f"{w_net} x {d_net}", "العدد": "1" if "سفلية" in u_type else "2"}
                    ]

                    # حسابات المخزن (الأمتار الكلية)
                    m_mufard = (h_net*4 + w_net*4 + d_net*4) + (sh_w*4*sh_n) + (dr_w*4*dr_n) + (dv_h*4*dv_n)
                    m_motaqareb = (h_net*2 + w_net*2)
                    f_area = (w_net*h_net) + (h_net*d_net*2) + (w_net*d_net*2)

                    st.session_state.project_list.append({
                        "name": name, "type": u_type, "dims": f"{width}x{height}x{depth}",
                        "alum_df": pd.DataFrame(alum_list), "fiber_df": pd.DataFrame(fiber_list),
                        "m_m": m_mufard, "m_t": m_motaqareb, "f_a": f_area, "note": notes
                    })
                    st.success("تم الحفظ بنجاح في مخزن المشروع!")
                    st.rerun()
                else:
                    st.error("يرجى إدخال مقاسات صحيحة (العرض والارتفاع)!")

    # عرض كشوفات التقطيع للوحدات المضافة
    if st.session_state.project_list:
        st.markdown(f"<h3 style='color:{accent_color};'>🧾 كشوف التقطيع والتخصيم</h3>", unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f"""
                <div class="unit-card">
                    <h2 style="color:{accent_color};">#{i+1} {item['name']} - {item['type']}</h2>
                    <p style="font-size:1.1em;">المقاس الكلي: <b>{item['dims']} سم</b></p>
                """, unsafe_allow_html=True)
                
                col_res1, col_res2 = st.columns([2, 1])
                with col_res1:
                    st.markdown("<b>🛠️ تقطيع الألومنيوم:</b>", unsafe_allow_html=True)
                    st.table(item['alum_df'])
                with col_res2:
                    st.markdown("<b>🪵 مقاسات الفيبر:</b>", unsafe_allow_html=True)
                    st.table(item['fiber_df'])
                
                if item['note']:
                    st.info(f"📌 ملاحظة: {item['note']}")
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 7. التذييل (Footer)
# ==========================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent_color}; font-weight:bold;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
