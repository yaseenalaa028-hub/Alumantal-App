import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة والواجهة
# ==========================================
st.set_page_config(page_title="DOGGA PRO SYSTEM", layout="wide")

if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'page' not in st.session_state: st.session_state.page = 'home'

accent = "#f1c40f"
bg_card = "#1c1f26"

st.markdown(f"""
    <style>
    .main {{ direction: rtl !important; text-align: right; }}
    .stApp {{ background-color: #0e1117; color: white; }}
    .section-header {{ 
        background: {accent}; color: #000; padding: 12px; 
        border-radius: 10px; font-weight: bold; margin: 20px 0; text-align: center; font-size: 20px;
    }}
    .metric-box {{
        background: {bg_card}; border: 2px solid {accent};
        padding: 15px; border-radius: 15px; text-align: center;
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الواجهة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div style="text-align: center; margin-top: 10%; padding: 50px; border-radius: 30px; border: 5px solid {accent}; background: {bg_card};">
            <h1 style="font-size: 5em; color: {accent}; font-weight: bold;">DOGGA SYSTEM PRO</h1>
            <h2 style="color:white;">ورشة المهندس ياسين علاء الذكية</h2>
            <p style="font-size: 1.5em; opacity: 0.8;">منظومة تخصيم وجرد الألمنيوم الاحترافية - إصدار 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم الآن", use_container_width=True, type="primary"):
        st.session_state.page = 'calc'
        st.rerun()

# ==========================================
# 3. صفحة الورشة
# ==========================================
else:
    c1, c2 = st.columns([8, 2])
    with c1: st.markdown(f"<h1 style='color:{accent}; text-align:right;'>🛠️ منطقة العمل | م/ ياسين علاء</h1>", unsafe_allow_html=True)
    with c2: 
        if st.button("🏠 العودة للرئيسية", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    st.divider()

    # --- نموذج الإدخال ---
    with st.expander("📝 إضافة وحدة جديدة للمشروع", expanded=True):
        with st.form("workshop_form", clear_on_submit=True):
            f1, f2 = st.columns(2)
            client = f1.text_input("اسم العميل / رقم الوحدة")
            u_type = f2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "وحدة أدراج"])
            
            d1, d2, d3 = st.columns(3)
            W = d1.number_input("العرض الكلي", value=None, placeholder="0")
            H = d2.number_input("الارتفاع الكلي", value=None, placeholder="0")
            D = d3.number_input("العمق الكلي", value=None, placeholder="0")

            st.markdown("#### ➕ الأرفف - الفواصل - الأدراج")
            a1, a2, a3 = st.columns(3)
            sh_n = a1.number_input("عدد الأرفف", min_value=0, value=0)
            sh_w = a2.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = a3.number_input("عمق الرف", value=None, placeholder="0")
            
            v1, v2, v3 = st.columns(3)
            v_n = v1.number_input("عدد الفواصل", min_value=0, value=0)
            v_h = v2.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            v_d = v3.number_input("عمق الفاصل", value=None, placeholder="0")

            dr1, dr2, dr3 = st.columns(3)
            dr_n = dr1.number_input("عدد الأدراج", min_value=0, value=0)
            dr_w = dr2.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = dr3.number_input("عمق الدرج", value=None, placeholder="0")

            if st.form_submit_button("✅ حفظ وحساب التخصيم", use_container_width=True):
                if W and H and D:
                    # تطبيق معادلات التخصيم
                    h_final = (H - 13) if (u_type == "وحدة سفلية" or u_type == "دولاب خزين") else (H - 5)
                    w_final = W - 5
                    d_final = D - 5

                    alum_data = []
                    # الهيكل (المعادلات اللي طلبتها)
                    if u_type == "وحدة سفلية":
                        alum_data.extend([["قوايم ارتفاع", int(h_final), 2, "مفرد"], ["قوايم ارتفاع", int(h_final), 2, "متقارب"],
                                         ["عوارض عرض", int(w_final), 3, "مفرد"], ["عوارض عرض", int(w_final), 1, "متقارب"],
                                         ["عوارض عمق", int(d_final), 2, "مفرد"], ["عوارض عمق", int(d_final), 2, "متقارب"]])
                    else:
                        alum_data.extend([["قوايم ارتفاع", int(h_final), 2, "مفرد"], ["قوايم ارتفاع", int(h_final), 2, "متقارب"],
                                         ["عوارض عرض", int(w_final), 2, "مفرد"], ["عوارض عرض", int(w_final), 2, "متقارب"],
                                         ["عوارض عمق", int(d_final), 0, "مفرد"], ["عوارض عمق", int(d_final), 4, "متقارب"]])

                    if sh_n > 0: alum_data.append(["أعواد أرفف", int(sh_w if sh_w else 0), int(sh_n*4), "مفرد"])
                    if v_n > 0: alum_data.append(["أعواد فواصل", int(v_h if v_h else 0), int(v_n*4), "مفرد"])
                    if dr_n > 0: 
                        alum_data.append(["براويز درج (عرض)", int((dr_w if dr_w else 0)-2.5), int(dr_n*2), "مفرد"])
                        alum_data.append(["براويز درج (عمق)", int(dr_d if dr_d else 0), int(dr_n*2), "مفرد"])

                    fiber_data = [["ضهرية", f"{int(w_final)}*{int(h_final)}", 1], ["أرضية", f"{int(w_final)}*{int(d_final)}", 1], ["أجناب", f"{int(h_final)}*{int(d_final)}", 2]]
                    if sh_n > 0: fiber_data.append(["فيبر أرفف", f"{int((sh_w if sh_w else 5)-5)}*{int((sh_d if sh_d else 5)-5)}", sh_n])
                    if v_n > 0: fiber_data.append(["فيبر فواصل", f"{int((v_h if v_h else 5)-5)}*{int((v_d if v_d else 5)-5)}", v_n])

                    st.session_state.project_list.append({"client": client, "alum": alum_data, "fiber": fiber_data})
                    st.rerun()

    # --- منطقة الجرد وحساب الأعواد ---
    if st.session_state.project_list:
        tab1, tab2 = st.tabs(["📊 حساب عدد الأعواد والجرد", "📋 تفصيل الوحدات"])
        
        with tab1:
            muf_all, mut_all, fib_all = [], [], []
            total_muf_cm = 0
            total_mut_cm = 0
            
            for u in st.session_state.project_list:
                for row in u['alum']:
                    if row[3] == "مفرد":
                        muf_all.append({"المقاس": row[1], "العدد": row[2]})
                        total_muf_cm += (row[1] * row[2])
                    else:
                        mut_all.append({"المقاس": row[1], "العدد": row[2]})
                        total_mut_cm += (row[1] * row[2])
                for f in u['fiber']: fib_all.append({"البيان": f[0], "المقاس": f[1], "العدد": f[2]})

            # عرض عدد الأعواد المطلوبة
            st.markdown("<div class='section-header'>الخامات المطلوبة (طول العود 6 متر)</div>", unsafe_allow_html=True)
            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f"""<div class='metric-box'>
                    <h3 style='color:{accent};'>أعواد المفرد</h3>
                    <h2 style='margin:0;'>{math.ceil(total_muf_cm / 600)} عود</h2>
                    <p style='opacity:0.7;'>إجمالي الطول: {total_muf_cm/100:.2f} متر</p>
                </div>""", unsafe_allow_html=True)
            with res2:
                st.markdown(f"""<div class='metric-box'>
                    <h3 style='color:{accent};'>أعواد المتقارب</h3>
                    <h2 style='margin:0;'>{math.ceil(total_mut_cm / 600)} عود</h2>
                    <p style='opacity:0.7;'>إجمالي الطول: {total_mut_cm/100:.2f} متر</p>
                </div>""", unsafe_allow_html=True)

            # الجداول التفصيلية
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("📋 مقاسات المفرد")
                if muf_all: st.table(pd.DataFrame(muf_all).groupby("المقاس").sum().reset_index().sort_values("المقاس", ascending=False))
            with c2:
                st.subheader("📋 مقاسات المتقارب")
                if mut_all: st.table(pd.DataFrame(mut_all).groupby("المقاس").sum().reset_index().sort_values("المقاس", ascending=False))
            with c3:
                st.subheader("🖼️ مقاسات الفيبر")
                if fib_all: st.table(pd.DataFrame(fib_all))

        with tab2:
            for idx, u in enumerate(st.session_state.project_list):
                with st.expander(f"تفصيل وحدة {idx+1}: {u['client']}"):
                    st.table(pd.DataFrame(u['alum'], columns=["البيان", "المقاس", "العدد", "النوع"]))

        if st.button("🗑️ مسح المشروع والبدء من جديد", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

st.markdown("<p style='text-align:center; opacity:0.3; margin-top:50px;'>DOGGA PRO | م/ ياسين علاء</p>", unsafe_allow_html=True)
