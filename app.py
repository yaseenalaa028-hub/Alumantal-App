import streamlit as st
import pandas as pd
import json
from datetime import datetime

# ==========================================
# 1. إعدادات النظام المحسنة
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM v2.0", layout="wide", initial_sidebar_state="expanded")

# تهيئة Session State المحسن
def init_session_state():
    defaults = {
        "project_list": [],
        "page": "home",
        "last_processed_id": None,
        "projects_history": {},
        "current_project": "مشروع جديد"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# وظيفة تنظيف الأرقام المحسنة
@st.cache_data
def clean_num(df):
    numeric_cols = df.select_dtypes(include=['number']).columns
    df_copy = df.copy()
    for col in numeric_cols:
        df_copy[col] = df_copy[col].apply(lambda x: f"{float(x):g}" if pd.notna(x) else "")
    return df_copy

# ==========================================
# 2. الشريط الجانبي (Sidebar) الجديد
# ==========================================
with st.sidebar:
    st.markdown("### 🎛️ لوحة التحكم")
    
    # اختيار المشروع
    project_options = ["مشروع جديد"] + list(st.session_state.projects_history.keys())
    selected_project = st.selectbox("📁 اختر المشروع:", project_options, key="project_selector")
    
    if selected_project != st.session_state.current_project:
        st.session_state.current_project = selected_project
        if selected_project != "مشروع جديد":
            st.session_state.project_list = st.session_state.projects_history[selected_project]["units"]
        else:
            st.session_state.project_list = []
        st.rerun()
    
    # حفظ مشروع جديد
    new_project_name = st.text_input("💾 اسم المشروع الجديد:", key="new_project")
    if st.button("💾 حفظ المشروع الحالي"):
        if st.session_state.project_list and new_project_name:
            st.session_state.projects_history[new_project_name] = {
                "units": st.session_state.project_list,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.current_project = new_project_name
            st.success(f"✅ تم حفظ '{new_project_name}'")
            st.rerun()

# ==========================================
# 3. الصفحة الرئيسية المحسنة
# ==========================================
if st.session_state.page == "home":
    st.markdown("""
        <div style='text-align:center; margin-top:5%;'>
            <h1 style='color:#f1c40f; font-size:4em; text-shadow:2px 2px 4px rgba(0,0,0,0.5);'>
                🚀 ضجة سمارت
            </h1>
            <h2 style='color:#2ecc71; font-size:2em;'>نظام التخصيم الفني المتكامل v2.0</h2>
            <p style='color:#ecf0f1; font-size:1.5em;'>دقة متناهية | حسابات فورية | تصدير Excel</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔨 بدء التخصيم", use_container_width=True, type="primary"):
            st.session_state.page = "calc"
            st.rerun()
    with col2:
        if st.button("📊 فاتورة سريعة", use_container_width=True):
            st.session_state.page = "invoice"
            st.rerun()
    with col3:
        if st.button("📁 مشاريعي", use_container_width=True):
            st.session_state.page = "projects"
            st.rerun()

# ==========================================
# 4. صفحة المشاريع الجديدة
# ==========================================
elif st.session_state.page == "projects":
    st.title("📁 إدارة المشاريع")
    
    if st.button("⬅️ العودة", key="back_projects"):
        st.session_state.page = "home"
        st.rerun()
    
    if st.session_state.projects_history:
        for proj_name, proj_data in st.session_state.projects_history.items():
            with st.expander(f"📦 {proj_name} - {proj_data['date']}"):
                st.info(f"عدد الوحدات: {len(proj_data['units'])}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📋 تحميل {proj_name}", key=f"load_{proj_name}"):
                        st.session_state.project_list = proj_data['units']
                        st.session_state.current_project = proj_name
                        st.session_state.page = "calc"
                        st.rerun()
                with col2:
                    if st.button(f"🗑️ حذف {proj_name}", key=f"del_{proj_name}"):
                        del st.session_state.projects_history[proj_name]
                        st.rerun()
    else:
        st.info("لا توجد مشاريع محفوظة بعد")

# ==========================================
# 5. صفحة الفاتورة المحسنة مع تصدير Excel
# ==========================================
elif st.session_state.page == "invoice":
    st.title("💰 فاتورة الخامات النهائية")
    
    col_back, col_export = st.columns([1, 3])
    with col_back:
        if st.button("⬅️ العودة للتخصيم"):
            st.session_state.page = "calc"
            st.rerun()
    
    # حساب الجرد الآمن
    t_m, t_t, t_f = 0, 0, 0
    for unit in st.session_state.project_list:
        for a in unit.get("alum", []):
            val = float(a[1]) if a[1] is not None else 0
            count = float(a[2]) if a[2] is not None else 0
            if a[3] == "مفرد": t_m += val * count
            else: t_t += val * count
        for f in unit.get("fiber", []):
            w, h, qty = float(f[1]) if f[1] is not None else 0, float(f[2]) if f[2] is not None else 0, float(f[3]) if f[3] is not None else 0
            t_f += w * h * qty

    qty_m, qty_t, qty_f = round(t_m / 600, 2), round(t_t / 600, 2), round(t_f / (280*130), 2)
    
    invoice_data = [
        {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
        {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
        {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
    ]
    
    df_invoice = pd.DataFrame(invoice_data)
    edited_df = st.data_editor(df_invoice, num_rows="dynamic", use_container_width=True, hide_index=True)
    edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    total = edited_df["الإجمالي"].sum()
    st.markdown(f"""
        <div style='text-align:center; padding:20px; background:#2ecc71; color:white; border-radius:10px;'>
            <h2>💵 إجمالي الفاتورة: {total:,.2f} جنيه</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # تصدير Excel
    csv = edited_df.to_csv(index=False)
    st.download_button(
        "📥 تحميل الفاتورة Excel",
        csv,
        f"فاتورة_{st.session_state.current_project}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        "text/csv"
    )
    
    st.dataframe(clean_num(edited_df), use_container_width=True)

# ==========================================
# 6. صفحة التخصيم المحسنة
# ==========================================
else:  # calc page
    st.title(f"🔨 لوحة تخصيم الوحدات - {st.session_state.current_project}")
    
    col_home, col_invoice = st.columns(2)
    with col_home:
        if st.button("🏠 الصفحة الرئيسية", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col_invoice:
        if st.button("💰 فاتورة نهائية", use_container_width=True, type="primary"):
            st.session_state.page = "invoice"
            st.rerun()
    
    # Form محسن مع validation
    with st.form(key="calc_form", clear_on_submit=False):
        col_client, col_type = st.columns(2)
        client = col_client.text_input("👤 اسم العميل:", key="client_name")
        unit_type = col_type.selectbox("📦 نوع الوحدة:", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])
        
        st.markdown("### 📐 المقاسات الرئيسية")
        col_w, col_h, col_d = st.columns(3)
        W = col_w.number_input("العرض (سم)", min_value=1.0, step=0.5)
        H = col_h.number_input("الارتفاع (سم)", min_value=1.0, step=0.5)
        D = col_d.number_input("العمق (سم)", min_value=1.0, step=0.5)
        
        st.markdown("### 📋 الإضافات الاختيارية")
        shelf_col1, shelf_col2, shelf_col3 = st.columns(3)
        sh_n = shelf_col1.number_input("عدد الأرفف:", min_value=0, step=1)
        sh_w = shelf_col2.number_input("عرض الرف:", min_value=1.0, step=0.5) if sh_n > 0 else 0
        sh_d = shelf_col3.number_input("عمق الرف:", min_value=1.0, step=0.5) if sh_n > 0 else 0
        
        vert_col1, vert_col2, vert_col3 = st.columns(3)
        v_n = vert_col1.number_input("عدد الفواصل:", min_value=0, step=1)
        v_h = vert_col2.number_input("ارتفاع الفاصل:", min_value=1.0, step=0.5) if v_n > 0 else 0
        v_d = vert_col3.number_input("عمق الفاصل:", min_value=1.0, step=0.5) if v_n > 0 else 0
        
        drw_col1, drw_col2, drw_col3 = st.columns(3)
        dr_n = drw_col1.number_input("عدد الأدراج:", min_value=0, step=1)
        dr_w = drw_col2.number_input("عرض الدرج:", min_value=1.0, step=0.5) if dr_n > 0 else 0
        dr_d = drw_col3.number_input("عمق الدرج:", min_value=1.0, step=0.5) if dr_n > 0 else 0
        
        submit_btn = st.form_submit_button("🚀 حساب وإضافة للجرد", type="primary", use_container_width=True)

    # معالجة التخصيم المحسنة
    if submit_btn and W and H and D:
        op_id = f"{client[:20]}-{W:.1f}-{H:.1f}-{D:.1f}"
        if st.session_state.last_processed_id != op_id:
            # حسابات محسنة
            h_f, w_f, d_f = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5), W - 5, D - 5
            alum, fiber = [], []
            
            # ألمنيوم أساسي
            base_alum = [
                ["ارتفاع", h_f, 2, "مفرد"], ["ارتفاع", h_f, 2, "متقارب"],
                ["عرض", w_f, 3 if unit_type == "وحدة سفلية" else 2, "مفرد"],
                ["عرض", w_f, 1 if unit_type == "وحدة سفلية" else 2, "متقارب"],
                ["عمق", d_f, 2 if unit_type == "وحدة سفلية" else 0, "مفرد"],
                ["عمق", d_f, 2 if unit_type == "وحدة سفلية" else 4, "متقارب"]
            ]
            alum.extend(base_alum)
            
            # إضافات
            if sh_n > 0:
                alum.extend([["رف-عرض", sh_w, sh_n*2, "مفرد"], ["رف-عمق", sh_d, sh_n*2, "مفرد"]])
                fiber.append(["رفوف", sh_w-5, sh_d-5, sh_n])
            
            if v_n > 0:
                alum.extend([["فاصل-ارتفاع", v_h, v_n*2, "مفرد"], ["فاصل-عمق", v_d, v_n*2, "مفرد"]])
                fiber.append(["فواصل", v_h-5, v_d-5, v_n])
            
            if dr_n > 0:
                alum.extend([["درج-عرض", dr_w-2.5, dr_n*2, "2x8"], ["درج-عمق", dr_d, dr_n*2, "2x8"]])
                fiber.append(["أدراج", dr_w, dr_d, dr_n])
            
            # فيبر أساسي
            fiber.extend([["ظهرية", w_f, h_f, 1], ["أرضية", w_f, d_f, 1], ["أجنحة", h_f, d_f, 2]])
            
            st.session_state.project_list.append({
                "client": client, "unit_type": unit_type, "alum": alum, "fiber": fiber
            })
            st.session_state.last_processed_id = op_id
            st.success("✅ تم إضافة الوحدة للجرد بنجاح!")
            st.rerun()
        else:
            st.warning("⚠️ هذه الوحدة موجودة بالفعل!")
    elif submit_btn:
        st.error("❌ يجب إدخال المقاسات الأساسية (W, H, D)!")

    # عرض الجرد مع أزرار التحكم
    if st.session_state.project_list:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💰 فاتورة", use_container_width=True, type="primary"):
                st.session_state.page = "invoice"
                st.rerun()
        
        with col2:
            if st.button("🗑️ مسح الجرد", use_container_width=True):
                st.session_state.project_list = []
                st.session_state.last_processed_id = None
                st.rerun()
        
        with col3:
            if st.button("💾 حفظ المشروع", use_container_width=True):
                if st.session_state.current_project == "مشروع جديد":
                    st.error("أدخل اسم المشروع في الشريط الجانبي أولاً!")
                else:
                    st.session_state.projects_history[st.session_state.current_project] = {
                        "units": st.session_state.project_list,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.success("✅ تم الحفظ!")
        
        # عرض الوحدات
        for i, unit in enumerate(st.session_state.project_list):
            with st.expander(f"🔢 وحدة #{i+1}: {unit['unit_type']} - {unit['client']}"):
                col_a, col_f = st.columns(2)
                with col_a:
                    st.write("**🥉 الألمنيوم:**")
                    st.dataframe(clean_num(pd.DataFrame(unit["alum"], columns=["القطعة", "المقاس", "العدد", "النوع"])), use_container_width=True)
                with col_f:
                    st.write("**🪵 الفيبر:**")
                    st.dataframe(clean_num(pd.DataFrame(unit["fiber"], columns=["القطعة", "العرض", "الارتفاع", "العدد"])), use_container_width=True)
                
                if st.button(f"🗑️ حذف وحدة #{i+1}", key=f"del_unit_{i}"):
                    st.session_state.project_list.pop(i)
                    st.rerun()
    else:
        st.info("📭 لا توجد وحدات في الجرد حالياً")
