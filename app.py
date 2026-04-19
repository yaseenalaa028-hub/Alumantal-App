import streamlit as st
import pandas as pd

st.set_page_config(page_title="تخصيم مصنع الألوميتال", layout="wide")

st.title("🏭 نظام تخصيم تقطيع الألوميتال (البيان الأساسي)")
st.markdown("---")

# وظيفة لإضافة البيانات للجدول لضمان عدم التكرار والوضوح
if 'cutting_list' not in st.session_state:
    st.session_state.cutting_list = []

def add_to_list(cat, name, length, qty, material="ألوميتال"):
    st.session_state.cutting_list.append({
        "الخامة": material,
        "القسم": cat,
        "اسم القطعة": name,
        "المقاس (L)": length,
        "العدد (Qty)": qty
    })

# =========================
# 📐 1. الوحدة الأساسية (العلبة)
# =========================
st.header("📐 الهيكل الأساسي للعلبة")
col_w, col_h, col_d = st.columns(3)
W = col_w.number_input("عرض العلبة الكلي", value=0.0, key="main_w")
H = col_h.number_input("ارتفاع العلبة الكلي", value=0.0, key="main_h")
D = col_d.number_input("عمق العلبة الكلي", value=0.0, key="main_d")

st.divider()

# =========================
# 📚 2. الرفوف (بمقاسات منفصلة)
# =========================
st.header("📚 الرفوف")
c1, c2, c3 = st.columns(3)
s_w = c1.number_input("عرض الرف المُراد", value=0.0)
s_d = c2.number_input("عمق الرف المُراد", value=0.0)
s_q = c3.number_input("عدد الرفوف", min_value=0, step=1)

st.divider()

# =========================
# 🧱 3. الفواصل (بمقاسات منفصلة)
# =========================
st.header("🧱 الفواصل")
f1, f2, f3 = st.columns(3)
v_h = f1.number_input("ارتفاع الفاصل", value=0.0)
v_d = f2.number_input("عمق الفاصل", value=0.0)
v_q = f3.number_input("عدد الفواصل", min_value=0, step=1)

st.divider()

# =========================
# 🗄️ 4. الأدراج (بمقاسات منفصلة)
# =========================
st.header("🗄️ الأدراج")
d1, d2, d3 = st.columns(3)
dr_w = d1.number_input("عرض الدرج", value=0.0)
dr_d = d2.number_input("عمق الدرج", value=0.0)
dr_q = d3.number_input("عدد الأدراج", min_value=0, step=1)

# =========================
# 🚀 زر التشغيل والحسابات
# =========================
if st.button("إصدار كشف التقطيع التفصيلي", use_container_width=True):
    st.session_state.cutting_list = [] # تصفير القائمة عند كل ضغطة
    
    # --- حسابات العلبة ---
    if W > 0 and H > 0:
        add_to_list("العلبة", "قائم ارتفاع", H, 4)
        add_to_list("العلبة", "عارضة عرض", W - 5, 4)
        add_to_list("العلبة", "رباط عمق", D - 5, 4)
        add_to_list("فيبر", "ضهرية", f"{W-5} × {H-13}", 1, "فيبر")

    # --- حسابات الرفوف ---
    if s_q > 0:
        add_to_list("الرفوف", "برواز رف عرض", s_w, s_q * 2)
        add_to_list("الرفوف", "برواز رف عمق", s_d, s_q * 2)
        add_to_list("فيبر", "حشو رف", f"{s_w-0.5} × {s_d-0.5}", s_q, "فيبر")

    # --- حسابات الفواصل ---
    if v_q > 0:
        add_to_list("الفواصل", "قائم فاصل", v_h, v_q * 2)
        add_to_list("الفواصل", "رباط فاصل عمق", v_d, v_q * 2)
        add_to_list("فيبر", "حشو فاصل", f"{v_h-0.5} × {v_d-0.5}", v_q, "فيبر")

    # --- حسابات الأدراج ---
    if dr_q > 0:
        add_to_list("الأدراج", "وش/ضهر درج", dr_w, dr_q * 2)
        add_to_list("الأدراج", "جنب درج عمق", dr_d, dr_q * 2)
        add_to_list("فيبر", "قاع درج", f"{dr_w-0.5} × {dr_d-0.5}", dr_q, "فيبر")

    # عرض النتائج
    if st.session_state.cutting_list:
        df = pd.DataFrame(st.session_state.cutting_list)
        st.subheader("📋 بيان التقطيع النهائي")
        st.table(df)
    else:
        st.error("برجاء إدخال بيانات صحيحة")
