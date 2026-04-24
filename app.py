import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة والواجهة الفضائية (نحاسي + أزرق كهربائي)
st.set_page_config(page_title="DOGGA SYSTEM - الإدارة الهندسية", layout="wide")

# كود التنسيق وإخفاء أدوات Streamlit و GitHub
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .stApp {
        background: radial-gradient(circle at top right, #0d1117, #050505, #020c1b);
        color: #d9a066;
    }
    .main-btn-container div.stButton > button {
        background: rgba(0, 150, 255, 0.05) !important;
        border: 2px solid #0096ff !important;
        color: #0096ff !important;
        border-radius: 20px !important;
        padding: 50px 20px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: 0.5s !important;
        text-shadow: 0 0 15px #0096ff !important;
        box-shadow: 0 0 10px rgba(0, 150, 255, 0.2) !important;
        margin-bottom: 25px !important;
    }
    .main-btn-container div.stButton > button:hover {
        background: #d9a066 !important;
        color: #1a1614 !important;
        border-color: #d9a066 !important;
        box-shadow: 0 0 40px #d9a066 !important;
        transform: scale(1.02) !important;
    }
    div[data-testid="stForm"], .stTable, .stDataFrame, div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(217, 160, 102, 0.4) !important;
        backdrop-filter: blur(5px);
    }
    h1 { 
        color: #0096ff !important; 
        text-shadow: 0 0 30px #0096ff; 
        text-align: center;
        font-size: 3.5rem !important;
    }
    h2, h3 { color: #d9a066 !important; text-align: center; }
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: #0d1117 !important;
        color: #0096ff !important;
        border: 1px solid #0096ff !important;
        border-radius: 10px !important;
        height: 50px !important;
    }
    label { 
        color: #d9a066 !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. تهيئة مخزن البيانات
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'

# دالة الجرد الذكية (منطق الورشة لمنع الهالك ودعم الكسور)
def calculate_real_bars(pieces_list, bar_length=600.0, kerf=0.5):
    if not pieces_list: return 0
    sorted_pieces = sorted([float(p) for p in pieces_list], reverse=True)
    bars = []
    for piece in sorted_pieces:
        added = False
        piece_with_kerf = piece + kerf
        for i in range(len(bars)):
            if bars[i] >= piece_with_kerf:
                bars[i] -= piece_with_kerf
                added = True
                break
        if not added:
            bars.append(bar_length - piece_with_kerf)
    return len(bars)

# تعديل دالة الإضافة لمنع الـ ValueError في مقاسات الفيبر
def add_to_project(unit_name, category, item_name, length, qty, unit_type="-"):
    try:
        final_length = float(length)
    except:
        final_length = length # لو فيبر (نص) سيبه زي ما هو
        
    st.session_state.project_data.append({
        "اسم الوحدة": unit_name,
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": final_length,
        "العدد": int(qty),
        "نوع التخصيم": unit_type
    })

# ==========================================
# 🌌 الصفحة 0: الواجهة الرئيسية
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown("<h1>⚡ DOGGA GALAXY SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d9a066; font-size: 1.3rem;'>برمجه المهندس ياسين علاء | DOGGA SMART KITCHEN</p>", unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("✨ ابدأ التخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
        if st.button("📏 تخصيم الدرف"):
            st.toast("🛸 جاري تجهيز محرك الدرف...")
        if st.button("📁 المشاريع"):
            st.session_state.page = 'inventory'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# الصفحة الأولى: التخصيم التفصيلي
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("<h1>🏗️ تخصيم مشروع متكامل</h1>", unsafe_allow_html=True)
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    with st.form("main_form", clear_on_submit=True):
        st.subheader("📏 إدخال بيانات الوحدة")
        u_label = st.text_input("اسم الوحدة", placeholder="مثلاً: وحدة سفلي 80")
        u_kind = st.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        st.divider()
        W = st.number_input("العرض الكلي (W)", min_value=0.0, step=0.1, format="%.1f")
        H = st.number_input("الارتفاع الكلي (H)", min_value=0.0, step=0.1, format="%.1f")
        D = st.number_input("العمق الكلي (D)", min_value=0.0, step=0.1, format="%.1f")

        st.divider()
        st.subheader("📦 الإضافات (أرفف - فواصل - أدراج)")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            s_w = st.number_input("عرض الرف", value=0.0, step=0.1)
            s_d = st.number_input("عمق الرف", value=0.0, step=0.1)
            s_q = st.number_input("عدد الأرفف", min_value=0)
        with col_s2:
            v_h = st.number_input("ارتفاع الفاصل", value=0.0, step=0.1)
            v_d = st.number_input("عمق الفاصل", value=0.0, step=0.1)
            v_q = st.number_input("عدد الفواصل", min_value=0)
        with col_s3:
            dr_w = st.number_input("عرض الدرج", value=0.0, step=0.1)
            dr_d = st.number_input("عمق الدرج", value=0.0, step=0.1)
            dr_q = st.number_input("عدد الأدراج", min_value=0)

        submit = st.form_submit_button("✅ إضافة الوحدة للمشروع", use_container_width=True)

    if submit:
        if W > 0 and H > 0:
            name = u_label if u_label else f"وحدة {u_kind}"
            # تخصيم الارتفاع: 13 سم للسفلي و 5 سم للعلوي
            h_ded = 13.0 if u_kind in ["سفلي", "دولاب خزين"] else 5.0
            f_h, f_w, f_d = H - h_ded, W - 5.0, D - 5.0

            # تخصيمات الألومنيوم
            if u_kind == "سفلي":
                items = [("قائم ارتفاع", f_h, 2, "مفرد"), ("قائم ارتفاع", f_h, 2, "متقارب"),
                         ("عارضة عرض", f_w, 3, "مفرد"), ("عارضة عرض", f_w, 1, "متقارب"),
                         ("رباط عمق", f_d, 2, "مفرد"), ("رباط عمق", f_d, 2, "متقارب")]
            else:
                items = [("قائم ارتفاع", f_h, 2, "مفرد"), ("قائم ارتفاع", f_h, 2, "متقارب"),
                         ("عارضة عرض", f_w, 2, "مفرد"), ("عارضة عرض", f_w, 2, "متقارب"),
                         ("رباط عمق", f_d, 4, "متقارب")]
            
            for itm in items: 
                add_to_project(name, "ألومنيوم", itm[0], itm[1], itm[2], itm[3])

            # تخصيمات الفيبر
            add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
            add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
            if u_kind != "سفلي":
                add_to_project(name, "فيبر", "سقفية", f"{f_w}×{f_d}", 1, "لوح")
            add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

            # الإضافات
            if s_q > 0:
                add_to_project(name, "ألومنيوم", "عرض رف", s_w, s_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق رف", s_d, s_q*2, "مفرد")
            if v_q > 0:
                add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
            if dr_q > 0:
                add_to_project(name, "ألومنيوم", "وش درج", dr_w - 2.5, dr_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "مفرد")

            st.success(f"🚀 تم حفظ {name} بنجاح")
            st.rerun()

    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            with st.expander(f"📍 مراجعة {n}"):
                st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 جرد الخامات وتسعير الفاتورة ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: الاستهلاك والفاتورة
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("<h1>📊 استهلاك خامات المشروع</h1>", unsafe_allow_html=True)
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')

        st.subheader("🥢 تقدير الأعواد (منطق الورشة الحقيقي)")
        inv_results = []
        for u_type, group in alum.groupby("نوع التخصيم"):
            all_pcs = []
            for _, row in group.iterrows():
                all_pcs.extend([row["المقاس (سم)"]] * int(row["العدد"]))
            
            bars = calculate_real_bars(all_pcs)
            inv_results.append({
                "نوع التخصيم": u_type,
                "إجمالي سم": round(sum(all_pcs), 1),
                "عدد الأعواد": bars
            })
        
        st.table(pd.DataFrame(inv_results))

        # حساب الفيبر تقريبي
        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            try:
                d = str(row["المقاس (سم)"]).split('×')
                total_area += float(d[0]) * float(d[1]) * row["العدد"]
            except: pass
        sheets = math.ceil(total_area / (280 * 122)) if total_area > 0 else 0
        st.metric("عدد ألواح الفيبر (تقريبي)", f"{sheets} لوح")

        st.divider()
        st.subheader("💵 الفاتورة النهائية")
        base_bill = [{"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["عدد الأعواد"], "السعر": 0.0} for r in inv_results]
        if sheets > 0: base_bill.append({"الصنف": "لوح فيبر", "الكمية": sheets, "السعر": 0.0})
        
        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        if not final_bill.empty:
            total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
            st.header(f"💰 التكلفة الكلية: {total:,.2f} ج.م")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ مسح كل البيانات", use_container_width=True):
                st.session_state.project_data = []
                st.session_state.page = 'main_menu'
                st.rerun()
