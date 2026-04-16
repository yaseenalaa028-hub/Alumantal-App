import streamlit as st
import pandas as pd

# --- إعدادات النظام ---
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# --- إدارة الذاكرة والتنقل ---
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'home'  # البداية من القائمة الخارجية

# --- تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right; }
    .home-card {
        background: linear-gradient(135deg, #1c1f26 0%, #343a40 100%);
        padding: 60px;
        border-radius: 25px;
        border: 4px solid #f1c40f;
        text-align: center;
        margin: 50px auto;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }
    .main-btn {
        background-color: #f1c40f !important;
        color: black !important;
        font-weight: bold !important;
        font-size: 20px !important;
        padding: 15px 30px !important;
    }
    .unit-title {
        background: #f1c40f;
        color: black;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 20px;
    }
    header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. القائمة الخارجية (الشاشة الرئيسية)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
        <div class="home-card">
            <h1 style="color:#f1c40f; font-size: 4em; margin-bottom: 0;">DOGGA SYSTEM</h1>
            <h2 style="color:white; margin-top: 0;">أقوى نظام لتخصيم المطابخ والدريسنج</h2>
            <hr style="border: 1px solid #f1c40f; width: 50%;">
            <p style="color:#f1c40f; font-size: 1.5em;">بلمسة المهندس الخبير: <b>ياسين علاء</b></p>
            <p style="color:#bdc3c7;">دقة متناهية في التخصيم .. جودة في التنفيذ .. سرعة في الأداء</p>
            <br>
        </div>
    """, unsafe_allow_html=True)
    
    col_entry = st.columns([1, 2, 1])
    with col_entry[1]:
        if st.button("🚀 الدخول لمنظومة التخصيم الآن", use_container_width=True):
            st.session_state.page = 'calc'
            st.rerun()

# ==========================================
# 2. قائمة التخصيم (ورشة العمل)
# ==========================================
elif st.session_state.page == 'calc':
    st.markdown('<h2 style="color:#f1c40f; border-bottom: 2px solid #f1c40f;">🛠️ ورشة عمل المقاسات</h2>', unsafe_allow_html=True)
    
    if st.button("⬅️ الرجوع للرئيسية"):
        st.session_state.page = 'home'
        st.rerun()

    # خانات الإدخال بدون أصفار افتراضية (value=None)
    with st.container():
        st.write("### 📝 بيانات الوحدة الجديدة")
        c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 1, 1])
        with c1: u_client = st.text_input("اسم العميل / كود الوحدة", placeholder="اكتب هنا...")
        with c2: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        with c3: w_in = st.number_input("العرض (W)", value=None, placeholder="0.0")
        with c4: h_in = st.number_input("الارتفاع (H)", value=None, placeholder="0.0")
        with c5: d_in = st.number_input("العمق (D)", value=None, placeholder="0.0")

        st.write("---")
        # الإضافات
        cx, cy, cz = st.columns(3)
        with cx:
            st.caption("📦 الأرفف")
            sh_n = st.number_input("العدد", step=1, value=0)
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
        with cy:
            st.caption("↕️ الفواصل")
            v_n = st.number_input("عدد الفواصل", step=1, value=0)
            v_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0.0")
            v_d = st.number_input("عمق الفاصل", value=None, placeholder="0.0")
        with cz:
            st.caption("🗄️ الأدراج")
            dr_n = st.number_input("عدد الأدراج", step=1, value=0)
            dr_w = st.number_input("عرض برواز الدرج", value=None, placeholder="0.0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0.0")

    if st.button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
        if w_in and h_in:
            # منطق التخصيم (المهندس ياسين)
            h_ded = 13 if (u_type == "وحدة سفلية" or u_type == "دولاب خزين") else 5
            h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

            # جداول منفصلة للألومنيوم والفيبر
            if u_type == "وحدة سفلية":
                alum = [["قوايم ارتفاع", h_net, 2, 2], ["عوارض عرض", w_net, 3, 1], ["عوارض عمق", d_net, 2, 2]]
            else:
                alum = [["قوايم ارتفاع", h_net, 2, 2], ["عوارض عرض", w_net, 2, 2], ["عوارض عمق", d_net, 0, 4]]
            
            # إضافات الألومنيوم
            if sh_n > 0: alum.append([f"أعواد أرفف ({sh_n})", f"{int(sh_w)}x{int(sh_d)}", sh_n*4, 0])
            if v_n > 0: alum.append([f"أعواد فواصل ({v_n})", int(v_h), v_n*4, 0])
            if dr_n > 0: alum.append([f"براويز درج ({dr_n})", f"{dr_w-2.5}x{dr_d}", dr_n*4, 0])

            # الفيبر المنفصل
            fiber = [["الظهرية", f"{w_net}x{h_net}", 1], ["الأرضية", f"{w_net}x{d_net}", 1], ["الأجناب", f"{h_net}x{d_net}", 2]]
            if sh_n > 0: fiber.append(["فيبر رف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])

            st.session_state.project_list.append({
                "client": u_client, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                "alum_df": pd.DataFrame(alum, columns=["البيان", "المقاس", "مفرد", "متقارب"]),
                "fiber_df": pd.DataFrame(fiber, columns=["القطعة", "المقاس", "العدد"])
            })
            st.success("تم التخصيم بنجاح!")

    # عرض النتائج تحت بعض بشكل منظم
    if st.session_state.project_list:
        st.write("---")
        for i, item in enumerate(st.session_state.project_list):
            st.markdown(f'<div class="unit-title">وحدة #{i+1}: {item["client"]} - {item["dims"]}</div>', unsafe_allow_html=True)
            col_a, col_f = st.columns([3, 2])
            with col_a:
                st.write("**📏 تفصيل الألومنيوم:**")
                st.table(item['alum_df'])
            with col_f:
                st.write("**✨ تفصيل الفيبر:**")
                st.table(item['fiber_df'])

        if st.button("🗑️ مسح جميع المقاسات"):
            st.session_state.project_list = []
            st.rerun()

st.markdown("<p style='text-align:center; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير م/ ياسين علاء</p>", unsafe_allow_html=True)
