import streamlit as st
from models import run_model

st.title('Pitch Detection')
uploaded_file = st.file_uploader("Import your audio file", type=['wav', 'mp3'])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    run_model = run_model(uploaded_file)

# 버튼을 클릭하면 탐지한 계이름을 시퀀셜하게 출력해 줍니다.
if st.button('Push button to detect keys'):
    st.write(" | ".join(run_model))