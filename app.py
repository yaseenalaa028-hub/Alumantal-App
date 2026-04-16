import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وحماية مجهود المهندس ياسين علاء
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# تهيئة المخزن وحالة النظام
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = False

# ألوان النظام بناءً على وضع الإضاءة
bg_color = "#1e272e" if st.session_state.dark_mode else "#ffffff"
text_color = "#ffffff" if st.session_state.dark_mode else "#1e272e"
card_bg = "#2d3436" if st.session_state.dark_mode else "#f8f9fa"

st.markdown(f"""
    <style>
    /* حماية مجهود المهندس: إخفاء القطة، المنيو، وزر Fork */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    button[title="View source"] {{ display: none !important; }}
    
    /* منع تحديد النصوص بالماوس لزيادة الأمان */
    body {{
        background-color: {bg_color};
        color: {text_color};
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }}

    /* تنسيق جداول التخصيمات */
    .stTable td {{ 
        font-size: 20px !important; 
        font-weight: bold !important; 
        color: {text_color} !important; 
        text-align: center !important;
        border: 1px solid #f1c40f !important;
    }}
    .stTable th {{ 
        background-color: #f1c40f !important; 
        color: #1e272e !important; 
        font-size: 18px !important;
    }}

    /* الهيدر المنسق (DOGGA SYSTEM) */
    .header-box {{ 
        background-color: #1e272e; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #f1c40f; 
        border-bottom: 8px solid #f1c40f; 
        text-align: center; 
        margin-bottom: 30px; 
    }}
    .main-title {{ color: #f1c40f; font-size: 3em; margin: 0; font-weight: 900; }}
    .sub-title {{ color: #ffffff; font-size: 1.4em; margin-top: 10px; font-weight: bold; }}
    
    .unit-card {{ 
        background-color: {card_bg}; 
        padding: 20px; 
        border-radius: 15px; 
        border-right: 15px solid #f1c40f; 
        margin-bottom: 30px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3); 
    }}
    .table-header {{
        background-color: #f1c40f; 
        color: #1e272e; 
        padding: 8px; 
        border-radius: 5px; 
        font-weight: bold; 
        margin-top: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (التحكم والجرد) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#f1c40f;'>🛠️ لوحة التحكم</h2>", unsafe_allow_html=True)
    
    # أزرار الوضع والرجوع
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🏠 الرئيسية"):
            st.session_state.page = 'welcome'
            st.rerun()
    with col_b:
        mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(mode_icon):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("---")
    
    # قسم الجرد الإجمالي
    if st.session_state.project_list:
        st.markdown("<h3 style='color:#f1c40f;'>📊 إجمالي الخامات</h3>", unsafe_allow_html=True)
        tm = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tt = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tf = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        
        st.sidebar.metric("🪵 أعواد مفرد", f"{round(tm, 1)} عود")
        st.sidebar.metric("🪵 أعواد متقارب", f"{round(tt, 1)} عود")
        st.sidebar.metric("💎 ألواح فيبر", f"{round(tf, 1)} لوح")
        
        if st.sidebar.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_list = []
            st.rerun()

# --- 1. واجهة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div class="header-box">
            <h1 class="main-title">DOGGA SYSTEM</h1>
            <p class="sub-title">المنظومة الذكية لتخصيمات المطابخ الحديثة</p>
            <p style="color:#f1c40f; font-weight:bold; font-size:1.2em;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("🚀 ابدأ التخصيم الآن", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- 2. واجهة التطبيق الرئيسية ---
elif st.session_state.page == 'app':
    with st.expander("➕ إضافة وحدة جديدة للمطبخ", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة (مثال: سفلي درجين)")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
            w = st.number_input("العرض الكلي (سم)", min_value=0.0)
            h = st.number_input("الارتفاع الكلي (سم)", min_value=0.0)
            d = st.number_input("العمق الكلي (سم)", min_value=0.0)
        with c2:
            st.markdown("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
            dv_h = st.number_input("ارتفاع الفاصل", value=0.0)
            dv_n = st.number_input("عدد الفواصل", value=0)
        with c3:
            st.markdown("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            u_notes = st.text_area("ملاحظات إضافية")
            
            if st.button("✅ حفظ وتحسيب التخصيم"):
                if w > 0 and h > 0:
                    # معادلات التخصيم الثابتة (13 سم للسفلي و 5 سم للعالي)
                    h_calc = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_calc, d_calc = int(w - 5), int(d - 5)
                    
                    # توزيع القطع (مفرد / متقارب)
                    if u_type == "سفلية":
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 3, 1, 2, 2
                    else:
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 2, 2, 0, 4

                    # بناء بيانات الألومنيوم
                    alum_data = [
                        {"البند": "قوايم الارتفاع", "مقاس المفرد": h_calc, "عدد": f"{h_m} ق", "مقاس المتقارب": h_calc, "عدد ": f"{h_t} ق"},
                        {"البند": "عوارض العرض", "مقاس المفرد": w_calc, "عدد": f"{w_m} ق", "مقاس المتقارب": w_calc, "عدد ": f"{w_t} ق"},
                        {"البند": "عوارض العمق", "مقاس المفرد": d_calc if d_m>0 else "-", "عدد": f"{d_m} ق" if d_m>0 else "-", "مقاس المتقارب": d_calc if d_t>0 else "-", "عدد ": f"{d_t} ق" if d_t>0 else "-"}
                    ]
                    
                    # إضافة الرفوف والأدراج
                    if sh_n > 0:
                        alum_data.append({"البند": "عوارض رف", "مقاس المفرد": int(sh_w), "عدد": f"{sh_n*2} ق", "مقاس المتقارب": int(sh_d), "عدد ": f"{sh_n*2} ق"})
                    if dr_n > 0:
                        alum_data.append({"البند": "إطار درج", "مقاس المفرد": int(dr_w-2.5), "عدد": f"{dr_n*2} ق", "مقاس المتقارب": int(dr_d), "عدد ": f"{dr_n*2} ق"})

                    # بناء بيانات الفيبر
                    fiber_data = [
                        {"القطعة": "فيبر ضهرية", "المقاس الصافي": f"{w_calc} x {h_calc}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس الصافي": f"{h_calc} x {d_calc}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس الصافي": f"{w_calc} x {d_calc}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n > 0: fiber_data.append({"القطعة": "فيبر رفوف", "المقاس الصافي": f"{int(sh_w-5)} x {int(sh_d-5)}", "العدد": sh_n})

                    # حساب أطوال الأعواد للجرد
                    m_m = (h_calc*h_m) + (w_calc*w_m) + (d_calc*d_m) + (sh_w*2 + sh_d*2)*sh_n + ((dr_w-2.5)*2 + dr_d*2)*dr_n
                    m_t = (h_calc*h_t) + (w_calc*w_t) + (d_b*d_t if 'd_b' in locals() else d_calc*d_t)
                    f_a = (w_calc*h_calc) + (h_calc*d_calc*2) + (w_calc*d_calc*(1 if u_type=="سفلية" else 2)) + (sh_w-5)*(sh_d-5)*sh_n

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}",
                        "alum": pd.DataFrame(alum_data), "fiber": pd.DataFrame(fiber_data),
                        "m_m": m_m, "m_t": m_t, "f_a": f_a, "notes": u_notes
                    })
                    st.rerun()

    # عرض كشوف التقطيع لكل وحدة
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]} - {item["dims"]} سم</h3>', unsafe_allow_html=True)
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.markdown('<div class="table-header">⚔️ تفاصيل تقطيع الألومنيوم</div>', unsafe_allow_html=True)
            st.table(item['alum'])
        with col_res2:
            st.markdown('<div class="table-header">🪵 تفاصيل تقطيع الفيبر</div>', unsafe_allow_html=True)
            st.table(item['fiber'])
        if item['notes']: st.warning(f"📌 ملاحظة: {item['notes']}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; padding:30px; font-weight:bold; color:#f1c40f;'>DOGGA SYSTEM 2026 | برمجة المهندس ياسين علاء</div>", unsafe_allow_html=True)
