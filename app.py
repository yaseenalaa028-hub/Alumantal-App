import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AL-PRINCE PROFESSIONAL SYSTEM", layout="wide")

# الستايل البروفيشينال (أصفر ورشة + أسود ملكي + تصميم فخم)
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; 
        border: 2px solid #2f3640; font-size: 19px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2f3640; color: #fbc531; }
    
    .report-card {
        background-color: white; padding: 35px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); direction: rtl; text-align: right;
        border-right: 15px solid #fbc531; margin-bottom: 30px; border-left: 1px solid #dcdde1;
    }
    .welcome-card {
        background: linear-gradient(135deg, #2f3640 0%, #1e272e 100%);
        padding: 60px; border-radius: 30px; color: #fbc531; text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4); margin-top: 50px;
    }
    .title-line { font-size: 30px; font-weight: bold; color: #1e3799; border-bottom: 4px solid #fbc531; padding-bottom: 12px; margin-bottom: 25px; }
    .section-label { color: #e84118; font-size: 24px; margin-top: 30px; font-weight: bold; border-right: 8px solid #e84118; padding-right: 15px; background: #fff5f5; }
    .data-line { font-size: 21px; margin: 15px 0; color: #2f3640; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 8px; }
    .highlight-blue { color: #0984e3; }
    .header-text { color: #2f3640; font-weight: bold; text-align: center; margin-bottom: 40px; font-size: 32px; }
    </style>
    """, unsafe_allow_html=True)

if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- 1. واجهة الترحيب البروفيشينال ---
if not st.session_state.started:
    st.markdown("""
        <div class="welcome-card">
            <h1 style='font-size: 50px; margin-bottom: 10px;'>🏗️ نظام التخصيم الهندسي</h1>
            <p style='font-size: 28px; color: #f5f6fa;'>إدارة المهندس ياسين علاء</p>
            <hr style='border: 1px solid #fbc531; width: 40%; margin: 25px auto;'>
            <p style='font-size: 20px; letter-spacing: 2px;'>دقة تقنية . معايير احترافية . جودة تنفيذ</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 دخول النظام الاحترافي"):
        st.session_state.started = True
        st.rerun()

# --- 2. واجهة إدخال البيانات المفصلة ---
else:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>⚙️ لوحة التحكم</h2>", unsafe_allow_html=True)
        if st.button("🗑️ مسح السجل والعودة"):
            st.session_state.storage = []
            st.session_state.started = False
            st.rerun()
        st.markdown("---")
        st.write("يتم حفظ جميع التخصيمات في الشيت السفلي.")

    st.markdown("<h2 class='header-text'>📝 مدخلات المواصفات الفنية</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 🏷️ تعريف القطعة")
        c_title, c_type = st.columns(2)
        with c_title: u_title = st.text_input("اسم الوحدة / العميل", "وحدة مطبخ")
        with c_type: u_type = st.selectbox("تصنيف الوحدة الفني", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
        
        st.markdown("### 📐 الأبعاد الكلية للوحدة (سم)")
        m1, m2, m3 = st.columns(3)
        with m1: w = st.number_input("إجمالي العرض الخارجي", value=None)
        with m2: h = st.number_input("إجمالي الارتفاع الخارجي", value=None)
        with m3: d = st.number_input("إجمالي العمق الخارجي", value=None)

        st.markdown("---")
        st.markdown("### 🧱 تفاصيل الإضافات (أرفف - فواصل - أدراج)")
        
        t1, t2, t3 = st.tabs(["💎 الرفوف", "💎 الفواصل", "💎 الأدراج"])
        
        with t1:
            r1, r2, r3 = st.columns(3)
            with r1: sh_w_in = st.number_input("عرض الرف الفعلي", value=0.0, key="shw")
            with r2: sh_d_in = st.number_input("عمق الرف الفعلي", value=0.0, key="shd")
            with r3: sh_n_in = st.number_input("إجمالي عدد الرفوف", value=0, step=1, key="shn")
            
        with t2:
            v1, v2, v3 = st.columns(3)
            with v1: dv_h_in = st.number_input("ارتفاع الفاصل الفعلي", value=0.0, key="dvh")
            with v2: dv_d_in = st.number_input("عمق الفاصل الفعلي", value=0.0, key="dvd")
            with v3: dv_n_in = st.number_input("إجمالي عدد الفواصل", value=0, step=1, key="dvn")
            
        with t3:
            d1, d2, d3 = st.columns(3)
            with d1: dr_w_in = st.number_input("عرض الدرج الخارجي", value=0.0, key="drw")
            with d2: dr_d_in = st.number_input("عمق الدرج الخارجي", value=0.0, key="drd")
            with d3: dr_n_in = st.number_input("إجمالي عدد الأدراج", value=0, step=1, key="drn")

        if st.button("📊 توليد شيت التخصيم الاحترافي"):
            if w and h and d:
                # تطبيق قواعد التخصيم الصارمة (13 سم للسفلي والخزين / 5 سم للباقي)
                h_c = h - 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else h - 5
                w_c = w - 5
                d_c = d - 5

                unit_entry = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_c': h_c, 'w_c': w_c, 'd_c': d_c,
                    'sh_w': sh_w_in, 'sh_d': sh_d_in, 'sh_n': sh_n_in,
                    'dv_h': dv_h_in, 'dv_d': dv_d_in, 'dv_n': dv_n_in,
                    'dr_w': dr_w_in, 'dr_d': dr_d_in, 'dr_n': dr_n_in
                }
                st.session_state.storage.append(unit_entry)
            else:
                st.error("برجاء إدخال الأبعاد الأساسية أولاً!")

    # --- 3. عرض شيت النتائج البروفيشينال ---
    if st.session_state.storage:
        st.markdown("<h2 class='header-text'>📋 سجل تقارير التخصيم المعتمدة</h2>", unsafe_allow_html=True)
        for u in st.session_state.storage:
            st.markdown(f"""
            <div class="report-card">
                <div class="title-line">📄 تقرير فني: {u['title']} ({u['type']})</div>
                
                <div class="section-label">🪵 أولاً: شيت قص الفيبر (الخشب/الكلادينج)</div>
                <div class="data-line">🔹 الضهرية: <span class="highlight-blue">{u['w_c']} × {u['h_c']}</span> (عدد 1)</div>
                <div class="data-line">🔹 الارضية: <span class="highlight-blue">{u['w_c']} × {u['d_c']}</span> (عدد 1)</div>
                <div class="data-line">🔹 الاجناب: <span class="highlight-blue">{u['h_c']} × {u['d_c']}</span> (عدد 2)</div>
            """, unsafe_allow_html=True)
            
            # تفاصيل الفيبر للإضافات
            if u['sh_n'] > 0:
                st.markdown(f'<div class="data-line">🔹 الارفف (فيبر): <span class="highlight-blue">{u["sh_w"]-5} × {u["sh_d"]-5}</span> (عدد {u["sh_n"]})</div>', unsafe_allow_html=True)
            if u['dv_n'] > 0:
                st.markdown(f'<div class="data-line">🔹 الفواصل (فيبر): <span class="highlight-blue">{u["dv_h"]-5} × {u["dv_d"]-5}</span> (عدد {u["dv_n"]})</div>', unsafe_allow_html=True)
            if u['dr_n'] > 0:
                st.markdown(f'<div class="data-line">🔹 الأدراج: العرض <span class="highlight-blue">{u["dr_w"]-2.5}</span> | العمق <span class="highlight-blue">{u["dr_d"]}</span> (عدد {u["dr_n"]})</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">📐 ثانياً: قائمة قص أعواد الألومنيوم (قطاع 2*8)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-line">🛠️ مقاس الارتفاع الصافي: <span class="highlight-blue">{u["h_c"]} سم</span> (عدد 2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            
            # العرض والعمق حسب التصنيف الفني
            if u['type'] == "وحدة سفلية":
                st.markdown(f'<div class="data-line">🛠️ مقاس العرض الصافي: <span class="highlight-blue">{u["w_c"]} سم</span> (عدد 3 مفرد + 1 متقارب)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="data-line">🛠️ مقاس العمق الصافي: <span class="highlight-blue">{u["d_c"]} سم</span> (عدد 2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="data-line">🛠️ مقاس العرض الصافي: <span class="highlight-blue">{u["w_c"]} سم</span> (عدد 2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="data-line">🛠️ مقاس العمق الصافي: <span class="highlight-blue">{u["d_c"]} سم</span> (عدد 4 متقارب)</div>', unsafe_allow_html=True)
            
            # ألومنيا الإضافات
            if u['sh_n'] > 0 or u['dv_n'] > 0:
                count = (u['sh_n'] + u['dv_n']) * 4
                st.markdown(f'<div class="data-line">🛠️ ألومنيا الرفوف/الفواصل: <span class="highlight-blue">{u["d_c"]} سم</span> (عدد {count} قطعة مفرد)</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
