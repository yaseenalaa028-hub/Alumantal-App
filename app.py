import streamlit as st
import pandas as pd

# =========================================================
# 1. إعدادات المنظومة (إجبار العرض الكامل)
# =========================================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    page_icon="📐",
    layout="wide", # دي بتفرد الصفحة
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. نظام الـ Dark Mode وتخزين البيانات
# =========================================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# توزيع الألوان الذكي
if st.session_state.dark_mode:
    bg, card, txt, accent = "#0e1117", "#161b22", "#ffffff", "#f1c40f"
else:
    bg, card, txt, accent = "#ffffff", "#f8f9fa", "#1e1e1e", "#d4ac0d"

# =========================================================
# 3. الـ CSS الاحترافي (حل مشكلة "الكلام في النص")
# =========================================================
st.markdown(f"""
    <style>
    /* منع الـ Streamlit من تضييق المحتوى في المنتصف */
    .block-container {{
        max-width: 100% !important;
        padding: 1rem 3rem !important;
    }}
    
    /* ضبط اتجاه الصفحة بالكامل */
    .stApp {{
        background-color: {bg} !important;
        color: {txt} !important;
        direction: rtl !important;
    }}

    /* تصميم الكروت العريضة للنتائج */
    .unit-card {{
        background-color: {card};
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid {accent};
        margin-bottom: 25px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.4);
    }}

    /* تنظيف الواجهة من أي عناصر عشوائية */
    header, footer {{visibility: hidden !important;}}
    
    /* تحسين شكل الجداول لتملأ الشاشة */
    .stTable {{
        width: 100% !important;
        margin-top: 10px;
    }}
    
    /* تكبير نصوص الإدخال عشان تبقى واضحة في الورشة */
    label {{
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: {accent} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 4. القائمة الجانبية (Sidebar)
# =========================================================
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center; color:{accent};'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>تطوير م/ ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # تفعيل زرار الوضع الليلي (Dark Mode)
    mode_label = "☀️ الوضع النهاري" if st.session_state.dark_mode else "🌙 الوضع الليلي"
    if st.button(mode_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        st.session_state.page = 'welcome'
        st.rerun()

    # مخزن المشروع التراكمي
    if st.session_state.project_list:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("📦 جرد الخامات")
        total_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        st.metric("أعواد ألومنيوم (6م)", f"{round(total_m, 1)}")
        if st.button("🗑️ مسح المشروع", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# =========================================================
# 5. إدارة الصفحات والمحتوى
# =========================================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:100px;">
            <h1 style="color:{accent}; font-size:5em; font-weight:900;">DOGGA SYSTEM</h1>
            <h2 style="color:{txt};">منظومة التخصيم الفني للمطابخ</h2>
            <p style="font-size:1.5em; color:{accent};">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_btn, _ = st.columns([1, 1, 1])
    with col_btn:
        if st.button("🚀 ابدأ العمل الآن", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق (التخصيم) ---
elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent};'>📋 لوحة إضافة الوحدات</h2>", unsafe_allow_html=True)
    
    # استخدام Container لتنظيم الخانات بعيداً عن تداخل الموبايل
    with st.container():
        # 3 أعمدة عريضة جداً
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            st.markdown("### 📏 المقاسات")
            u_name = st.text_input("اسم الوحدة / الكود")
            u_type = st.selectbox("نوع الوحدة", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
            w = st.number_input("العرض الكلي (W)", value=None, placeholder="0.0")
            h = st.number_input("الارتفاع الكلي (H)", value=None, placeholder="0.0")
            d = st.number_input("العمق الكلي (D)", value=None, placeholder="0.0")
            
        with c2:
            st.markdown("### 🧱 الرفوف والفواصل")
            s_w = st.number_input("عرض الرف", value=None)
            s_d = st.number_input("عمق الرف", value=None)
            s_n = st.number_input("عدد الرفوف", value=None)
            st.write("---")
            v_h = st.number_input("ارتفاع الفاصل", value=None)
            v_n = st.number_input("عدد الفواصل", value=None)

        with c3:
            st.markdown("### 🗄️ الأدراج")
            dr_w = st.number_input("عرض الدرج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=None)
            st.write("---")
            notes = st.text_area("ملاحظات إضافية")
            
            if st.button("✅ حفظ وحساب التخصيم", use_container_width=True):
                if w and h:
                    # معادلات التخصيم
                    deduction = 13 if "13" in u_type else 5
                    h_net = int(h - deduction)
                    w_net, d_net = int(w - 5), int((d or 0) - 5)
                    
                    # جداول الألومنيوم
                    alum = [
                        {"البيان": "قوايم الارتفاع", "المقاس": h_net, "العدد": "4"},
                        {"البيان": "عوارض العرض", "المقاس": w_net, "العدد": "4"},
                        {"البيان": "عوارض العمق", "المقاس": d_net, "العدد": "4"}
                    ]
                    if v_n: alum.append({"البيان": "فواصل", "المقاس": int(v_h), "العدد": int(v_n*4)})
                    
                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}", "type": u_type,
                        "alum_df": pd.DataFrame(alum),
                        "m_m": (h_net*4 + w_net*4 + d_net*4),
                        "f_a": (w_net*h_net) + (h_net*d_net*2)
                    })
                    st.rerun()

    # عرض كشوفات التقطيع
    st.write("---")
    for i, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h2>#{i+1} {item["name"]} - {item["dims"]} ({item["type"]})</h2></div>', unsafe_allow_html=True)
        res_c1, res_c2 = st.columns([3, 1])
        with res_c1:
            st.table(item['alum_df'])
        with res_c2:
            st.metric("مساحة الفيبر", f"{item['f_a']} سم²")

# تذييل الصفحة
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent}; font-weight:bold; font-size:1.3em;'>DOGGA SYSTEM 2026 | تطوير م/ ياسين علاء</p>", unsafe_allow_html=True)
