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

st.title("🏭 نظام DOGGA للهندسة والتخصيم (إصدار الفواصل والأرفف المنفصلة)")
st.info("تخصيم احترافي: (مفرد / متقارب) + فيبر + فواصل وأرفف منفصلة تماماً")

# --- إدارة حالة البيانات ---
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": round(length, 1) if isinstance(length, (int, float)) else length,
        "العدد (Qty)": qty,
        "نوع التخصيم": unit_type
    })

# --- واجهة إدخال البيانات ---
with st.container():
    st.subheader("📏 1. أبعاد الوحدة الأساسية")
    c1, c2, c3, c4 = st.columns(4)
    unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
    W = c2.number_input("عرض القطعة الكلي (W)", min_value=0.0, key="main_w")
    H = c3.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0, key="main_h")
    D = c4.number_input("عمق القطعة الكلي (D)", min_value=0.0, key="main_d")

    st.divider()
    
    # قسم الأرفف المنفصل
    st.subheader("📚 2. الأرفف (منفصلة)")
    col_s1, col_s2, col_s3 = st.columns(3)
    s_w_input = col_s1.number_input("عرض الرف الصافي", value=0.0, key="shelf_w")
    s_d_input = col_s2.number_input("عمق الرف الصافي", value=0.0, key="shelf_d")
    s_q_input = col_s3.number_input("عدد الأرفف", min_value=0, step=1, key="shelf_q")

    st.divider()

    # قسم الفواصل المنفصل
    st.subheader("🧱 3. الفواصل (منفصلة)")
    col_v1, col_v2, col_v3 = st.columns(3)
    v_h_input = col_v1.number_input("ارتفاع الفاصل الصافي", value=0.0, key="divider_h")
    v_d_input = col_v2.number_input("عمق الفاصل الصافي", value=0.0, key="divider_d")
    v_q_input = col_v3.number_input("عدد الفواصل", min_value=0, step=1, key="divider_q")

    st.divider()
    
    st.subheader("🗄️ 4. الأدراج")
    dr_col1, dr_col2, dr_col3 = st.columns(3)
    dr_w_input = dr_col1.number_input("عرض الدرج", value=0.0, key="drawer_w")
    dr_d_input = dr_col2.number_input("عمق الدرج ثابت", value=0.0, key="drawer_d")
    dr_q_input = dr_col3.number_input("عدد الأدراج", min_value=0, step=1, key="drawer_q")

# --- محرك الحسابات الهندسي ---
if st.button("🚀 إصدار بيان التقطيع وفاتورة الخامات النهائية", use_container_width=True):
    st.session_state.data_list = []
    
    if W > 0 and H > 0 and D > 0:
        # --- [ أ ] تخصيم الألومنيوم للوحدة الأساسية ---
        h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
        final_h = H - h_ded
        final_w = W - 5
        final_d = D - 5

        if unit_kind == "سفلي":
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "متقارب")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 3, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 1, "متقارب")
            add_to_bill("ألومنيوم", "رباط عمق", final_d, 2, "مفرد")
            add_to_bill("ألومنيوم", "رباط عمق", final_d, 2, "متقارب")
        else:
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع", final_h, 2, "متقارب")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 2, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض", final_w, 2, "متقارب")
            add_to_bill("ألومنيوم", "رباط عمق", final_d, 4, "متقارب")

        # --- [ ب ] تخصيم الفيبر للوحدة الأساسية ---
        add_to_bill("فيبر", "ضهرية الوحدة", f"{final_w} × {final_h}", 1, "حشو")
        add_to_bill("فيبر", "أرضية الوحدة", f"{final_w} × {final_d}", 1, "حشو")
        add_to_bill("فيبر", "أجناب الوحدة", f"{final_h} × {final_d}", 2, "حشو")

        # --- [ ج ] تخصيم الأرفف (منفصل) ---
        if s_q_input > 0:
            add_to_bill("ألومنيوم", "عرض الرف", s_w_input, s_q_input * 2, "مفرد")
            add_to_bill("ألومنيوم", "عمق الرف", s_d_input, s_q_input * 2, "مفرد")
            add_to_bill("فيبر", "حشو رف", f"{s_w_input-5} × {s_d_input-5}", s_q_input, "خصم 5 سم")

        # --- [ د ] تخصيم الفواصل (منفصل) ---
        if v_q_input > 0:
            add_to_bill("ألومنيوم", "ارتفاع فاصل", v_h_input, v_q_input * 2, "مفرد")
            add_to_bill("ألومنيوم", "عمق فاصل", v_d_input, v_q_input * 2, "مفرد")
            add_to_bill("فيبر", "حشو فاصل", f"{v_h_input-5} × {v_d_input-5}", v_q_input, "خصم 5 سم")

        # --- [ هـ ] تخصيم الأدراج ---
        if dr_q_input > 0:
            add_to_bill("ألومنيوم", "وش/ضهر درج", dr_w_input - 2.5, dr_q_input * 2, "مفرد")
            add_to_bill("ألومنيوم", "جنب درج عمق", dr_d_input, dr_q_input * 2, "مفرد")

    # --- عرض النتائج في جداول احترافية ---
    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        
        st.subheader("📋 شيت التخصيم الكامل لورشة DED EL KASR")
        st.table(df)
        
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل شيت التخصيم (Excel/CSV)", csv, "DOGGA_SHEET_FULL.csv", "text/csv")
    else:
        st.error("الرجاء إدخال البيانات الأساسية.")
