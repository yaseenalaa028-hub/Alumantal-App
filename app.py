import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام تخصيم الألوميتال", layout="centered")

st.title("🏭 نظام تخصيم مصنع الألوميتال")
st.markdown("---")

# =========================
# 📐 الوحدة الأساسية
# =========================
st.header("📐 بيانات الوحدة الأساسية")
col1, col2, col3 = st.columns(3)
with col1:
    W = st.number_input("عرض الوحدة (W)", min_value=0.0, step=0.1)
with col2:
    H = st.number_input("ارتفاع الوحدة (H)", min_value=0.0, step=0.1)
with col3:
    D = st.number_input("عمق الوحدة (D)", min_value=0.0, step=0.1)

st.divider()

# =========================
# 📚 الرفوف والفواصل والأدراج
# =========================
tab1, tab2, tab3 = st.tabs(["📚 الرفوف", "🧱 الفواصل", "🗄️ الأدراج"])

with tab1:
    c1, c2, c3 = st.columns(3)
    shelf_w = c1.number_input("عرض الرف", value=W-5 if W > 5 else 0.0)
    shelf_d = c2.number_input("عمق الرف", value=D-5 if D > 5 else 0.0)
    shelf_q = c3.number_input("عدد الرفوف", min_value=0, step=1)

with tab2:
    c1, c2, c3 = st.columns(3)
    div_h = c1.number_input("ارتفاع الفاصل", value=H-13 if H > 13 else 0.0)
    div_d = c2.number_input("عمق الفاصل", value=D-5 if D > 5 else 0.0)
    div_q = c3.number_input("عدد الفواصل", min_value=0, step=1)

with tab3:
    c1, c2, c3 = st.columns(3)
    draw_w = c1.number_input("عرض الدرج", value=0.0)
    draw_d = c2.number_input("عمق الدرج", value=0.0)
    draw_q = c3.number_input("عدد الأدراج", min_value=0, step=1)

st.divider()

# =========================
# تشغيل الحسابات
# =========================
if st.button("🚀 تشغيل التخصيم واستخراج النتائج", use_container_width=True):
    if W == 0 or H == 0:
        st.error("⚠️ يرجى إدخال أبعاد الوحدة الأساسية أولاً")
    else:
        data = []

        def add(category, desc, size, qty):
            data.append({"النوع": category, "الوصف": desc, "المقاس (سم)": size, "العدد": qty})

        # --- الجسم الأساسي ---
        body_w = W - 5
        body_h = H - 13
        body_d = D - 5

        add("فيبر", "ضهرية (W-5 x H-13)", f"{body_w} × {body_h}", 1)
        add("فيبر", "أرضية (W-5 x D-5)", f"{body_w} × {body_d}", 1)
        add("فيبر", "أجناب (H-13 x D-5)", f"{body_h} × {body_d}", 2)

        # --- الرفوف ---
        if shelf_q > 0:
            add("فيبر", "رف داخلي", f"{shelf_w - 0.5} × {shelf_d - 0.5}", shelf_q)
            add("ألوميتال", "مقاس عرض الرف", f"{shelf_w}", shelf_q * 2)
            add("ألوميتال", "مقاس عمق الرف", f"{shelf_d}", shelf_q * 2)

        # --- الفواصل ---
        if div_q > 0:
            add("فيبر", "فاصل رأسي", f"{div_h - 0.5} × {div_d - 0.5}", div_q)
            add("ألوميتال", "مقاس ارتفاع الفاصل", f"{div_h}", div_q * 2)
            add("ألوميتال", "مقاس عمق الفاصل", f"{div_d}", div_q * 2)

        # --- الأدراج ---
        if draw_q > 0:
            add("فيبر", "قاع الدرج", f"{draw_w} × {draw_d}", draw_q)
            add("ألوميتال", "عرض الدرج (خارجي)", f"{draw_w + 2}", draw_q * 2)
            add("ألوميتال", "جوانب الدرج", f"{draw_d}", draw_q * 2)

        # عرض النتائج
        df = pd.DataFrame(data)
        st.success("✅ تم حساب المقاسات بنجاح")
        st.table(df) # استخدام table لعرض أوضح في الجداول الصغيرة
