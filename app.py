import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="نظام DOGGA للتخصيم الاحترافي", layout="wide")

st.markdown("""
    <style>
    .main { text-align: right; }
    .stTable { direction: rtl; }
    th { background-color: #1E3A8A !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏭 محرك التخصيم الهندسي (مفرد / متقارب / فيبر)")
st.info("نظام تخصيم الوحدات السفلية، العلوية، دواليب الخزين، والمطبقيات")

# --- دالة إضافة البنود للقائمة ---
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

def add_to_bill(category, item_name, length, qty, unit_type):
    st.session_state.data_list.append({
        "النوع": category,
        "البيان": item_name,
        "المقاس (سم)": round(length, 1) if isinstance(length, (int, float)) else length,
        "العدد": qty,
        "نوع القطاع": unit_type
    })

# --- خانات الإدخال ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
    W = c2.number_input("عرض القطعة (W)", min_value=0.0)
    H = c3.number_input("ارتفاع القطعة (H)", min_value=0.0)
    D = c4.number_input("عمق القطعة (D)", min_value=0.0)

    st.divider()
    
    col_s1, col_s2, col_s3 = st.columns(3)
    s_w = col_s1.number_input("عرض الرف/الفاصل الصافي", value=0.0)
    s_d = col_s2.number_input("عمق الرف/الفاصل الصافي", value=0.0)
    s_q = col_s3.number_input("العدد (رفوف/فواصل)", min_value=0, step=1)

    st.divider()
    
    dr_col1, dr_col2, dr_col3 = st.columns(3)
    dr_w = dr_col1.number_input("عرض الدرج", value=0.0)
    dr_d = dr_col2.number_input("عمق الدرج", value=0.0)
    dr_q = dr_col3.number_input("عدد الأدراج", min_value=0, step=1)

# --- محرك الحسابات ---
if st.button("إصدار الشيت التفصيلي وفاتورة الخامات", use_container_width=True):
    st.session_state.data_list = []
    
    # 1. تخصيم الألوميتال (مفرد ومتقارب)
    if W > 0 and H > 0 and D > 0:
        # تحديد خصم الارتفاع بناء على النوع
        h_deduction = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
        final_h = H - h_deduction
        final_w = W - 5
        final_d = D - 5

        if unit_kind == "سفلي":
            # الارتفاع
            add_to_bill("ألومنيوم", "قائم ارتفاع (مفرد)", final_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع (متقارب)", final_h, 2, "متقارب")
            # العرض
            add_to_bill("ألومنيوم", "عارضة عرض (مفرد)", final_w, 3, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض (متقارب)", final_w, 1, "متقارب")
            # العمق
            add_to_bill("ألومنيوم", "رباط عمق (مفرد)", final_d, 2, "مفرد")
            add_to_bill("ألومنيوم", "رباط عمق (متقارب)", final_d, 2, "متقارب")
        
        else: # باقي الوحدات (علوي، دولاب، مطبقيه)
            add_to_bill("ألومنيوم", "قائم ارتفاع (مفرد)", final_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع (متقارب)", final_h, 2, "متقارب")
            add_to_bill("ألومنيوم", "عارضة عرض (مفرد)", final_w, 2, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض (متقارب)", final_w, 2, "متقارب")
            add_to_bill("ألومنيوم", "رباط عمق (متقارب)", final_d, 4, "متقارب")

        # 2. تخصيم الفيبر (حسب القواعد المطلوبة)
        add_to_bill("فيبر", "ظهرية", f"{final_w} × {final_h}", 1, "فيبر")
        add_to_bill("فيبر", "أرضية", f"{final_w} × {final_d}", 1, "فيبر")
        add_to_bill("فيبر", "أجناب", f"{final_h} × {final_d}", 2, "فيبر")

        # 3. الرفوف والفواصل
        if s_q > 0:
            # ألومنيوم: الرف الواحد يحتاج 4 قطع
            add_to_bill("ألومنيوم", "رف/فاصل (عرض)", s_w, s_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "رف/فاصل (عمق)", s_d, s_q * 2, "مفرد")
            # فيبر: نشيل 5 سم من العرض والعمق
            add_to_bill("فيبر", "حشو رف/فاصل", f"{s_w-5} × {s_d-5}", s_q, "فيبر")

        # 4. الأدراج
        if dr_q > 0:
            add_to_bill("ألومنيوم", "درج (عرض - خصم 2.5)", dr_w - 2.5, dr_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "درج (عمق ثابت)", dr_d, dr_q * 2, "مفرد")

    # --- عرض النتائج في جداول ---
    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        
        st.subheader("📋 شيت التفصيل النهائي (Excel View)")
        st.dataframe(df, use_container_width=True)
        
        # تقسيم الفاتورة لتسهيل التجميع
        st.subheader("🧾 قائمة الفاتورة وتجميع الخامات")
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("**🔹 قطع الألومنيوم المطلوبة:**")
            aluminum_df = df[df["النوع"] == "ألومنيوم"]
            st.table(aluminum_df[["البيان", "المقاس (سم)", "العدد", "نوع القطاع"]])
            
        with col_res2:
            st.markdown("**🔹 قطع الفيبر المطلوبة:**")
            fiber_df = df[df["النوع"] == "فيبر"]
            st.table(fiber_df[["البيان", "المقاس (سم)", "العدد"]])

        # زر التحميل
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل شيت التخصيم (Excel/CSV)", csv, "DOGGA_Deduction.csv", "text/csv")
    else:
        st.warning("برجاء إدخال المقاسات الأساسية")
