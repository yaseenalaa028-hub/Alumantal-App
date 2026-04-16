import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. إعدادات المنظومة المتطورة
# ==========================================
st.set_page_config(page_title="DOGGA PRO SYSTEM", layout="wide")

if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

# تصميم الواجهة الاحترافية
accent = "#f1c40f" if st.session_state.dark_mode else "#d4ac0d"
bg_card = "#1c1f26" if st.session_state.dark_mode else "#f8f9fa"

st.markdown(f"""
    <style>
    .main {{ direction: rtl !important; text-align: right; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; }}
    .stTabs [data-baseweb="tab"] {{ 
        background-color: {bg_card}; border-radius: 10px 10px 0 0; padding: 10px 20px; color: {accent};
    }}
    .stat-box {{ 
        background: {bg_card}; border: 1px solid {accent}; border-radius: 15px; 
        padding: 20px; text-align: center; margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# الهيدر الاحترافي
c1, c2 = st.columns([8, 2])
with c1:
    st.markdown(f"<h1 style='color:{accent};'>🛠️ DOGGA PRO | المهندس ياسين علاء</h1>", unsafe_allow_html=True)
with c2:
    if st.button("🌓 تبديل المظهر"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. منطق التخصيم الاحترافي (Advanced Calculation)
# ==========================================
def calculate_deductions(u_type, w, h, d):
    # تخصيمات الهيكل (Framework)
    if u_type == "وحدة سفلية":
        h_ded, w_ded, d_ded = 13, 5, 5
        struc = [
            ["قوايم رئيسية", h - h_ded, 2, "مفرد"],
            ["عوارض عرض", w - w_ded, 3, "مفرد"],
            ["عوارض عمق", d - d_ded, 2, "مفرد"],
            ["وزرة سفلية", w - w_ded, 1, "متقارب"]
        ]
    elif u_type == "وحدة علوية":
        h_ded, w_ded, d_ded = 5, 5, 5
        struc = [
            ["قوايم رئيسية", h - h_ded, 2, "مفرد"],
            ["عوارض عرض", w - w_ded, 2, "مفرد"],
            ["عوارض عمق", d - d_ded, 2, "مفرد"]
        ]
    else: # دولاب خزين
        h_ded, w_ded, d_ded = 13, 5, 5
        struc = [
            ["قوايم طويلة", h - h_ded, 2, "مفرد"],
            ["عوارض عرض", w - w_ded, 4, "مفرد"],
            ["عوارض عمق", d - d_ded, 2, "مفرد"]
        ]
    
    # تخصيم الفيبر (Fiberboard)
    fiber = [
        ["الظهر", f"{w-6} x {h-h_ded-1}", 1],
        ["الأرضية", f"{w-6} x {d-6}", 1],
        ["الأجناب", f"{h-h_ded-1} x {d-6}", 2]
    ]
    
    # تخصيم الضلف (Doors) - افتراض ضلفتين
    door_w = (w - 0.8) / 2
    door_h = h - h_ded - 0.4
    doors = [["برواز ضلفة", f"{door_w} x {door_h}", 2]]

    return struc, fiber, doors

# ==========================================
# 3. تقسيم الواجهة لتبويبات (Tabs)
# ==========================================
tab1, tab2, tab3 = st.tabs(["➕ إضافة وحدة", "📋 شيت التفصيل", "📊 الجرد والطلب"])

with tab1:
    with st.container():
        st.markdown("### 📥 إدخال بيانات المقاسات")
        with st.form("entry_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            client = col1.text_input("اسم العميل")
            u_type = col2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])
            note = col3.text_input("ملاحظات (مثل: لون خاص)")
            
            m1, m2, m3 = st.columns(3)
            W = m1.number_input("العرض (سم)", min_value=10.0, step=0.1)
            H = m2.number_input("الارتفاع (سم)", min_value=10.0, step=0.1)
            D = m3.number_input("العمق (سم)", min_value=10.0, step=0.1)
            
            if st.form_submit_button("حساب وإضافة للمشروع"):
                if W and H and D:
                    struc, fiber, doors = calculate_deductions(u_type, W, H, D)
                    st.session_state.project_list.append({
                        "client": client if client else "عام",
                        "type": u_type, "W": W, "H": H, "D": D,
                        "struc": struc, "fiber": fiber, "doors": doors, "note": note
                    })
                    st.success(f"تمت إضافة {u_type} بنجاح")
                    st.rerun()

with tab2:
    if not st.session_state.project_list:
        st.warning("لا توجد وحدات مضافة حالياً.")
    else:
        for idx, item in enumerate(st.session_state.project_list):
            with st.expander(f"📌 وحدة {idx+1}: {item['client']} | {item['type']} ({item['W']}x{item['H']})"):
                c_a, c_f, c_d = st.columns(3)
                with c_a:
                    st.write("**📐 هيكل الألومنيوم**")
                    st.table(pd.DataFrame(item['struc'], columns=["البيان", "المقاس", "العدد", "النوع"]))
                with c_f:
                    st.write("**🖼️ مقاسات الفيبر**")
                    st.table(pd.DataFrame(item['fiber'], columns=["القطعة", "المقاس", "العدد"]))
                with c_d:
                    st.write("**🚪 الضلف والملاحظات**")
                    st.table(pd.DataFrame(item['doors'], columns=["البيان", "المقاس", "العدد"]))
                    st.info(f"ملاحظة: {item['note']}")
        
        if st.button("🗑️ مسح الكل"):
            st.session_state.project_list = []
            st.rerun()

with tab3:
    if st.session_state.project_list:
        st.markdown("### 📈 إجمالي احتياجات المشروع")
        
        # تجميع كل الأعواد للحساب الإجمالي
        all_cuts = []
        for item in st.session_state.project_list:
            for cut in item['struc']:
                all_cuts.append({"المقاس": cut[1], "العدد": cut[2]})
        
        df_total = pd.DataFrame(all_cuts).groupby("المقاس").sum().reset_index()
        
        total_len = (df_total['المقاس'] * df_total['العدد']).sum()
        num_bars = math.ceil(total_len / 600)
        
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("إجمالي الأمتار", f"{total_len/100:.2f} م")
        col_s2.metric("عدد الأعواد (6م)", f"{num_bars} عود")
        col_s3.metric("عدد الوحدات", len(st.session_state.project_list))
        
        st.markdown("#### 📋 جدول تقطيع الأعواد النهائي")
        st.dataframe(df_total.sort_values(by="المقاس", ascending=False), use_container_width=True)
        
        # تحويل البيانات لـ CSV للتحميل
        csv = df_total.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تحميل شيت الطلبية (Excel/CSV)", data=csv, file_name="order.csv", mime="text/csv")

# الفوتر
st.markdown("---")
st.markdown(f"<div style='text-align:center; opacity:0.6;'>نظام دقة برو 2026 | تطوير م/ ياسين علاء</div>", unsafe_allow_html=True)
