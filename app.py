import streamlit as st
import pandas as pd

# إعدادات الصفحة لتظهر بشكل احترافي
st.set_page_config(page_title="نظام تخصيم الألومنيوم - المهندس ياسين علاء", layout="wide")

# إضافة لمسة جمالية وتنسيق اتجاه النص (RTL)
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div.stButton > button { width: 100%; background-color: #27ae60; color: white; font-weight: bold; border-radius: 10px; height: 3em; }
    .header-box { background-color: #2f3640; color: #fbc531; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; border-bottom: 4px solid #e1b12c; }
    .unit-card { background-color: #ffffff; padding: 15px; border: 1px solid #2ecc71; border-radius: 10px; margin-bottom: 10px; white-space: pre-wrap; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>برمجة المهندس ياسين علاء</h1><h3>نظام تخصيم الألومنيوم وجرد الخامات</h3></div>', unsafe_allow_html=True)

# تهيئة مخزن البيانات في المتصفح
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- منطقة المدخلات (نفس الترتيب والمسميات في كودك) ---
with st.sidebar:
    st.header("📝 مدخلات المقاسات")
    unit_title = st.text_input("اسم الوحدة", "وحدة جديدة")
    unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    col_w, col_h, col_d = st.columns(3)
    w = col_w.number_input("العرض الكلي", value=0.0)
    h = col_h.number_input("الارتفاع الكلي", value=0.0)
    d = col_d.number_input("العمق الكلي", value=0.0)
    
    st.subheader("🧱 الرفوف")
    sh_w = st.number_input("الرف (عرض)", value=0.0)
    sh_d = st.number_input("الرف (عمق)", value=0.0)
    sh_n = st.number_input("الرفوف (عدد)", value=0, step=1)
    
    st.subheader("📐 الفواصل")
    dv_h = st.number_input("الفاصل (ارتفاع)", value=0.0)
    dv_d = st.number_input("الفاصل (عمق)", value=0.0)
    dv_n = st.number_input("الفواصل (عدد)", value=0, step=1)
    
    st.subheader("🗄️ الأدراج")
    dr_w = st.number_input("الدرج (عرض)", value=0.0)
    dr_d = st.number_input("الدرج (عمق)", value=0.0)
    dr_n = st.number_input("الأدراج (عدد)", value=0, step=1)

    if st.button("💾 إضافة للجدول"):
        # نفس معادلاتك بالظبط بدون أي تغيير
        u = {
            'title': unit_title, 'type': unit_type,
            'w': w, 'h': h, 'd': d,
            'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
            'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
            'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
        }
        st.session_state.project_storage.append(u)
        st.success(f"تمت إضافة {unit_title}")

# --- عرض النتائج ---
if st.session_state.project_storage:
    col_main, col_table = st.columns([7, 3])
    
    all_text_report = "" # لتجميع التقرير النهائي للحفظ
    
    with col_main:
        st.subheader("📐 تفاصيل التخصيم")
        for idx, u in enumerate(st.session_state.project_storage):
            # نفس منطق العرض النصي في كودك
            h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_baky, d_baky = u['w'] - 5, u['d'] - 5

            txt = f"\n📦 {u['title']} | {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
            txt += "━" * 40 + "\n"
            txt += "📐 [1] تخصيم الألومنيوم (2*8):\n"
            if u['type'] == "سفلية":
                txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"  - عــــرض {w_baky}: [3 مفرد] [1 متقارب]\n"
                txt += f"  - عمــــق {d_baky}: [2 مفرد] [2 متقارب]\n"
            else:
                txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"  - عــــرض {w_baky}: [2 مفرد] [2 متقارب]\n"
                txt += f"  - عمــــق {d_baky}: [4 متقارب]\n"

            txt += "\n🪵 [2] تخصيم الفيبر (التقطيع):\n"
            txt += f"  - ضهرية: {w_baky} × {h_baky} (1)\n"
            txt += f"  - أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n"
            txt += f"  - أجناب: {h_baky} × {d_baky} (2)\n"
            
            if u['sh_n'] > 0:
                txt += f"\n🧱 [3] الرفوف ({u['sh_n']}):\n"
                txt += f"  - ألومنيوم: {u['sh_w']} × {u['sh_n']*2} قطعة | {u['sh_d']} × {u['sh_n']*2} قطعة [مفرد]\n"
                txt += f"  - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5} ({u['sh_n']} قطعة)\n"
            
            if u['dv_n'] > 0:
                txt += f"\n📐 [4] الفواصل ({u['dv_n']}):\n"
                txt += f"  - ألومنيوم: {u['dv_h']} × {u['dv_n']*2} قطعة | {u['dv_d']} × {u['dv_n']*2} قطعة [مفرد]\n"
                txt += f"  - فيبر الفاصل: {u['dv_h']-5} × {u['dv_d']-5} ({u['dv_n']} قطعة)\n"

            if u['dr_n'] > 0:
                txt += f"\n🗄️ [5] الأدراج ({u['dr_n']}):\n"
                txt += f"  - ألومنيوم العرض: {u['dr_w']-2.5} × {u['dr_n']*2} | العمق: {u['dr_d']} × {u['dr_n']*2}\n"

            st.markdown(f'<div class="unit-card">{txt}</div>', unsafe_allow_html=True)
            all_text_report += txt + "\n"

    with col_table:
        st.subheader("📊 ملخص المشروع")
        df = pd.DataFrame(st.session_state.project_storage)[['title', 'w', 'h', 'd']]
        st.table(df)
        
        # أزرار العمليات
        if st.button("📊 جرد الخامات"):
            m_sum, t_sum, f_area = 0, 0, 0
            for u in st.session_state.project_storage:
                h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
                w_b, d_b = u['w'] - 5, u['d'] - 5
                if u['type'] == "سفلية":
                    m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                    f_area += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
                else:
                    m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(u['w']-5)*2+(d_b*4)
                    f_area += (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
                
                m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
                m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
                f_area += (max(0, u['sh_w']-5))*(max(0, u['sh_d']-5))*u['sh_n'] + (max(0, u['dv_h']-5))*(max(0, u['dv_d']-5))*u['dv_n']
                m_sum += ((max(0, u['dr_w']-2.5))*2 + u['dr_d']*2) * u['dr_n']

            st.info(f"""
            **جرد خامات المشروع:**
            - ألومنيوم مفرد: {m_sum/600:.2f} عود
            - ألومنيوم متقارب: {t_sum/600:.2f} عود
            - فيبر: {f_area/36400:.2f} لوح
            """)

        # تحميل التقرير
        full_output = f"تقرير المهندس ياسين علاء\n{all_text_report}"
        st.download_button("💾 حفظ المشروع (Text)", full_output, file_name="Alumantal_Report.txt")
        
        if st.button("🗑️ مسح الكل"):
            st.session_state.project_storage = []
            st.rerun()
else:
    st.info("أدخل بيانات الوحدة من القائمة الجانبية لبدء التخصيم.")