import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة الأساسية
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إدارة الذاكرة (Session State)
# ==========================================
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# تطبيق نظام الألوان (Dark/Light)
if st.session_state.dark_mode:
    bg, txt, accent, card_bg = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card_bg = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

# ==========================================
# 3. تصميم الواجهة (CSS الكامل)
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ 
        background-color: {bg} !important; 
        color: {txt} !important; 
        direction: rtl !important; 
        text-align: right; 
    }}
    .main-title-box {{
        text-align: center;
        border: 3px solid {accent};
        padding: 15 / 1.5px;
        border-radius: 15px;
        margin-bottom: 25px;
        background-color: {card_bg};
    }}
    .unit-card {{
        border-right: 10px solid {accent};
        padding: 20px;
        background-color: {card_bg};
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }}
    .stTable {{
        background-color: {card_bg} !important;
        border-radius: 8px !important;
    }}
    .inventory-header {{
        background-color: {accent};
        color: #000;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. الهيدر (الاسم + التحكم)
# ==========================================
top_col1, top_col2 = st.columns([10, 2])
with top_col1:
    st.markdown(f'<h2 style="color:{accent}; margin:0;">DOGGA SYSTEM | م/ ياسين علاء</h2>', unsafe_allow_html=True)
with top_col2:
    if st.button("🌙/☀️ تبديل الوضع", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 5. اللوحة الرئيسية (إدخال البيانات)
# ==========================================
st.markdown('<div class="main-title-box"><h1>📋 اللوحة الرئيسية لإدخال المقاسات</h1></div>', unsafe_allow_html=True)

with st.container():
    # ترتيب الخانات: العميل -> النوع -> المقاسات
    r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns([2, 2, 1, 1, 1])
    with r1c1: client_name = st.text_input("اسم العميل / كود الوحدة")
    with r1c2: unit_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
    with r1c3: w_total = st.number_input("العرض الكلي (W)", min_value=0.0, format="%.1f")
    with r1c4: h_total = st.number_input("الارتفاع الكلي (H)", min_value=0.0, format="%.1f")
    with r1c5: d_total = st.number_input("العمق الكلي (D)", min_value=0.0, format="%.1f")

    st.markdown("---")
    # تفاصيل الأرفف والفواصل والأدراج
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        st.markdown(f"<b style='color:{accent};'>📦 الأرفف</b>", unsafe_allow_html=True)
        shelf_n = st.number_input("عدد الأرفف", min_value=0, step=1)
        shelf_w = st.number_input("عرض الرف", min_value=0.0)
        shelf_d = st.number_input("عمق الرف", min_value=0.0)
    with r2c2:
        st.markdown(f"<b style='color:{accent};'>↕️ الفواصل</b>", unsafe_allow_html=True)
        v_n = st.number_input("عدد الفواصل", min_value=0, step=1)
        v_h = st.number_input("ارتفاع الفاصل", min_value=0.0)
        v_d = st.number_input("عمق الفاصل", min_value=0.0)
    with r2c3:
        st.markdown(f"<b style='color:{accent};'>🗄️ الأدراج</b>", unsafe_allow_html=True)
        draw_n = st.number_input("عدد الأدراج", min_value=0, step=1)
        draw_w = st.number_input("عرض برواز الدرج", min_value=0.0)
        draw_d = st.number_input("عمق الدرج", min_value=0.0)

    # زر الحفظ والتنفيذ
    if st.button("🚀 تنفيذ التخصيم الفني وحفظ الوحدة", use_container_width=True):
        if w_total > 0 and h_total > 0:
            # --- معادلات التخصيم (بناءً على تعليماتك) ---
            # 1. تخصيم الألومنيوم الأساسي
            h_deduction = 13 if (unit_type == "وحدة سفلية" or unit_type == "دولاب خزين") else 5
            h_net = int(h_total - h_deduction)
            w_net = int(w_total - 5)
            d_net = int(d_total - 5)

            # توزيع الألومنيوم (مفرد ومتقارب)
            if unit_type == "وحدة سفلية":
                alum_rows = [
                    ["قوايم ارتفاع", h_net, 2, 2],
                    ["عوارض عرض", w_net, 3, 1],
                    ["عوارض عمق", d_net, 2, 2]
                ]
            else:
                # باقي الوحدات (الارتفاع والعرض 2 مفرد/2 متقارب، العمق 4 متقارب)
                alum_rows = [
                    ["قوايم ارتفاع", h_net, 2, 2],
                    ["عوارض عرض", w_net, 2, 2],
                    ["عوارض عمق", d_net, 0, 4]
                ]

            # حسابات الإضافات (الألومنيوم = العدد × 4 مفرد)
            if shelf_n > 0: alum_rows.append([f"أعواد أرفف ({shelf_n})", f"ع:{int(shelf_w)} / عق:{int(shelf_d)}", shelf_n*4, 0])
            if v_n > 0: alum_rows.append([f"أعواد فواصل ({v_n})", int(v_h), v_n*4, 0])
            if draw_n > 0: alum_rows.append([f"براويز أدراج ({draw_n})", f"عرض {draw_w-2.5} / عمق {draw_d}", draw_n*4, 0])

            # 2. تخصيم الفيبر (الضهرية، الأرضية، الأجناب)
            fiber_rows = [
                ["الظهرية", f"{w_net} × {h_net}", 1],
                ["الأرضية", f"{w_net} × {d_net}", 1],
                ["الأجناب", f"{h_net} × {d_net}", 2]
            ]
            # تخصيم فيبر الأرفف والفواصل (خصم 5 سم من العرض والعمق)
            if shelf_n > 0: fiber_rows.append(["فيبر أرفف", f"{int(shelf_w-5)} × {int(shelf_d-5)}", shelf_n])
            if v_n > 0: fiber_rows.append(["فيبر فواصل", f"{int(v_h-5)} × {int(v_d-5)}", v_n])

            # حفظ في القائمة الكلية
            st.session_state.project_list.append({
                "client": client_name,
                "type": unit_type,
                "dims": f"{w_total}x{h_total}x{d_total}",
                "alum_df": pd.DataFrame(alum_rows, columns=["البيان", "المقاس", "مفرد", "متقارب"]),
                "fiber_df": pd.DataFrame(fiber_rows, columns=["القطعة", "المقاس", "العدد"]),
                "raw_cm": (h_net*4 + w_net*4 + d_net*4) + (shelf_n*shelf_w*4 if shelf_n > 0 else 0)
            })
            st.rerun()

# ==========================================
# 6. القائمة الخارجية (شيت التفصيل والجرد)
# ==========================================
if st.session_state.project_list:
    st.write("---")
    st.markdown('<div class="inventory-header">📊 بيان جرد خامات المشروع (القائمة الخارجية)</div>', unsafe_allow_html=True)
    
    # حساب إجمالي الألومنيوم المطلوب
    total_rods = sum([x['raw_cm'] for x in st.session_state.project_list]) / 600
    st.info(f"💡 إجمالي الألومنيوم المطلوب لهذا المشروع: **{round(total_rods, 1)} عود** (طول 6 متر)")

    # عرض تفاصيل كل وحدة بشكل مستقل
    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f"""
                <div class="unit-card">
                    <h3 style="margin:0;">📌 وحدة #{i+1}: {item['client']}</h3>
                    <p style="margin:5px 0;">النوع: {item['type']} | المقاس الكلي: {item['dims']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            c_alum, c_fiber = st.columns([3, 2])
            with c_alum:
                st.markdown(f"<b style='color:{accent};'>🔗 شيت تقطيع الألومنيوم</b>", unsafe_allow_html=True)
                st.table(item['alum_df'])
            with c_fiber:
                st.markdown(f"<b style='color:{accent};'>✨ شيت تفصيل الفيبر</b>", unsafe_allow_html=True)
                st.table(item['fiber_df'])

    st.write("---")
    if st.button("🗑️ مسح بيانات المشروع بالكامل والبدء من جديد", use_container_width=True):
        st.session_state.project_list = []
        st.rerun()

# التذييل
st.markdown(f"<p style='text-align:center; color:{accent}; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
