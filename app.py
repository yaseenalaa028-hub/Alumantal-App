import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (DOGGA SYSTEM)
st.set_page_config(page_title="DOGGA SYSTEM - التخصيم والتسعير", layout="wide")

# 2. نظام التنقل بين الصفحات والحالة
if 'page' not in st.session_state:
    st.session_state.page = 'deduction'
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

# --- دالة إضافة البنود للقائمة ---
def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": round(length, 1) if isinstance(length, (int, float)) else length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# ==========================================
# الصفحة الأولى: التخصيم (Deduction)
# ==========================================
if st.session_state.page == 'deduction':
    st.title("🏭 نظام DOGGA للتخصيم الهندسي")
    st.info("تخصيم (مفرد/متقارب) لورشة DED EL KASR")

    # مدخلات المقاسات
    with st.container():
        st.subheader("📏 أبعاد الوحدة")
        c1, c2, c3, c4 = st.columns(4)
        unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
        W = c2.number_input("عرض القطعة الكلي (W)", min_value=0.0)
        H = c3.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0)
        D = c4.number_input("عمق القطعة الكلي (D)", min_value=0.0)

    st.divider()

    # الرفوف والفواصل
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    s_w = col_s1.number_input("عرض الرف", value=0.0)
    s_d = col_s2.number_input("عمق الرف", value=0.0)
    s_q = col_s3.number_input("عدد الرفوف", min_value=0)
    
    st.divider()
    
    col_v1, col_v2, col_v3 = st.columns(3)
    v_h = col_v1.number_input("ارتفاع الفاصل", value=0.0)
    v_d = col_v2.number_input("عمق الفاصل", value=0.0)
    v_q = col_v3.number_input("عدد الفواصل", min_value=0)

    # زر الحساب
    if st.button("🚀 تشغيل التخصيم", use_container_width=True):
        st.session_state.data_list = [] # تصوير قائمة جديدة
        
        if W > 0 and H > 0 and D > 0:
            # معادلات التخصيم (قواعد ورشة DED EL KASR)
            h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            # إضافة الألومنيوم
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

            # إضافة الفيبر
            add_to_bill("فيبر", "ضهرية", f"{f_w} × {f_h}", 1, "فيبر")
            add_to_bill("فيبر", "أرضية", f"{f_w} × {f_d}", 1, "فيبر")
            add_to_bill("فيبر", "أجناب", f"{f_h} × {f_d}", 2, "فيبر")

            # الرفوف والفواصل
            if s_q > 0:
                add_to_bill("ألومنيوم", "عرض الرف", s_w, s_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "عمق الرف", s_d, s_q * 2, "مفرد")
                add_to_bill("فيبر", "حشو رف", f"{s_w-5} × {s_d-5}", s_q, "فيبر")
            
            if v_q > 0:
                add_to_bill("ألومنيوم", "ارتفاع فاصل", v_h, v_q * 2, "مفرد")
                add_to_bill("ألومنيوم", "عمق فاصل", v_d, v_q * 2, "مفرد")
                add_to_bill("فيبر", "حشو فاصل", f"{v_h-5} × {v_d-5}", v_q, "فيبر")

    # عرض النتائج وزر الانتقال
    if st.session_state.data_list:
        df_full = pd.DataFrame(st.session_state.data_list)
        st.subheader("🟦 جدول الألومنيوم")
        st.table(df_full[df_full["الخامة"] == "ألومنيوم"])
        st.subheader("⬜ جدول الفيبر")
        st.table(df_full[df_full["الخامة"] == "فيبر"])
        
        st.divider()
        if st.button("💰 الانتقال لتسعير الفاتورة ⬅️", use_container_width=True):
            st.session_state.page = 'billing'
            st.rerun()

# ==========================================
# الصفحة الثانية: فاتورة الأسعار (Billing)
# ==========================================
elif st.session_state.page == 'billing':
    st.title("🧾 فاتورة بيان الأسعار - Excel Mode")
    st.info("قم بتعديل عمود 'سعر الوحدة' لحساب التكلفة الإجمالية")

    if st.session_state.data_list:
        df_bill = pd.DataFrame(st.session_state.data_list)
        if "سعر الوحدة" not in df_bill.columns:
            df_bill["سعر الوحدة"] = 0.0

        # الجدول التفاعلي (إكسيل داخل التطبيق)
        edited_df = st.data_editor(
            df_bill,
            column_config={
                "سعر الوحدة": st.column_config.NumberColumn("السعر (ج.م)", min_value=0),
                "العدد": st.column_config.NumberColumn(disabled=True),
                "اسم القطعة": st.column_config.TextColumn(disabled=True),
                "الخامة": st.column_config.TextColumn(disabled=True)
            },
            use_container_width=True
        )

        # حساب الإجمالي
        def calc_total(row):
            try:
                # محاولة تحويل المقاس لرقم للضرب (للألومنيوم)، لو فيبر استخدم العدد فقط
                val = float(row["المقاس (سم)"]) if isinstance(row["المقاس (سم)"], (int, float)) else 1
                return val * row["العدد"] * row["سعر الوحدة"]
            except:
                return row["العدد"] * row["سعر الوحدة"]

        edited_df["الإجمالي"] = edited_df.apply(calc_total, axis=1)
        st.header(f"💵 الإجمالي الكلي: {edited_df['الإجمالي'].sum():,.2f} ج.م")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅️ العودة للتخصيم"):
                st.session_state.page = 'deduction'
                st.rerun()
        with c2:
            csv = edited_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل الفاتورة (Excel)", csv, "DOGGA_Invoice.csv", "text/csv")
    else:
        st.warning("لا توجد بيانات، ارجع لصفحة التخصيم أولاً.")
        if st.button("العودة للتخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
