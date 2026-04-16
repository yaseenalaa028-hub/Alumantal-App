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
    /* تصميم اللوجو الملموم */
    .brand-box {{
        text-align: center;
        padding: 20px;
        background: {card};
        border-radius: 15px;
        border: 2px solid {accent};
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
    }}
    .unit-card {{
        background-color: {card};
        padding: 15px;
        border-radius: 10px;
        border-right: 10px solid {accent};
        margin-bottom: 15px;
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
    /* تحسين عرض الجداول */
    .stTable {{
        width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. زرار الـ Dark Mode في أعلى الزاوية
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
        <div style="text-align:center; padding-top:100px;">
            <div class="brand-box">
                <h1 style="color:{accent}; font-size:4.5em; font-weight:900; margin:0; letter-spacing: 2px;">DOGGA SYSTEM</h1>
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

# --- لوحة العمل الداخلية (app) ---
elif st.session_state.page == 'app':
    # زرار الرجوع والاسم الملموم فوق
    n_col1, n_col2 = st.columns([1, 8])
    with n_col1:
        if st.button("⬅️ رجوع"):
            st.session_state.page = 'welcome'
            st.rerun()
    with n_col2:
        st.markdown(f"<h2 style='color:{accent}; margin:0;'>📋 لوحة التخصيم الفني الشاملة</h2>", unsafe_allow_html=True)

    st.write("---")

    # نموذج الإدخال التفصيلي (كل بند لوحده)
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown('<p class="section-head">📏 المقاسات الأساسية</p>', unsafe_allow_html=True)
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الخصم", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
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
                    # معادلات التخصيم الثابتة (م/ ياسين علاء)
                    ded = 13 if "13" in u_type else 5
                    h_net = int(h - ded)
                    w_net, d_net = int(w - 5), int((d or 0) - 5)
                    
                    # 1. جدول الألومنيوم التفصيلي
                    alum_data = [
                        {"البيان": "قوايم الارتفاع الرئيسية", "المقاس": h_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العرض", "المقاس": w_net, "العدد": "4 ق"},
                        {"البيان": "عوارض العمق", "المقاس": d_net, "العدد": "4 ق"}
                    ]
                    
                    # إضافة تفاصيل الرفوف للجدول
                    if sh_n:
                        alum_data.append({"البيان": "أعواد عرض الرفوف", "المقاس": int(sh_w or 0), "العدد": int(sh_n*2)})
                        alum_data.append({"البيان": "أعواد عمق الرفوف", "المقاس": int(sh_d or 0), "العدد": int(sh_n*2)})
                    
                    # إضافة تفاصيل الفواصل للجدول
                    if v_n:
                        alum_data.append({"البيان": "أعواد ارتفاع الفواصل", "المقاس": int(v_h or 0), "العدد": int(v_n*2)})
                        alum_data.append({"البيان": "أعواد عمق الفواصل", "المقاس": int(v_d or 0), "العدد": int(v_n*2)})
                    
                    # إضافة تفاصيل الأدراج للجدول
                    if dr_n:
                        alum_data.append({"البيان": "أعواد عرض برواز الدرج", "المقاس": int(dr_w or 0), "العدد": int(dr_n*2)})
                        alum_data.append({"البيان": "أعواد عمق الدرج", "المقاس": int(dr_d or 0), "العدد": int(dr_n*2)})

                    # حساب إجمالي الأمتار الطولية للوحدة (للجرد)
                    total_unit_m = (h_net*4 + w_net*4 + d_net*4)
                    if sh_n: total_unit_m += (int(sh_w or 0)*2 + int(sh_d or 0)*2) * sh_n
                    if v_n: total_unit_m += (int(v_h or 0)*2 + int(v_d or 0)*2) * v_n
                    if dr_n: total_unit_m += (int(dr_w or 0)*2 + int(dr_d or 0)*2) * dr_n

                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}", "type": u_type,
                        "alum_df": pd.DataFrame(alum_data),
                        "m_m": total_unit_m,
                        "f_a": (w_net * h_net) + (h_net * d_net * 2) # مساحة تقريبية للفيبر
                    })
                    st.rerun()

    # عرض الجداول التفصيلية (بعد التخصيم)
    st.write("---")
    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f"""
                <div class="unit-card">
                    <h3 style="color:{accent}; margin:0;">#{i+1} {item['name']} | مقاس {item['dims']} | ({item['type']})</h3>
                </div>
            """, unsafe_allow_html=True)
            
            res_c1, res_c2 = st.columns([4, 1])
            with res_c1:
                st.table(item['alum_df']) # الجداول كاملة بدون اختصار
            with res_c2:
                st.metric("فيبر الوحدة (سم²)", item['f_a'])

    # زرار حساب الخامات النهائي (في نهاية الجداول)
    if st.session_state.project_list:
        st.write("---")
        if st.button("📊 حساب إجمالي خامات المشروع بالكامل", use_container_width=True):
            total_m_linear = sum([x['m_m'] for x in st.session_state.project_list]) / 600
            st.markdown(f"""
                <div style="background-color:{accent}; color:#000; padding:30px; border-radius:15px; text-align:center;">
                    <h2>تقرير جرد المشروع النهائي</h2>
                    <hr style="border:1px solid #000">
                    <p style="font-size:1.8em;">إجمالي أعواد الألومنيوم (6 متر): <b>{round(total_m_linear, 1)} عود</b></p>
                    <p style="font-size:1.2em;">* هذا الجرد يشمل القوايم والعوارض والرفوف والفواصل والأدراج المضافة.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️ تفريغ بيانات المشروع"):
                st.session_state.project_list = []
                st.rerun()

# التذييل الثابت
st.markdown(f"<p style='text-align:center; color:{accent}; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
