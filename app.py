import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتنسيق الواجهة
st.set_page_config(page_title="نظام تخصيم الألومنيوم PRO", layout="wide")

# تنسيق CSS مخصص للواجهة واللغة العربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .main-header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .unit-card { background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .section-title { color: #2c3e50; border-bottom: 2px solid #e67e22; padding-bottom: 5px; margin-bottom: 10px; font-weight: bold; }
    .alum-box { color: #d35400; font-weight: bold; }
    .fiber-box { color: #27ae60; font-weight: bold; }
    .extra-box { color: #2980b9; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="main-header"><h1>🔐 تسجيل دخول نظام الورشة</h1></div>', unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submit = st.form_submit_button("دخول للنظام")
        if submit:
            if user == "admin" and password == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ بيانات الدخول غير صحيحة")
    st.stop()

# 3. إدارة البيانات (Session State)
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

st.markdown('<div class="main-header"><h1>🏗️ لوحة تحكم تخصيم الألومنيوم والفيبر</h1></div>', unsafe_allow_html=True)

# --- القائمة الجانبية لإدخال البيانات ---
with st.sidebar:
    st.header("⚙️ إضافة وحدة جديدة")
    u_title = st.text_input("اسم الوحدة (مثال: علوية مطبخ)")
    u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    col_dim1, col_dim2, col_dim3 = st.columns(3)
    u_w = col_dim1.number_input("العرض", min_value=0.0)
    u_h = col_dim2.number_input("الارتفاع", min_value=0.0)
    u_d = col_dim3.number_input("العمق", min_value=0.0)
    
    st.divider()
    st.subheader("🧱 الرفوف")
    s_n = st.number_input("عدد الرفوف", min_value=0, step=1)
    s_w = st.number_input("عرض الرف", min_value=0.0)
    s_d = st.number_input("عمق الرف", min_value=0.0)
    
    st.subheader("🗄️ الأدراج")
    dr_n = st.number_input("عدد الأدراج", min_value=0, step=1)
    dr_w = st.number_input("عرض الدرج", min_value=0.0)
    dr_d = st.number_input("عمق الدرج", min_value=0.0)

    if st.button("💾 حفظ الوحدة للمشروع"):
        if u_w > 0 and u_h > 0:
            st.session_state.project_storage.append({
                'title': u_title or f"وحدة {len(st.session_state.project_storage)+1}",
                'type': u_type, 'w': u_w, 'h': u_h, 'd': u_d,
                'sh_n': s_n, 'sh_w': s_w, 'sh_d': s_d,
                'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d
            })
            st.success("تم الحفظ بنجاح")
        else:
            st.error("يرجى إدخال المقاسات الأساسية")

# --- عرض النتائج والجرد ---
if st.session_state.project_storage:
    tab1, tab2 = st.tabs(["📋 قائمة الوحدات", "📊 بيان التقطيع والجرد"])
    
    with tab1:
        df = pd.DataFrame(st.session_state.project_storage)
        st.table(df[['title', 'type', 'w', 'h', 'd']])
        if st.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_storage = []
            st.rerun()

    with tab2:
        m_total, t_total, f_total = 0, 0, 0
        
        for u in st.session_state.project_storage:
            # تخصيمات الهيكل
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b, d_b = u['w'] - 5, u['d'] - 5
            
            # حساب الخامات الإجمالية
            if u['type'] == "سفلية":
                m_curr = (h_b*2)+(w_b*3)+(d_b*2)
                t_curr = (h_b*2)+(w_b*1)+(d_b*2)
                f_unit = (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_curr = (h_b*2)+(w_b*2)
                t_curr = (h_b*2)+(w_b*2)+(d_b*4)
                f_unit = (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
            
            # إضافة الرفوف والأدراج للحسابات
            m_curr += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            m_curr += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']
            f_unit += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n']
            
            m_total += m_curr
            t_total += t_curr
            f_total += f_unit

            # عرض الوحدة في قسم منفصل
            with st.container():
                st.markdown(f'<div class="unit-card">', unsafe_allow_html=True)
                st.subheader(f"📍 {u['title']} ({u['type']})")
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown('<p class="section-title">📏 بند الألومنيوم</p>', unsafe_allow_html=True)
                    st.write(f"• ارتفاع: {h_b} سم (4 قطع)")
                    st.write(f"• عرض: {w_b} سم (4 قطع)")
                    st.write(f"• عمق: {d_b} سم (4 قطع)")
                
                with c2:
                    st.markdown('<p class="section-title">🪵 بند الفيبر</p>', unsafe_allow_html=True)
                    st.write(f"• ضهرية: {w_b} × {h_b}")
                    st.write(f"• أرضية/سقف: {w_b} × {d_b}")
                    st.write(f"• أجناب: {h_b} × {d_b}")

                with c3:
                    st.markdown('<p class="section-title">⚙️ بند الإضافات</p>', unsafe_allow_html=True)
                    if u['sh_n'] > 0:
                        st.write(f"• {u['sh_n']} رف: {u['sh_w']} × {u['sh_d']}")
                    if u['dr_n'] > 0:
                        st.write(f"• {u['dr_n']} درج: عرض {u['dr_w']-2.5} × عمق {u['dr_d']}")
                    if u['sh_n'] == 0 and u['dr_n'] == 0:
                        st.write("لا توجد إضافات")
                
                st.markdown('</div>', unsafe_allow_html=True)

        # الجرد النهائي للمشروع
        st.divider()
        st.markdown('<div class="main-header"><h2>💰 إجمالي خامات المشروع بالكامل</h2></div>', unsafe_allow_html=True)
        res1, res2, res3 = st.columns(3)
        res1.metric("ألومنيوم مفرد (عود)", f"{m_total/600:.2f}")
        res2.metric("ألومنيوم متقارب (عود)", f"{t_total/600:.2f}")
        res3.metric("فيبر لوح (2.8*1.3)", f"{f_total/36400:.2f}")

else:
    st.info("👋 مرحباً بك! قم بإضافة الوحدات من القائمة الجانبية لعرض بيان التقطيع.")
