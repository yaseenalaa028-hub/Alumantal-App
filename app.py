import streamlit as st
import pandas as pd

# إعداد الصفحة وتنسيق احترافي
st.set_page_config(page_title="DOGGA SYSTEM - تخصيم الألوميتال", layout="wide")

st.markdown("""
    <style>
    .report-font { font-family: 'Arial'; font-size: 18px; }
    .stNumberInput label { font-weight: bold; color: #1E3A8A; }
    </style>
    """, unsafe_allow_index=True)

st.title("🏭 نظام DOGGA للهندسة والتخصيم (الإصدار الاحترافي)")
st.write("حسابات دقيقة بناءً على أبعاد القطاع الفعلي والخصومات الفنية")

# --- قاعدة بيانات القطاعات (سماكة العود) ---
PROFILES = {
    "قطاع مطبخ (4 سم)": {"frame": 4.0, "fiber_add": 1.4},
    "قطاع مطبخ (4.5 سم)": {"frame": 4.5, "fiber_add": 1.6},
    "قطاع جامبو (5 سم)": {"frame": 5.0, "fiber_add": 1.8}
}

# --- إدارة الحالة (Session State) ---
if 'final_list' not in st.session_state:
    st.session_state.final_list = []

def add_item(cat, name, length, qty, note="", material="ألوميتال"):
    st.session_state.final_list.append({
        "الخامة": material,
        "القسم": cat,
        "اسم القطعة": name,
        "المقاس (L)": length,
        "العدد (Qty)": qty,
        "ملاحظات": note
    })

# =========================
# ⚙️ الإعدادات الفنية (السر في الدقة)
# =========================
with st.sidebar:
    st.header("⚙️ الإعدادات الهندسية")
    profile_type = st.selectbox("نوع القطاع", list(PROFILES.keys()))
    P_FRAME = PROFILES[profile_type]["frame"]
    F_ADD = PROFILES[profile_type]["fiber_add"]
    
    st.divider()
    st.subheader("إعدادات الأدراج والسكة")
    rail_deduction = st.number_input("خصم السكة الإجمالي (للطرفين)", value=2.6) # المعتاد للسكة البلي
    st.info(f"يتم الخصم بناءً على سماكة قطاع: {P_FRAME} سم")

# =========================
# 📐 المدخلات الأساسية
# =========================
c1, c2, c3 = st.columns(3)
with c1:
    W = st.number_input("العرض الكلي (W)", min_value=0.0)
with c2:
    H = st.number_input("الارتفاع الكلي (H)", min_value=0.0)
with c3:
    D = st.number_input("العمق الكلي (D)", min_value=0.0)

st.divider()

# أقسام الملحقات
col_shelf, col_divider, col_drawer = st.columns(3)

with col_shelf:
    st.subheader("📚 الرفوف")
    s_q = st.number_input("عدد الرفوف", min_value=0, step=1)

with col_divider:
    st.subheader("🧱 الفواصل")
    v_q = st.number_input("عدد الفواصل", min_value=0, step=1)
    v_h = st.number_input("ارتفاع الفاصل الصافي", value=0.0)

with col_drawer:
    st.subheader("🗄️ الأدراج")
    dr_q = st.number_input("عدد الأدراج", min_value=0, step=1)
    dr_h = st.number_input("ارتفاع وجه الدرج", value=0.0)

# =========================
# 🚀 محرك الحسابات (Logic)
# =========================
if st.button("إصدار كشف التقطيع الهندسي النهائي", use_container_width=True):
    st.session_state.final_list = []
    
    if W > 0 and H > 0 and D > 0:
        # 1. الهيكل الأساسي
        # القائم يؤخذ بالكامل
        add_item("العلبة", "قائم ارتفاع", H, 4, "قطع عدل")
        
        # العارضة = العرض - (2 × سماكة القطاع)
        main_w_cut = W - (2 * P_FRAME)
        add_item("العلبة", "عارضة عرض", round(main_w_cut, 2), 4, "تخصيم قوائم")
        
        # الرباط = العمق - (2 × سماكة القطاع)
        main_d_cut = D - (2 * P_FRAME)
        add_item("العلبة", "رباط عمق", round(main_d_cut, 2), 4, "تخصيم قوائم")
        
        # الظهرية (فيبر) = العرض الصافي + مقدار دخول الفيبر في المجرى
        fiber_w = main_w_cut + F_ADD
        fiber_h = H - 13 # الخصم الفني المعتمد للعلب السفلية
        add_item("الفيبر", "ظهرية العلبة", f"{round(fiber_w, 2)} × {round(fiber_h, 2)}", 1, "فيبر 3ملم", "فيبر")

        # 2. الرفوف (تخصيم الرف ليدخل داخل العلبة بمرونة)
        if s_q > 0:
            shelf_w = main_w_cut - 0.2 # خلوص بسيط للتركيب
            shelf_d = main_d_cut - 1.0 # خلوص للظهرية
            add_item("الرفوف", "برواز رف عرض", round(shelf_w, 2), s_q * 2)
            add_item("الرفوف", "برواز رف عمق", round(shelf_d, 2), s_q * 2)
            add_item("الفيبر", "حشو رف", f"{round(shelf_w - 0.5, 2)} × {round(shelf_d - 0.5, 2)}", s_q, "حشو داخلي", "فيبر")

        # 3. الفواصل
        if v_q > 0 and v_h > 0:
            add_item("الفواصل", "قائم فاصل", v_h, v_q * 2)
            add_item("الفواصل", "رباط فاصل عمق", main_d_cut, v_q * 2)
            add_item("الفيبر", "حشو فاصل", f"{round(v_h - 0.5, 2)} × {round(main_d_cut - 0.5, 2)}", v_q, "", "فيبر")

        # 4. الأدراج (تخصيم السكة)
        if dr_q > 0:
            # عرض الدرج الصافي = العرض الداخلي للعلبة - سماكة السكتين
            dr_w_final = main_w_cut - rail_deduction
            add_item("الأدراج", "وش/ضهر درج", round(dr_w_final, 2), dr_q * 2, "تخصيم السكة")
            add_item("الأدراج", "جنب درج عمق", main_d_cut - 2, dr_q * 2, "تخصيم الرجوع")
            add_item("الفيبر", "قاع درج", f"{round(dr_w_final - 0.5, 2)} × {round(main_d_cut - 2.5, 2)}", dr_q, "", "فيبر")

    # عرض النتائج
    if st.session_state.final_list:
        df = pd.DataFrame(st.session_state.final_list)
        st.subheader("📋 بيان التقطيع النهائي لورشة DED EL KASR")
        st.table(df)
    else:
        st.error("برجاء إدخال الأبعاد الأساسية (الطول، العرض، العمق) أولاً")
