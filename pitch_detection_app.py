import os
import streamlit as st
from utils import get_audio_info
from models import run_model

sample_folder = "./piano_samples"

st.title('Pitch Detection')
uploaded_file = st.file_uploader("Import your audio file", type=['wav', 'mp3'])
sample = st.selectbox(
    'Select the piano sample',
    ('piano_sample_01.mp3', 'piano_sample_02.mp3', 'piano_sample_03.mp3', 'piano_sample_04.mp3')
    )
if uploaded_file is not None:
    samplerate, frames, max_time_duration = get_audio_info(uploaded_file)

else:
    uploaded_file = os.path.join(sample_folder, sample)
    samplerate, frames, max_time_duration = get_audio_info(uploaded_file)

st.audio(uploaded_file, format='audio/wav')
time_duration = st.slider('Select a range of audio length you want to detect', 
                            value=[0, max_time_duration], 
                            max_value=max_time_duration
                            )

# 버튼을 클릭하면 탐지한 계이름을 시퀀셜하게 출력해 줍니다.
if st.button('Push button to detect keys'):
    run_model = run_model(uploaded_file, samplerate=samplerate, time_duration=time_duration)
    st.write("  |  ".join(run_model))