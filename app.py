import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة DOGGA SYSTEM
st.set_page_config(page_title="DOGGA SYSTEM - إدارة مشروعات الألوميتال", layout="wide")

# 2. تهيئة مخزن بيانات المشروع
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'deduction'

# دالة إضافة البنود
def add_to_project(unit_name, category, item_name, length, qty, unit_type="-"):
    st.session_state.project_data.append({
        "اسم الوحدة": unit_name,
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# ==========================================
# الصفحة الأولى: إضافة الوحدات (التخصيم)
# ==========================================
if st.session_state.page == 'deduction':
    st.title("🏗️ بناء مشروع متكامل - ورشة DED EL KASR")
    
    with st.form("unit_form", clear_on_submit=True):
        st.subheader("➕ إضافة وحدة جديدة")
        
        c_name, c_kind = st.columns(2)
        u_label = c_name.text_input("📝 اسم الوحدة", placeholder="مثلاً: مطبخ سفلي")
        u_kind = c_kind.selectbox("🛠️ نوع التخصيم", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        c1, c2, c3 = st.columns(3)
        W = c1.number_input("عرض الوحدة الكلي (W)", min_value=0.0)
        H = c2.number_input("ارتفاع الوحدة الكلي (H)", min_value=0.0)
        D = c3.number_input("عمق الوحدة الكلي (D)", min_value=0.0)

        st.divider()
        st.write("📦 مدخلات إضافية لهذه الوحدة:")
        
        # الأرفف والفواصل والأدراج
        col_s1, col_s2, col_s3 = st.columns(3)
        s_w = col_s1.number_input("عرض الرف", value=0.0)
        s_d = col_s2.number_input("عمق الرف", value=0.0)
        s_q = col_s3.number_input("عدد الأرفف", min_value=0, step=1)

        col_v1, col_v2, col_v3 = st.columns(3)
        v_h = col_v1.number_input("ارتفاع الفاصل", value=0.0)
        v_d = col_v2.number_input("عمق الفاصل", value=0.0)
        v_q = col_v3.number_input("عدد الفواصل", min_value=0, step=1)

        col_dr1, col_dr2, col_dr3 = st.columns(3)
        dr_w = col_dr1.number_input("عرض الدرج", value=0.0)
        dr_d = col_dr2.number_input("عمق الدرج", value=0.0)
        dr_q = col_dr3.number_input("عدد الأدراج", min_value=0, step=1)

        submit_btn = st.form_submit_button("✅ إضافة هذه الوحدة للمشروع")

    if submit_btn:
        if W > 0 and H > 0:
            current_label = u_label if u_label else f"وحدة {u_kind}"
            
            # التخصيم الأساسي
            h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            if u_kind == "سفلي":
                add_to_project(current_label, "ألومنيوم", "قائم", f_h, 4, "مفرد")
                add_to_project(current_label, "ألومنيوم", "عارضة", f_w, 4, "مفرد")
                add_to_project(current_label, "ألومنيوم", "رباط", f_d, 4, "مفرد")
            else:
                add_to_project(current_label, "ألومنيوم", "قائم", f_h, 4, "مفرد")
                add_to_project(current_label, "ألومنيوم", "عارضة", f_w, 4, "مفرد")
                add_to_project(current_label, "ألومنيوم", "رباط", f_d, 4, "مفرد")

            add_to_project(current_label, "فيبر", "حشو", f"{f_w}×{f_h}", 1)

            # الأرفف والفواصل
            if s_q > 0:
                add_to_project(current_label, "ألومنيوم", "رف", s_w, s_q*2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "رف", s_d, s_q*2, "مفرد")
            if v_q > 0:
                add_to_project(current_label, "ألومنيوم", "فاصل", v_h, v_q*2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "فاصل", v_d, v_q*2, "مفرد")

            # الأدراج (المسمى المعدل: علبه درج)
            if dr_q > 0:
                add_to_project(current_label, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "علبه درج")
                add_to_project(current_label, "ألومنيوم", "جنب درج", dr_d, dr_q * 2, "علبه درج")

            st.success(f"تمت إضافة '{current_label}'")

    if st.session_state.project_data:
        st.divider()
        full_df = pd.DataFrame(st.session_state.project_data)
        for name, group in full_df.groupby("اسم الوحدة"):
            st.markdown(f"#### 📍 {name}")
            st.table(group.drop(columns=["اسم الوحدة"]))

        if st.button("💰 الانتقال لحساب الخامات والتسعير ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: استهلاك الخامات والفاتورة المفتوحة
# ==========================================
elif st.session_state.page == 'inventory':
    st.title("📊 تقرير الخامات والتسعير - DOGGA SYSTEM")
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum_df = df[df["الخامة"] == "ألومنيوم"].copy()
        alum_df["المقاس (سم)"] = pd.to_numeric(alum_df["المقاس (سم)"], errors='coerce')

        # 1. حساب الأعواد (بما فيها علبه درج)
        st.subheader("🥢 تقدير أعواد الألومنيوم")
        summary_alum = alum_df.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="الإجمالي (سم)")
        summary_alum["عدد الأعواد (6م)"] = summary_alum["الإجمالي (سم)"].apply(lambda x: math.ceil(x / 600))
        st.table(summary_alum)

        # 2. حساب الفيبر
        fiber_df = df[df["الخامة"] == "فيبر"]
        total_area = 0
        for _, row in fiber_df.iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2: total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
        sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر", f"{sheets} لوح")

        st.divider()

        # 3. جدول حساب الخامات (خانات مفتوحة للإضافة)
        st.subheader("💵 فاتورة المشتريات (يمكنك إضافة أصناف يدوياً)")
        st.info("💡 اضغط على الزر (+) أسفل الجدول لإضافة مقابض، مفصلات، أو أي خامة أخرى.")
        
        # تحضير البيانات الأساسية للفاتورة
        base_bill = []
        for _, r in summary_alum.iterrows():
            base_bill.append({"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["عدد الأعواد (6م)"], "السعر": 0.0})
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})

        # الجدول التفاعلي (num_rows="dynamic" يسمح بإضافة أسطر)
        final_bill = st.data_editor(
            pd.DataFrame(base_bill),
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "السعر": st.column_config.NumberColumn("السعر (ج.م)", min_value=0),
                "الكمية": st.column_config.NumberColumn("الكمية", min_value=0)
            }
        )

        total_sum = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.header(f"💰 التكلفة الإجمالية: {total_sum:,.2f} ج.م")

        if st.button("⬅️ العودة لإضافة وحدات"):
            st.session_state.page = 'deduction'
            st.rerun()
            # --- تابع الصفحة الثانية (inventory) ---
        
        st.divider()
        
        # عرض إجمالي الأمتار الطولية للتوضيح (قبل تحويلها لأعواد)
        with st.expander("🔍 تفاصيل الأطوال الكلية للمشروع"):
            st.dataframe(summary_alum, use_container_width=True)

        # أزرار الإجراءات النهائية
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        
        with c_inv1:
            if st.button("⬅️ العودة لإضافة وحدات", use_container_width=True):
                st.session_state.page = 'deduction'
                st.rerun()
                
        with c_inv2:
            # زر لتحميل الفاتورة كملف CSV
            csv_data = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 تحميل الفاتورة (Excel)",
                data=csv_data,
                file_name="DOGGA_Final_Bill.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with c_inv3:
            if st.button("🗑️ إفراغ المشروع تماماً", use_container_width=True):
                st.session_state.project_data = []
                st.session_state.page = 'deduction'
                st.rerun()

    else:
        # رسالة في حالة محاولة دخول الصفحة بدون بيانات
        st.warning("⚠️ لا توجد بيانات في المشروع حالياً. يرجى إضافة وحدات أولاً من صفحة التخصيم.")
        if st.button("الذهاب لصفحة التخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()

# --- نهاية كود DOGGA SYSTEM ---
