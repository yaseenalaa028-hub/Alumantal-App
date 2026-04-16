import streamlit as st
import pandas as pd

# --- إعدادات الصفحة ---
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# --- إدارة الحالة ---
if 'project_list' not in st.session_state:
    st.session_state.project_list = []

# --- التصميم (CSS) ---
st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right; }
    .unit-card { border-right: 10px solid #f1c40f; padding: 15px; background: #1c1f26; border-radius: 10px; margin-bottom: 20px; }
    .section-head { color: #f1c40f; border-bottom: 1px solid #f1c40f; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛠️ منظومة DOGGA SYSTEM للتخصيم الفني")
st.caption("تطوير المهندس ياسين علاء")

# --- مدخلات البيانات ---
with st.expander("📝 إضافة وحدة جديدة", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        u_name = st.text_input("اسم/كود الوحدة")
        u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
    with c2:
        w_in = st.number_input("العرض الكلي (سم)", value=0.0)
        h_in = st.number_input("الارتفاع الكلي (سم)", value=0.0)
    with c3:
        d_in = st.number_input("العمق الكلي (سم)", value=0.0)

    st.markdown("---")
    cx, cy, cz = st.columns(3)
    with cx:
        sh_n = st.number_input("عدد الأرفف", value=0, step=1)
        sh_w = st.number_input("عرض الرف", value=0.0)
        sh_d = st.number_input("عمق الرف", value=0.0)
    with cy:
        v_n = st.number_input("عدد الفواصل", value=0, step=1)
        v_h = st.number_input("ارتفاع الفاصل", value=0.0)
        v_d = st.number_input("عمق الفاصل", value=0.0)
    with cz:
        dr_n = st.number_input("عدد الأدراج", value=0, step=1)
        dr_w = st.number_input("عرض الدرج", value=0.0)
        dr_d = st.number_input("عمق الدرج", value=0.0)

    if st.button("🚀 تنفيذ التخصيم وحفظ الوحدة", use_container_width=True):
        if w_in > 0 and h_in > 0:
            # 1. حسابات الألومنيوم الأساسية
            # السفلية ودولاب الخزين يشيلوا 13 سم من الارتفاع، الباقي 5 سم
            h_ded = 13 if (u_type == "وحدة سفلية" or u_type == "دولاب خزين") else 5
            h_net = h_in - h_ded
            w_net = w_in - 5
            d_net = d_in - 5

            # توزيع الألومنيوم (مفرد ومتقارب)
            if u_type == "وحدة سفلية":
                alum_data = [
                    {"البيان": "قوايم الارتفاع", "المقاس": h_net, "مفرد": 2, "متقارب": 2},
                    {"البيان": "عوارض العرض", "المقاس": w_net, "مفرد": 3, "متقارب": 1},
                    {"البيان": "عوارض العمق", "المقاس": d_net, "مفرد": 2, "متقارب": 2}
                ]
            else:
                alum_data = [
                    {"البيان": "قوايم الارتفاع", "المقاس": h_net, "مفرد": 2, "متقارب": 2},
                    {"البيان": "عوارض العرض", "المقاس": w_net, "مفرد": 2, "متقارب": 2},
                    {"البيان": "عوارض العمق", "المقاس": d_net, "مفرد": 0, "متقارب": 4}
                ]

            # إضافات الأرفف والفواصل (العدد في 4 ألومنيوم)
            if sh_n > 0: alum_data.append({"البيان": f"أعواد أرفف ({sh_n})", "المقاس": f"ع:{int(sh_w)}/عق:{int(sh_d)}", "مفرد": sh_n*4, "متقارب": 0})
            if v_n > 0: alum_data.append({"البيان": f"أعواد فواصل ({v_n})", "المقاس": f"{int(v_h)}", "مفرد": v_n*4, "متقارب": 0})
            if dr_n > 0: 
                # تخصيم الدرج: العرض -2.5 والعمق كما هو
                alum_data.append({"البيان": f"براويز أدراج ({dr_n})", "المقاس": f"ع:{dr_w-2.5}/عق:{dr_d}", "مفرد": dr_n*4, "متقارب": 0})

            # 2. حسابات الفيبر
            fiber_data = [
                {"القطعة": "الظهرية", "المقاس": f"{int(w_net)} × {int(h_net)}", "العدد": 1},
                {"القطعة": "الأرضية", "المقاس": f"{int(w_net)} × {int(d_net)}", "العدد": 1},
                {"القطعة": "الأجناب", "المقاس": f"{int(h_net)} × {int(d_net)}", "العدد": 2}
            ]
            if sh_n > 0: fiber_data.append({"القطعة": "فيبر أرفف", "المقاس": f"{int(sh_w-5)} × {int(sh_d-5)}", "العدد": sh_n})
            if v_n > 0: fiber_data.append({"القطعة": "فيبر فواصل", "المقاس": f"{int(v_h-5)} × {int(v_d-5)}", "العدد": v_n})

            # حفظ البيانات
            st.session_state.project_list.append({
                "info": f"{u_name} ({u_type}) - {w_in}x{h_in}x{d_in}",
                "alum": pd.DataFrame(alum_data),
                "fiber": pd.DataFrame(fiber_data),
                "total_m": (h_net*4 + w_net*4 + d_net*4) / 100 # تقريبي للمتر
            })
            st.rerun()

# --- عرض النتائج وفاتورة الخامات ---
if st.session_state.project_list:
    st.write("---")
    st.header("📋 شيت التفصيل الكامل")
    
    for item in st.session_state.project_list:
        with st.container():
            st.markdown(f'<div class="unit-card"><b>📌 {item["info"]}</b></div>', unsafe_allow_html=True)
            col_alum, col_fiber = st.columns([3, 2])
            with col_alum:
                st.markdown("**🔍 تخصيم الألومنيوم**")
                st.table(item['alum'])
            with col_fiber:
                st.markdown("**✨ تخصيم الفيبر**")
                st.table(item['fiber'])

    st.write("---")
    if st.button("🗑️ مسح جميع البيانات"):
        st.session_state.project_list = []
        st.rerun()

st.markdown("<p style='text-align:center;'>DOGGA SYSTEM 2026 | المهندس ياسين علاء</p>", unsafe_allow_html=True)
