import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة
# ==========================================
st.set_page_config(page_title="DOGGA PRO SYSTEM", layout="wide")

if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

accent = "#f1c40f" if st.session_state.dark_mode else "#d4ac0d"
bg_card = "#1c1f26" if st.session_state.dark_mode else "#f8f9fa"

# ==========================================
# 2. الواجهة الرئيسية (Landing Page)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <style>
        .home-center {{ text-align: center; margin-top: 10%; padding: 50px; border-radius: 30px; border: 5px solid {accent}; background: {bg_card}; }}
        .title-main {{ font-size: 5em; color: {accent}; font-weight: bold; margin-bottom: 10px; }}
        </style>
        <div class="home-center">
            <h1 class="title-main">DOGGA SYSTEM PRO</h1>
            <h2 style="color:white;">ورشة المهندس ياسين علاء الذكية</h2>
            <p style="font-size: 1.5em; opacity: 0.8;">منظومة تخصيم وجرد الألمنيوم الاحترافية - إصدار 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم الآن (دخول للورشة)", use_container_width=True, type="primary"):
        st.session_state.page = 'calc'
        st.rerun()

# ==========================================
# 3. صفحة العمل (Workshop)
# ==========================================
else:
    # هيدر صفحة العمل
    h1, h2, h3 = st.columns([7, 2, 1])
    with h1: st.markdown(f"<h1 style='color:{accent};'>🛠️ منطقة العمل | م/ ياسين علاء</h1>", unsafe_allow_html=True)
    with h2:
        if st.button("🏠 العودة للرئيسية", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    with h3:
        if st.button("🌙/☀️", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.divider()

    # --- نموذج الإدخال (مساحة واسعة) ---
    with st.expander("📝 إضافة وحدة جديدة للمشروع", expanded=True):
        with st.form("main_workshop_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            client = c1.text_input("اسم العميل / رقم الوحدة")
            u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])
            note = c3.text_input("ملاحظات إضافية")

            st.markdown("#### 📐 الأبعاد الأساسية (سم)")
            d1, d2, d3 = st.columns(3)
            W = d1.number_input("العرض الكلي", value=None, placeholder="0")
            H = d2.number_input("الارتفاع الكلي", value=None, placeholder="0")
            D = d3.number_input("العمق الكلي", value=None, placeholder="0")

            st.markdown("#### ➕ الإضافات (أرفف - فواصل - أدراج)")
            # صف الأرفف
            a1, a2, a3 = st.columns(3)
            sh_n = a1.number_input("عدد الأرفف", min_value=0, value=0)
            sh_w = a2.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = a3.number_input("عمق الرف", value=None, placeholder="0")
            
            # صف الفواصل والأدراج
            v1, v2, dr1, dr2, dr3 = st.columns(5)
            v_n = v1.number_input("عدد الفواصل", min_value=0, value=0)
            v_h = v2.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            
            dr_n = dr1.number_input("عدد الأدراج", min_value=0, value=0)
            dr_w = dr2.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = dr3.number_input("عمق الدرج", value=None, placeholder="0")

            if st.form_submit_button("✅ حفظ وحساب التخصيم فوراً", use_container_width=True):
                if W and H and D:
                    # منطق التخصيم
                    h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
                    hn, wn, dn = H - h_ded, W - 5, D - 5
                    
                    # 1. قائمة الألمنيوم
                    alum = [
                        ["قوايم رئيسية", int(hn), 2, "مفرد"],
                        ["عوارض عرض", int(wn), 2 if u_type == "وحدة علوية" else 3, "مفرد"],
                        ["عوارض عمق", int(dn), 2, "مفرد"],
                        ["وزرة / فرشة", int(wn), 1 if u_type == "وحدة سفلية" else 0, "متقارب"]
                    ]
                    if sh_n > 0: alum.append([f"أعواد أرفف ({sh_n})", int(sh_w if sh_w else 0), int(sh_n*4), "مفرد"])
                    if v_n > 0: alum.append([f"أعواد فواصل ({v_n})", int(v_h if v_h else 0), int(v_n*4), "مفرد"])
                    if dr_n > 0: alum.append([f"براويز درج ({dr_n})", int((dr_w if dr_w else 0) - 2.5), int(dr_n*4), "مفرد"])

                    # 2. قائمة الفيبر
                    fiber = [
                        ["ظهرية صافي", f"{int(wn)}x{int(hn)}", 1],
                        ["أرضية صافي", f"{int(wn)}x{int(dn)}", 1],
                        ["أجناب صافي", f"{int(hn)}x{int(dn)}", 2]
                    ]
                    if sh_n > 0: fiber.append(["فيبر أرفف", f"{int((sh_w if sh_w else 0)-0.5)}x{int((sh_d if sh_d else 0)-0.5)}", sh_n])

                    st.session_state.project_list.append({
                        "client": client if client else "بدون اسم",
                        "type": u_type, "dims": f"{W}x{H}x{D}",
                        "alum": alum, "fiber": fiber, "note": note
                    })
                    st.success("تمت الإضافة بنجاح!")
                    st.rerun()

    # --- عرض النتائج والجرد ---
    if st.session_state.project_list:
        tab1, tab2 = st.tabs(["📊 الجرد الكلي للمشروع", "📋 شيتات تفصيل كل وحدة"])

        with tab1:
            muf_list, mut_list, fib_list = [], [], []
            for unit in st.session_state.project_list:
                for row in unit['alum']:
                    if row[3] == "مفرد": muf_list.append({"المقاس": row[1], "العدد": row[2]})
                    elif row[3] == "متقارب": mut_list.append({"المقاس": row[1], "العدد": row[2]})
                for row in unit['fiber']:
                    fib_list.append({"البيان": row[0], "المقاس": row[1], "العدد": row[2]})

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div style='background:{accent}; color:black; text-align:center; padding:5px; border-radius:5px;'><b>📋 جرد المفرد</b></div>", unsafe_allow_html=True)
                if muf_list:
                    df_muf = pd.DataFrame(muf_list).groupby("المقاس").sum().reset_index()
                    st.table(df_muf)
                    total = (df_muf['المقاس'] * df_muf['العدد']).sum()
                    st.info(f"الأعواد المطلوبة: {math.ceil(total/600)} (6م)")
            
            with c2:
                st.markdown(f"<div style='background:{accent}; color:black; text-align:center; padding:5px; border-radius:5px;'><b>📋 جرد المتقارب</b></div>", unsafe_allow_html=True)
                if mut_list:
                    df_mut = pd.DataFrame(mut_list).groupby("المقاس").sum().reset_index()
                    st.table(df_mut)
                    total = (df_mut['المقاس'] * df_mut['العدد']).sum()
                    st.info(f"الأعواد المطلوبة: {math.ceil(total/600)} (6م)")

            with c3:
                st.markdown(f"<div style='background:{accent}; color:black; text-align:center; padding:5px; border-radius:5px;'><b>🖼️ جرد الفيبر</b></div>", unsafe_allow_html=True)
                if fib_list: st.table(pd.DataFrame(fib_list))

        with tab2:
            for idx, item in enumerate(st.session_state.project_list):
                with st.expander(f"📌 وحدة {idx+1}: {item['client']} | {item['dims']}"):
                    col1, col2 = st.columns([3, 2])
                    with col1: st.write("**📐 تفصيل الألمنيوم**"); st.table(pd.DataFrame(item['alum'], columns=["البيان", "المقاس", "العدد", "النوع"]))
                    with col2: st.write("**🖼️ تفصيل الفيبر**"); st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))

        if st.button("🗑️ مسح المشروع بالكامل", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

st.markdown(f"<p style='text-align:center; opacity:0.3; margin-top:50px;'>DOGGA PRO | 2026</p>", unsafe_allow_html=True)
