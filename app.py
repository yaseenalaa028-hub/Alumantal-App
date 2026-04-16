import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (المهندس ياسين علاء)
# ==========================================
st.set_page_config(page_title="DOGGA SYSTEM", layout="wide")

# حل مشكلة الـ KeyError بتعريف المتغيرات الأساسية
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# تطبيق الألوان (الوضع الليلي / النهاري)
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; direction: rtl !important; text-align: right; }}
    .home-card {{ background: {card}; padding: 50px; border-radius: 25px; border: 4px solid {accent}; text-align: center; margin-top: 50px; }}
    .unit-card {{ background: {card}; border-right: 8px solid {accent}; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #444; }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# الهيدر (زرار الدرك مود ثابت)
t1, t2 = st.columns([10, 2])
with t1: st.markdown(f'<h3 style="color:{accent};">DOGGA SYSTEM | م/ ياسين علاء</h3>', unsafe_allow_html=True)
with t2:
    if st.button("🌙/☀️ الإضاءة"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. الواجهة الرئيسية (استقبال فقط)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="home-card">
            <h1 style="color:{accent}; font-size: 4em; margin:0;">DOGGA SYSTEM</h1>
            <p style="color:{accent}; font-size: 1.5em; margin:15px 0;">برمجة وتطوير المهندس: <b>ياسين علاء</b></p>
            <hr style="border:1px solid {accent}; width:30%; margin:auto;">
        </div>
    """, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🚀 الدخول لمنظومة التخصيم", use_container_width=True, type="primary"):
        st.session_state.page = 'calc'
        st.rerun()

# ==========================================
# 3. بند التخصيم (الورشة الكاملة)
# ==========================================
elif st.session_state.page == 'calc':
    st.markdown(f'<h2 style="color:{accent};">🛠️ ورشة التخصيم وحساب الخامات</h2>', unsafe_allow_html=True)
    if st.button("⬅️ خروج للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

    # استمارة الإدخال
    with st.form("main_workshop"):
        st.write("### 📏 إدخال البيانات")
        c1, c2 = st.columns(2)
        u_name = c1.text_input("اسم العميل / الوحدة", placeholder="...")
        u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        c3, c4, c5 = st.columns(3)
        w_in = c3.number_input("العرض", value=None, placeholder="0")
        h_in = c4.number_input("الارتفاع", value=None, placeholder="0")
        d_in = c5.number_input("العمق", value=None, placeholder="0")
        
        st.write("---")
        # الإضافات
        a1, a2, a3 = st.columns(3)
        with a1:
            sh_n = st.number_input("عدد الأرفف", value=0, step=1)
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0")
        with a2:
            v_n = st.number_input("عدد الفواصل", value=0, step=1)
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            v_d = st.number_input("عمق الفاصل", value=None, placeholder="0")
        with a3:
            dr_n = st.number_input("عدد الأدراج", value=0, step=1)
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0")

        if st.form_submit_button("✅ تنفيذ التخصيم وحفظ الوحدة", use_container_width=True):
            if w_in and h_in and d_in:
                # تخصيمات الورشة (13 و 5)
                h_d = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
                hn, wn, dn = int(h_in - h_d), int(w_in - 5), int(d_in - 5)

                # الألومنيوم (توزيع المفرد والمتقارب)
                if u_type == "وحدة سفلية":
                    alum = [["ارتفاع", hn, 2, 2], ["عرض", wn, 3, 1], ["عمق", dn, 2, 2]]
                else:
                    alum = [["ارتفاع", hn, 2, 2], ["عرض", wn, 2, 2], ["عمق", dn, 0, 4]]
                
                # إضافة الأرفف/الفواصل/الأدراج (العدد في 4 مفرد)
                if sh_n > 0: alum.append(["أعواد رف", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
                if v_n > 0: alum.append(["أعواد فاصل", int(v_h), v_n*4, 0])
                if dr_n > 0: alum.append(["برواز درج", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

                # الفيبر (الصافي)
                fiber = [["ظهرية", f"{wn}x{hn}", 1], ["أرضية", f"{wn}x{dn}", 1], ["أجناب", f"{hn}x{dn}", 2]]
                if sh_n > 0: fiber.append(["فيبر رف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

                st.session_state.project_list.append({
                    "name": u_name, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                    "alum_data": alum, "fiber_data": fiber,
                    "muf": sum([x[2] for x in alum]), "mut": sum([x[3] for x in alum])
                })
                st.rerun()

    # عرض النتائج (الجرد وشيتات التفصيل) جوه بند التخصيم
    if st.session_state.project_list:
        st.write("---")
        with st.expander("📊 عرض إجمالي خامات المشروع (الجرد)"):
            tmuf = sum([x['muf'] for x in st.session_state.project_list])
            tmut = sum([x['mut'] for x in st.session_state.project_list])
            tfib = sum([len(x['fiber_data']) for x in st.session_state.project_list])
            st.info(f"إجمالي المفرد: {tmuf} | إجمالي المتقارب: {tmut} | إجمالي الفيبر: {tfib}")

        st.write("### 📄 شيتات تفصيل الوحدات")
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f'<div class="unit-card">📌 وحدة #{i+1}: {item["name"]} ({item["dims"]})</div>', unsafe_allow_html=True)
                col_a, col_f = st.columns([3, 2])
                with col_a:
                    st.table(pd.DataFrame(item['alum_data'], columns=["البيان", "المقاس", "مفرد", "متقارب"]))
                with col_f:
                    st.table(pd.DataFrame(item['fiber_data'], columns=["القطعة", "المقاس", "العدد"]))

        if st.button("🗑️ مسح الكل"):
            st.session_state.project_list = []
            st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
