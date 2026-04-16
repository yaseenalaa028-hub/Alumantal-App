import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (Eng. Yassin Alaa)
# ==========================================
st.set_page_config(page_title="DOGGA SYSTEM", layout="wide")

if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# تطبيق الألوان (الدرك مود)
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; direction: rtl !important; text-align: right; }}
    .home-card {{ background: {card}; padding: 60px; border-radius: 25px; border: 4px solid {accent}; text-align: center; margin-top: 50px; }}
    .workshop-box {{ background: {card}; border: 2px solid {accent}; padding: 20px; border-radius: 15px; margin-top: 20px; }}
    .unit-card {{ background: {card}; border-right: 8px solid {accent}; padding: 15px; border-radius: 10px; margin-bottom: 20px; }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# الهيدر الثابت (زرار الدرك مود)
top_l, top_r = st.columns([10, 2])
with top_l:
    st.markdown(f'<h3 style="color:{accent}; margin:0;">DOGGA SYSTEM | م/ ياسين علاء</h3>', unsafe_allow_html=True)
with top_r:
    if st.button("🌙/☀️ وضع الإضاءة", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. الواجهة الرئيسية (استقبال فقط)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="home-card">
            <h1 style="color:{accent}; font-size: 4em; margin:0;">DOGGA SYSTEM</h1>
            <h2 style="color:{txt}; margin:0;">نظام التخصيم الفني الاحترافي</h2>
            <p style="color:{accent}; font-size: 1.5em; margin:15px 0;">برمجة وتطوير المهندس: <b>ياسين علاء</b></p>
            <hr style="border:1px solid {accent}; width:30%; margin:auto;">
            <br>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🚀 الدخول لمنظومة التخصيم والورشة", use_container_width=True, type="primary"):
        st.session_state.page = 'calc'
        st.rerun()

# ==========================================
# 3. بند التخصيم (كل الشغل هنا)
# ==========================================
elif st.session_state.page == 'calc':
    st.markdown(f'<h2 style="color:{accent};">🛠️ ورشة التخصيم وحساب الخامات</h2>', unsafe_allow_html=True)
    if st.button("⬅️ خروج للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

    # أولاً: إدخال البيانات
    with st.form("input_form"):
        st.write("### 📏 إدخال مقاسات الوحدة")
        r1c1, r1c2 = st.columns(2)
        with r1c1: u_client = st.text_input("اسم العميل / الوحدة", placeholder="اكتب هنا...")
        with r1c2: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1: w_in = st.number_input("العرض (W)", value=None, placeholder="0")
        with r2c2: h_in = st.number_input("الارتفاع (H)", value=None, placeholder="0")
        with r2c3: d_in = st.number_input("العمق (D)", value=None, placeholder="0")
        
        st.write("---")
        # الإضافات
        ax, ay, az = st.columns(3)
        with ax:
            sh_n = st.number_input("عدد الأرفف", value=0, step=1)
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0")
        with ay:
            v_n = st.number_input("عدد الفواصل", value=0, step=1)
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            v_d = st.number_input("عمق الفاصل", value=None, placeholder="0")
        with az:
            dr_n = st.number_input("عدد الأدراج", value=0, step=1)
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0")

        if st.form_submit_button("✅ تنفيذ التخصيم وحفظ الوحدة", use_container_width=True):
            if w_in and h_in:
                # معادلات المهندس ياسين
                h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
                h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

                if u_type == "وحدة سفلية":
                    alum = [["ارتفاع", h_net, 2, 2], ["عرض", w_net, 3, 1], ["عمق", d_net, 2, 2]]
                else:
                    alum = [["ارتفاع", h_net, 2, 2], ["عرض", w_net, 2, 2], ["عمق", d_net, 0, 4]]
                
                if sh_n > 0: alum.append(["أرفف", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
                if v_n > 0: alum.append(["فواصل", int(v_h), v_n*4, 0])
                if dr_n > 0: alum.append(["أدراج", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

                fiber = [["ظهرية", f"{w_net}x{h_net}", 1], ["أرضية", f"{w_net}x{d_net}", 1], ["أجناب", f"{h_net}x{d_net}", 2]]
                if sh_n > 0: fiber.append(["رفوف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

                st.session_state.project_list.append({
                    "client": u_client, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                    "alum": alum, "fiber": fiber,
                    "muf": sum([x[2] for x in alum]), "mut": sum([x[3] for x in alum])
                })
                st.rerun()

    # ثانياً: بند جرد الخامات (داخل التخصيم)
    if st.session_state.project_list:
        st.write("---")
        with st.expander("📊 عرض إجمالي الخامات المطلوبة (الجرد)"):
            t_muf = sum([x['muf'] for x in st.session_state.project_list])
            t_mut = sum([x['mut'] for x in st.session_state.project_list])
            t_fib = sum([len(x['fiber']) for x in st.session_state.project_list])
            
            st.markdown(f"""
                <div style="background:{accent}; color:black; padding:15px; border-radius:10px;">
                    <b>إجمالي المفرد: {t_muf} قطعة | إجمالي المتقارب: {t_mut} قطعة | إجمالي الفيبر: {t_fib} قطعة</b>
                </div>
            """, unsafe_allow_html=True)

        # ثالثاً: شيتات التفصيل (داخل التخصيم)
        st.write("### 📄 شيتات تقطيع الوحدات")
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f'<div class="unit-card">📌 وحدة #{i+1}: {item["client"]}</div>', unsafe_allow_html=True)
                ca, cf = st.columns([3, 2])
                with ca: st.table(pd.DataFrame(item['alum'], columns=["البيان", "المقاس", "مفرد", "متقارب"]))
                with cf: st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))

        if st.button("🗑️ مسح الكل والبدء من جديد"):
            st.session_state.project_list = []
            st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير م/ ياسين علاء</p>", unsafe_allow_html=True)
