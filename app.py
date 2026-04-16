import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. الإعدادات وتصميم الواجهة (UI)
# ==========================================
st.set_page_config(page_title="DOGGA SYSTEM PRO", layout="wide")

if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

accent = "#f1c40f" if st.session_state.dark_mode else "#d4ac0d"
bg_card = "#1c1f26" if st.session_state.dark_mode else "#f8f9fa"

st.markdown(f"""
    <style>
    .main {{ direction: rtl !important; text-align: right; }}
    .stApp {{ background-color: {"#0e1117" if st.session_state.dark_mode else "#ffffff"}; }}
    .section-header {{ 
        background: {accent}; color: #000; padding: 10px; 
        border-radius: 8px; font-weight: bold; margin: 20px 0;
        text-align: center;
    }}
    .unit-box {{ 
        background: {bg_card}; border: 1px solid {accent}; 
        padding: 15px; border-radius: 10px; margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# الهيدر
h1, h2 = st.columns([8, 2])
with h1: st.markdown(f"<h1 style='color:{accent};'>DOGGA SYSTEM PRO | م/ ياسين علاء</h1>", unsafe_allow_html=True)
with h2:
    if st.button("🌓 تبديل المظهر"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. منطقة إدخال البيانات (Sidebar)
# ==========================================
with st.sidebar:
    st.markdown(f"<h3 style='color:{accent};'>➕ إضافة وحدة جديدة</h3>", unsafe_allow_html=True)
    with st.form("input_form", clear_on_submit=True):
        u_client = st.text_input("اسم العميل / رقم الوحدة")
        u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])
        
        st.write("---")
        st.write("📐 الأبعاد الأساسية")
        c1, c2, c3 = st.columns(3)
        # تم ضبط value=None لإزالة الصفر
        W = c1.number_input("العرض", value=None, placeholder="0")
        H = c2.number_input("الارتفاع", value=None, placeholder="0")
        D = c3.number_input("العمق", value=None, placeholder="0")
        
        with st.expander("➕ إضافات (أرفف/فواصل/أدراج)"):
            sh_n = st.number_input("عدد الأرفف", min_value=0, value=0)
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0")
            st.divider()
            v_n = st.number_input("عدد الفواصل", min_value=0, value=0)
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            st.divider()
            dr_n = st.number_input("عدد الأدراج", min_value=0, value=0)
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0")

        if st.form_submit_button("✅ حفظ وتخصيم", use_container_width=True):
            if W and H and D:
                h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
                hn, wn, dn = H - h_ded, W - 5, D - 5
                
                # تخصيم الألومنيوم
                alum = [
                    ["قوايم رئيسية", int(hn), 2, "مفرد"],
                    ["عوارض عرض", int(wn), 2 if u_type == "وحدة علوية" else 3, "مفرد"],
                    ["عوارض عمق", int(dn), 2, "مفرد"],
                    ["وزرة / فرشة", int(wn), 1 if u_type == "وحدة سفلية" else 0, "متقارب"]
                ]
                
                if sh_n > 0 and sh_w and sh_d: 
                    alum.append([f"أعواد أرفف ({sh_n})", int(sh_w), int(sh_n*4), "مفرد"])
                if v_n > 0 and v_h: 
                    alum.append([f"أعواد فواصل ({v_n})", int(v_h), int(v_n*4), "مفرد"])
                if dr_n > 0 and dr_w and dr_d: 
                    alum.append([f"براويز درج ({dr_n})", int(dr_w - 2.5), int(dr_n*4), "مفرد"])

                # تخصيم الفيبر
                fiber = [
                    ["ظهرية", f"{int(wn)}x{int(hn)}", 1],
                    ["أرضية", f"{int(wn)}x{int(dn)}", 1],
                    ["أجناب", f"{int(hn)}x{int(dn)}", 2]
                ]
                if sh_n > 0 and sh_w and sh_d: 
                    fiber.append(["فيبر أرفف", f"{int(sh_w-0.5)}x{int(sh_d-0.5)}", sh_n])

                st.session_state.project_list.append({
                    "client": u_client if u_client else "بدون اسم",
                    "type": u_type, "dims": f"{W}x{H}x{D}",
                    "alum": alum, "fiber": fiber
                })
                st.rerun()

    if st.button("🗑️ مسح كل البيانات", use_container_width=True):
        st.session_state.project_list = []
        st.rerun()

# ==========================================
# 3. عرض النتائج والجرد الاحترافي
# ==========================================
if not st.session_state.project_list:
    st.info("👈 ابدأ بإضافة الوحدات من القائمة الجانبية")
else:
    tab1, tab2 = st.tabs(["📊 جرد الخامات الإجمالي", "📋 شيتات تفصيل الوحدات"])

    with tab1:
        muf_list, mut_list, fib_list = [], [], []
        
        for unit in st.session_state.project_list:
            for row in unit.get("alum", []):
                item = {"المقاس": row[1], "العدد": row[2]}
                if row[3] == "مفرد": muf_list.append(item)
                else: mut_list.append(item)
            for row in unit.get("fiber", []):
                fib_list.append({"البيان": row[0], "المقاس": row[1], "العدد": row[2]})

        c_muf, c_mut, c_fib = st.columns(3)
        
        with c_muf:
            st.markdown("<div class='section-header'>📋 جرد المفرد</div>", unsafe_allow_html=True)
            if muf_list:
                df_muf = pd.DataFrame(muf_list).groupby("المقاس").sum().reset_index()
                st.table(df_muf)
                total_muf = (df_muf['المقاس'] * df_muf['العدد']).sum()
                st.success(f"الأعواد: {math.ceil(total_muf/600)} (6م)")

        with c_mut:
            st.markdown("<div class='section-header'>📋 جرد المتقارب</div>", unsafe_allow_html=True)
            if mut_list:
                df_mut = pd.DataFrame(mut_list).groupby("المقاس").sum().reset_index()
                st.table(df_mut)
                total_mut = (df_mut['المقاس'] * df_mut['العدد']).sum()
                st.success(f"الأعواد: {math.ceil(total_mut/600)} (6م)")

        with c_fib:
            st.markdown("<div class='section-header'>🖼️ جرد الفيبر</div>", unsafe_allow_html=True)
            if fib_list:
                st.table(pd.DataFrame(fib_list))

    with tab2:
        for idx, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f"""<div class='unit-box'>
                    <b>وحدة #{idx+1}: {item.get('client')}</b> | {item.get('type')} | {item.get('dims')}
                </div>""", unsafe_allow_html=True)
                col_a, col_f = st.columns([3, 2])
                with col_a: 
                    st.dataframe(pd.DataFrame(item.get('alum'), columns=["البيان", "المقاس", "العدد", "النوع"]), use_container_width=True)
                with col_f: 
                    st.dataframe(pd.DataFrame(item.get('fiber'), columns=["القطعة", "المقاس", "العدد"]), use_container_width=True)

st.markdown(f"<p style='text-align:center; opacity:0.5; margin-top:50px;'>DOGGA PRO 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
