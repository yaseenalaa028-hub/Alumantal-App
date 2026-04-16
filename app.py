import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (يجب أن تكون أول سطر)
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# 2. تهيئة مخزن البيانات (session_state)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True  # افتراضي وضع ليلي

# 3. إعدادات الألوان بناءً على الوضع المختار
if st.session_state.dark_mode:
    bg_color = "#1e272e"
    text_color = "#ffffff"
    card_bg = "#2d3436"
    table_text = "#ffffff"
else:
    bg_color = "#f5f6fa"
    text_color = "#1e272e"
    card_bg = "#ffffff"
    table_text = "#2f3640"

# 4. الحماية وتنسيق الواجهة (CSS)
st.markdown(f"""
    <style>
    /* إخفاء علامة القطة (GitHub) والمنيو واللوجو تماماً */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    /* منع التحديد لحماية الكود من السرقة */
    body {{
        background-color: {bg_color};
        color: {text_color};
        -webkit-user-select: none;
        user-select: none;
    }}

    /* تنسيق الكروت والجداول */
    .unit-card {{
        background-color: {card_bg};
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid #f1c40f;
        margin-bottom: 30px;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.3);
        color: {text_color};
    }}
    .stTable td {{ 
        color: {table_text} !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        border: 1px solid #f1c40f !important;
    }}
    .stTable th {{ 
        background-color: #f1c40f !important; 
        color: #1e272e !important; 
    }}
    
    .header-box {{
        background-color: #1e272e; padding: 30px; border-radius: 15px;
        border: 3px solid #f1c40f; border-bottom: 10px solid #f1c40f;
        text-align: center; margin-bottom: 40px;
    }}
    .main-title {{ color: #f1c40f; font-size: 3.5em; margin: 0; font-weight: 900; }}
    </style>
""", unsafe_allow_html=True)

# 5. القائمة الجانبية (الأزرار والجرد)
with st.sidebar:
    st.markdown("<h1 style='color:#f1c40f; text-align:center;'>DOGGA SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{text_color};'>برمجة: م/ ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # أزرار التحكم
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🏠 الرئيسية"):
            st.session_state.page = 'welcome'
            st.rerun()
    with col_btn2:
        mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(mode_icon):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("---")
    
    # قسم الجرد (Calculations)
    if st.session_state.project_list:
        st.markdown("<h3 style='color:#f1c40f;'>📊 إجمالي المشروع</h3>", unsafe_allow_html=True)
        tm = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tt = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tf = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("🪵 أعواد مفرد", f"{round(tm, 1)} عود")
        st.metric("🪵 أعواد متقارب", f"{round(tt, 1)} عود")
        st.metric("💎 ألواح فيبر", f"{round(tf, 1)} لوح")
        
        if st.button("🗑️ مسح المشروع بالكامل", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# 6. شاشات النظام
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 class="main-title">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:1.5em; font-weight:bold;">المنظومة الاحترافية لتخصيمات المطابخ</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ابدأ العمل الآن", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

elif st.session_state.page == 'app':
    with st.expander("📝 إضافة وحدة جديدة", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
            w = st.number_input("العرض (سم)", min_value=0.0)
            h = st.number_input("الارتفاع (سم)", min_value=0.0)
            d = st.number_input("العمق (سم)", min_value=0.0)
        with c2:
            st.markdown("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
        with c3:
            st.markdown("**🗄️ الأدراج والملاحظات**")
            dr_w = st.number_input("عرض الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            u_notes = st.text_area("ملاحظات")
            
            if st.button("✅ حفظ وتحسيب", use_container_width=True):
                if w > 0 and h > 0:
                    # معادلات التخصيم الأساسية
                    h_b = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_b, d_b = int(w - 5), int(d - 5)
                    
                    # توزيع مفرد ومتقارب
                    if u_type == "سفلية":
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 3, 1, 2, 2
                    else:
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 2, 2, 0, 4

                    # بناء جداول الألومنيوم والفيبر
                    alum_rows = [
                        {"البند": "قوايم الارتفاع", "مقاس المفرد": h_b, "عدد": f"{h_m} ق", "مقاس المتقارب": h_b, "عدد ": f"{h_t} ق"},
                        {"البند": "عوارض العرض", "مقاس المفرد": w_b, "عدد": f"{w_m} ق", "مقاس المتقارب": w_b, "عدد ": f"{w_t} ق"},
                        {"البند": "عوارض العمق", "مقاس المفرد": d_b if d_m>0 else "-", "عدد": f"{d_m} ق" if d_m>0 else "-", "مقاس المتقارب": d_b if d_t>0 else "-", "عدد ": f"{d_t} ق" if d_t>0 else "-"}
                    ]
                    
                    if sh_n > 0:
                        alum_rows.append({"البند": "عوارض الرف", "مقاس المفرد": int(sh_w), "عدد": f"{sh_n*2} ق", "مقاس المتقارب": int(sh_d), "عدد ": f"{sh_n*2} ق"})
                    if dr_n > 0:
                        alum_rows.append({"البند": "إطارات الأدراج", "مقاس المفرد": int(dr_w-2.5), "عدد": f"{dr_n*2} ق", "مقاس المتقارب": int(dr_d), "عدد ": f"{dr_n*2} ق"})

                    fiber_rows = [
                        {"القطعة": "فيبر ضهرية", "المقاس": f"{w_b} x {h_b}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس": f"{h_b} x {d_b}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس": f"{w_b} x {d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]

                    # حساب الجرد
                    m_m = (h_b*h_m) + (w_b*w_m) + (d_b*d_m) + (sh_w*2 + sh_d*2)*sh_n + ((dr_w-2.5)*2 + dr_d*2)*dr_n
                    m_t = (h_b*h_t) + (w_b*w_t) + (d_b*d_t)
                    f_area = (w_b*h_b) + (h_b*d_b*2) + (w_b*d_b*(1 if u_type=="سفلية" else 2))

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}",
                        "alum": pd.DataFrame(alum_rows), "fiber": pd.DataFrame(fiber_rows),
                        "m_m": m_m, "m_t": m_t, "f_a": f_area, "notes": u_notes
                    })
                    st.rerun()

    # عرض كشوف التقطيع
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]} ({item["dims"]} سم)</h3>', unsafe_allow_html=True)
        c_tab1, c_tab2 = st.columns([2, 1])
        with c_tab1:
            st.markdown("<h4 style='color:#f1c40f;'>⚔️ الألومنيوم</h4>", unsafe_allow_html=True)
            st.table(item['alum'])
        with c_tab2:
            st.markdown("<h4 style='color:#f1c40f;'>🪵 الفيبر</h4>", unsafe_allow_html=True)
            st.table(item['fiber'])
        if item['notes']: st.warning(f"📌 {item['notes']}")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; padding:30px; font-weight:bold; color:#f1c40f;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
