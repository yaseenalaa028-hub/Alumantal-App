import streamlit as st
import pandas as pd

# --- إعدادات الصفحة ---
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# --- إدارة الحالة ---
if 'project_list' not in st.session_state:
    st.session_state.project_list = []

# --- التصميم (CSS) - تقليل حجم اللوجو وتنسيق الجداول ---
st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right; }
    /* تصغير اللوجو */
    .mini-logo {
        border: 1px solid #f1c40f;
        padding: 5px 15px;
        border-radius: 5px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .unit-card { border-right: 5px solid #f1c40f; padding: 10px; background: #1c1f26; border-radius: 8px; margin-bottom: 15px; }
    .inventory-box { background-color: #f1c40f; color: #000; padding: 15px; border-radius: 10px; font-weight: bold; }
    header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# لوجو صغير في الأعلى
st.markdown('<div class="mini-logo"><b style="color:#f1c40f;">DOGGA SYSTEM</b> | م/ ياسين علاء</div>', unsafe_allow_html=True)

# --- خانات الإدخال بالترتيب الجديد ---
with st.container():
    st.subheader("📝 إدخال بيانات الوحدة")
    r1_c1, r1_c2, r1_c3, r1_c4, r1_c5 = st.columns([2, 2, 1, 1, 1])
    
    with r1_c1:
        u_name = st.text_input("اسم العميل / كود الوحدة")
    with r1_c2:
        u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
    with r1_c3:
        w_in = st.number_input("العرض (W)", value=0.0)
    with r1_c4:
        h_in = st.number_input("الارتفاع (H)", value=0.0)
    with r1_c5:
        d_in = st.number_input("العمق (D)", value=0.0)

    st.markdown("---")
    # خانات الرفوف والأدراج والفواصل
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r2_c1:
        st.caption("➕ الأرفف")
        sh_n = st.number_input("العدد", key="shn", value=0)
        sh_w = st.number_input("عرض الرف", key="shw", value=0.0)
        sh_d = st.number_input("عمق الرف", key="shd", value=0.0)
    with r2_c2:
        st.caption("➕ الفواصل")
        v_n = st.number_input("العدد", key="vn", value=0)
        v_h = st.number_input("ارتفاع الفاصل", key="vh", value=0.0)
        v_d = st.number_input("عمق الفاصل", key="vd", value=0.0)
    with r2_c3:
        st.caption("➕ الأدراج")
        dr_n = st.number_input("العدد", key="drn", value=0)
        dr_w = st.number_input("عرض الدرج", key="drw", value=0.0)
        dr_d = st.number_input("عمق الدرج", key="drd", value=0.0)

    if st.button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
        if w_in > 0 and h_in > 0:
            # الحسابات بناءً على القائمة اللي بعتها
            h_ded = 13 if (u_type == "وحدة سفلية" or u_type == "دولاب خزين") else 5
            h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

            # 1. تخصيم الألومنيوم
            if u_type == "وحدة سفلية":
                alum_list = [
                    ["قوايم ارتفاع", h_net, 2, 2],
                    ["عوارض عرض", w_net, 3, 1],
                    ["عوارض عمق", d_net, 2, 2]
                ]
            else:
                alum_list = [
                    ["قوايم ارتفاع", h_net, 2, 2],
                    ["عوارض عرض", w_net, 2, 2],
                    ["عوارض عمق", d_net, 0, 4]
                ]
            
            # إضافة الرفوف والفواصل (ألومنيوم 4 قطع لكل وحدة)
            if sh_n > 0: alum_list.append([f"أعواد رفوف ({sh_n})", f"ع:{int(sh_w)}/عق:{int(sh_d)}", sh_n*4, 0])
            if v_n > 0: alum_list.append([f"أعواد فواصل ({v_n})", int(v_h), v_n*4, 0])
            if dr_n > 0: alum_list.append([f"براويز أدراج ({dr_n})", f"ع:{dr_w-2.5}/عق:{dr_d}", dr_n*4, 0])

            # 2. تخصيم الفيبر
            fiber_list = [
                ["الظهرية", f"{w_net} × {h_net}", 1],
                ["الأرضية", f"{w_net} × {d_net}", 1],
                ["الأجناب", f"{h_net} × {d_net}", 2]
            ]
            if sh_n > 0: fiber_list.append(["فيبر أرفف", f"{int(sh_w-5)} × {int(sh_d-5)}", sh_n])
            if v_n > 0: fiber_list.append(["فيبر فواصل", f"{int(v_h-5)} × {int(v_d-5)}", v_n])

            st.session_state.project_list.append({
                "client": u_name,
                "type": u_type,
                "dims": f"{w_in}x{h_in}x{d_in}",
                "alum": pd.DataFrame(alum_list, columns=["البيان", "المقاس", "مفرد", "متقارب"]),
                "fiber": pd.DataFrame(fiber_list, columns=["القطعة", "المقاس", "العدد"]),
                "raw_m": (h_net*4 + w_net*4 + d_net*4) # للجرد الكلي
            })
            st.rerun()

# --- عرض النتائج والقائمة الخارجية ---
if st.session_state.project_list:
    st.divider()
    
    # القائمة الخارجية (الجرد الكلي للمشروع)
    st.subheader("📊 قائمة جرد خامات المشروع (فاتورة المورد)")
    total_rods = sum([x['raw_m'] for x in st.session_state.project_list]) / 600
    
    c_inv1, c_inv2 = st.columns(2)
    with c_inv1:
        st.markdown(f'<div class="inventory-box">إجمالي الألومنيوم المطلوب: {round(total_rods, 1)} عود (6 متر)</div>', unsafe_allow_html=True)
    with c_inv2:
        total_fiber_units = len(st.session_state.project_list)
        st.markdown(f'<div class="inventory-box">عدد الوحدات الجاري تفصيلها: {total_fiber_units} وحدة</div>', unsafe_allow_html=True)

    st.write("---")
    
    # تفاصيل كل وحدة
    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f'<div class="unit-card"><b>وحدة #{i+1}: {item["client"]} | {item["type"]} | {item["dims"]}</b></div>', unsafe_allow_html=True)
            res_c1, res_c2 = st.columns([3, 2])
            with res_c1:
                st.table(item['alum'])
            with res_c2:
                st.table(item['fiber'])

    if st.button("🗑️ تفريغ المشروع بالكامل"):
        st.session_state.project_list = []
        st.rerun()

st.markdown("<br><p style='text-align:center; font-size:0.8em;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
