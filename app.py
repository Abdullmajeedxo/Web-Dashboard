import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحتك لتحليل معلوماتك", layout="wide")
st.title("📊 Excel اداة ذكية لتحليل ملفات")
st.markdown("تحول البيانات الى مؤشرات و رسوم تفاعلية، مع امكانية فلترة البيانات وتصديرها Excel اداة ذكية لتحليل ملفات ")


uploaded_file = st.file_uploader("ارفع ملف الإكسل", type=["xlsx", "csv"])

if uploaded_file is not None:
    
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    
    st.sidebar.header(" إعدادات العرض والفلترة")
    
    if categorical_cols:
        selected_cat = st.sidebar.selectbox("اختر التصنيف الأساسي للتحليل:", categorical_cols)
        unique_vals = df[selected_cat].dropna().unique().tolist()
        selected_filter = st.sidebar.multiselect(f"تصفية حسب ({selected_cat}):", unique_vals, default=unique_vals)
        df = df[df[selected_cat].isin(selected_filter)]
    
    
    st.markdown(" 📈 مؤشرات الأداء الرئيسية")
    if numeric_cols:
        cols = st.columns(min(len(numeric_cols), 4))
        for i, col_name in enumerate(numeric_cols[:4]):
            total_val = df[col_name].sum()
            cols[i].metric(f"إجمالي {col_name}", f"{total_val:,.2f}")
    else:
        st.info("لا توجد أعمدة رقمية لحساب المؤشرات الإحصائية تلقائياً.")
        
    st.markdown("---")
    
    
    st.markdown(" 📊 التحليل المرئي للبيانات")
    c1, c2 = st.columns(2)
    
    if categorical_cols and numeric_cols:
        fig_bar = px.bar(df, x=categorical_cols[0], y=numeric_cols[0], title="التحليل المرئي", color=numeric_cols[0], color_continuous_scale='Blues')
        c1.plotly_chart(fig_bar, use_container_width=True)
        
        fig_pie = px.pie(df, names=categorical_cols[0], values=numeric_cols[0], title="نسب التوزيع", hole=0.3)
        c2.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("الرجاء التأكد أن الملف يحتوي على أعمدة نصية وأعمدة رقمية لكي تعمل الرسوم البيانية بكفاءة.")

    
    st.markdown(" جدول البيانات التفصيلي")
    search_query = st.text_input("🔍 بحث سريع في البيانات:")
    if search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        filtered_df = df[mask]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
        
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label=" تحميل البيانات المصفاة (CSV)",
        data=csv,
        file_name='exported_analytics_report.csv',
        mime='text/csv',
    )
else:
    st.info("الرجاء رفع أي ملف بيانات (إكسل أو سي إس في) لتبدأ لوحة التحكم في تحليلها وعرضها فوراً")