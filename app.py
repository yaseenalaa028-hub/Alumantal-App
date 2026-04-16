import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (برمجة المهندس ياسين علاء)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إدارة الحالة وتأمين البيانات
# ==========================================
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# تعريف الألوان
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

# ==========================================
# 3. CSS الاحترافي (لمسة المهندس ياسين)
# ==========================================
st.markdown(f"""
    <style>
    .block-container {{ max-width: 100% !important; padding: 1rem 2rem !important; }}
    .stApp {{ background-color: {bg} !important; color: {txt} !important; direction: rtl !important; }}
    
    .brand-box {{
        text-align: center;
        padding: 25px;
        background: {card};
        border-radius: 15px;
        border: 3px solid {accent};
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }}
    
    .unit-card {{
        background-color: {card};
        padding: 15px;
        border-radius: 10px;
        border-right: 12px solid {accent};
        margin-bottom: 20px;
        position: relative;
    }}
    
    /* توقيع المهندس في كل مكان */
    .yassin-watermark {{
        position: fixed;
        bottom: 10px;
        left: 10px;
        opacity: 0.5;
        font-size: 0.8em;
        color: {accent};
        z-index: 100;
    }}

    .section-head {{
        color: {accent};
        font-weight: bold;
        border-bottom: 2px solid {accent};
        margin-bottom: 15px;
        text-align: center;
    }}
    
    header, footer {{visibility: hidden !important;}}
    </style>
    <div class="yassin-watermark">Developed by: Eng. Yassin Alaa</div>
""", unsafe_allow_html=True)

# زرار الـ Dark Mode واسم المهندس فوق
top_l, top_r = st.columns([10, 2])
with top_r:
    mode_btn = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(mode_btn):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
with top_l:
    st.markdown(f"<p style='color:{accent};'>المهندس ياسين علاء | DOGGA SYSTEM</p>", unsafe_allow_html=True)

# ==========================================
# 4. محتوى الصفحات
# ==========================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:80px;">
            <div class="brand-box">
                <h1 style="color:{accent}; font-size:5em; font-weight:900; margin:0;">DOGGA SYSTEM</h1>
                <h3 style="color:{txt}; margin:10px 0;">"الدقة في التفاصيل.. سر الاحتراف"</h3>
                <hr style="border-color:{accent}; width:40%; margin: 15px auto;">
                <h2 style="color:{accent};">برمجة وتطوير: المهندس ياسين علاء</h2>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🚀 ابدأ العمل الآن", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- لوحة العمل الداخلية ---
elif st.session_state.page == 'app':
    nav_1, nav_2 = st.columns([1, 8])
    with nav_1:
        if st.button("⬅️ خروج"):
            st.session_state.page = 'welcome'
            st.rerun()
    with nav_2:
        st.markdown(f"<h2 style='color:{accent};'>📋 لوحة التخصيم - المهندس ياسين علاء</h2>", unsafe_allow_html=True)

    st.write("---")

    # مدخلات البيانات
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<p class="section-head">📏 المقاسات الرئيسية</p>', unsafe_allow_html=True)
            u_name = st.text_input("كود الوحدة")
            u_type = st.selectbox("نوع الخصم", ["سفلية (13سم)", "علوية (5سم)", "دولاب (13سم)"])
            w = st.number_input("العرض (W)", min_value=0.0, format="%.1f")
            h = st.number_input("الارتفاع (H)", min_value=0.0, format="%.1f")
            d = st.number_input("العمق (D)", min_value=0.0, format="%.1f")
        with c2:
            st.markdown('<p class="section-head">🧱 الرفوف</p>', unsafe_allow_html=True)
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
        with c3:
            st.markdown('<p class="section-head">↕️ الفواصل</p>', unsafe_allow_html=True)
            v_h = st.number_input("ارتفاع الفاصل", value=0.0)
            v_d = st.number_input("عمق الفاصل", value=0.0)
            v_n = st.number_input("عدد الفواصل", value=0)
        with c4:
            st.markdown('<p class="section-head">🗄️ الأدراج</p>', unsafe_allow_html=True)
            dr_w = st.number_input("عرض برواز الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            
            st.write("")
            if st.button("✅ حفظ وحساب المهندس ياسين", use_container_width=True):
                if w > 0 and h > 0:
                    ded = 13 if "13" in u_type else 5
                    h_n, w_n, d_n = int(h - ded), int(w - 5), int(d - 5)
                    
                    # جداول الألومنيوم (المتقارب)
                    g_df = pd.DataFrame([
                        ["قوايم رئيسية", h_n, 4],
                        ["عوارض عرض", w_n, 4],
                        ["عوارض عمق", d_n, 4]
                    ], columns=["البيان", "المقاس", "العدد"])
                    
                    # جداول الألومنيوم (المفرد)
                    s_data = []
                    if sh_n > 0: s_data.append(["عضو رف", f"{int(sh_w)}x{int(sh_d)}", sh_n*4])
                    if v_n > 0: s_data.append(["عضو فاصل", f"{int(v_h)}x{int(v_d)}", v_n*4])
                    if dr_n > 0: s_data.append(["برواز درج", f"{int(dr_w)}x{int(dr_d)}", dr_n*4])
                    s_df = pd.DataFrame(s_data, columns=["البيان", "المقاس", "العدد"]) if s_data else None

                    # جدول الفيبر
                    f_df = pd.DataFrame([
                        ["الظهر", f"{w_n}x{h_n}", 1],
                        ["الجوانب", f"{d_n}x{h_n}", 2],
                        ["أرضية/سقف", f"{w_n}x{d_n}", 2]
                    ], columns=["القطعة", "المقاس", "العدد"])

                    st.session_state.project_list.append({
                        "header": f"وحدة: {u_name} | مقاس: {w}x{h}x{d}",
                        "alum_g": g_df,
                        "alum_s": s_df,
                        "fiber": f_df,
                        "meterage": (h_n*4 + w_n*4 + d_n*4)
                    })
                    st.rerun()

    # عرض النتائج
    st.write("---")
    for item in st.session_state.project_list:
        st.markdown(f"""
            <div class="unit-card">
                <h3 style="margin:0;">{item['header']}</h3>
                <small>بإشراف المهندس ياسين علاء</small>
            </div>
        """, unsafe_allow_html=True)
        
        ca, cb, cf = st.columns(3)
        with ca:
            st.markdown("**🔗 ألومنيوم (متقارب)**")
            st.table(item['alum_g'])
        with cb:
            st.markdown("**📍 ألومنيوم (مفرد)**")
            if item['alum_s'] is not None: st.table(item['alum_s'])
            else: st.info("لا توجد إضافات")
        with cf:
            st.markdown("**✨ تفصيل الفيبر**")
            st.table(item['fiber'])

    if st.session_state.project_list:
        st.write("---")
        if st.button("📊 جرد المشروع النهائي", use_container_width=True):
            total_m = sum([x['meterage'] for x in st.session_state.project_list]) / 600
            st.success(f"إجمالي الألومنيوم المطلوب للمهندس ياسين: {round(total_m, 1)} عود")
            if st.button("🗑️ مسح الكل"):
                st.session_state.project_list = []
                st.rerun()

# التذييل النهائي
st.markdown(f"<p style='text-align:center; color:{accent}; font-weight:bold;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
