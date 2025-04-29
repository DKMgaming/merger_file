import streamlit as st
import pandas as pd
import io

# Hàm tự động đọc file .xls hoặc .xlsx
def read_excel_auto(file):
    if file.name.endswith('.xls'):
        return pd.read_excel(file, engine='xlrd')
    else:
        return pd.read_excel(file, engine='openpyxl')

# Giao diện Streamlit
st.title("Nối nhiều file Excel (.xls, .xlsx) thành 1 file (bỏ tiêu đề trùng)")

uploaded_files = st.file_uploader(
    "Tải lên nhiều file Excel (.xls hoặc .xlsx)", 
    type=["xls", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    all_dfs = []

    for i, file in enumerate(uploaded_files):
        df = read_excel_auto(file)

        # Nếu không phải file đầu tiên, bỏ dòng tiêu đề (giả sử là dòng đầu)
        if i > 0:
            df.columns = all_dfs[0].columns  # đảm bảo cột giống nhau
            df = df[1:]  # bỏ dòng đầu

        all_dfs.append(df)

    # Ghép tất cả các file lại
    merged_df = pd.concat(all_dfs, ignore_index=True)

    st.success(f"Đã ghép {len(uploaded_files)} file lại với nhau, bỏ dòng tiêu đề ở các file sau.")
    st.dataframe(merged_df)

    def convert_df(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        return processed_data

    merged_file = convert_df(merged_df)
    st.download_button(
        label="📥 Tải file Excel đã ghép",
        data=merged_file,
        file_name="merged_file.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
