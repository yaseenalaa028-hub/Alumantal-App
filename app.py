import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة DOGGA SYSTEM
st.set_page_config(page_title="DOGGA SYSTEM - التخصيم والاستهلاك", layout="wide")

# 2. نظام التنقل والحالة
if 'page' not in st.session_state:
    st.session_state.page = 'deduction'
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# ==========================================
# الصفحة الأولى: صفحة التخصيم والمدخلات
# ==========================================
if st.session_state.page == 'deduction':
    st.title("🏭 نظام DOGGA للتخصيم الهندسي - DED EL KASR")
    
    with st.container():
        st.subheader("📏 1. أبعاد الوحدة الأساسية")
        c1, c2, c3, c4 = st.columns(4)
        unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
        W = c2.number_input("عرض القطعة الكلي (W)", min_value=0.0)
        H = c3.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0)
        D = c4.number_input("عمق القطعة الكلي (D)", min_value=0.0)

    st.divider()
    
    st.subheader("📚 2. الأرفف والفواصل")
    col_s1, col_s2, col_s3 = st.columns(3)
    s_w = col_s1.number_input("عرض الرف", value=0.0)
    s_d = col_s2.number_input("عمق الرف", value=0.0)
    s_q = col_s3.number_input("عدد الأرفف", min_value=0)
    
    col_v1, col_v2, col_v3 = st.columns(3)
    v_h = col_v1.number_input("ارتفاع الفاصل", value=0.0)
    v_d = col_v2.number_input("عمق الفاصل", value=0.0)
    v_q = col_v3.number_input("عدد الفواصل", min_value=0)

    st.divider()
    
    st.subheader("🗄️ 3. الأدراج")
    col_dr1, col_dr2, col_dr3 = st.columns(3)
    dr_w = col_dr1.number_input("عرض الدرج الصافي", value=0.0)
    dr_d = col_dr2.number_input("عمق الدرج", value=0.0)
    dr_q = col_dr3.number_input("عدد الأدراج", min_value=0)

    if st.button("🚀 تشغيل التخصيم وحساب الهالك", use_container_width=True):
        st.session_state.data_list = []
        if W > 0 and H > 0 and D > 0:
            # تخصيم الوحدة
            h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            # الألومنيوم الأساسي
            if unit_kind == "سفلي":
                add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_bill("ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
                add_to_bill("ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
                add_to_bill("ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
                add_to_bill("ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
            else:
                add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_bill("ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
                add_to_bill("ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
                add_to_bill("ألومنيوم", "رباط عمق", f_d, 4, "متقارب")

            # فيبر الوحدة
            add_to_bill("فيبر", "ضهرية", f"{f_w}×{f_h}", 1)
            add_to_bill("فيبر", "أرضية", f"{f_w}×{f_d}", 1)
            add_to_bill("فيبر", "أجناب", f"{f_h}×{f_d}", 2)

            # الرفوف
            if s_q > 0:
                add_to_bill("ألومنيوم", "عرض رف", s_w, s_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "عمق رف", s_d, s_q * 2, "مفرد")
                add_to_bill("فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q)

            # الفواصل
            if v_q > 0:
                add_to_bill("ألومنيوم", "ارتفاع فاصل", v_h, v_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "عمق فاصل", v_d, v_q * 2, "مفرد")
                add_to_bill("فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q)

            # الأدراج
            if dr_q > 0:
                add_to_bill("ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "جنب درج", dr_d, dr_q * 2, "مفرد")

    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        st.subheader("🟦 جداول التخصيم")
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        if st.button("💰 حساب الأعواد والفيبر والتسعير ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: حساب الاستهلاك والفاتورة
# ==========================================
elif st.session_state.page == 'inventory':
    st.title("📦 حساب استهلاك الخامات والفاتورة")
    
    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        alum_df = df[df["الخامة"] == "ألومنيوم"].copy()
        fiber_df = df[df["الخامة"] == "فيبر"].copy()

        # 1. حساب الأعواد 6 متر
        st.subheader("🥢 استهلاك الألومنيوم (العود 600 سم)")
        summary_alum = alum_df.groupby("نوع التخصيم").apply(
            lambda x: (pd.to_numeric(x["المقاس (سم)"], errors='coerce') * x["العدد"]).sum()
        ).reset_index(name="إجمالي الطول")
        summary_alum["عدد الأعواد"] = summary_alum["إجمالي الطول"].apply(lambda x: math.ceil(x / 600))
        st.table(summary_alum)

        # 2. حساب ألواح الفيبر 280×130
        st.subheader("🖼️ استهلاك الفيبر (اللوح 280×130)")
        total_area = 0
        for _, row in fiber_df.iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
        
        needed_sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة", f"{needed_sheets} لوح")

        st.divider()
        st.subheader("💵 فاتورة المشتريات (اكتب السعر يدوي)")
        
        # تجهيز بيانات الفاتورة
        inv_data = []
        for _, r in summary_alum.iterrows():
            inv_data.append({"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["عدد الأعواد"], "وحدة": "عود", "السعر": 0.0})
        inv_data.append({"الصنف": "لوح فيبر 280×130", "الكمية": needed_sheets, "وحدة": "لوح", "السعر": 0.0})
        
        edited_bill = st.data_editor(pd.DataFrame(inv_data), use_container_width=True)
        total_price = (edited_bill["الكمية"] * edited_bill["السعر"]).sum()
        st.header(f"💰 الإجمالي: {total_price:,.2f} ج.م")

        if st.button("⬅️ العودة للتخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
    else:
        st.warning("ارجع للتخصيم أولاً")
        if st.button("العودة"):
            st.session_state.page = 'deduction'
            st.rerun()
            # --- [ج] حسابات الأرفف (لو العدد أكبر من صفر) ---
            if s_q > 0:
                # الرف بيحتاج 2 عرض و 2 عمق (برواز مفرد)
                add_to_bill("ألومنيوم", "عرض رف", s_w, s_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "عمق رف", s_d, s_q * 2, "مفرد")
                # الفيبر بيخصم 5 سم من الطول والعرض
                if s_w > 5 and s_d > 5:
                    add_to_bill("فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "حشو رف")

            # --- [د] حسابات الفواصل (لو العدد أكبر من صفر) ---
            if v_q > 0:
                # الفاصل بيحتاج 2 ارتفاع و 2 عمق
                add_to_bill("ألومنيوم", "ارتفاع فاصل", v_h, v_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "عمق فاصل", v_d, v_q * 2, "مفرد")
                # الفيبر بيخصم 5 سم من الطول والعرض
                if v_h > 5 and v_d > 5:
                    add_to_bill("فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "حشو فاصل")

            # --- [هـ] حسابات الأدراج (تخصيم الورشة 2.5 سم) ---
            if dr_q > 0:
                # وش وضهر الدرج بيتخصم منهم 2.5 سم
                add_to_bill("ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "مفرد")
                # الجنب بيفضل زي ما هو (العمق الثابت)
                add_to_bill("ألومنيوم", "جنب درج", dr_d, dr_q * 2, "مفرد")
                # حشو أرضية الدرج (اختياري حسب رغبتك)
                add_to_bill("فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "حشو درج")
