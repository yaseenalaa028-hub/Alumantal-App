import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (العرض الكامل 100%)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إدارة الحالة (تأمين البيانات ومنع KeyError)
# ==========================================
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# تعريف الألوان بناءً على الوضع
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

# ==========================================
# 3. CSS التصميم والاحترافية
# ==========================================
st.markdown(f"""
    <style>
    .block-container {{ max-width: 100% !important; padding: 1rem 2rem !important; }}
    .stApp {{ background-color: {bg} !important; color: {txt} !important; direction: rtl !important; }}
    
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

# زرار الـ Dark Mode في أعلى الزاوية
_, t_col = st.columns([12, 1])
with t_col:
    mode_icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(mode_icon, key="mode_switch"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 4. محتوى الصفحات
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

    # نموذج الإدخال الكامل (بدون اختصار)
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown('<p class="section-head">📏 المقاسات الأساسية</p>', unsafe_allow_html=True)
            u_name = st.text_input("اسم الوحدة (كود)")
            u_type = st.selectbox("نوع التخصيم", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
            w = st.number_input("العرض الكلي (W)", value=0.0)
            h = st.number_input("الارتفاع الكلي (H)", value=0.0)
            d = st.number_input("العمق الكلي (D)", value=0.0)
            
        with c2:
            st.markdown('<p class="section-head">🧱 الرفوف</p>', unsafe_allow_html=True)
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0, step=1)
            
        with c3:
            st.markdown('<p class="section-head">↕️ الفواصل</p>', unsafe_allow_html=True)
            v_h = st.number_input("ارتفاع الفاصل", value=0.0)
            v_d = st.number_input("عمق الفاصل", value=0.0)
            v_n = st.number_input("عدد الفواصل", value=0, step=1)
            
        with c4:
            st.markdown('<p class="section-head">🗄️ الأدراج</p>', unsafe_allow_html=True)
            dr_w = st.number_input("عرض برواز الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0, step=1)
            
            st.write("")
            if st.button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
                if w > 0 and h > 0:
                    # معادلات التخصيم الأساسية
                    ded = 13 if "13" in u_type else 5
                    h_net, w_net, d_net = int(h - ded), int(w - 5), int(d - 5)
                    
                    # 1. بناء جدول الألومنيوم المتقارب
                    g_list = [
                        {"البيان": "قوايم رئيسية", "المقاس": h_net, "العدد": 4},
                        {"البيان": "عوارض عرض", "المقاس": w_net, "العدد": 4},
                        {"البيان": "عوارض عمق", "المقاس": d_net, "العدد": 4}
                    ]
                    
                    # 2. بناء جدول الألومنيوم المفرد (الإضافات)
                    s_list = []
                    if sh_n > 0:
                        s_list.append({"البيان": "أعواد عرض الرف", "المقاس": int(sh_w), "العدد": sh_n*2})
                        s_list.append({"البيان": "أعواد عمق الرف", "المقاس": int(sh_d), "العدد": sh_n*2})
                    if v_n > 0:
                        s_list.append({"البيان": "أعواد ارتفاع الفاصل", "المقاس": int(v_h), "العدد": v_n*2})
                        s_list.append({"البيان": "أعواد عمق الفاصل", "المقاس": int(v_d), "العدد": v_n*2})
                    if dr_n > 0:
                        s_list.append({"البيان": "أعواد عرض الدرج", "المقاس": int(dr_w), "العدد": dr_n*2})
                        s_list.append({"البيان": "أعواد عمق الدرج", "المقاس": int(dr_d), "العدد": dr_n*2})

                    # 3. بناء جدول الفيبر التفصيلي
                    f_list = [
                        {"القطعة": "الظهر الرئيسي", "المقاس": f"{w_net} × {h_net}", "العدد": 1},
                        {"القطعة": "جوانب الوحدة", "المقاس": f"{d_net} × {h_net}", "العدد": 2},
                        {"القطعة": "أرضية وسقف", "المقاس": f"{w_net} × {d_net}", "العدد": 2}
                    ]

                    # حفظ في القائمة مع التأكد من وجود المفاتيح
                    st.session_state.project_list.append({
                        "id": f"{w}x{h}x{d} - {u_name}",
                        "alum_g": pd.DataFrame(g_list),
                        "alum_s": pd.DataFrame(s_list) if s_list else None,
                        "fiber": pd.DataFrame(f_list),
                        "m_total": (h_net*4 + w_net*4 + d_net*4) + (sum([x['المقاس']*x['العدد'] for x in s_list]) if s_list else 0)
                    })
                    st.rerun()

    # عرض النتائج (جداول كاملة)
    st.write("---")
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><b>📌 وحدة رقم {idx+1}: {item["id"]}</b></div>', unsafe_allow_html=True)
        
        col_g, col_s, col_f = st.columns(3)
        with col_g:
            st.markdown("**🔗 ألومنيوم (متقارب)**")
            st.table(item['alum_g'])
            
        with col_s:
            st.markdown("**📍 ألومنيوم (مفرد/إضافي)**")
            if item['alum_s'] is not None:
                st.table(item['alum_s'])
            else:
                st.info("لا توجد إضافات (رفوف/أدراج)")
                
        with col_f:
            st.markdown("**✨ تفصيل الفيبر**")
            st.table(item['fiber'])

    # الجرد النهائي للمشروع
    if st.session_state.project_list:
        st.write("---")
        if st.button("📊 حساب خامات المشروع بالكامل", use_container_width=True):
            total_cm = sum([x['m_total'] for x in st.session_state.project_list])
            total_rods = total_cm / 600
            st.markdown(f"""
                <div style="background-color:{accent}; color:#000; padding:20px; border-radius:10px; text-align:center;">
                    <h3>إجمالي جرد الألومنيوم</h3>
                    <p style="font-size:1.8em; margin:0;"><b>{round(total_rods, 1)} عود (6 متر)</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🗑️ مسح جميع البيانات والبدء من جديد"):
                st.session_state.project_list = []
                st.rerun()

# التذييل الاحترافي
st.markdown(f"<p style='text-align:center; color:{accent}; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
