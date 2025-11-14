import streamlit as st
import pandas as pd

st.set_page_config(page_title="Графики из Excel", layout="wide")
st.title("Генератор графиков из Excel")

uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Читаем Excel
    df = pd.read_excel(uploaded_file)

    st.subheader("Предпросмотр данных")
    st.dataframe(df.head())

    # Списки колонок
    all_columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    # Выбор типа графика
    chart_type = st.selectbox(
        "Тип графика",
        ["Линейный", "Столбчатый", "Точечный (scatter)", "Boxplot"]
    )

    # Выбор осей
    x_col = st.selectbox("Ось X", all_columns)

    y_cols = st.multiselect(
        "Ось Y (можно несколько, только числовые)",
        numeric_columns,
        default=numeric_columns[:1] if numeric_columns else []
    )

    build_btn = st.button("Построить график")

    if build_btn:
        if not y_cols:
            st.warning("Выберите хотя бы одну числовую колонку для оси Y.")
        else:
            # В зависимости от типа графика — разные реализации
            if chart_type == "Линейный":
                st.subheader("Линейный график")
                st.line_chart(df.set_index(x_col)[y_cols])

            elif chart_type == "Столбчатый":
                st.subheader("Столбчатый график")
                st.bar_chart(df.set_index(x_col)[y_cols])

            elif chart_type == "Точечный (scatter)":
                import altair as alt
                st.subheader("Scatter-график")
                # Берём первую выбранную Y для scatter
                chart = (
                    alt.Chart(df)
                    .mark_circle()
                    .encode(
                        x=x_col,
                        y=y_cols[0],
                        tooltip=all_columns,
                    )
                    .interactive()
                )
                st.altair_chart(chart, use_container_width=True)

            elif chart_type == "Boxplot":
                import plotly.express as px
                st.subheader("Boxplot")
                # Boxplot обычно по одной метрике
                fig = px.box(df, x=x_col, y=y_cols[0])
                st.plotly_chart(fig, use_container_width=True)
