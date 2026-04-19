import streamlit as st

st.title("📊 تطبيق تخصيم الألوميتال")

# =========================
# بيانات الوحدة
# =========================
st.header("بيانات الوحدة")

width = st.number_input("عرض الوحدة (سم)", value=None, placeholder="اكتب العرض")
height = st.number_input("ارتفاع الوحدة (سم)", value=None, placeholder="اكتب الارتفاع")
depth = st.number_input("عمق الوحدة (سم)", value=None, placeholder="اكتب العمق")

# =========================
# الأرفف
# =========================
st.header("الأرفف")

shelf_width = st.number_input("عرض الرف (سم)", value=None, placeholder="عرض الرف")
shelf_depth = st.number_input("عمق الرف (سم)", value=None, placeholder="عمق الرف")
shelves_count = st.number_input("عدد الأرفف", value=0, step=1)

# =========================
# الفواصل
# =========================
st.header("الفواصل")

divider_height = st.number_input("ارتفاع الفاصل (سم)", value=None, placeholder="ارتفاع الفاصل")
divider_depth = st.number_input("عمق الفاصل (سم)", value=None, placeholder="عمق الفاصل")
dividers_count = st.number_input("عدد الفواصل", value=0, step=1)

# =========================
# الأدراج
# =========================
st.header("الأدراج")

drawer_width = st.number_input("عرض الدرج (سم)", value=None, placeholder="عرض الدرج")
drawer_depth = st.number_input("عمق الدرج (سم)", value=None, placeholder="عمق الدرج")
drawers_count = st.number_input("عدد الأدراج", value=0, step=1)

# =========================
# زر الحساب
# =========================
if st.button("احسب التخصيم"):

    if width and height and depth:

        cut_w = width - 5
        cut_h = height - 13
        cut_d = depth - 5

        st.subheader("📌 التخصيم الأساسي")

        st.write("عرض:", cut_w)
        st.write("ارتفاع:", cut_h)
        st.write("عمق:", cut_d)

        # =========================
        # الأرفف
        # =========================
        if shelf_width and shelf_depth:
            st.subheader("📌 الأرفف")

            fiber_w = shelf_width - 5
            fiber_d = shelf_depth - 5

            st.write(f"فيبر رف: {fiber_w} × {fiber_d} × {shelves_count}")
            st.write(f"ألوميتال رف: {cut_h} × {shelves_count * 2}")

        # =========================
        # الفواصل
        # =========================
        if divider_height and divider_depth:
            st.subheader("📌 الفواصل")

            fiber_d = divider_depth - 5

            st.write(f"فيبر فاصل: {divider_height} × {fiber_d} × {dividers_count}")
            st.write(f"ألوميتال فاصل: {cut_h} × {dividers_count * 2}")

        # =========================
        # الأدراج
        # =========================
        if drawer_width and drawer_depth:
            st.subheader("📌 الأدراج")

            cut_dw = drawer_width - 2.5

            st.write(f"درج: {cut_dw} × {drawer_depth} × {drawers_count}")

    else:
        st.error("من فضلك ادخل بيانات الوحدة الأساسية")
