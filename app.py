import streamlit as st
import pandas as pd
import time

# =========================================================
# 1. إعدادات المنظومة وحماية العلامة التجارية (DOGGA)
# =========================================================
st.set_page_config(
    page_title="DOGGA SYSTEM | المهندس ياسين علاء",
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
# 3. محرك الألوان الديناميكي (Dark/Light Mode)
# =========================================================
accent = "#f1c40f" if st.session_state.dark_mode else "#d4ac0d"
bg_main = "#1e272e" if st.session_state.dark_mode else "#ffffff"
txt_main = "#ffffff" if st.session_state.dark_mode else "#1e272e"
card_bg = "#2d3436" if st.session_state.dark_mode else "#f2f2f2"

# تنسيقات CSS المتقدمة
st.markdown(f"""
    <style>
    /* إخفاء شعار المنصة وحماية الكود */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    
    body {{
        background-color: {bg_main} !important;
        color: {txt_main} !important;
        direction: rtl;
        font-family: 'Cairo', sans-serif;
    }}

    /* تصميم الكروت الاحترافية */
    .unit-card {{
        background-color: {card_bg};
        padding: 30px;
        border-radius: 20px;
        border-right: 15px solid {accent};
        margin-bottom: 30px;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.5);
    }}
    
    /* تنسيق الجداول بدقة */
    .stTable td {{ 
        color: {txt_main} !important; 
        font-weight: bold !important; 
        border: 1px solid {accent} !important;
        text-align: center !important;
        font-size: 16px;
    }}
    .stTable th {{ 
        background-color: {accent} !important; 
        color: #1e272e !important; 
        text-align: center !important;
        font-size: 18px;
    }}

    .header-box {{
        background-color: #1e272e;
        padding: 50px;
        border-radius: 30px;
        border: 5px solid {accent};
        border-bottom: 15px solid {accent};
        text-align: center;
        margin-bottom: 50px;
    }}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 4. القائمة الجانبية (Sidebar) - المخزن والتحكم
# =========================================================
with st.sidebar:
    st.markdown(f"<h1 style='color:{accent}; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{txt_main};'><b>المهندس: ياسين علاء</b></p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.subheader("⚙️ الإعدادات")
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
    with c_nav2:
        mode_label = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(mode_label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # --- مخزن جرد الخامات التراكمي ---
    if st.session_state.project_list:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{accent}; text-align:center;'>📦 مخزن المشروع الكلي</h3>", unsafe_allow_html=True)
        
        # الحسابات الكلية بناءً على عدد الأمتار الطولية والمساحة
        t_m_mufard = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        t_m_motaqareb = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        t_f_panels = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("🪵 أعواد مفرد (6م)", f"{round(t_m_mufard, 1)} عود")
        st.metric("🪵 أعواد متقارب (6م)", f"{round(t_m_motaqareb, 1)} عود")
        st.metric("💎 ألواح فيبر (122x280)", f"{round(t_f_panels, 1)} لوح")
        
        if st.button("🗑️ مسح المشروع والبدء من جديد", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# =========================================================
# 5. منطق الشاشات والتنقل
# =========================================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div class="header-box">
            <h1 style="color:{accent}; font-size:5em; margin:0; font-weight:900;">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:2em; font-weight:bold;">نظام تخصيم المطابخ الاحترافي</p>
            <p style="color:{accent}; font-size:1.5em;">برمجة وتطوير المهندس: ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        if st.button("🚀 ابدأ العمل الآن (دخول النظام)", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق الرئيسية (التخصيم) ---
elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent};'>📋 لوحة إدخال البيانات</h2>", unsafe_allow_html=True)
    
    with st.expander("🛠️ إضافة وحدة جديدة (الخانات جاهزة بدون أصفار تعطل الكتابة)", expanded=True):
        col_in1, col_in2, col_in3 = st.columns(3)
        
        with col_in1:
            st.markdown("### 📐 المقاسات الرئيسية")
            u_name = st.text_input("اسم الوحدة (مثال: وحدة حوض)")
            u_type = st.selectbox("نوع الوحدة (سيستم التخصيم)", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
            # تم إزالة الأصفار باستخدام value=None
            w_val = st.number_input("العرض الكلي (W)", value=None, placeholder="0.0")
            h_val = st.number_input("الارتفاع الكلي (H)", value=None, placeholder="0.0")
            d_val = st.number_input("العمق الكلي (D)", value=None, placeholder="0.0")
            
        with col_in2:
            st.markdown("### 🧱 تفاصيل الرفوف")
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
            sh_n = st.number_input("عدد الرفوف", value=None, placeholder="0")
            st.markdown("---")
            st.markdown("### 📐 تفاصيل الفواصل")
            dv_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0.0")
            dv_d = st.number_input("عمق الفاصل", value=None, placeholder="0.0")
            dv_n = st.number_input("عدد الفواصل", value=None, placeholder="0")
            
        with col_in3:
            st.markdown("### 🗄️ تفاصيل الأدراج")
            dr_w = st.number_input("عرض برواز الدرج", value=None, placeholder="0.0")
            dr_d = st.number_input("عمق برواز الدرج", value=None, placeholder="0.0")
            dr_n = st.number_input("عدد الأدراج المطلوبة", value=None, placeholder="0")
            st.markdown("---")
            notes = st.text_area("ملاحظات فنية إضافية")
            
            if st.button("✅ تنفيذ التخصيم وحفظ بالخزنة", use_container_width=True):
                if w_val and h_val:
                    # تطبيق خوارزمية التخصيم (13 للسفلي و 5 للعالي)
                    deduction = 13 if "13" in u_type else 5
                    h_net = int(h_val - deduction)
                    w_net, d_net = int(w_val - 5), int((d_val or 0) - 5)
                    
                    # إنشاء قائمة تقطيع الألومنيوم
                    alum_list = [
                        {"البيان": "قوايم الارتفاع", "المقاس": h_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العرض", "المقاس": w_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العمق", "المقاس": d_net, "العدد": "4 ق"}
                    ]
                    # دمج تفاصيل المهندس ياسين الإضافية
                    if sh_n: alum_list.append({"البيان": "أعواد رفوف", "المقاس": f"{int(sh_w)}x{int(sh_d)}", "العدد": f"{int(sh_n)*4} ق"})
                    if dv_n: alum_data_extra = {"البيان": "أعواد فواصل", "المقاس": f"{int(dv_h)}x{int(dv_d)}", "العدد": f"{int(dv_n)*4} ق"} ; alum_list.append(alum_data_extra)
                    if dr_n: alum_list.append({"البيان": "إطار درج (خصم 2.5)", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{int(dr_n)*4} ق"})

                    # كشف الفيبر
                    fiber_list = [
                        {"القطعة": "فيبر ظهر", "المقاس": f"{w_net}x{h_net}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس": f"{h_net}x{d_net}", "العدد": "2"},
                        {"القطعة": "أرضية/سقف", "المقاس": f"{w_net}x{d_net}", "العدد": "2"}
                    ]

                    # حسابات المخزن (بالمللي لضمان الدقة)
                    m_mufard = (h_net*4 + w_net*4 + d_net*4) + ((sh_w or 0)*4*(sh_n or 0)) + ((dv_h or 0)*4*(dv_n or 0)) + ((dr_w or 0)*4*(dr_n or 0))
                    m_motaqareb = (h_net*2 + w_net*2)
                    f_area = (w_net*h_net) + (h_net*d_net*2) + (w_net*d_net*2)

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w_val}x{h_val}x{d_val}",
                        "alum_df": pd.DataFrame(alum_list), "fiber_df": pd.DataFrame(fiber_list),
                        "m_m": m_mufard, "m_t": m_motaqareb, "f_a": f_area, "note": notes
                    })
                    st.success("تم التخصيم بنجاح وحفظ البيانات!")
                    st.rerun()

    # --- عرض النتائج المحفوظة ---
    if st.session_state.project_list:
        st.markdown(f"<h3 style='color:{accent};'>🧾 كشوفات التقطيع الحالية</h3>", unsafe_allow_html=True)
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f"""
                <div class="unit-card">
                    <h2 style="color:{accent};">#{i+1} {item['name']} | {item['type']}</h2>
                    <p style="font-size:1.2em;">مقاس الوحدة الكلي: <b>{item['dims']} سم</b></p>
                """, unsafe_allow_html=True)
                
                c_res1, c_res2 = st.columns([2, 1])
                with c_res1:
                    st.write("**⚒️ تقطيعات الألومنيوم:**")
                    st.table(item['alum_df'])
                with c_res2:
                    st.write("**🪵 مقاسات الفيبر:**")
                    st.table(item['fiber_df'])
                
                if item['note']: st.info(f"📌 ملاحظة المهندس: {item['note']}")
                st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# 6. تذييل المنظومة (Footer)
# =========================================================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent}; font-weight:bold; font-size:1.3em;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
