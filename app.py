import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="DOGGA SYSTEM - الإدارة الهندسية", layout="wide")

# 2. تهيئة مخزن البيانات
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'deduction'

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
# الصفحة الأولى: التخصيم التفصيلي
# ==========================================
if st.session_state.page == 'deduction':
    st.title("🏗️ تخصيم مشروع متكامل - ورشة DED EL KASR")
    
    with st.form("main_form", clear_on_submit=True):
        st.subheader("📏 إدخال بيانات الوحدة")
        c_name, c_kind = st.columns(2)
        u_label = c_name.text_input("اسم الوحدة (مثلاً: سفلي 80 سم)", placeholder="وحدة 1")
        u_kind = c_kind.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        c1, c2, c3 = st.columns(3)
        W = c1.number_input("العرض الكلي (W)", min_value=0.0)
        H = c2.number_input("الارتفاع الكلي (H)", min_value=0.0)
        D = c3.number_input("العمق الكلي (D)", min_value=0.0)

        st.divider()
        st.subheader("📦 الأرفف والفواصل والأدراج")
        
        # مدخلات الأرفف
        cs1, cs2, cs3 = st.columns(3)
        s_w = cs1.number_input("عرض الرف", value=0.0)
        s_d = cs2.number_input("عمق الرف", value=0.0)
        s_q = cs3.number_input("عدد الأرفف", min_value=0)

        # مدخلات الفواصل
        cv1, cv2, cv3 = st.columns(3)
        v_h = cv1.number_input("ارتفاع الفاصل", value=0.0)
        v_d = cv2.number_input("عمق الفاصل", value=0.0)
        v_q = cv3.number_input("عدد الفواصل", min_value=0)

        # مدخلات الأدراج
        cd1, cd2, cd3 = st.columns(3)
        dr_w = cd1.number_input("عرض الدرج", value=0.0)
        dr_d = cd2.number_input("عمق الدرج", value=0.0)
        dr_q = cd3.number_input("عدد الأدراج", min_value=0)

        submit = st.form_submit_button("✅ إضافة الوحدة للمشروع")

    if submit:
        if W > 0 and H > 0:
            name = u_label if u_label else f"وحدة {u_kind}"
            # --- أساسيات التخصيم ---
            h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            # ألومنيوم الهيكل
            if u_kind == "سفلي":
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
            else: # علوي ومطبقيه
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 4, "متقارب")

            # فيبر الهيكل
            add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
            add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
            add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

            # حسابات الأرفف
            if s_q > 0:
                add_to_project(name, "ألومنيوم", "عرض رف", s_w, s_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق رف", s_d, s_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "لوح")

            # حسابات الفواصل
            if v_q > 0:
                add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "لوح")

            # حسابات الأدراج (علبه درج)
            if dr_q > 0:
                add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبه درج")
                add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبه درج")
                add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "لوح")

            st.success(f"تمت إضافة {name} للمشروع")

    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            st.subheader(f"📍 {n}")
            st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 حساب استهلاك الخامات والتسعير ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: الاستهلاك والفاتورة المفتوحة
# ==========================================
elif st.session_state.page == 'inventory':
    st.title("📊 استهلاك خامات المشروع - DOGGA SYSTEM")
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')

        # 1. حساب الأعواد
        st.subheader("🥢 تقدير أعواد الألومنيوم (6 متر)")
        summary = alum.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        st.table(summary)

        # 2. حساب الفيبر
        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
        sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة", f"{sheets} لوح")

        st.divider()
        st.subheader("💵 فاتورة المشتريات المفتوحة")
        
        base_bill = []
        for _, r in summary.iterrows():
            base_bill.append({"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["الأعواد"], "السعر": 0.0})
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})

        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        
        total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.header(f"💰 التكلفة الإجمالية: {total:,.2f} ج.م")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ العودة للتخصيم"):
            st.session_state.page = 'deduction'; st.rerun()
        if col2.button("🗑️ مسح المشروع"):
            st.session_state.project_data = []; st.session_state.page = 'deduction'; st.rerun()
            # --- تابع الصفحة الثانية (inventory) ---
        
        st.divider()
        
        # 4. تفاصيل إضافية للمراجعة
        with st.expander("🔍 مراجعة الأطوال الكلية قبل التقطيع"):
            st.write("الأطوال التالية هي ناتج جمع كل القطع المضافة للمشروع:")
            st.dataframe(summary, use_container_width=True)

        # 5. منطقة أزرار الإجراءات
        st.write("### ⚙️ خيارات المشروع")
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        
        with c_inv1:
            if st.button("⬅️ إضافة وحدات أخرى", use_container_width=True):
                st.session_state.page = 'deduction'
                st.rerun()
                
        with c_inv2:
            # تصدير الفاتورة النهائية شاملة الأصناف المضافة يدوياً
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 تحميل الفاتورة (Excel)",
                data=csv_final,
                file_name=f"DOGGA_Project_Invoice.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with c_inv3:
            # زر المسح النهائي مع تأكيد
            if st.button("🗑️ تفريغ المشروع بالكامل", use_container_width=True, type="secondary"):
                st.session_state.project_data = []
                st.session_state.page = 'deduction'
                st.rerun()

    else:
        # حماية في حالة الدخول للصفحة مباشرة بدون بيانات
        st.error("⚠️ لا توجد بيانات مسجلة في المشروع حالياً.")
        if st.button("الذهاب لصفحة التخصيم لإضافة وحدات"):
            st.session_state.page = 'deduction'
            st.rerun()

# --- نهاية كود تطبيق DOGGA SYSTEM الأصلي ---
# المهندس: ياسين علاء
# ورشة: DED EL KASR
