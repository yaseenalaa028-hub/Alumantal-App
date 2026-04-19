import streamlit as st
import pandas as pd

st.set_page_config(page_title="تخصيم المصنع", layout="wide")

st.title("🏭 نظام تخصيم تقطيع الألوميتال")
st.write("أدخل المقاسات الكلية للحصول على مقاسات كل قطعة منفردة")

# =========================
# 📐 المدخلات الأساسية
# =========================
with st.sidebar:
    st.header("⚙️ إعدادات الخصم")
    # خليت الخصومات هنا عشان لو حبيت تغيرها حسب القطاع
    off_w = st.number_input("خصم العرض (سم)", value=5.0)
    off_h = st.number_input("خصم الارتفاع (سم)", value=13.0)
    off_d = st.number_input("خصم العمق (سم)", value=5.0)

col1, col2, col3 = st.columns(3)
with col1: W = st.number_input("عرض الوحدة الكلي", min_value=0.0)
with col2: H = st.number_input("ارتفاع الوحدة الكلي", min_value=0.0)
with col3: D = st.number_input("عمق الوحدة الكلي", min_value=0.0)

st.divider()

# رفوف وأدراج
c1, c2 = st.columns(2)
with c1: shelf_q = st.number_input("عدد الرفوف", min_value=0, step=1)
with c2: draw_q = st.number_input("عدد الأدراج", min_value=0, step=1)

# =========================
# 🛠️ منطق الحساب (تخصيم يدوي دقيق)
# =========================
if st.button("إصدار بيان التقطيع النهائي", use_container_width=True):
    if W > 0 and H > 0:
        cutting_data = []

        # وظيفة لإضافة القطع للجدول
        def add_piece(cat, name, length, qty, material="ألوميتال"):
            cutting_data.append({
                "التصنيف": cat,
                "اسم القطعة": name,
                "طول القطعة (سم)": length,
                "العدد (حتة)": qty,
                "الخامة": material
            })

        # 1. تخصيم الألوميتال (الأعواد)
        # القوايم (ارتفاع)
        add_piece("الهيكل", "قائم ارتفاع", H, 4)
        # العوارض (عرض)
        add_piece("الهيكل", "عارضة عرض", W - off_w, 4)
        # الروابط (عمق)
        add_piece("الهيكل", "رباط عمق", D - off_d, 4)

        # 2. الرفوف (ألوميتال)
        if shelf_q > 0:
            add_piece("الرفوف", "برواز رف عرض", W - off_w, shelf_q * 2)
            add_piece("الرفوف", "برواز رف عمق", D - off_d, shelf_q * 2)

        # 3. الفيبر (مقاسات قص الألواح)
        # الفيبر بيتحسب كأبعاد (طول في عرض) - هنضيفهم كقطع منفصلة للوضوح
        add_piece("الفيبر", "ضهرية (عرض × ارتفاع)", f"{W-off_w} × {H-off_h}", 1, "لوح فيبر")
        add_piece("الفيبر", "أرضية وسقف (عرض × عمق)", f"{W-off_w} × {D-off_d}", 2, "لوح فيبر")
        add_piece("الفيبر", "أجناب (ارتفاع × عمق)", f"{H-off_h} × {D-off_d}", 2, "لوح فيبر")

        if shelf_q > 0:
            add_piece("الفيبر", "حشو رف (عرض × عمق)", f"{W-off_w-0.5} × {D-off_d-0.5}", shelf_q, "لوح فيبر")

        # عرض الجدول
        df = pd.DataFrame(cutting_data)
        
        # تنسيق العرض
        st.subheader("📋 كشف التقطيع")
        st.dataframe(df, use_container_width=True)
        
        # ملخص سريع للمخزن
        st.success(f"تم حساب {len(df)} بند تقطيع بنجاح")
    else:
        st.error("يا هندسة لازم تدخل العرض والارتفاع على الأقل!")
