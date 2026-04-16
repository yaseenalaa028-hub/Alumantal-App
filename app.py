import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وحماية مجهود المهندس ياسين علاء
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# 2. تهيئة المخزن والحالات (لضمان عدم ضياع البيانات عند التبديل)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

# 3. نظام الألوان (ديناميكي بناءً على الزر)
bg = "#1e272e" if st.session_state.dark_mode else "#ffffff"
txt = "#ffffff" if st.session_state.dark_mode else "#1e272e"
card = "#2d3436" if st.session_state.dark_mode else "#f8f9fa"

st.markdown(f"""
    <style>
    /* حماية مجهود المهندس: إخفاء القطة والمنيو العلوي تماماً */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    /* منع تحديد النصوص لحماية الكود */
    body {{
        background-color: {bg} !important;
        color: {txt} !important;
        -webkit-user-select: none;
        user-select: none;
    }}

    /* تنسيق كروت الوحدات */
    .unit-card {{
        background-color: {card};
        padding: 25px;
        border-radius: 15px;
        border-right: 15px solid #f1c40f;
        margin-bottom: 30px;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.3);
    }}
    
    /* تنسيق جداول التخصيم */
    .stTable td {{ 
        color: {txt} !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        border: 1px solid #f1c40f !important;
        text-align: center !important;
    }}
    .stTable th {{ 
        background-color: #f1c40f !important; 
        color: #1e272e !important; 
    }}
    </style>
""", unsafe_allow_html=True)

# 4. القائمة الجانبية (الأزرار + مخزن الجرد الكلي)
with st.sidebar:
    st.markdown("<h1 style='color:#f1c40f; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{txt};'>المهندس ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # أزرار التحكم الجديدة
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🏠 الرئيسية"):
            st.session_state.page = 'welcome'
            st.rerun()
    with col_s2:
        mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(mode_icon):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # مخزن المشروع (الجرد الكلي للخامات)
    if st.session_state.project_list:
        st.markdown("---")
        st.markdown("<h3 style='color:#f1c40f;'>📊 إجمالي خامات المشروع</h3>", unsafe_allow_html=True)
        # حسابات الجرد بناءً على كل الوحدات المضافة
        total_mufard = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_motaqareb = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_fiber = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("🪵 أعواد مفرد", f"{round(total_mufard, 1)} عود")
        st.metric("🪵 أعواد متقارب", f"{round(total_motaqareb, 1)} عود")
        st.metric("💎 ألواح فيبر", f"{round(total_fiber, 1)} لوح")
        
        if st.button("🗑️ مسح المشروع بالكامل", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# 5. عرض الشاشات
# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="background-color:#1e272e; padding:40px; border-radius:20px; border:4px solid #f1c40f; border-bottom:12px solid #f1c40f; text-align:center;">
            <h1 style="color:#f1c40f; font-size:4em; margin:0;">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:1.5em; font-weight:bold;">المنظومة الاحترافية لتخصيمات المطابخ الحديثة</p>
            <p style="color:#f1c40f; font-size:1.2em;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("\n")
    c_w1, c_w2, c_w3 = st.columns([1, 2, 1])
    with c_w2:
        if st.button("🚀 دخول نظام التخصيم", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق الرئيسية ---
elif st.session_state.page == 'app':
    with st.expander("📝 إضافة مقاسات وتفاصيل الوحدة", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
            w = st.number_input("العرض الكلي (سم)", value=0.0)
            h = st.number_input("الارتفاع الكلي (سم)", value=0.0)
            d = st.number_input("العمق الكلي (سم)", value=0.0)
        with col2:
            st.write("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
            dv_h = st.number_input("ارتفاع الفاصل الداخلي", value=0.0)
            dv_n = st.number_input("عدد الفواصل", value=0)
        with col3:
            st.write("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            
            if st.button("✅ حفظ وتحسيب التخصيم", use_container_width=True):
                if w > 0 and h > 0:
                    # معادلات التخصيم الأساسية
                    h_calc = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_calc, d_calc = int(w - 5), int(d - 5)
                    
                    # بناء جدول الألومنيوم بالتفصيل
                    alum_rows = [
                        {"البند": "قوايم الارتفاع", "مقاس المفرد": h_calc, "عدد": "2 ق", "مقاس المتقارب": h_calc, "عدد ": "2 ق"},
                        {"البند": "عوارض العرض", "مقاس المفرد": w_calc, "عدد": "3 ق" if u_type=="سفلية" else "2 ق", "مقاس المتقارب": w_calc, "عدد ": "1 ق" if u_type=="سفلية" else "2 ق"},
                        {"البند": "عوارض العمق", "مقاس المفرد": d_calc, "عدد": "2 ق", "مقاس المتقارب": d_calc, "عدد ": "2 ق"}
                    ]
                    
                    # إضافة الرفوف، الفواصل، والأدراج
                    if sh_n > 0:
                        alum_rows.append({"البند": "عوارض الرف", "مقاس المفرد": int(sh_w), "عدد": f"{sh_n*2} ق", "مقاس المتقارب": int(sh_d), "عدد ": f"{sh_n*2} ق"})
                    if dv_n > 0:
                        alum_rows.append({"البند": "فواصل داخلية", "مقاس المفرد": int(dv_h), "عدد": f"{dv_n*2} ق", "مقاس المتقارب": int(d_calc), "عدد ": f"{dv_n*2} ق"})
                    if dr_n > 0:
                        alum_rows.append({"البند": "إطار درج", "مقاس المفرد": int(dr_w-2.5), "عدد": f"{dr_n*2} ق", "مقاس المتقارب": int(dr_d), "عدد ": f"{dr_n*2} ق"})

                    # بناء جدول الفيبر
                    fiber_rows = [
                        {"القطعة": "فيبر ضهرية", "المقاس الصافي": f"{w_calc} x {h_calc}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس الصافي": f"{h_calc} x {d_calc}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس الصافي": f"{w_calc} x {d_calc}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]

                    # حساب أطوال الأعواد للجرد الإجمالي
                    m_m = (h_calc*2 + w_calc*3 + d_calc*2) + (sh_w*2 + sh_d*2)*sh_n + (dv_h*2 + d_calc*2)*dv_n + (dr_w*2 + dr_d*2)*dr_n
                    m_t = (h_calc*2 + w_calc*1 + d_calc*2)
                    f_a = (w_calc*h_calc) + (h_calc*d_calc*2) + (w_calc*d_calc*2)

                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}",
                        "alum": pd.DataFrame(alum_rows), "fiber": pd.DataFrame(fiber_rows),
                        "m_m": m_m, "m_t": m_t, "f_a": f_a
                    })
                    st.rerun()

    # عرض كشوف تقطيع الوحدات المضافة
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]} ({item["dims"]} سم)</h3>', unsafe_allow_html=True)
        c_res1, c_res2 = st.columns([2, 1])
        with c_res1:
            st.markdown("<h4 style='color:#f1c40f;'>⚔️ تخصيم الألومنيوم</h4>", unsafe_allow_html=True)
            st.table(item['alum'])
        with c_res2:
            st.markdown("<h4 style='color:#f1c40f;'>🪵 تخصيم الفيبر</h4>", unsafe_allow_html=True)
            st.table(item['fiber'])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; padding:30px; font-weight:bold; color:#f1c40f;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
