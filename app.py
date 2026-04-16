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

# ==========================================
# 2. تصميم الواجهة (CSS)
# ==========================================
st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right; background-color: #0e1117; color: white; }
    .home-card {
        background: #1c1f26; padding: 40px; border-radius: 20px;
        border: 4px solid #f1c40f; text-align: center; margin-top: 30px;
    }
    .inventory-card {
        background: #262730; border: 2px solid #f1c40f;
        padding: 20px; border-radius: 15px; margin-top: 20px;
    }
    .unit-box {
        background: #1c1f26; border-right: 8px solid #f1c40f;
        padding: 15px; border-radius: 10px; margin-bottom: 20px;
    }
    header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. الشاشة الرئيسية (الواجهة الخارجية)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="home-card">
            <h1 style="color:#f1c40f; font-size: 3.5em; margin:0;">DOGGA SYSTEM</h1>
            <h2 style="color:white; margin:0;">نظام التخصيم الفني الشامل</h2>
            <p style="color:#f1c40f; font-size: 1.5em; margin:10px 0;">برمجة وتطوير المهندس: <b>ياسين علاء</b></p>
            <hr style="border:1px solid #f1c40f; width:30%; margin:auto;">
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, c_btn3 = st.columns(3)
    with c_btn1:
        if st.button("➕ إضافة مقاسات وتخصيم", use_container_width=True, type="primary"):
            st.session_state.page = 'calc'
            st.rerun()
    with c_btn2:
        if st.button("📊 جرد الخامات (مفرد/متقارب/فيبر)", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()
    with c_btn3:
        if st.button("📄 عرض شيتات التفصيل", use_container_width=True):
            st.session_state.page = 'report'
            st.rerun()

# ==========================================
# 4. صفحة الإدخال والحسابات
# ==========================================
elif st.session_state.page == 'calc':
    st.markdown('<h2 style="color:#f1c40f;">📏 إدخال المقاسات</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'home'; st.rerun()

    with st.form("input_form"):
        r1c1, r1c2 = st.columns(2)
        with r1c1: u_client = st.text_input("اسم العميل / الوحدة", placeholder="...")
        with r1c2: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1: w_in = st.number_input("العرض", value=None, placeholder="0")
        with r2c2: h_in = st.number_input("الارتفاع", value=None, placeholder="0")
        with r2c3: d_in = st.number_input("العمق", value=None, placeholder="0")
        
        st.write("---")
        # الإضافات
        a1, a2, a3 = st.columns(3)
        with a1:
            sh_n = st.number_input("عدد الأرفف", value=0)
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0")
        with a2:
            v_n = st.number_input("عدد الفواصل", value=0)
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0")
            v_d = st.number_input("عمق الفاصل", value=None, placeholder="0")
        with a3:
            dr_n = st.number_input("عدد الأدراج", value=0)
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0")

        if st.form_submit_button("✅ حفظ وتخصيم الآن", use_container_width=True):
            if w_in and h_in:
                # منطق التخصيم
                h_ded = 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else 5
                h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

                # ألومنيوم
                if u_type == "وحدة سفلية":
                    alum = [["ارتفاع", h_net, 2, 2], ["عرض", w_net, 3, 1], ["عمق", d_net, 2, 2]]
                else:
                    alum = [["ارتفاع", h_net, 2, 2], ["عرض", w_net, 2, 2], ["عمق", d_net, 0, 4]]
                
                if sh_n > 0: alum.append(["أعواد رف", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
                if v_n > 0: alum.append(["أعواد فاصل", int(v_h), v_n*4, 0])
                if dr_n > 0: alum.append(["برواز درج", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

                # فيبر
                fiber = [["ظهرية", f"{w_net}x{h_net}", 1], ["أرضية", f"{w_net}x{d_net}", 1], ["أجناب", f"{h_net}x{d_net}", 2]]
                if sh_n > 0: fiber.append(["رفوف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

                st.session_state.project_list.append({
                    "client": u_client, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                    "alum": alum, "fiber": fiber,
                    "m_muf": sum([x[2] for x in alum]), "m_mut": sum([x[3] for x in alum])
                })
                st.session_state.page = 'home'
                st.rerun()

# ==========================================
# 5. صفحة جرد الخامات (التي سألت عنها)
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown('<h2 style="color:#f1c40f;">📊 قائمة جرد خامات المشروع</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'home'; st.rerun()

    if not st.session_state.project_list:
        st.warning("لا توجد بيانات حالياً.")
    else:
        # حساب الإجماليات
        t_muf = sum([x['m_muf'] for x in st.session_state.project_list])
        t_mut = sum([x['m_mut'] for x in st.session_state.project_list])
        t_fib = sum([len(x['fiber']) for x in st.session_state.project_list])

        st.markdown(f"""
            <div class="inventory-card">
                <h3>ملخص الطلبية:</h3>
                <p>✅ إجمالي عدد قطع (المفرد): <b>{t_muf} قطعة</b></p>
                <p>✅ إجمالي عدد قطع (المتقارب): <b>{t_mut} قطعة</b></p>
                <p>✅ إجمالي عدد قطع الفيبر: <b>{t_fib} قطعة</b></p>
                <hr>
                <p>💡 تقدير الألومنيوم: <b>{round((t_muf + t_mut)*0.5, 1)} عود تقريباً</b></p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 6. صفحة شيتات التفصيل
# ==========================================
elif st.session_state.page == 'report':
    st.markdown('<h2 style="color:#f1c40f;">📄 شيتات التفصيل</h2>', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'home'; st.rerun()

    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f'<div class="unit-box">📌 وحدة #{i+1}: {item["client"]}</div>', unsafe_allow_html=True)
            ca, cf = st.columns([3, 2])
            with ca: st.table(pd.DataFrame(item['alum'], columns=["البيان", "المقاس", "مفرد", "متقارب"]))
            with cf: st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))

st.markdown("<p style='text-align:center; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
