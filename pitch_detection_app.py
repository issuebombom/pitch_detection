import streamlit as st
from soundfile import SoundFile
from models import run_model

st.title('Pitch Detection')
uploaded_file = st.file_uploader("Import your audio file", type=['wav', 'mp3'])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    samplerate = SoundFile(uploaded_file).samplerate # extract samplerate
    frames = SoundFile(uploaded_file).frames # extract audio frames
    max_time_duration = int(frames / samplerate) # switch audio frames to second length

    time_duration = st.slider('Select a range of audio length you want to detect', 
                            value=[0, max_time_duration], 
                            max_value=max_time_duration
                            )
    
# 버튼을 클릭하면 탐지한 계이름을 시퀀셜하게 출력해 줍니다.
if st.button('Push button to detect keys'):
    run_model = run_model(uploaded_file, samplerate=samplerate, time_duration=time_duration)
    st.write("  |  ".join(run_model))