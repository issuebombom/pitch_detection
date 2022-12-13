import streamlit as st
from models import run_model

st.title('Pitch Detection')
audio_file = st.file_uploader("Import your mp3 file")
run_model = run_model(audio_file)

st.button('push button to run', on_click=run_model)