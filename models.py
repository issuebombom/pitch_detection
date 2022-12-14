import librosa
import numpy as np
import statsmodels.api as sm
from scipy.signal import find_peaks
from utils import *

def run_model(audio_file):

    hertz2keys = load_pickle("hertz2keys.pkl")

    # 음원 길이 설정(초)
    duration = 20
    data, sample_rate = librosa.load(audio_file, sr=44100, mono=True, duration=duration)


    # 0.01초 단위로 데이터 슬라이싱
    sec = 0.01
    trim_sec = int(1 / sec)
    n_rows = data.shape[0] // sample_rate * trim_sec # 지정한 주기로 슬라이싱
    dataset = data.reshape(n_rows, -1)

    detected_hertz = []
    for sample in dataset:
        if sample.mean() == 0: # 구간 내 소리가 없는 경우 0 입력
            detected_hertz.append(0) # No Signal
            continue
        
        autocorrelation = sm.tsa.acf(sample, nlags=200)
        peaks = find_peaks(autocorrelation)[0] # Find peaks of the autocorrelation (threshold=0.001)
        
        if peaks.shape[0] == 0: # peak가 없는 경우 0 입력
            detected_hertz.append(0) # No Peak
            continue
        
        lag = peaks[0] # Choose the first peak as our pitch component lag
        pitch = int(sample_rate / lag) # Transform lag into frequency
        
        detected_hertz.append(find_closed_key(pitch)) # change hertz to closed key hertz

        
    # task 1
    # 0.1초 단위로 가장 빈도수가 높은 키 하나만 남기기
    sec = 0.1
    trim_sec = int(1 / sec)
    n_rows = duration * trim_sec
    result = np.array(detected_hertz).reshape(n_rows, -1) # (220, 10)

    freq_hertz_result = np.array([freq_check(array) for array in result])


    # task 2
    # n개 단위로 그룹화한 뒤 빈도수 낮은 key값을 제외
    group_size = 10
    drop_rate = 0.1
    reshaped = freq_hertz_result.reshape(-1, group_size) # (22, 10)
    final_result = freq_check2(reshaped, drop_rate) # length의 10% 이하 빈도수 key값은 제외

    final_result = [hertz2keys[hertz] for hertz in final_result]
    final_result = delete_continuous_value(final_result)

    return final_result
