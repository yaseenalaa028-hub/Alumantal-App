import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة والواجهة
# ==========================================
st.set_page_config(page_title="DOGGA PRO SYSTEM", layout="wide")

# تهيئة المخازن
if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'page' not in st.session_state: st.session_state.page = 'home'

accent = "#f1c40f"
bg_card = "#1c1f26"

st.markdown(f"""
    <style>
    .main {{ direction: rtl !important; text-align: right; }}
    .stApp {{ background-color: #0e1117; color: white; }}
    
    /* تعديل كلمة ضجة للموبايل */
    .hero-title {{
        font-size: 5vw; /* حجم خط مرن حسب عرض الشاشة */
        color: {accent}; 
        font-weight: bold;
        white-space: nowrap; /* منع الكلمة من النزول لسطر جديد */
    }}
    
    @media (max-width: 600px) {{
        .hero-title {{
            font-size: 10vw; /* حجم أكبر قليلاً للموبايل ليملأ العرض */
        }}
    }}

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
        <div style="text-align: center; margin-top: 10%; padding: 30px; border-radius: 30px; border: 5px solid {accent}; background: {bg_card};">
            <h1 class="hero-title">DOGGA SYSTEM PRO</h1>
            <h2 style="color:white;">ورشة المهندس ياسين علاء الذكية</h2>
            <p style="font-size: 1.2em; opacity: 0.8;">منظومة تخصيم الألمنيوم والفيبر - الإصدار المعتمد 2026</p>
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
        if st.button("🏠 الرئيسية"): st.session_state.page = 'home'; st.rerun()

    st.divider()

    # --- نموذج الإدخال (مقاسات ثابتة لا تُمحى) ---
    with st.expander("📝 إدخال وتعديل المقاسات", expanded=True):
        with st.form("workshop_form", clear_on_submit=False):
            f1, f2 = st.columns(2)
            client_name = f1.text_input("اسم العميل / رقم الوحدة")
            unit_type = f2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])
            
            d1, d2, d3 = st.columns(3)
            W_val = d1.number_input("العرض الكلي", value=0.0)
            H_val = d2.number_input("الارتفاع الكلي", value=0.0)
            D_val = d3.number_input("العمق الكلي", value=0.0)

            st.markdown("#### ➕ الأرفف والفواصل")
            a1, a2, a3 = st.columns(3)
            sh_n = a1.number_input("عدد الأرفف", min_value=0, step=1)
            sh_w = a2.number_input("عرض الرف", value=0.0)
            sh_d = a3.number_input("عمق الرف", value=0.0)
            
            v1, v2, v3 = st.columns(3)
            v_n = v1.number_input("عدد الفواصل", min_value=0, step=1)
            v_h = v2.number_input("ارتفاع الفاصل", value=0.0)
            v_d = v3.number_input("عمق الفاصل", value=0.0)

            if st.form_submit_button("✅ حفظ وإضافة للجدول", use_container_width=True):
                if W_val > 0 and H_val > 0 and D_val > 0:
                    # التخصيم الأساسي
                    h_final = (H_val - 13) if (unit_type in ["وحدة سفلية", "دولاب خزين"]) else (H_val - 5)
                    w_final = W_val - 5
                    d_final = D_val - 5

                    alum_res = []
                    # هيكل الوحدة
                    if unit_type == "وحدة سفلية":
                        alum_res.extend([
                            ["قوايم ارتفاع", int(h_final), 2, "مفرد"], ["قوايم ارتفاع", int(h_final), 2, "متقارب"],
                            ["عوارض عرض", int(w_final), 3, "مفرد"], ["عوارض عرض", int(w_final), 1, "متقارب"],
                            ["عوارض عمق", int(d_final), 2, "مفرد"], ["عوارض عمق", int(d_final), 2, "متقارب"]
                        ])
                    else:
                        alum_res.extend([
                            ["قوايم ارتفاع", int(h_final), 2, "مفرد"], ["قوايم ارتفاع", int(h_final), 2, "متقارب"],
                            ["عوارض عرض", int(w_final), 2, "مفرد"], ["عوارض عرض", int(w_final), 2, "متقارب"],
                            ["عوارض عمق", int(d_final), 0, "مفرد"], ["عوارض عمق", int(d_final), 4, "متقارب"]
                        ])

                    # تخصيم الأرفف والفواصل (العدد في 4 أعواد ألمنيوم)
                    if sh_n > 0:
                        alum_res.append(["أعواد أرفف (عرض)", int(sh_w), int(sh_n * 4), "مفرد"])
                        alum_res.append(["أعواد أرفف (عمق)", int(sh_d), int(sh_n * 4), "مفرد"])
                    if v_n > 0:
                        alum_res.append(["أعواد فواصل (ارتفاع)", int(v_h), int(v_n * 4), "مفرد"])
                        alum_res.append(["أعواد فواصل (عمق)", int(v_d), int(v_n * 4), "مفرد"])

                    # تخصيم الفيبر
                    fiber_res = [
                        ["ضهرية", int(w_final), int(h_final), 1],
                        ["أرضية", int(w_final), int(d_final), 1],
                        ["أجناب", int(h_final), int(d_final), 2]
                    ]
                    if sh_n > 0: fiber_res.append(["فيبر أرفف", int(sh_w-5), int(sh_d-5), sh_n])
                    if v_n > 0: fiber_res.append(["فيبر فواصل", int(v_h-5), int(v_d-5), v_n])

                    st.session_state.project_list.append({
                        "client": client_name if client_name else "بدون اسم",
                        "type": unit_type,
                        "dims": f"{W_val}x{H_val}x{D_val}",
                        "alum": alum_res,
                        "fiber": fiber_res
                    })
                    st.success("تم الحفظ في الجدول")
                    st.rerun()

    # --- عرض الجداول والجرد ---
    if st.session_state.project_list:
        tab1, tab2 = st.tabs(["📊 الإجمالي (الطلبية)", "📋 تفصيل الوحدات"])
        
        with tab1:
            total_muf_cm = total_mut_cm = total_fiber_sqcm = 0
            muf_all, mut_all, fib_all = [], [], []
            
            for unit in st.session_state.project_list:
                for row in unit["alum"]:
                    if row[3] == "مفرد":
                        muf_all.append({"المقاس": row[1], "العدد": row[2]})
                        total_muf_cm += (row[1] * row[2])
                    else:
                        mut_all.append({"المقاس": row[1], "العدد": row[2]})
                        total_mut_cm += (row[1] * row[2])
                for f in unit["fiber"]:
                    fib_all.append({"البيان": f[0], "المقاس": f"{f[1]}*{f[2]}", "العدد": f[3]})
                    total_fiber_sqcm += (f[1] * f[2] * f[3])

            st.markdown("<div class='section-header'>تقرير الخامات الإجمالي</div>", unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1: st.markdown(f"<div class='metric-box'><h3>أعواد المفرد</h3><h2>{math.ceil(total_muf_cm / 600)} عود</h2></div>", unsafe_allow_html=True)
            with r2: st.markdown(f"<div class='metric-box'><h3>أعواد المتقارب</h3><h2>{math.ceil(total_mut_cm / 600)} عود</h2></div>", unsafe_allow_html=True)
            with r3:
                panel_area = 280 * 130 
                needed_panels = math.ceil((total_fiber_sqcm * 1.10) / panel_area)
                st.markdown(f"<div class='metric-box'><h3>ألواح الفيبر</h3><h2>{needed_panels} لوح</h2></div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("📋 جرد المفرد")
                if muf_all: st.table(pd.DataFrame(muf_all).groupby("المقاس").sum().reset_index())
            with c2:
                st.subheader("📋 جرد المتقارب")
                if mut_all: st.table(pd.DataFrame(mut_all).groupby("المقاس").sum().reset_index())
            with c3:
                st.subheader("🖼️ جرد الفيبر")
                if fib_all: st.table(pd.DataFrame(fib_all))

        with tab2:
            for idx, unit in enumerate(st.session_state.project_list):
                with st.expander(f"📌 وحدة {idx+1}: {unit['client']}"):
                    st.write("**الألمنيوم:**")
                    st.table(pd.DataFrame(unit['alum'], columns=["البيان", "المقاس", "العدد", "النوع"]))
                    st.write("**الفيبر:**")
                    st.table(pd.DataFrame(unit['fiber'], columns=["البيان", "العرض", "الارتفاع", "العدد"]))

        if st.button("🗑️ مسح الجدول بالكامل", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

st.markdown("<p style='text-align:center; opacity:0.3; margin-top:50px;'>DOGGA PRO SYSTEM | م/ ياسين علاء</p>", unsafe_allow_html=True)
