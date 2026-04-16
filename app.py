import streamlit as st
import pandas as pd

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
# 3. CSS التصميم الملموم والأنيق
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
    .brand-box {{
        text-align: center;
        padding: 20px;
        background: {card};
        border-radius: 15px;
        border: 2px solid {accent};
        display: inline-block;
        margin-bottom: 20px;
    }}
    .unit-card {{
        background-color: {card};
        padding: 15px;
        border-radius: 10px;
        border-right: 10px solid {accent};
        margin-bottom: 15px;
    }}
    .section-head {{
        color: {accent};
        font-weight: bold;
        border-bottom: 1px solid {accent};
        margin-bottom: 15px;
        padding-bottom: 5px;
        text-align: center;
    }}
    header, footer {{visibility: hidden !important;}}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. زرار الـ Dark Mode
# ==========================================
_, t_col = st.columns([12, 1])
with t_col:
    mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(mode_icon, key="mode_switch"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:100px;">
            <div class="brand-box">
                <h1 style="color:{accent}; font-size:4.5em; font-weight:900; margin:0;">DOGGA SYSTEM</h1>
                <h3 style="color:{txt}; margin:10px 0; font-style: italic;">"الدقة في التفاصيل.. سر الاحتراف"</h3>
                <hr style="border-color:{accent}; width:50%; margin: 10px auto;">
                <p style="font-size:1.4em; color:{txt};">برمجة وتطوير: المهندس <b>ياسين علاء</b></p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    _, b_col, _ = st.columns([1, 1, 1])
    with b_col:
        if st.button("🚀 دخول لوحة المقاسات", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- لوحة العمل الداخلية ---
elif st.session_state.page == 'app':
    n_col1, n_col2 = st.columns([1, 8])
    with n_col1:
        if st.button("⬅️ رجوع"):
            st.session_state.page = 'welcome'
            st.rerun()
    with n_col2:
        st.markdown(f"<h2 style='color:{accent}; margin:0;'>📋 لوحة التخصيم والتقطيع الفني</h2>", unsafe_allow_html=True)

    st.write("---")

    # نموذج الإدخال
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<p class="section-head">📏 الأساسيات</p>', unsafe_allow_html=True)
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الخصم", ["سفلية (13سم)", "علوية (5سم)", "دولاب (13سم)"])
            w = st.number_input("العرض الكلي", value=None)
            h = st.number_input("الارتفاع الكلي", value=None)
            d = st.number_input("العمق الكلي", value=None)
        with c2:
            st.markdown('<p class="section-head">🧱 الرفوف</p>', unsafe_allow_html=True)
            sh_w, sh_d = st.number_input("عرض الرف", value=None), st.number_input("عمق الرف", value=None)
            sh_n = st.number_input("عدد الرفوف", value=None, step=1)
        with c3:
            st.markdown('<p class="section-head">↕️ الفواصل</p>', unsafe_allow_html=True)
            v_h, v_d = st.number_input("ارتفاع الفاصل", value=None), st.number_input("عمق الفاصل", value=None)
            v_n = st.number_input("عدد الفواصل", value=None, step=1)
        with c4:
            st.markdown('<p class="section-head">🗄️ الأدراج</p>', unsafe_allow_html=True)
            dr_w, dr_d = st.number_input("عرض الدرج", value=None), st.number_input("عمق الدرج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=None, step=1)
            
            if st.button("✅ حفظ وتخصيم", use_container_width=True):
                if w and h:
                    ded = 13 if "13" in u_type else 5
                    h_n, w_n, d_n = int(h - ded), int(w - 5), int((d or 0) - 5)
                    
                    # 1. الألومنيوم المتقارب (الأساسيات)
                    alum_grouped = [
                        {"البيان": "قوايم رئيسية", "المقاس": h_n, "العدد": 4},
                        {"البيان": "عوارض عرض", "المقاس": w_n, "العدد": 4},
                        {"البيan": "عوارض عمق", "المقاس": d_n, "العدد": 4}
                    ]
                    
                    # 2. الألومنيوم المفرد (الإضافات)
                    alum_single = []
                    if sh_n: alum_single.append({"البيان": "أعواد رفوف", "المقاس": f"{int(sh_w or 0)} عرض / {int(sh_d or 0)} عمق", "العدد": int(sh_n*4)})
                    if v_n: alum_single.append({"البيان": "أعواد فواصل", "المقاس": f"{int(v_h or 0)} ارتفاع / {int(v_d or 0)} عمق", "العدد": int(v_n*4)})
                    if dr_n: alum_single.append({"البيان": "إطار درج", "المقاس": f"{int(dr_w or 0)} عرض / {int(dr_d or 0)} عمق", "العدد": int(dr_n*4)})

                    # 3. جدول الفيبر
                    fiber_data = [
                        {"الجنب": "الظهر", "المقاس": f"{w_n} × {h_n}", "العدد": 1},
                        {"الجنب": "الجوانب", "المقاس": f"{d_n} × {h_n}", "العدد": 2},
                        {"الجنب": "الأرضية/السقف", "المقاس": f"{w_n} × {d_n}", "العدد": 2}
                    ]

                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}", "type": u_type,
                        "alum_g": pd.DataFrame(alum_grouped),
                        "alum_s": pd.DataFrame(alum_single) if alum_single else None,
                        "fiber": pd.DataFrame(fiber_data),
                        "m_total": (h_n*4 + w_n*4 + d_n*4)
                    })
                    st.rerun()

    # عرض الجداول
    st.write("---")
    for i, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><b>#{i+1} {item["name"]} - {item["dims"]}</b></div>', unsafe_allow_html=True)
        col_a, col_b, col_f = st.columns(3)
        with col_a:
            st.markdown("**🔗 ألومنيوم (متقارب)**")
            st.table(item['alum_g'])
        with col_b:
            st.markdown("**📍 ألومنيوم (مفرد/إضافي)**")
            if item['alum_s'] is not None: st.table(item['alum_s'])
            else: st.caption("لا توجد إضافات")
        with col_f:
            st.markdown("**✨ تفصيل الفيبر**")
            st.table(item['fiber'])

    # حساب الإجمالي
    if st.session_state.project_list:
        st.write("---")
        if st.button("📊 حساب خامات المشروع", use_container_width=True):
            total = sum([x['m_total'] for x in st.session_state.project_list]) / 600
            st.success(f"إجمالي الألومنيوم المطلوب: {round(total, 1)} عود (6 متر)")
            if st.button("🗑️ مسح الكل"):
                st.session_state.project_list = []
                st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
