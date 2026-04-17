import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام تخصيم الألومنيوم", layout="wide")

# =======================
# بيانات الجلسة
# =======================
if "units" not in st.session_state:
    st.session_state.units = []

# =======================
# العنوان
# =======================
st.title("🧠 نظام تخصيم الألومنيوم - نسخة احترافية (Web)")

st.markdown("برنامج حساب التخصيم + الرفوف + الفواصل + الأدراج + الجرد")

# =======================
# الإدخالات
# =======================
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("اسم الوحدة")

with col2:
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])

with col3:
    w = st.number_input("العرض", min_value=0.0, step=0.5)
    h = st.number_input("الارتفاع", min_value=0.0, step=0.5)
    d = st.number_input("العمق", min_value=0.0, step=0.5)

col4, col5, col6 = st.columns(3)

with col4:
    shelves = st.number_input("عدد الرفوف", min_value=0)

with col5:
    dividers = st.number_input("عدد الفواصل", min_value=0)

with col6:
    drawers = st.number_input("عدد الأدراج", min_value=0)

# =======================
# دالة التخصيم
# =======================
def calc_cut(w, h, d, t):
    if t in ["سفلية", "دولاب خزين"]:
        h2 = h - 13
    else:
        h2 = h - 5

    w2 = w - 5
    d2 = d - 5

    return max(h2, 0), max(w2, 0), max(d2, 0)

# =======================
# إضافة وحدة
# =======================
if st.button("➕ إضافة وحدة"):
    if name and w > 0 and h > 0 and d > 0:

        h2, w2, d2 = calc_cut(w, h, d, unit_type)

        unit = {
            "اسم الوحدة": name,
            "النوع": unit_type,
            "العرض": w,
            "الارتفاع": h,
            "العمق": d,
            "تخصيم_ارتفاع": h2,
            "تخصيم_عرض": w2,
            "تخصيم_عمق": d2,
            "رفوف": int(shelves),
            "فواصل": int(dividers),
            "أدراج": int(drawers),
        }

        st.session_state.units.append(unit)
        st.success("✔ تم إضافة الوحدة بنجاح")

    else:
        st.error("❌ املأ البيانات الأساسية")

# =======================
# الجدول
# =======================
if st.session_state.units:
    df = pd.DataFrame(st.session_state.units)

    st.subheader("📋 جدول الوحدات")
    st.dataframe(df, use_container_width=True)

    # =======================
    # الجرد (Totals)
    # =======================
    st.subheader("📊 جرد المشروع")

    total_units = len(st.session_state.units)
    total_shelves = sum(u["رفوف"] for u in st.session_state.units)
    total_dividers = sum(u["فواصل"] for u in st.session_state.units)
    total_drawers = sum(u["أدراج"] for u in st.session_state.units)

    # حساب خامات تقريبية (زي فكرة مشروعك)
    alu_simple = sum(u["تخصيم_عرض"] + u["تخصيم_ارتفاع"] + u["تخصيم_عمق"] for u in st.session_state.units)
    fiber_area = sum(u["تخصيم_عرض"] * u["تخصيم_ارتفاع"] for u in st.session_state.units)

    colA, colB, colC, colD = st.columns(4)

    colA.metric("عدد الوحدات", total_units)
    colB.metric("الرفوف", total_shelves)
    colC.metric("الفواصل", total_dividers)
    colD.metric("الأدراج", total_drawers)

    st.divider()

    st.write("🔩 تقدير الألومنيوم:", round(alu_simple / 600, 2), "عود")
    st.write("🪵 تقدير الفيبر:", round(fiber_area / 36400, 2), "لوح")

# =======================
# مسح البيانات
# =======================
if st.button("🗑️ مسح المشروع بالكامل"):
    st.session_state.units = []
    st.rerun()

# =======================
# تحميل التقرير
# =======================
if st.session_state.units:
    report_df = pd.DataFrame(st.session_state.units)

    csv = report_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ تحميل التقرير (CSV)",
        data=csv,
        file_name="aluminum_report.csv",
        mime="text/csv"
    )
