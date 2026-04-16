import streamlit as st
from fpdf import FPDF

# كود لمعالجة اللغة العربية في الـ PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Alumantal Cutting Sheet - Eng. Yassin Alaa', 0, 1, 'C')

def main():
    st.set_page_config(page_title="تخصيمات المهندس ياسين", layout="wide")
    st.title("🛠️ نظام تخصيم الألومنيوم والفيبر التفصيلي")

    # المدخلات الأساسية
    col1, col2, col3 = st.columns(3)
    with col1:
        unit_name = st.text_input("اسم الوحدة", "مطبخ 1")
        unit_type = st.selectbox("نوع القطعة", ["سفلية", "علوية", "دولاب خزين"])
    with col2:
        width = st.number_input("العرض الكلي (W)", value=200.0)
        height = st.number_input("الارتفاع الكلي (H)", value=90.0)
    with col3:
        depth = st.number_input("العمق الكلي (D)", value=50.0)

    # قسم الرفوف والفواصل
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🧱 الرفوف")
        sh_w = st.number_input("عرض الرف", value=77.0)
        sh_d = st.number_input("عمق الرف", value=47.0)
        sh_n = st.number_input("عدد الرفوف", value=2, step=1)
    with c2:
        st.subheader("📐 الفواصل")
        dv_h = st.number_input("ارتفاع الفاصل", value=77.0)
        dv_d = st.number_input("عمق الفاصل", value=47.0)
        dv_n = st.number_input("عدد الفواصل", value=2, step=1)
    with c3:
        st.subheader("🗄️ الأدراج")
        dr_w = st.number_input("عرض الدرج", value=0.0)
        dr_n = st.number_input("عدد الأدراج", value=0, step=1)

    if st.button("💾 احسب وفصّل الجداول"):
        # الحسابات المعتمدة من قبلك
        h_sub = 13 if unit_type in ["سفلية", "دولاب خزين"] else 5
        h_net, w_net, d_net = height - h_sub, width - 5, depth - 5

        # --- عرض النتائج في جداول منفصلة تماماً ---
        res_col1, res_col2 = st.columns(2)

        with res_col1:
            st.success("📝 جدول تقطيع الألومنيوم")
            st.markdown(f"""
            * **الهيكل الأساسي:**
                * العرض {w_net}: (3 مفرد + 1 متقارب)
                * الارتفاع {h_net}: (2 مفرد + 2 متقارب)
                * العمق {d_net}: (2 مفرد + 2 متقارب)
            """)
            if sh_n > 0:
                st.markdown(f"**الرفوف ألومنيوم (عدد {sh_n}):**")
                st.markdown(f"* مقاس {sh_w}: (عدد {sh_n*4}) مفرد")
                st.markdown(f"* مقاس {sh_d}: (عدد {sh_n*4}) مفرد")
            if dv_n > 0:
                st.markdown(f"**الفواصل ألومنيوم (عدد {dv_n}):**")
                st.markdown(f"* مقاس {dv_h}: (عدد {dv_n*4}) مفرد")
                st.markdown(f"* مقاس {dv_d}: (عدد {dv_n*4} مفرد)")

        with res_col2:
            st.info("🪵 جدول تقطيع الفيبر")
            st.markdown(f"""
            * **الهيكل الأساسي:**
                * ضهرية: {w_net} × {h_net} (عدد 1)
                * أرضية: {w_net} × {d_net} (عدد 1)
                * أجناب: {h_net} × {d_net} (عدد 2)
            """)
            if sh_n > 0:
                st.markdown(f"* **فيبر الرفوف:** {sh_w - 5} × {sh_d - 5} (عدد {sh_n})")
            if dv_n > 0:
                st.markdown(f"* **فيبر الفواصل:** {dv_h - 5} × {dv_d - 5} (عدد {dv_n})")

if __name__ == "__main__":
    main()
