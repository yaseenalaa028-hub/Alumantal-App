import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة
# ==========================================
st.set_page_config(page_title="DOGGA PRO SYSTEM", layout="wide")

if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

# تصميم الواجهة
accent = "#f1c40f" if st.session_state.dark_mode else "#d4ac0d"
bg_card = "#1c1f26" if st.session_state.dark_mode else "#f8f9fa"

st.markdown(f"""
    <style>
    .main {{ direction: rtl !important; text-align: right; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; }}
    .stTabs [data-baseweb="tab"] {{ background-color: {bg_card}; border-radius: 10px 10px 0 0; padding: 10px 20px; color: {accent}; }}
    .unit-card {{ background: {bg_card}; border-right: 5px solid {accent}; padding: 15px; border-radius: 10px; margin-bottom: 20px; }}
    </style>
""", unsafe_allow_html=True)

# الهيدر
c1, c2 = st.columns([8, 2])
with c1: st.markdown(f"<h1 style='color:{accent};'>🛠️ DOGGA PRO | المهندس ياسين علاء</h1>", unsafe_allow_html=True)
with c2:
    if st.button("🌓 تبديل المظهر"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. منطق التخصيم الشامل (Logic Pro)
# ==========================================
def calculate_advanced_deductions(u_type, w, h, d, sh_n, sh_w, sh_d, v_n, v_h, v_d, dr_n, dr_w, dr_d):
    # تخصيم الهيكل الأساسي
    h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
    hn, wn, dn = h - h_ded, w - 5, d - 5
    
    struc = [
        ["قوايم رئيسية", hn, 2, "مفرد"],
        ["عوارض عرض", wn, 2 if u_type == "وحدة علوية" else 3, "مفرد"],
        ["عوارض عمق", dn, 2, "مفرد"]
    ]
    
    # إضافة الأرفف
    if sh_n > 0:
        struc.append([f"أعواد أرفف ({sh_n})", sh_w, sh_n * 2, "مفرد"])
        struc.append([f"أعواد عمق رف", sh_d, sh_n * 2, "مفرد"])
        
    # إضافة الفواصل
    if v_n > 0:
        struc.append([f"أعواد فواصل ({v_n})", v_h, v_n * 2, "مفرد"])
        struc.append([f"عمق فاصل", v_d, v_n * 2, "مفرد"])
        
    # إضافة الأدراج
    if dr_n > 0:
        struc.append([f"براويز درج عرض ({dr_n})", dr_w - 2.5, dr_n * 2, "مفرد"])
        struc.append([f"براويز درج عمق", dr_d, dr_n * 2, "مفرد"])

    # تخصيم الفيبر
    fiber = [
        ["الظهر", f"{wn} x {hn}", 1],
        ["الأرضية", f"{wn} x {dn}", 1],
        ["أجناب", f"{hn} x {dn}", 2]
    ]
    if sh_n > 0: fiber.append(["فيبر أرفف", f"{sh_w-0.5} x {sh_d-0.5}", sh_n])
    if v_n > 0: fiber.append(["فيبر فواصل", f"{v_h-0.5} x {v_d-0.5}", v_n])

    return struc, fiber

# ==========================================
# 3. الواجهة والتبويبات
# ==========================================
tab1, tab2, tab3 = st.tabs(["➕ إضافة وحدة", "📋 شيت التفصيل", "📊 الجرد والطلب"])

with tab1:
    with st.form("main_form", clear_on_submit=True):
        st.markdown("#### 📐 الأبعاد الأساسية")
        r1c1, r1c2, r1c3 = st.columns(3)
        client = r1c1.text_input("اسم العميل")
        u_type = r1c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])
        W = r1c3.number_input("العرض الكلي", min_value=0.0)
        
        r2c1, r2c2, r2c3 = st.columns(3)
        H = r2c1.number_input("الارتفاع الكلي", min_value=0.0)
        D = r2c2.number_input("العمق الكلي", min_value=0.0)
        
        st.divider()
        st.markdown("#### ➕ الإضافات (أرفف - فواصل - أدراج)")
        
        # صف الأرفف
        f1, f2, f3 = st.columns(3)
        sh_n = f1.number_input("عدد الأرفف", min_value=0)
        sh_w = f2.number_input("عرض الرف", min_value=0.0)
        sh_d = f3.number_input("عمق الرف", min_value=0.0)
        
        # صف الفواصل
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", min_value=0)
        v_h = v2.number_input("ارتفاع الفاصل", min_value=0.0)
        v_d = v3.number_input("عمق الفاصل", min_value=0.0)
        
        # صف الأدراج
        d1, d2, d3 = st.columns(3)
        dr_n = d1.number_input("عدد الأدراج", min_value=0)
        dr_w = d2.number_input("عرض برواز الدرج", min_value=0.0)
        dr_d = d3.number_input("عمق الدرج", min_value=0.0)

        if st.form_submit_button("✅ حفظ وحساب التخصيم", use_container_width=True):
            if W > 0 and H > 0:
                struc, fiber = calculate_advanced_deductions(u_type, W, H, D, sh_n, sh_w, sh_d, v_n, v_h, v_d, dr_n, dr_w, dr_d)
                st.session_state.project_list.append({
                    "client": client if client else "بدون اسم",
                    "type": u_type, "W": W, "H": H, "D": D,
                    "struc": struc, "fiber": fiber
                })
                st.success("تمت الإضافة!")
                st.rerun()

with tab2:
    for idx, item in enumerate(st.session_state.project_list):
        with st.expander(f"📌 وحدة {idx+1}: {item['client']} | {item['type']} ({item['W']}x{item['H']})", expanded=True):
            c_a, c_f = st.columns([3, 2])
            with c_a:
                st.write("**📐 تخصيم الألومنيوم**")
                st.table(pd.DataFrame(item['struc'], columns=["البيان", "المقاس", "العدد", "النوع"]))
            with c_f:
                st.write("**🖼️ مقاسات الفيبر**")
                st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))
    
    if st.session_state.project_list and st.button("🗑️ مسح الكل"):
        st.session_state.project_list = []
        st.rerun()

with tab3:
    if st.session_state.project_list:
        all_cuts = []
        for item in st.session_state.project_list:
            for cut in item['struc']:
                all_cuts.append({"المقاس": cut[1], "العدد": cut[2]})
        
        df_total = pd.DataFrame(all_cuts).groupby("المقاس").sum().reset_index()
        total_cm = (df_total['المقاس'] * df_total['العدد']).sum()
        
        st.metric("إجمالي الأعواد المطلوبة (6 متر)", f"{math.ceil(total_cm / 600)} عود")
        st.dataframe(df_total.sort_values(by="المقاس", ascending=False), use_container_width=True)
