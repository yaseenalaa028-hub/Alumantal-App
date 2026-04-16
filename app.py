import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (Eng. Yassin Alaa)
# ==========================================
st.set_page_config(page_title="DOGGA SYSTEM", layout="wide")

if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# تطبيق الألوان بناءً على زرار الدرك مود
if st.session_state.dark_mode:
    bg, txt, accent, card_bg = "#0e1117", "#ffffff", "#f1c40f", "#1c1f26"
else:
    bg, txt, accent, card_bg = "#ffffff", "#000000", "#d4ac0d", "#f0f2f6"

# ==========================================
# 2. تصميم الواجهة (CSS)
# ==========================================
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg} !important; color: {txt} !important; direction: rtl !important; text-align: right; }}
    .home-card {{
        background: {card_bg}; padding: 40px; border-radius: 20px;
        border: 4px solid {accent}; text-align: center; margin-top: 30px;
    }}
    .unit-box {{
        background: {card_bg}; border-right: 8px solid {accent};
        padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }}
    .inventory-card {{
        background: {card_bg}; border: 2px solid {accent};
        padding: 20px; border-radius: 15px;
    }}
    header, footer {{ visibility: hidden; }}
    </style>
""", unsafe_allow_html=True)

# الهيدر الثابت (الاسم + زرار الدرك مود)
top_l, top_r = st.columns([10, 2])
with top_l:
    st.markdown(f'<h3 style="color:{accent}; margin:0;">DOGGA SYSTEM | م/ ياسين علاء</h3>', unsafe_allow_html=True)
with top_r:
    btn_label = "🌙 وضع النوم" if not st.session_state.dark_mode else "☀️ وضع النهار"
    if st.button(btn_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 3. الشاشة الرئيسية (القائمة الخارجية)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="home-card">
            <h1 style="color:{accent}; font-size: 3.5em; margin:0;">DOGGA SYSTEM</h1>
            <h2 style="color:{txt}; margin:0;">نظام التخصيم الفني الشامل</h2>
            <p style="color:{accent}; font-size: 1.5em; margin:10px 0;">برمجة وتطوير المهندس: <b>ياسين علاء</b></p>
            <hr style="border:1px solid {accent}; width:30%; margin:auto;">
            <p style="margin-top:15px;">دقة في حسابات المفرد والمتقارب والفيبر لكل قطعة</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("➕ إضافة مقاسات وتخصيم", use_container_width=True, type="primary"):
            st.session_state.page = 'calc'
            st.rerun()
    with c2:
        if st.button("📊 جرد الخامات الكلي", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()
    with c3:
        if st.button("📄 عرض شيتات التفصيل", use_container_width=True):
            st.session_state.page = 'report'
            st.rerun()

# ==========================================
# 4. ورشة العمل (إدخال المقاسات)
# ==========================================
elif st.session_state.page == 'calc':
    st.markdown(f'<h2 style="color:{accent};">📏 ورشة إدخال المقاسات</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'home'; st.rerun()

    with st.container():
        # خانات الإدخال بدون أصفار (Placeholder)
        r1c1, r1c2 = st.columns(2)
        with r1c1: u_client = st.text_input("اسم العميل / الوحدة", placeholder="اكتب هنا...")
        with r1c2: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1: w_in = st.number_input("العرض (W)", value=None, placeholder="0")
        with r2c2: h_in = st.number_input("الارتفاع (H)", value=None, placeholder="0")
        with r2c3: d_in = st.number_input("العمق (D)", value=None, placeholder="0")
        
        st.write("---")
        # الإضافات (أرفف، فواصل، أدراج)
        ax, ay, az = st.columns(3)
        with ax:
            sh_n = st.number_input("عدد الأرفف", value=0, step=1)
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0")
        with ay:
            v_n = st.number_input("عدد الفواصل", value=0, step=1)
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            v_d = st.number_input("عمق الفاصل", value=None, placeholder="0")
        with az:
            dr_n = st.number_input("عدد الأدراج", value=0, step=1)
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0")

    if st.button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
        if w_in and h_in:
            # التخصيمات (13 للسفلية، 5 للباقي)
            h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
            h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

            # توزيع الألومنيوم
            if u_type == "وحدة سفلية":
                alum = [["ارتفاع", h_net, 2, 2], ["عرض", w_net, 3, 1], ["عمق", d_net, 2, 2]]
            else:
                alum = [["ارتفاع", h_net, 2, 2], ["عرض", w_net, 2, 2], ["عمق", d_net, 0, 4]]
            
            # حساب الإضافات (العدد × 4 مفرد)
            if sh_n > 0: alum.append([f"أرفف ({sh_n})", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
            if v_n > 0: alum.append([f"فواصل ({v_n})", int(v_h), v_n*4, 0])
            if dr_n > 0: alum.append([f"أدراج ({dr_n})", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

            # حساب الفيبر
            fiber = [["ظهرية", f"{w_net}x{h_net}", 1], ["أرضية", f"{w_net}x{d_net}", 1], ["أجناب", f"{h_net}x{d_net}", 2]]
            if sh_n > 0: fiber.append(["رفوف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

            st.session_state.project_list.append({
                "client": u_client, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                "alum": alum, "fiber": fiber,
                "muf": sum([x[2] for x in alum]), "mut": sum([x[3] for x in alum])
            })
            st.session_state.page = 'home'
            st.rerun()

# ==========================================
# 5. جرد الخامات (مفرد/متقارب/فيبر)
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown(f'<h2 style="color:{accent};">📊 جرد خامات المشروع بالكامل</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'home'; st.rerun()

    if not st.session_state.project_list:
        st.warning("لا يوجد وحدات مضافة بعد.")
    else:
        total_muf = sum([x['muf'] for x in st.session_state.project_list])
        total_mut = sum([x['mut'] for x in st.session_state.project_list])
        total_fiber_pcs = sum([len(x['fiber']) for x in st.session_state.project_list])

        st.markdown(f"""
            <div class="inventory-card">
                <h3>📋 الطلبية المطلوبة:</h3>
                <p>📍 إجمالي قطع الألومنيوم (المفرد): <b>{total_muf} قطعة</b></p>
                <p>📍 إجمالي قطع الألومنيوم (المتقارب): <b>{total_mut} قطعة</b></p>
                <p>📍 إجمالي عدد قطع الفيبر: <b>{total_fiber_pcs} قطعة</b></p>
                <hr>
                <p>💡 تقدير الألومنيوم بالأعواد: <b>{round((total_muf + total_mut)*0.5, 1)} عود تقريباً</b></p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 6. شيتات التفصيل
# ==========================================
elif st.session_state.page == 'report':
    st.markdown(f'<h2 style="color:{accent};">📄 شيتات التفصيل لكل وحدة</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'home'; st.rerun()

    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f'<div class="unit-box">📌 {item["client"]} | {item["dims"]}</div>', unsafe_allow_html=True)
            ca, cf = st.columns([3, 2])
            with ca: st.table(pd.DataFrame(item['alum'], columns=["البيان", "المقاس", "مفرد", "متقارب"]))
            with cf: st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))

    if st.button("🗑️ مسح المشروع"):
        st.session_state.project_list = []
        st.rerun()

st.markdown(f"<p style='text-align:center; color:{accent}; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير م/ ياسين علاء</p>", unsafe_allow_html=True)
