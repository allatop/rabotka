import streamlit as st
import requests
import io

BACKEND_URL = "https://university-cgs.onrender.com/convert"
#BACKEND_URL = "http://127.0.0.1:8000"

st.title("Преобразование координатных данных")
st.write("""
Загрузите CSV-файл с колонками `Name`, `X`, `Y`, `Z`, и получите Markdown-отчет
с преобразованными координатами.
""")

# Загрузка файла
uploaded_file = st.file_uploader("Выберите CSV-файл", type=["csv"])

if uploaded_file is not None:
    if st.button("Преобразовать координаты"):
        with st.spinner("Обработка файла..."):
            try:
                # Отправка файла на бэкенд
                files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                response = requests.post(f"{BACKEND_URL}/process-csv/", files=files)

                if response.status_code == 200:
                    # Успешный ответ — это Markdown-файл
                    st.download_button(
                        label="Скачать Markdown-отчет",
                        data=response.content,
                        file_name="report.md",
                        mime="text/markdown"
                    )
                    st.success("Отчет успешно сгенерирован!")
                else:
                    # Ошибка — пытаемся разобрать JSON
                    try:
                        error_detail = response.json().get('detail', 'Неизвестная ошибка')
                    except ValueError:
                        error_detail = response.text or 'Неизвестная ошибка'
                    st.error(f"Ошибка: {error_detail}")

            except requests.exceptions.RequestException as e:
                st.error(f"Ошибка подключения: {str(e)}")
