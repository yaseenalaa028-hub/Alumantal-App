import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة (المهندس ياسين علاء)
# ==========================================
st.set_page_config(page_title="DOGGA SYSTEM", layout="wide")

if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# تطبيق الألوان بناءً على الوضع
if st.session_state.dark_mode:
    bg, txt, accent, card = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; direction: rtl !important; text-align: right; }}
    .home-card {{ background: {card}; padding: 50px; border-radius: 25px; border: 4px solid {accent}; text-align: center; margin-top: 50px; }}
    .unit-card {{ background: {card}; border-right: 8px solid {accent}; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #444; }}
    .inv-box {{ background: {card}; border: 2px solid {accent}; padding: 15px; border-radius: 12px; margin-bottom: 10px; }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# الهيدر
h1, h2 = st.columns([10, 2])
with h1: st.markdown(f'<h3 style="color:{accent};">DOGGA SYSTEM | م/ ياسين علاء</h3>', unsafe_allow_html=True)
with h2:
    if st.button("🌙/☀️ الإضاءة"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. الواجهة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="home-card">
            <h1 style="color:{accent}; font-size: 4em; margin:0;">DOGGA SYSTEM</h1>
            <p style="color:{accent}; font-size: 1.8em; margin:15px 0;">الورشة الذكية للمهندس: <b>ياسين علاء</b></p>
            <hr style="border:1px solid {accent}; width:30%; margin:auto;">
        </div>
    """, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🚀 الدخول لمنظومة التخصيم والجرد", use_container_width=True, type="primary"):
        st.session_state.page = 'calc'; st.rerun()

# ==========================================
# 3. بند التخصيم والجرد (الشغل كله هنا)
# ==========================================
elif st.session_state.page == 'calc':
    st.markdown(f'<h2 style="color:{accent};">🛠️ ورشة التخصيم وحساب الأعواد</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = 'home'; st.rerun()

    with st.form("pro_workshop"):
        st.write("### 📝 بيانات الوحدة الجديدة")
        c1, c2 = st.columns(2)
        u_name = c1.text_input("اسم العميل / رقم الوحدة", placeholder="...")
        u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        c3, c4, c5 = st.columns(3)
        w_in = c3.number_input("العرض الكلي (W)", value=None, placeholder="0")
        h_in = c4.number_input("الارتفاع الكلي (H)", value=None, placeholder="0")
        d_in = c5.number_input("العمق الكلي (D)", value=None, placeholder="0")
        
        st.write("---")
        st.write("### ➕ الإضافات (أرفف - فواصل - أدراج)")
        a1, a2, a3 = st.columns(3)
        with a1:
            sh_n = st.number_input("عدد الأرفف", value=0)
            sh_w = st.number_input("عرض الرف", value=None)
            sh_d = st.number_input("عمق الرف", value=None)
        with a2:
            v_n = st.number_input("عدد الفواصل", value=0)
            v_h = st.number_input("ارتفاع الفاصل", value=None)
        with a3:
            dr_n = st.number_input("عدد الأدراج", value=0)
            dr_w = st.number_input("عرض برواز الدرج", value=None)
            dr_d = st.number_input("عمق الدرج", value=None)

        if st.form_submit_button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
            if w_in and h_in and d_in:
                # منطق التخصيم الثابت
                h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
                hn, wn, dn = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

                # الألومنيوم (البيان، المقاس، مفرد، متقارب)
                if u_type == "وحدة سفلية":
                    alum = [["قوايم ارتفاع", hn, 2, 2], ["عوارض عرض", wn, 3, 1], ["عوارض عمق", dn, 2, 2]]
                else:
                    alum = [["قوايم ارتفاع", hn, 2, 2], ["عوارض عرض", wn, 2, 2], ["عوارض عمق", dn, 0, 4]]
                
                # حساب إضافات الألومنيوم (العدد في 4 مفرد)
                if sh_n > 0: alum.append([f"أعواد أرفف ({sh_n})", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
                if v_n > 0: alum.append([f"أعواد فواصل ({v_n})", int(v_h), v_n*4, 0])
                if dr_n > 0: alum.append([f"براويز درج ({dr_n})", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

                # حساب الفيبر الصافي
                fiber = [["ظهرية", f"{wn}x{hn}", 1], ["أرضية", f"{wn}x{dn}", 1], ["أجناب", f"{hn}x{dn}", 2]]
                if sh_n > 0: fiber.append(["فيبر أرفف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

                st.session_state.project_list.append({
                    "name": u_name, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                    "alum": alum, "fiber": fiber
                })
                st.rerun()

    # قسم الجرد والتقارير (يظهر فقط عند وجود بيانات)
    if st.session_state.project_list:
        st.write("---")
        with st.expander("📊 جرد الخامات الكلي وحساب الأعواد (مفرد ومتقارب)", expanded=True):
            muf_data, mut_data = [], []
            for item in st.session_state.project_list:
                for row in item['alum']:
                    # نجمع المقاسات العددية فقط للجرد الطولي
                    if isinstance(row[1], int):
                        if row[2] > 0: muf_data.append({"المقاس": row[1], "العدد": row[2]})
                        if row[3] > 0: mut_data.append({"المقاس": row[1], "العدد": row[3]})
            
            # تجميع المقاسات المتشابهة
            df_muf = pd.DataFrame(muf_data).groupby("المقاس").sum().reset_index() if muf_data else pd.DataFrame()
            df_mut = pd.DataFrame(mut_data).groupby("المقاس").sum().reset_index() if mut_data else pd.DataFrame()

            inv_c1, inv_c2 = st.columns(2)
            with inv_c1:
                st.markdown(f'<h4 style="color:{accent};">📋 جرد المفرد</h4>', unsafe_allow_html=True)
                if not df_muf.empty:
                    st.table(df_muf)
                    total_cm = (df_muf['المقاس'] * df_muf['العدد']).sum()
                    st.success(f"إجمالي الطول: {total_cm/100:.2f} متر ⮕ {math.ceil(total_cm/600)} عود")
            with inv_c2:
                st.markdown(f'<h4 style="color:{accent};">📋 جرد المتقارب</h4>', unsafe_allow_html=True)
                if not df_mut.empty:
                    st.table(df_mut)
                    total_cm_t = (df_mut['المقاس'] * df_mut['العدد']).sum()
                    st.success(f"إجمالي الطول: {total_cm_t/100:.2f} متر ⮕ {math.ceil(total_cm_t/600)} عود")

        st.write("### 📄 شيتات تفصيل الوحدات")
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f'<div class="unit-card">📌 وحدة #{i+1}: {item["name"]} | {item["dims"]}</div>', unsafe_allow_html=True)
                ca, cf = st.columns([3, 2])
                with ca: st.table(pd.DataFrame(item['alum'], columns=["البيان", "المقاس", "مفرد", "متقارب"]))
                with cf: st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))

        if st.button("🗑️ مسح المشروع"): st.session_state.project_list = []; st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
