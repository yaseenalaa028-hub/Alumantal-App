import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="DOGGA SYSTEM - حساب الخامات", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'deduction'
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

# --- دالة إضافة البنود ---
def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# ==========================================
# الصفحة الأولى: التخصيم والحسابات الفنية
# ==========================================
if st.session_state.page == 'deduction':
    st.title("🏭 محرك التخصيم واستهلاك الخامات")
    
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين"])
        W, H, D = c2.number_input("العرض (W)"), c3.number_input("الارتفاع (H)"), c4.number_input("العمق (D)")

    if st.button("🚀 تشغيل التخصيم وحساب الهالك", use_container_width=True):
        st.session_state.data_list = []
        if W > 0 and H > 0 and D > 0:
            h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            # ألومنيوم (مفرد ومتقارب)
            if unit_kind == "سفلي":
                add_to_bill("ألومنيوم", "قائم (مفرد)", f_h, 2, "مفرد")
                add_to_bill("ألومنيوم", "قائم (متقارب)", f_h, 2, "متقارب")
                add_to_bill("ألومنيوم", "عارضة (مفرد)", f_w, 3, "مفرد")
                add_to_bill("ألومنيوم", "عارضة (متقارب)", f_w, 1, "متقارب")
                add_to_bill("ألومنيوم", "رباط (مفرد)", f_d, 2, "مفرد")
                add_to_bill("ألومنيوم", "رباط (متقارب)", f_d, 2, "متقارب")
            else:
                add_to_bill("ألومنيوم", "قائم (مفرد)", f_h, 2, "مفرد")
                add_to_bill("ألومنيوم", "قائم (متقارب)", f_h, 2, "متقارب")
                add_to_bill("ألومنيوم", "عارضة (مفرد)", f_w, 2, "مفرد")
                add_to_bill("ألومنيوم", "عارضة (متقارب)", f_w, 2, "متقارب")
                add_to_bill("ألومنيوم", "رباط (متقارب)", f_d, 4, "متقارب")

            # فيبر (مساحات)
            add_to_bill("فيبر", "ظهرية", f"{f_w}×{f_h}", 1)
            add_to_bill("فيبر", "أرضية", f"{f_w}×{f_d}", 1)
            add_to_bill("فيبر", "أجناب", f"{f_h}×{f_d}", 2)

    if st.session_state.data_list:
        st.subheader("📋 نتائج التخصيم")
        df = pd.DataFrame(st.session_state.data_list)
        st.dataframe(df, use_container_width=True)
        
        if st.button("💰 الانتقال لحساب الأعواد والواح الفيبر ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: حساب الاستهلاك الفعلي (الأعواد والواح الفيبر)
# ==========================================
elif st.session_state.page == 'inventory':
    st.title("📦 حساب استهلاك الأعواد والواح الفيبر")
    
    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        alum_df = df[df["الخامة"] == "ألومنيوم"].copy()
        fiber_df = df[df["الخامة"] == "فيبر"].copy()

        # --- 1. حساب أعواد الألومنيوم (6 متر) ---
        st.subheader("🥢 استهلاك أعواد الألومنيوم (العود = 600 سم)")
        
        # تجميع الأطوال حسب نوع القطاع (مفرد / متقارب)
        summary_alum = alum_df.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="إجمالي الأطوال (سم)")
        
        summary_alum["عدد الأعواد (تقريبي)"] = summary_alum["إجمالي الأطوال (سم)"].apply(lambda x: math.ceil(x / 600))
        
        st.table(summary_alum)

        # --- 2. حساب الواح الفيبر (280 × 130) ---
        st.subheader("🖼️ استهلاك الواح الفيبر (اللوح = 280 × 130 سم)")
        
        total_fiber_area = 0
        for idx, row in fiber_df.iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            area = float(dims[0]) * float(dims[1]) * row["العدد"]
            total_fiber_area += area
        
        sheet_area = 280 * 130  # مساحة اللوح الواحد بالسم مربع
        needed_sheets = math.ceil(total_fiber_area / sheet_area)
        
        col_f1, col_f2 = st.columns(2)
        col_f1.metric("إجمالي مساحة الفيبر المطلوبة", f"{total_fiber_area:,.0f} سم²")
        col_f2.metric("عدد ألواح الفيبر المطلوبة", f"{needed_sheets} لوح")

        # --- 3. جدول الأسعار النهائي ---
        st.divider()
        st.subheader("💵 بيان أسعار الخامات")
        
        # تحضير جدول للفاتورة
        invoice_data = []
        for index, row in summary_alum.iterrows():
            invoice_data.append({"الصنف": f"ألومنيوم {row['نوع التخصيم']}", "الكمية": row["عدد الأعواد (تقريبي)"], "وحدة القياس": "عود (6م)", "السعر": 0.0})
        
        invoice_data.append({"الصنف": "لوح فيبر (280×130)", "الكمية": needed_sheets, "وحدة القياس": "لوح", "السعر": 0.0})
        
        final_bill = st.data_editor(pd.DataFrame(invoice_data), use_container_width=True)
        
        total_cost = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.header(f"💰 إجمالي التكلفة: {total_cost:,.2f} ج.م")

        if st.button("⬅️ العودة للتخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
    else:
        st.warning("لا توجد بيانات!") 
# --- كود صفحة حساب الاستهلاك (توضع بعد كود صفحة التخصيم) ---

elif st.session_state.page == 'inventory':
    st.title("📦 حساب أمتار الأعواد وألواح الفيبر - DOGGA SYSTEM")
    st.info("هذه الصفحة تحول المقاسات المقطوعة إلى خامات صحيحة (أعواد وألواح)")

    if st.session_state.data_list:
        df = pd.DataFrame(st.session_state.data_list)
        
        # --- 1. حساب الألومنيوم (مفرد ومتقارب) ---
        st.subheader("🥢 تقدير أعواد الألومنيوم (العود = 6 متر)")
        
        # تصفية الألومنيوم فقط
        alum_df = df[df["الخامة"] == "ألومنيوم"].copy()
        
        # تجميع الأطوال الكلية لكل نوع
        alum_summary = alum_df.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="إجمالي السنتيمترات")

        # حساب عدد الأعواد (600 سم لكل عود) مع إضافة 5% هالك تقطيع
        alum_summary["عدد الأعواد (6م)"] = alum_summary["إجمالي السنتيمترات"].apply(
            lambda x: math.ceil((x * 1.05) / 600) 
        )

        st.table(alum_summary)

        # --- 2. حساب الفيبر (لوح 280 × 130) ---
        st.subheader("🖼️ تقدير ألواح الفيبر (اللوح = 280 × 130)")
        
        fiber_df = df[df["الخامة"] == "فيبر"].copy()
        total_fiber_area = 0

        for _, row in fiber_df.iterrows():
            # فك النص (مثلاً 195×77) لعمل عملية حسابية للمساحة
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                area = float(dims[0]) * float(dims[1]) * row["العدد"]
                total_fiber_area += area
        
        # مساحة اللوح الواحد بالسم2 = 36,400
        sheet_area = 280 * 130
        needed_sheets = math.ceil(total_fiber_area / sheet_area)

        c1, c2 = st.columns(2)
        c1.metric("إجمالي مساحة الحشو المطلوبة", f"{total_fiber_area:,.0f} سم²")
        c2.metric("عدد ألواح الفيبر المطلوبة", f"{needed_sheets} لوح")

        st.divider()

        # --- 3. فاتورة الأسعار النهائية (بناءً على الأعواد والألواح) ---
        st.subheader("💰 بيان أسعار المشتريات")
        
        # تجهيز جدول الفاتورة للمستخدم
        invoice_items = []
        for _, row in alum_summary.iterrows():
            invoice_items.append({
                "الصنف": f"ألومنيوم - {row['نوع التخصيم']}",
                "الكمية المطلوبة": row["عدد الأعواد (6م)"],
                "وحدة القياس": "عود 6م",
                "سعر الوحدة": 0.0
            })
        
        invoice_items.append({
            "الصنف": "لوح فيبر (280×130)",
            "الكمية المطلوبة": needed_sheets,
            "وحدة القياس": "لوح كامل",
            "سعر الوحدة": 0.0
        })

        # جدول إيديتور لكتابة السعر
        final_invoice = st.data_editor(
            pd.DataFrame(invoice_items),
            use_container_width=True,
            column_config={"سعر الوحدة": st.column_config.NumberColumn("السعر (ج.م)", min_value=0)}
        )

        total_final = (final_invoice["الكمية المطلوبة"] * final_invoice["سعر الوحدة"]).sum()
        st.subheader(f"💵 إجمالي مبلغ الشراء: {total_final:,.2f} ج.م")

        # أزرار التنقل
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("⬅️ العودة لتعديل التخصيم"):
                st.session_state.page = 'deduction'
                st.rerun()
        with col_btn2:
            # تصدير فاتورة المشتريات
            csv_inv = final_invoice.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل فاتورة المشتريات (Excel)", csv_inv, "DOGGA_Purchase_Order.csv", "text/csv")
    else:
        st.warning("برجاء إجراء التخصيم أولاً في الصفحة السابقة.")
        if st.button("الذهاب للتخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
