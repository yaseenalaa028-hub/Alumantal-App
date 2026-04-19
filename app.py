import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة والاسم التجاري
st.set_page_config(page_title="DOGGA SYSTEM", layout="wide")

# 2. تهيئة مخزن البيانات والصفحات
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'

# --- التصميم الجمالي المعتمد (الذهب والأسود والنجوم) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #D4AF37 50%, #121212 50%);
        background-image: 
            linear-gradient(to right, #D4AF37 50%, transparent 50%),
            radial-gradient(circle at 75% 20%, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle at 85% 50%, #D4AF37 2px, transparent 2px),
            radial-gradient(circle at 70% 80%, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle at 92% 30%, #D4AF37 1.2px, transparent 1.2px);
        background-size: 100% 100%, 120px 120px, 180px 180px, 250px 250px, 150px 150px;
    }
    .main-title-text {
        text-align: center; color: #ffffff; font-family: 'Segoe UI'; font-size: 45px;
        font-weight: 900; margin-top: 60px; text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
    }
    .dev-tag { color: #000000; text-align: center; font-weight: bold; font-size: 22px; margin-bottom: 60px; }
    div.stButton > button {
        width: 100%; border-radius: 50px !important; height: 65px; font-weight: bold;
        border: 3px solid #D4AF37; background-color: #1e1e1e; color: #D4AF37;
    }
    div.stButton > button:hover { border-color: #ffffff; color: #ffffff; background-color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

def add_to_project(unit_name, category, item_name, length, qty, unit_type="-"):
    st.session_state.project_data.append({
        "اسم الوحدة": unit_name, "الخامة": category, "اسم القطعة": item_name,
        "المقاس (سم)": length, "العدد": qty, "نوع التخصيم": unit_type
    })

# ==========================================
# القائمة الرئيسية
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown('<div class="main-title-text">DOGGA SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="dev-tag">برمجة المهندس ياسين علاء</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 ابدأ تخصيم الوحدات"): st.session_state.page = 'deduction'; st.rerun()
        if st.button("🖼️ تخصيم مقاسات الدرف"): st.session_state.page = 'doors'; st.rerun()
        if st.button("📁 مراجعة المشروع والمخزن"): st.session_state.page = 'inventory'; st.rerun()

# ==========================================
# صفحة تخصيم الدرف
# ==========================================
elif st.session_state.page == 'doors':
    st.markdown("<style>.stApp { background: white !important; color: black !important; }</style>", unsafe_allow_html=True)
    st.title("🖼️ حساب مقاسات الدرف - DED EL KASR")
    if st.button("⬅️ عودة"): st.session_state.page = 'main_menu'; st.rerun()
    with st.form("door_form"):
        d_w = st.number_input("عرض الفتحة (سم)", 0.0); d_h = st.number_input("ارتفاع الفتحة (سم)", 0.0)
        d_num = st.selectbox("عدد الدرف", [1, 2])
        if st.form_submit_button("احسب"):
            f_w = d_w - 0.5 if d_num == 1 else (d_w / 2) - 0.4
            f_h = d_h - 0.5
            st.success(f"المقاس: {f_w} × {f_h}")
            add_to_project("درفة", "ألومنيوم", "برواز درفة", f_w, d_num*2, "درف")
            add_to_project("درفة", "ألومنيوم", "برواز درفة", f_h, d_num*2, "درف")

# ==========================================
# صفحة التخصيم التفصيلي للوحدات
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("<style>.stApp { background: white !important; color: black !important; }</style>", unsafe_allow_html=True)
    st.title("🏗️ تخصيم الوحدات - ورشة DED EL KASR")
    if st.button("⬅️ عودة"): st.session_state.page = 'main_menu'; st.rerun()

    with st.form("main_form", clear_on_submit=True):
        u_label = st.text_input("اسم الوحدة")
        u_kind = st.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
        c1, c2, c3 = st.columns(3); W, H, D = c1.number_input("العرض"), c2.number_input("الارتفاع"), c3.number_input("العمق")
        
        st.divider(); st.subheader("📦 الأرفف والفواصل والأدراج")
        cs1, cs2, cs3 = st.columns(3); s_w, s_d, s_q = cs1.number_input("عرض الرف"), cs2.number_input("عمق الرف"), cs3.number_input("عدد الأرفف", 0)
        cv1, cv2, cv3 = st.columns(3); v_h, v_d, v_q = cv1.number_input("ارتفاع الفاصل"), cv2.number_input("عمق الفاصل"), cv3.number_input("عدد الفواصل", 0)
        cd1, cd2, cd3 = st.columns(3); dr_w, dr_d, dr_q = cd1.number_input("عرض الدرج"), cd2.number_input("عمق الدرج"), cd3.number_input("عدد الأدراج", 0)

        if st.form_submit_button("✅ إضافة للمشروع"):
            if W > 0 and H > 0:
                name = u_label if u_label else f"وحدة {u_kind}"
                h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
                f_h, f_w, f_d = H - h_ded, W - 5, D - 5

                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 4, "علبة")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 4, "علبة")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 4, "علبة")

                # لوجيك الأرضية والسقفية
                if u_kind == "سفلي":
                    add_to_project(name, "فيبر", "أرضية فقط", f"{f_w}×{f_d}", 1, "حشو")
                else:
                    add_to_project(name, "فيبر", "أرضية + سقفية", f"{f_w}×{f_d}", 2, "حشو")
                
                # إضافة الأرفف والفواصل والأدراج
                if s_q > 0: add_to_project(name, "ألومنيوم", "رف", s_w, s_q*2); add_to_project(name, "فيبر", "حشو رف", f"{s_w}×{s_d}", s_q)
                if dr_q > 0: add_to_project(name, "ألومنيوم", "درج", dr_w, dr_q*2); add_to_project(name, "فيبر", "أرضية درج", f"{dr_w}×{dr_d}", dr_q)
                
                st.success(f"تمت إضافة {name}")

# ==========================================
# صفحة الجرد والفاتورة (كودك الأصلي المدمج)
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("<style>.stApp { background: white !important; color: black !important; }</style>", unsafe_allow_html=True)
    st.title("📊 مراجعة استهلاك الخامات")
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')
        summary = alum.groupby(["اسم القطعة"]).apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="إجمالي")
        
        # عرض الفاتورة للتسعير
        st.subheader("💵 تسعير الفاتورة")
        bill_df = pd.DataFrame([{"الصنف": r["اسم القطعة"], "الكمية": math.ceil(r["إجمالي"]/600), "السعر": 0.0} for _, r in summary.iterrows()])
        final_bill = st.data_editor(bill_df, num_rows="dynamic")
        
        st.divider()
        # --- الجزء اللي بعته يا هندسة ---
        with st.expander("🔍 مراجعة الأطوال الكلية قبل التقطيع"):
            st.write("الأطوال التالية هي ناتج جمع كل القطع المضافة للمشروع:")
            st.dataframe(summary, use_container_width=True)

        st.write("### ⚙️ خيارات المشروع")
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        
        with c_inv1:
            if st.button("⬅️ إضافة وحدات أخرى", use_container_width=True):
                st.session_state.page = 'deduction'; st.rerun()
                
        with c_inv2:
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 تحميل الفاتورة (Excel)", data=csv_final, file_name="DOGGA_Project_Invoice.csv", mime="text/csv", use_container_width=True)
            
        with c_inv3:
            if st.button("🗑️ تفريغ المشروع بالكامل", use_container_width=True, type="secondary"):
                st.session_state.project_data = []; st.session_state.page = 'main_menu'; st.rerun()
    else:
        st.error("⚠️ لا توجد بيانات مسجلة في المشروع حالياً.")
        if st.button("الذهاب لصفحة التخصيم لإضافة وحدات"):
            st.session_state.page = 'deduction'; st.rerun()

# نهاية كود DOGGA SYSTEM - المهندس ياسين علاء - ورشة DED EL KASR
