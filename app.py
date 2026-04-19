import streamlit as st

st.title("تطبيق تخصيم الألوميتال")

# =========================
# بيانات الوحدة
# =========================
width = st.number_input("عرض الوحدة", value=200.0)
height = st.number_input("ارتفاع الوحدة", value=90.0)
depth = st.number_input("عمق الوحدة", value=50.0)

# =========================
# أرفف / فواصل / أدراج
# =========================
shelves = st.number_input("عدد الأرفف", value=0, step=1)
dividers = st.number_input("عدد الفواصل", value=0, step=1)
drawers = st.number_input("عدد الأدراج", value=0, step=1)

# =========================
# زر الحساب
# =========================
if st.button("احسب التخصيم"):

    # التخصيم الأساسي
    cut_w = width - 5
    cut_h = height - 13
    cut_d = depth - 5

    st.subheader("📌 الألوميتال")

    st.write(f"ارتفاع مفرد/متقارب: {cut_h}")
    st.write(f"عرض مفرد/متقارب: {cut_w}")
    st.write(f"عمق مفرد/متقارب: {cut_d}")

    st.subheader("📌 الفيبر")

    st.write(f"الضهرية: {cut_w} × {cut_h}")
    st.write(f"الأرضية: {cut_w} × {cut_d}")
    st.write(f"الأجناب: {cut_h} × {cut_d}")

    # =========================
    # الأرفف
    # =========================
    if shelves > 0:
        shelf_w = cut_w - 5
        shelf_d = cut_d - 5

        st.subheader("📌 الأرفف")
        st.write(f"فيبر رف: {shelf_w} × {shelf_d} × {shelves}")
        st.write(f"ألوميتال رف: {cut_h} × {shelves * 2}")

    # =========================
    # الفواصل
    # =========================
    if dividers > 0:
        divider_h = cut_h
        divider_d = cut_d - 5

        st.subheader("📌 الفواصل")
        st.write(f"فيبر فاصل: {divider_h} × {divider_d} × {dividers}")
        st.write(f"ألوميتال فاصل: {cut_h} × {dividers * 2}")

    # =========================
    # الأدراج
    # =========================
    if drawers > 0:
        drawer_w = width - 2.5
        drawer_d = depth

        st.subheader("📌 الأدراج")
        st.write(f"درج: {drawer_w} × {drawer_d} × {drawers}")
