import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. Cấu hình AI Gemini
genai.configure(api_key="AIzaSy..._Thay_API_Key_Cua_Ban_Vao_Day")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Bao Cao Song Ngu", layout="centered")
st.title("🇰🇷 Trợ Lý Báo Cáo Hàn - Việt 🇻🇳")

# 2. Upload file báo cáo (Dùng file Excel của bạn)
uploaded_file = st.file_uploader("Tai len file bao cao (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # Chuyển dữ liệu thành dạng văn bản để AI hiểu
    data_context = df.to_string()
    st.success("Da nap du lieu bao cao!")

    # 3. Giao diện hỏi đáp
    st.subheader("Hoi dap cung Sep")
    user_input = st.chat_input("Sep noi tieng Han hoac Ban nhap tieng Viet...")

    if user_input:
        prompt = f"""
        DATA: {data_context}
        INPUT: {user_input}
        
        TASK:
        - Nếu INPUT là tiếng Hàn: Hãy phân tích DATA và trả lời bằng tiếng Hàn lịch sự. Kèm bản dịch tiếng Việt.
        - Nếu INPUT là tiếng Việt: Hãy dịch sang tiếng Hàn một cách tự nhiên cho sếp.
        
        FORMAT:
        [KOREAN]: (Câu trả lời tiếng Hàn)
        [VIETNAMESE]: (Bản dịch tiếng Việt)
        """
        
        with st.spinner('AI dang suy nghi...'):
            response = model.generate_content(prompt)
            result = response.text
            
            # Hiển thị kết quả
            st.markdown(f"### Ket qua:\n{result}")
            
            # Tự động tạo nút phát âm thanh cho phần tiếng Hàn
            korean_part = result.split("[VIETNAMESE]")[0].replace("[KOREAN]:", "").strip()
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={korean_part}&tl=ko&client=tw-ob")