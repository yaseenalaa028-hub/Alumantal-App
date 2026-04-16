import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (Eng. Yassin Alaa)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إدارة الحالة (الدرك مود والبيانات)
# ==========================================
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# تعريف الألوان بناءً على الوضع
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
    st.markdown("<style>.stApp {background-color: #0e1117; color: white;}</style>", unsafe_allow_html=True)
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"
    st.markdown("<style>.stApp {background-color: white; color: black;}</style>", unsafe_allow_html=True)

# ==========================================
# 3. CSS التصميم والاحترافية
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ direction: rtl !important; text-align: right; }}
    .mini-logo {{
        border: 1px solid {accent};
        padding: 5px 15px;
        border-radius: 8px;
        display: inline-block;
        font-weight: bold;
        color: {accent};
    }}
    .nav-card {{
        background: {card};
        padding: 30px;
        border-radius: 15px;
        border: 2px solid {accent};
        text-align: center;
        margin-top: 50px;
    }}
    .stat-box {{
        background: {card};
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid {accent};
        text-align: center;
    }}
    .unit-box {{
        background: {card};
        border-right: 10px solid {accent};
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# شريط علوي ثابت (اللوجو + زرار الدرك مود)
top_l, top_r = st.columns([10, 2])
with top_l:
    st.markdown(f'<div class="mini-logo">DOGGA SYSTEM | م/ ياسين علاء</div>', unsafe_allow_html=True)
with top_r:
    mode_label = "🌙 وضع النوم" if not st.session_state.dark_mode else "☀️ وضع النهار"
    if st.button(mode_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 4. التنقل بين الصفحات
# ==========================================

# --- الصفحة الأولى: الوجهة الرئيسية ---
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="nav-card">
            <h1 style="color:{accent}; font-size: 3.5em;">DOGGA SYSTEM</h1>
            <p style="font-size: 1.2em;">نظام تخصيم الألومنيوم والفيبر - إصدار 2026</p>
            <p>برمجة المهندس: <b>ياسين علاء</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.write("### 📊 خلاصة المشروع الحالي")
    c1, c2, c3 = st.columns(3)
    total_m = sum([x['raw_m'] for x in st.session_state.project_list]) / 600
    with c1: st.markdown(f'<div class="stat-box"><h3>{len(st.session_state.project_list)}</h3><p>وحدة مضافة</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-box"><h3>{round(total_m, 1)}</h3><p>عود ألومنيوم</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-box"><h3>2026</h3><p>سنة الإصدار</p></div>', unsafe_allow_html=True)

    st.write("---")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("➕ إضافة مقاسات جديدة", use_container_width=True, type="primary"):
            st.session_state.page = 'calc'
            st.rerun()
    with btn_col2:
        if st.button("📄 عرض شيتات التفصيل", use_container_width=True):
            st.session_state.page = 'report'
            st.rerun()

# --- الصفحة الثانية: حساب المقاسات ---
elif st.session_state.page == 'calc':
    if st.button("⬅️ عودة للوجهة الرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown("### 📏 حساب المقاسات والتخصيم")
    with st.form("calc_form"):
        # الترتيب: العميل -> النوع -> المقاسات
        f_col1, f_col2 = st.columns(2)
        with f_col1: client = st.text_input("اسم العميل / كود الوحدة")
        with f_col2: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: w_in = st.number_input("العرض الكلي (سم)", value=0.0)
        with m_col2: h_in = st.number_input("الارتفاع الكلي (سم)", value=0.0)
        with m_col3: d_in = st.number_input("العمق الكلي (سم)", value=0.0)
        
        st.markdown("**➕ الإضافات (أرفف، فواصل، أدراج)**")
        a_col1, a_col2, a_col3 = st.columns(3)
        with a_col1:
            sh_n = st.number_input("عدد الأرفف", value=0)
            sh_w = st.number_input("عرض الرف", value=0.0); sh_d = st.number_input("عمق الرف", value=0.0)
        with a_col2:
            v_n = st.number_input("عدد الفواصل", value=0)
            v_h = st.number_input("ارتفاع الفاصل", value=0.0); v_d = st.number_input("عمق الفاصل", value=0.0)
        with a_col3:
            dr_n = st.number_input("عدد الأدراج", value=0)
            dr_w = st.number_input("عرض الدرج", value=0.0); dr_d = st.number_input("عمق الدرج", value=0.0)
        
        if st.form_submit_button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
            if w_in > 0 and h_in > 0:
                # منطق المهندس ياسين
                h_ded = 13 if (u_type == "وحدة سفلية" or u_type == "دولاب خزين") else 5
                h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

                # ألومنيوم
                if u_type == "وحدة سفلية":
                    alum = [["قوايم ارتفاع", h_net, 2, 2], ["عوارض عرض", w_net, 3, 1], ["عوارض عمق", d_net, 2, 2]]
                else:
                    alum = [["قوايم ارتفاع", h_net, 2, 2], ["عوارض عرض", w_net, 2, 2], ["عوارض عمق", d_net, 0, 4]]
                
                # إضافات
                if sh_n > 0: alum.append([f"أعواد رف ({sh_n})", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
                if v_n > 0: alum.append([f"أعواد فاصل ({v_n})", int(v_h), v_n*4, 0])
                if dr_n > 0: alum.append([f"براويز درج ({dr_n})", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

                # فيبر
                fiber = [["الظهرية", f"{w_net}x{h_net}", 1], ["الأرضية", f"{w_net}x{d_net}", 1], ["الأجناب", f"{h_net}x{d_net}", 2]]
                if sh_n > 0: fiber.append(["فيبر أرفف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

                st.session_state.project_list.append({
                    "client": client, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                    "alum_df": pd.DataFrame(alum, columns=["البيان", "المقاس", "مفرد", "متقارب"]),
                    "fiber_df": pd.DataFrame(fiber, columns=["القطعة", "المقاس", "العدد"]),
                    "raw_m": (h_net*4 + w_net*4 + d_net*4)
                })
                st.session_state.page = 'home'
                st.rerun()

# --- الصفحة الثالثة: شيتات التفصيل ---
elif st.session_state.page == 'report':
    if st.button("⬅️ عودة للوجهة الرئيسية"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.subheader("📄 شيتات التفصيل الكاملة")
    if not st.session_state.project_list:
        st.info("لا توجد وحدات مضافة بعد.")
    else:
        for item in st.session_state.project_list:
            with st.container():
                st.markdown(f'<div class="unit-box"><b>📌 {item["client"]} | {item["dims"]}</b></div>', unsafe_allow_html=True)
                col_a, col_f = st.columns([3, 2])
                with col_a: st.table(item['alum_df'])
                with col_f: st.table(item['fiber_df'])
        
        st.divider()
        if st.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_list = []
            st.session_state.page = 'home'
            st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
