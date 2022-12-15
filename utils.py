import pickle
import numpy as np
import soundfile as sf
from collections import Counter


def load_pickle(path):
    """Load json file

    Args:
        path (str): input file directory about json file

    Returns:
        dict: json file to dictionary
    """
    with open(path, 'rb') as fr:
        pickle_data = pickle.load(fr)
    
    return pickle_data


def read_audio(audio_file, samplerate, time_duration, mono=True):
    """read audio signal data and sample rate

    Args:
        audio_file (Audio_File): audio file path(mp3, wav)
        duration (int): input audio length(seconds)

    Returns:
        y (np.ndarray): output sound amplitude
    """

    context = sf.SoundFile(audio_file)

    with context as sf_desc:
        frame_duration = int(time_duration * samplerate)

        # Load the target number of frames, and transpose to match librosa form
        y = sf_desc.read(frames=frame_duration, always_2d=False).T

        if mono == True: # 모노 음원이 들어왔을 경우에 대한 예외처리 필요
            y = np.mean(y, axis=0) # to mono

    return y


def find_closed_key(hertz):
    """음원이 계이름과 정확하게 일치하는 hertz를 출력하지 않으므로 근사하는 계이름을 출력하는 도구

    Args:
        hertz (float): input hertz for change neighborhood key

    Returns:
        float: output neighborhood key close with hertz you input
    """
    hertz2keys = load_pickle("hertz2keys.pkl")
    if hertz == 0:
        return 0.0
    
    herts_array = np.array(list(hertz2keys.keys())) # 딕셔너리 key값을 리스트로 변경
    closed_index = np.argmin(abs(herts_array - hertz)) # 확인 대상과 가장 가까운 계이름 hertz 찾기
    
    return herts_array[closed_index] # 출력


def freq_check(array):
    """np.array에서 빈도수가 가장 높은 원소를 출력

    Args:
        array (np.array): 최고 빈도수 원소 추출을 위한 array 입력

    Returns:
        int: 빈도수가 가장 높은 값을 출력
    """
    freq_result = np.unique(array, return_counts=True) # (array([ 980, 1002, 1260]), array([1, 8, 1])) 튜플 반환
    result = freq_result[0][np.argmax(freq_result[1])] # 최대 빈도수 인덱싱
    
    return result # int


def freq_check2(array, threshold:float):
    """범위 내 요소별 빈도수 체크 및 일정 빈도수 이하 요소 제외

    Args:
        array (np.array): 빈도수 체크를 위한 array 입력
        threshold (float): array 길이의 n 비율에 해당하는 값 이하의 빈도수를 가진 key 제외

    Returns:
        list: 낮은 빈도수를 갖는 원소가 제외된 리스트를 출력합니다.
    """
    result = []
    for hertz_list in array:
        counter = Counter(hertz_list)
        temp = [hertz for hertz in hertz_list if counter[hertz] > hertz_list.shape[0] * threshold]
        result = result + temp
    return result # list


def delete_continuous_value(array:list):
    """리스트 내 연속된 중복값을 제거합니다.

    Args:
        array (list): 중복값 제거 대상 리스트 입력

    Returns:
        list: 연속 중복값을 제외한 리스트 출력
    """
    curr_key = ""
    new_list = []
    for key in array:
        if curr_key == key:
            continue
        new_list.append(key)
        curr_key = key
        
    return new_list
