import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة والواجهة
# ==========================================
st.set_page_config(page_title="DOGGA PRO SYSTEM", layout="wide")

if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'page' not in st.session_state: st.session_state.page = 'home'

accent = "#f1c40f"
bg_card = "#1c1f26"

st.markdown(f"""
    <style>
    .main {{ direction: rtl !important; text-align: right; }}
    .stApp {{ background-color: #0e1117; color: white; }}
    .section-header {{ 
        background: {accent}; color: #000; padding: 12px; 
        border-radius: 10px; font-weight: bold; margin: 20px 0; text-align: center; font-size: 20px;
    }}
    .unit-box {{ 
        background: {bg_card}; border: 1px solid {accent}; 
        padding: 15px; border-radius: 10px; margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الواجهة الرئيسية
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div style="text-align: center; margin-top: 10%; padding: 50px; border-radius: 30px; border: 5px solid {accent}; background: {bg_card};">
            <h1 style="font-size: 5em; color: {accent}; font-weight: bold;">DOGGA SYSTEM PRO</h1>
            <h2 style="color:white;">ورشة المهندس ياسين علاء الذكية</h2>
            <p style="font-size: 1.5em; opacity: 0.8;">منظومة تخصيم وجرد الألمنيوم الاحترافية - إصدار 2026</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم الآن", use_container_width=True, type="primary"):
        st.session_state.page = 'calc'
        st.rerun()

# ==========================================
# 3. صفحة الورشة الواسعة
# ==========================================
else:
    c1, c2 = st.columns([8, 2])
    with c1: st.markdown(f"<h1 style='color:{accent}; text-align:right;'>🛠️ منطقة العمل | م/ ياسين علاء</h1>", unsafe_allow_html=True)
    with c2: 
        if st.button("🏠 العودة للرئيسية", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    st.divider()

    # --- نموذج الإدخال الشامل ---
    with st.expander("📝 إضافة وحدة جديدة (أدخل المقاسات هنا)", expanded=True):
        with st.form("workshop_form", clear_on_submit=True):
            f1, f2, f3 = st.columns(3)
            client = f1.text_input("اسم العميل / رقم الوحدة")
            u_type = f2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "وحدة أدراج"])
            
            st.markdown("#### 📐 المقاسات الإجمالية (سم)")
            d1, d2, d3 = st.columns(3)
            W = d1.number_input("العرض الكلي", value=None, placeholder="0")
            H = d2.number_input("الارتفاع الكلي", value=None, placeholder="0")
            D = d3.number_input("العمق الكلي", value=None, placeholder="0")

            st.markdown("#### ➕ الأرفف - الفواصل - الأدراج")
            a1, a2, a3 = st.columns(3)
            sh_n = a1.number_input("عدد الأرفف", min_value=0, value=0)
            sh_w = a2.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = a3.number_input("عمق الرف", value=None, placeholder="0")
            
            v1, v2 = st.columns(2)
            v_n = v1.number_input("عدد الفواصل", min_value=0, value=0)
            v_h = v2.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            v_d = v2.number_input("عمق الفاصل", value=None, placeholder="0") # أضفت عمق الفاصل بناء على طلبك

            dr1, dr2, dr3 = st.columns(3)
            dr_n = dr1.number_input("عدد الأدراج", min_value=0, value=0)
            dr_w = dr2.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = dr3.number_input("عمق الدرج", value=None, placeholder="0")

            if st.form_submit_button("✅ تنفيذ التخصيم وإضافته للجدول", use_container_width=True):
                if W and H and D:
                    # --- تطبيق معادلات المهندس ياسين ---
                    # 1. تخصيم الألمنيوم
                    if u_type == "وحدة سفلية" or u_type == "دولاب خزين":
                        h_alum = H - 13 # تخصيم ثابت 13 سم
                        h_final = h_alum # الارتفاع الصافي
                    else:
                        h_final = H - 5 # باقي الوحدات - 5 سم
                    
                    w_final = W - 5
                    d_final = D - 5

                    alum_data = []
                    # الهيكل الأساسي (مفرد ومتقارب)
                    if u_type == "وحدة سفلية":
                        alum_data.append(["قوايم ارتفاع", h_final, 2, "مفرد"])
                        alum_data.append(["قوايم ارتفاع", h_final, 2, "متقارب"])
                        alum_data.append(["عوارض عرض", w_final, 3, "مفرد"])
                        alum_data.append(["عوارض عرض", w_final, 1, "متقارب"])
                        alum_data.append(["عوارض عمق", d_final, 2, "مفرد"])
                        alum_data.append(["عوارض عمق", d_final, 2, "متقارب"])
                    else:
                        alum_data.append(["قوايم ارتفاع", h_final, 2, "مفرد"])
                        alum_data.append(["قوايم ارتفاع", h_final, 2, "متقارب"])
                        alum_data.append(["عوارض عرض", w_final, 2, "مفرد"])
                        alum_data.append(["عوارض عرض", w_final, 2, "متقارب"])
                        alum_data.append(["عوارض عمق", d_final, 0, "مفرد"])
                        alum_data.append(["عوارض عمق", d_final, 4, "متقارب"])

                    # تخصيم الأرفف والفواصل (العدد * 4)
                    if sh_n > 0:
                        alum_data.append(["أعواد أرفف (عرض)", sh_w if sh_w else 0, int(sh_n*4), "مفرد"])
                    if v_n > 0:
                        alum_data.append(["أعواد فواصل (ارتفاع)", v_h if v_h else 0, int(v_n*4), "مفرد"])
                    if dr_n > 0:
                        alum_data.append(["براويز أدراج (عرض)", (dr_w if dr_w else 0) - 2.5, int(dr_n*2), "مفرد"])
                        alum_data.append(["براويز أدراج (عمق)", (dr_d if dr_d else 0), int(dr_n*2), "مفرد"])

                    # 2. تخصيم الفيبر (المعادلة: 195*77)
                    fiber_data = [
                        ["ضهرية", f"{int(w_final)} * {int(h_final)}", 1],
                        ["أرضية", f"{int(w_final)} * {int(d_final)}", 1],
                        ["أجناب", f"{int(h_final)} * {int(d_final)}", 2]
                    ]
                    if sh_n > 0:
                        # تخصيم 5 سم من العرض والعمق للأرفف في الفيبر
                        fiber_data.append(["فيبر أرفف", f"{int((sh_w if sh_w else 5)-5)} * {int((sh_d if sh_d else 5)-5)}", sh_n])
                    if v_n > 0:
                        fiber_data.append(["فيبر فواصل", f"{int((v_h if v_h else 5)-5)} * {int((v_d if v_d else 5)-5)}", v_n])

                    st.session_state.project_list.append({
                        "client": client, "type": u_type, "dims": f"{W}x{H}x{D}",
                        "alum": alum_data, "fiber": fiber_data
                    })
                    st.rerun()

    # --- منطقة النتائج والجرد المنظم ---
    if st.session_state.project_list:
        t1, t2 = st.tabs(["📊 الفاتورة والجرد النهائي", "📋 تفاصيل التخصيم لكل وحدة"])

        with t1:
            st.markdown("<div class='section-header'>قائمة الخامات المطلوبة للمشروع بالكامل</div>", unsafe_allow_html=True)
            
            muf_all, mut_all, fib_all = [], [], []
            for u in st.session_state.project_list:
                for row in u['alum']:
                    if row[2] > 0:
                        if row[3] == "مفرد": muf_all.append({"المقاس": row[1], "العدد": row[2]})
                        else: mut_all.append({"المقاس": row[1], "العدد": row[2]})
                for row in u['fiber']:
                    fib_all.append({"البيان": row[0], "المقاس": row[1], "العدد": row[2]})

            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("🛠️ جرد المفرد")
                if muf_all:
                    df = pd.DataFrame(muf_all).groupby("المقاس").sum().reset_index()
                    st.table(df.sort_values(by="المقاس", ascending=False))
            
            with c2:
                st.subheader("🛠️ جرد المتقارب")
                if mut_all:
                    df = pd.DataFrame(mut_all).groupby("المقاس").sum().reset_index()
                    st.table(df.sort_values(by="المقاس", ascending=False))

            with c3:
                st.subheader("🖼️ جرد الفيبر")
                if fib_all:
                    st.table(pd.DataFrame(fib_all))

        with t2:
            for idx, u in enumerate(st.session_state.project_list):
                with st.expander(f"تفاصيل الوحدة {idx+1}: {u['client']} ({u['dims']})"):
                    ca, cf = st.columns([3, 2])
                    with ca: st.write("**تخصيم الألمنيوم**"); st.table(pd.DataFrame(u['alum'], columns=["البيان", "المقاس", "العدد", "النوع"]))
                    with cf: st.write("**تخصيم الفيبر**"); st.table(pd.DataFrame(u['fiber'], columns=["البيان", "المقاس", "العدد"]))

        if st.button("🗑️ مسح المشروع والبدء من جديد", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

st.markdown("<br><p style='text-align:center; opacity:0.3;'>DOGGA PRO | 2026</p>", unsafe_allow_html=True)
