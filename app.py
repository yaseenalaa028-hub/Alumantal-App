import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة DOGGA SYSTEM
st.set_page_config(page_title="DOGGA SYSTEM - إدارة مشروعات الألوميتال", layout="wide")

# 2. تهيئة مخزن بيانات المشروع (session_state)
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] # لتخزين كل الوحدات المضافة
if 'page' not in st.session_state:
    st.session_state.page = 'deduction'

# دالة إضافة البنود مع اسم الوحدة المخصص لها
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
    st.info("قم بإضافة الوحدات واحدة تلو الأخرى، وسيتم تجميعها تلقائياً في فاتورة واحدة.")

    # --- نموذج إدخال الوحدة ---
    with st.form("unit_form", clear_on_submit=True):
        st.subheader("➕ إضافة وحدة جديدة")
        
        c_name, c_kind = st.columns(2)
        u_label = c_name.text_input("📝 اسم الوحدة (مثلاً: سفلي حوض / علوي يمين)", placeholder="وحدة رقم 1")
        u_kind = c_kind.selectbox("🛠️ نوع التخصيم", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        c1, c2, c3 = st.columns(3)
        W = c1.number_input("عرض الوحدة الكلي (W)", min_value=0.0)
        H = c2.number_input("ارتفاع الوحدة الكلي (H)", min_value=0.0)
        D = c3.number_input("عمق الوحدة الكلي (D)", min_value=0.0)

        st.divider()
        st.write("📦 أرفف وفواصل وأدراج لهذه الوحدة:")
        
        # الأرفف
        col_s1, col_s2, col_s3 = st.columns(3)
        s_w = col_s1.number_input("عرض الرف الصافي", value=0.0)
        s_d = col_s2.number_input("عمق الرف الصافي", value=0.0)
        s_q = col_s3.number_input("عدد الأرفف", min_value=0, step=1)

        # الفواصل
        col_v1, col_v2, col_v3 = st.columns(3)
        v_h = col_v1.number_input("ارتفاع الفاصل الصافي", value=0.0)
        v_d = col_v2.number_input("عمق الفاصل الصافي", value=0.0)
        v_q = col_v3.number_input("عدد الفواصل", min_value=0, step=1)

        # الأدراج
        col_dr1, col_dr2, col_dr3 = st.columns(3)
        dr_w = col_dr1.number_input("عرض الدرج الصافي (قبل الخصم)", value=0.0)
        dr_d = col_dr2.number_input("عمق الدرج (ثابت)", value=0.0)
        dr_q = col_dr3.number_input("عدد الأدراج", min_value=0, step=1)

        submit_btn = st.form_submit_button("✅ إضافة هذه الوحدة للمشروع")

    # --- محرك الحسابات عند الضغط على الزر ---
    if submit_btn:
        if W > 0 and H > 0 and D > 0:
            current_label = u_label if u_label else f"وحدة غير مسماة ({u_kind})"
            
            # 1. تخصيم الوحدة الأساسية
            h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            if u_kind == "سفلي":
                add_to_project(current_label, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_project(current_label, "ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
                add_to_project(current_label, "ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
                add_to_project(current_label, "ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
            else:
                add_to_project(current_label, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_project(current_label, "ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
                add_to_project(current_label, "ألومنيوم", "رباط عمق", f_d, 4, "متقارب")

            # فيبر الوحدة
            add_to_project(current_label, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "حشو")
            add_to_project(current_label, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "حشو")
            add_to_project(current_label, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "حشو")

            # 2. حسابات الأرفف
            if s_q > 0:
                add_to_project(current_label, "ألومنيوم", "عرض رف", s_w, s_q * 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "عمق رف", s_d, s_q * 2, "مفرد")
                add_to_project(current_label, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "حشو رف")

            # 3. حسابات الفواصل
            if v_q > 0:
                add_to_project(current_label, "ألومنيوم", "ارتفاع فاصل", v_h, v_q * 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "عمق فاصل", v_d, v_q * 2, "مفرد")
                add_to_project(current_label, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "حشو فاصل")

            # 4. حسابات الأدراج (خصم 2.5 سم)
            if dr_q > 0:
                add_to_project(current_label, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "مفرد")
                add_to_project(current_label, "ألومنيوم", "جنب درج عمق", dr_d, dr_q * 2, "مفرد")
                add_to_project(current_label, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "حشو درج")

            st.success(f"تمت إضافة '{current_label}' بنجاح!")
        else:
            st.error("يرجى إدخال أبعاد الوحدة أولاً!")

    # --- عرض المشروع الحالي ---
    if st.session_state.project_data:
        st.divider()
        st.subheader("📋 تفاصيل مشروعك الحالي")
        full_df = pd.DataFrame(st.session_state.project_data)
        
        # عرض كل وحدة في جدول منفصل باسمها
        for name, group in full_df.groupby("اسم الوحدة"):
            st.markdown(f"#### 📍 {name}")
            st.table(group.drop(columns=["اسم الوحدة"]))

        # أزرار التحكم
        c_clear, c_next = st.columns(2)
        if c_clear.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_data = []
            st.rerun()
        if c_next.button("💰 حساب استهلاك الخامات والتسعير للمشروع ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: استهلاك الأعواد واللوحات
# ==========================================
elif st.session_state.page == 'inventory':
    st.title("📊 تقرير استهلاك الخامات - DOGGA SYSTEM")
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum_df = df[df["الخامة"] == "ألومنيوم"].copy()
        fiber_df = df[df["الخامة"] == "فيبر"].copy()

        # 1. حساب الألومنيوم
        st.subheader("🥢 تقدير أعواد الألومنيوم (600 سم / عود)")
        # تحويل المقاس لرقم للعمليات الحسابية
        alum_df["المقاس (سم)"] = pd.to_numeric(alum_df["المقاس (سم)"], errors='coerce')
        
        summary_alum = alum_df.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="إجمالي الأطوال (سم)")
        
        summary_alum["عدد الأعواد المطلوبة"] = summary_alum["إجمالي الأطوال (سم)"].apply(lambda x: math.ceil(x / 600))
        st.table(summary_alum)

        # 2. حساب الفيبر
        st.subheader("🖼️ تقدير ألواح الفيبر (280 × 130)")
        total_fiber_area = 0
        for _, row in fiber_df.iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                total_fiber_area += float(dims[0]) * float(dims[1]) * row["العدد"]
        
        sheets = math.ceil(total_fiber_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة للمشروع", f"{sheets} لوح")

        st.divider()
        
        # 3. فاتورة الأسعار النهائية
        st.subheader("💵 فاتورة المشروع (Excel Mode)")
        bill_items = []
        for _, r in summary_alum.iterrows():
            bill_items.append({"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["عدد الأعواد المطلوبة"], "سعر الوحدة": 0.0})
        bill_items.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "سعر الوحدة": 0.0})
        
        edited_bill = st.data_editor(pd.DataFrame(bill_items), use_container_width=True)
        total_inv = (edited_bill["الكمية"] * edited_bill["سعر الوحدة"]).sum()
        st.header(f"💰 التكلفة الإجمالية: {total_inv:,.2f} ج.م")

        if st.button("⬅️ العودة لإضافة وحدات أخرى"):
            st.session_state.page = 'deduction'
            st.rerun()
    else:
        st.warning("المشروع لا يحتوي على بيانات.")
        if st.button("العودة للبداية"):
            st.session_state.page = 'deduction'
            st.rerun()
