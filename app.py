import streamlit as st
import pandas as pd

# إعداد الصفحة وتنسيق DOGGA SYSTEM
st.set_page_config(page_title="DOGGA SYSTEM - تخصيم الألوميتال", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stTable { direction: rtl; }
    th { background-color: #1E3A8A !important; color: white !important; text-align: center; }
    td { text-align: center; }
    label { font-weight: bold; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏭 نظام DOGGA للهندسة والتخصيم (الإصدار الشامل)")
st.info("تخصيم دقيق: (مفرد / متقارب) + تخصيم الفيبر + تخصيم الفواصل والأرفف")

# --- إدارة حالة البيانات ---
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": round(length, 1) if isinstance(length, (int, float)) else length,
        "العدد (الكمية)": qty,
        "نوع التخصيم": unit_type
    })

# --- واجهة إدخال البيانات ---
with st.container():
    st.subheader("📏 1. أبعاد الوحدة الأساسية")
    c1, c2, c3, c4 = st.columns(4)
    unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
    W = c2.number_input("عرض القطعة الكلي (W)", min_value=0.0)
    H = c3.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0)
    D = c4.number_input("عمق القطعة الكلي (D)", min_value=0.0)

    st.divider()
    
    st.subheader("🧱 2. الفواصل والأرفف (تخصيم تفصيلي)")
    col_v1, col_v2, col_v3 = st.columns(3)
    v_h = col_v1.number_input("ارتفاع الفاصل / عرض الرف", value=0.0)
    v_d = col_v2.number_input("عمق الفاصل / الرف", value=0.0)
    v_q = col_v3.number_input("عدد (الفواصل أو الرفوف)", min_value=0, step=1)

    st.divider()
    
    st.subheader("🗄️ 3. الأدراج")
    dr_col1, dr_col2, dr_col3 = st.columns(3)
    dr_w = dr_col1.number_input("عرض الدرج", value=0.0)
    dr_d = dr_col2.number_input("عمق الدرج ثابت", value=0.0)
    dr_q = dr_col3.number_input("عدد الأدراج المطلوبة", min_value=0, step=1)

# --- محرك الحسابات الهندسي ---
if st.button("🚀 إصدار بيان التقطيع وفاتورة الخامات", use_container_width=True):
    st.session_state.data_list = []
    
    if W > 0 and H > 0 and D > 0:
        # --- [ أ ] تخصيم الألومنيوم للوحدة الأساسية ---
        h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
        final_h = H - h_ded
        final_w = W - 5
        final_d = D - 5

        if unit_kind == "سفلي":
            # الارتفاع
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "متقارب")
            # العرض
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 3, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 1, "متقارب")
            # العمق
            add_to_bill("ألومنيوم", "رباط عمق", final_d, 2, "مفرد")
            add_to_bill("ألومنيوم", "رباط عمق", final_d, 2, "متقارب")
        else:
            # علوي / خزين / مطبقيه
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "متقارب")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 2, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 2, "متقارب")
            add_to_bill("ألومنيوم", "رباط عمق", final_d, 4, "متقارب")

        # --- [ ب ] تخصيم الفيبر للوحدة الأساسية ---
        add_to_bill("فيبر", "ضهرية الوحدة", f"{final_w} × {final_h}", 1, "حشو")
        add_to_bill("فيبر", "أرضية الوحدة", f"{final_w} × {final_d}", 1, "حشو")
        add_to_bill("فيبر", "أجناب الوحدة", f"{final_h} × {final_d}", 2, "حشو")

        # --- [ ج ] تخصيم الفواصل والأرفف (التعديل الجديد) ---
        if v_q > 0:
            # الألومنيوم (4 قطع لكل رف/فاصل)
            add_to_bill("ألومنيوم", "قائم فاصل / عارضة رف", v_h, v_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "رباط عمق فاصل/رف", v_d, v_q * 2, "مفرد")
            # الفيبر (خصم 5 سم من العرض والعمق)
            f_v_w = v_h - 5
            f_v_d = v_d - 5
            add_to_bill("فيبر", "حشو فاصل / رف", f"{f_v_w} × {f_v_d}", v_q, "خصم 5 سم")

        # --- [ د ] تخصيم الأدراج ---
        if dr_q > 0:
            add_to_bill("ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "جنب درج عمق", dr_d, dr_q * 2, "مفرد")

    # --- عرض النتائج ---
    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        
        st.subheader("📋 شيت التخصيم التفصيلي (جدول العمل)")
        st.table(df) # عرض جدول ثابت سهل القراءة للورشة
        
        # تصدير إكسيل
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل شيت التخصيم (Excel)", csv, "DOGGA_SHEET.csv", "text/csv")
        
        # فاتورة الخامات المجمعة
        st.subheader("🧾 ملخص قائمة الخامات")
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.write("**🔹 الألومنيوم (مفرد/متقارب):**")
            st.dataframe(df[df["الخامة"] == "ألومنيوم"][["اسم القطعة", "المقاس (سم)", "العدد (الكمية)", "نوع التخصيم"]])
        with c_res2:
            st.write("**🔹 الفيبر:**")
            st.dataframe(df[df["الخامة"] == "فيبر"][["اسم القطعة", "المقاس (سم)", "العدد (الكمية)"]])
    else:
        st.error("الرجاء إدخال البيانات الأساسية للبدء.")
