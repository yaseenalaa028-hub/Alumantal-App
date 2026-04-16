import streamlit as st
import pandas as pdشimport streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (إجبار العرض الكامل)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إدارة الحالة والوضع الليلي
# ==========================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# تعريف الألوان
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

# ==========================================
# 3. CSS لمنع تداخل الكلام وتوسيع الواجهة
# ==========================================
st.markdown(f"""
    <style>
    .block-container {{
        max-width: 100% !important;
        padding: 0.5rem 2rem !important;
    }}
    .stApp {{
        background-color: {bg} !important;
        color: {txt} !important;
        direction: rtl !important;
    }}
    .unit-card {{
        background-color: {card};
        padding: 15px;
        border-radius: 10px;
        border-right: 10px solid {accent};
        margin-bottom: 10px;
    }}
    header, footer {{visibility: hidden !important;}}
    .section-head {{
        color: {accent};
        font-weight: bold;
        border-bottom: 1px solid {accent};
        margin-bottom: 15px;
        padding-bottom: 5px;
        text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. شريط التحكم العلوي (Dark Mode لوحده)
# ==========================================
t_col1, t_col2 = st.columns([12, 1])
with t_col2:
    mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(mode_icon, key="mode_switch"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 5. محتوى الصفحات
# ==========================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:150px;">
            <h1 style="color:{accent}; font-size:5em; font-weight:900; margin:0;">DOGGA SYSTEM</h1>
            <p style="font-size:1.5em; margin-top:0;">المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, b_col, _ = st.columns([1, 1, 1])
    with b_col:
        if st.button("🚀 دخول لوحة المقاسات", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- لوحة العمل الداخلية (app) ---
elif st.session_state.page == 'app':
    # زرار الرجوع في أعلى الوجهة الداخلية
    n_col1, n_col2 = st.columns([1, 8])
    with n_col1:
        if st.button("⬅️ رجوع"):
            st.session_state.page = 'welcome'
            st.rerun()
    with n_col2:
        st.markdown(f"<h2 style='color:{accent}; margin:0;'>📋 لوحة إدخال المقاسات والتخصيم</h2>", unsafe_allow_html=True)

    st.write("---")

    # نموذج الإدخال (كل بند لوحده وبترتيب دقيق)
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown('<p class="section-head">📏 المقاسات الأساسية</p>', unsafe_allow_html=True)
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الخصم", ["سفلية (13سم)", "علوية (5سم)", "دولاب (13سم)"])
            w = st.number_input("العرض الكلي (W)", value=None)
            h = st.number_input("الارتفاع الكلي (H)", value=None)
            d = st.number_input("العمق الكلي (D)", value=None)
            
        with c2:
            st.markdown('<p class="section-head">🧱 الرفوف</p>', unsafe_allow_html=True)
            sh_w = st.number_input("عرض الرف", value=None)
            sh_d = st.number_input("عمق الرفوف", value=None)
            sh_n = st.number_input("عدد الرفوف", value=None, step=1)
            
        with c3:
            st.markdown('<p class="section-head">↕️ الفواصل</p>', unsafe_allow_html=True)
            v_h = st.number_input("ارتفاع الفاصل", value=None)
            v_d = st.number_input("عمق الفواصل", value=None)
            v_n = st.number_input("عدد الفواصل", value=None, step=1)
            
        with c4:
            st.markdown('<p class="section-head">🗄️ الأدراج</p>', unsafe_allow_html=True)
            dr_w = st.number_input("عرض برواز الدرج", value=None)
            dr_d = st.number_input("عمق الأدراج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=None, step=1)
            st.write("")
            if st.button("✅ حفظ وحساب التخصيم", use_container_width=True):
                if w and h:
                    ded = 13 if "13" in u_type else 5
                    h_n, w_n, d_n = int(h - ded), int(w - 5), int((d or 0) - 5)
                    
                    # بنود الألومنيوم
                    alum = [
                        {"البيان": "قوايم رئيسية", "المقاس": h_n, "العدد": "4 ق"},
                        {"البيان": "عوارض عرض", "المقاس": w_n, "العدد": "4 ق"},
                        {"البيان": "عوارض عمق", "المقاس": d_n, "العدد": "4 ق"}
                    ]
                    
                    if sh_n: alum.append({"البيان": "أعواد رفوف", "المقاس": f"{int(sh_w)}x{int(sh_d or 0)}", "العدد": int(sh_n*4)})
                    if v_n: alum.append({"البيان": "أعواد فواصل", "المقاس": f"{int(v_h)}x{int(v_d or 0)}", "العدد": int(v_n*4)})
                    if dr_n: alum.append({"البيان": "إطار درج", "المقاس": f"{int(dr_w)}x{int(dr_d or 0)}", "العدد": int(dr_n*4)})
                    
                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}", "type": u_type,
                        "alum_df": pd.DataFrame(alum),
                        "m_m": (h_n*4 + w_n*4 + d_n*4) + (int(sh_n or 0)*20),
                        "f_a": (w_net*h_net) + (h_net*d_net*2) if 'w_net' in locals() else 0
                    })
                    st.rerun()

    # عرض الجداول (بعد التخصيم)
    st.write("---")
    for i, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><b>#{i+1} {item["name"]} - {item["dims"]}</b></div>', unsafe_allow_html=True)
        st.table(item['alum_df'])

    # زرار حساب الخامات (في نهاية الصفحة)
    if st.session_state.project_list:
        st.write("---")
        if st.button("📊 حساب إجمالي خامات المشروع بالكامل", use_container_width=True):
            total_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
            st.markdown(f"""
                <div style="background-color:{accent}; color:#000; padding:20px; border-radius:10px; text-align:center;">
                    <h3>التقرير النهائي للمشروع</h3>
                    <p style="font-size:1.5em;">إجمالي أعواد الألومنيوم: <b>{round(total_m, 1)} عود</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️ تفريغ البيانات"):
                st.session_state.project_list = []
                st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)

# ==========================================
# 1. إعدادات المنظومة (العرض الكامل)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إدارة الحالة والوضع الليلي
# ==========================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# تعريف الألوان
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

# ==========================================
# 3. CSS الاحترافي (منع الزحمة وتوسيع الواجهة)
# ==========================================
st.markdown(f"""
    <style>
    .block-container {{
        max-width: 100% !important;
        padding: 0.5rem 2rem !important;
    }}
    .stApp {{
        background-color: {bg} !important;
        color: {txt} !important;
        direction: rtl !important;
    }}
    .unit-card {{
        background-color: {card};
        padding: 20px;
        border-radius: 12px;
        border-right: 10px solid {accent};
        margin-bottom: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }}
    header, footer {{visibility: hidden !important;}}
    
    /* تنسيق الجداول لتكون عريضة واضحة */
    .stTable {{
        width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. شريط التحكم العلوي (زرار الدرك مود لوحده)
# ==========================================
top_col1, top_col2 = st.columns([12, 1])
with top_col2:
    mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(mode_icon, help="تبديل الوضع"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 5. محتوى الصفحات
# ==========================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:150px;">
            <h1 style="color:{accent}; font-size:5em; font-weight:900; margin-bottom:0;">DOGGA SYSTEM</h1>
            <p style="font-size:1.5em; margin-top:0;">المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, btn_start, _ = st.columns([1, 1, 1])
    with btn_start:
        if st.button("🚀 دخول لوحة المقاسات", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- لوحة العمل الداخلية (app) ---
elif st.session_state.page == 'app':
    # شريط علوي داخلي فيه زرار الرجوع
    nav_col1, nav_col2 = st.columns([1, 8])
    with nav_col1:
        if st.button("⬅️ رجوع"):
            st.session_state.page = 'welcome'
            st.rerun()
    with nav_col2:
        st.markdown(f"<h2 style='color:{accent}; margin:0;'>📋 لوحة إدخال المقاسات</h2>", unsafe_allow_html=True)

    st.write("---")

    # نموذج الإدخال (3 أعمدة عريضة) مع الحفاظ على بنود الإدخال
    with st.container():
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"**📏 المقاسات الأساسية**")
            u_name = st.text_input("اسم الوحدة", placeholder="مثال: وحدة أدراج")
            u_type = st.selectbox("نوع التخصيم", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
            w = st.number_input("العرض الكلي (W)", value=None)
            
        with c2:
            st.markdown(f"**🧱 الرفوف والفواصل**")
            h = st.number_input("الارتفاع الكلي (H)", value=None)
            d = st.number_input("العمق الكلي (D)", value=None)
            sh_n = st.number_input("عدد الرفوف", value=None)
            v_n = st.number_input("عدد الفواصل", value=None)
            
        with c3:
            st.markdown(f"**🗄️ الأدراج والإضافات**")
            dr_n = st.number_input("عدد الأدراج", value=None)
            note = st.text_area("ملاحظات فنية")
            
            st.write("") # مسافة
            if st.button("✅ حفظ الوحدة وتخصيمها", use_container_width=True):
                if w and h:
                    # أساسيات التخصيم (م/ ياسين علاء)
                    ded = 13 if "13" in u_type else 5
                    h_net = int(h - ded)
                    w_net, d_net = int(w - 5), int((d or 0) - 5)
                    
                    # كشف الألومنيوم
                    alum = [
                        {"البيان": "قوايم رئيسية", "المقاس": h_net, "العدد": "4"},
                        {"البيان": "عوارض عرض", "المقاس": w_net, "العدد": "4"},
                        {"البيان": "عوارض عمق", "المقاس": d_net, "العدد": "4"}
                    ]
                    
                    if v_n: alum.append({"البيان": "أعواد فواصل", "المقاس": "تلقائي", "العدد": int(v_n*4)})
                    
                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}", "type": u_type,
                        "alum_df": pd.DataFrame(alum),
                        "m_m": (h_net*4 + w_net*4 + d_net*4),
                        "f_a": (w_net*h_net) + (h_net*d_net*2) + (w_net*d_net*2),
                        "note": note
                    })
                    st.rerun()

    # عرض الجداول بعد التخصيم
    st.write("---")
    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f"""
                <div class="unit-card">
                    <h3 style="color:{accent}; margin:0;">#{i+1} {item['name']} | مقاس {item['dims']} | ({item['type']})</h3>
                </div>
            """, unsafe_allow_html=True)
            
            res_c1, res_c2 = st.columns([3, 1])
            with res_c1:
                st.table(item['alum_df'])
            with res_c2:
                st.metric("مساحة الفيبر (سم²)", item['f_a'])
                if item['note']: st.caption(f"📌 {item['note']}")

    # زرار حساب الخامات (في آخر الجداول)
    if st.session_state.project_list:
        st.write("---")
        if st.button("📊 حساب إجمالي خامات المشروع بالكامل", use_container_width=True):
            total_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
            total_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
            
            st.markdown(f"""
                <div style="background-color:{accent}; color:#000; padding:30px; border-radius:15px; text-align:center;">
                    <h2>تقرير جرد المشروع (DOGGA SYSTEM)</h2>
                    <hr style="border:1px solid #000">
                    <p style="font-size:1.5em;">إجمالي أعواد الألومنيوم: <b>{round(total_m, 1)} عود</b></p>
                    <p style="font-size:1.5em;">إجمالي ألواح الفيبر: <b>{round(total_f, 1)} لوح</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️ مسح المشروع والبدء من جديد"):
                st.session_state.project_list = []
                st.rerun()

# تذييل المنظومة
st.markdown(f"<p style='text-align:center; color:{accent}; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
