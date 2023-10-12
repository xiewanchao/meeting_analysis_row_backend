
import torch
import os
import json
import numpy as np
from scipy.spatial.distance import cdist

from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
from pyannote.audio import Pipeline



#  load pre-trained model and define audio pre-processing
model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cpu"))
audio = Audio(sample_rate=16000, mono="downmix")

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token="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")


class DiarizationResult:
    def __init__(self, start_time, end_time, speaker):
        self.start_time = start_time
        self.end_time = end_time
        self.speaker = speaker




# 1. define a function that generates embedding for a given audio file
def generate_embedding(audio_file,start = 1.0,end = 4.0):
    # extract embedding for a speaker speaking between t=7s and t=12s
    speaker = Segment(start, end)
    waveform, sample_rate = audio.crop(audio_file, speaker)
    embedding = model(waveform[None])
    # return embedding
    return embedding


def calculate_euclidean_distance(embedding1, embedding2):
    distance = cdist(embedding1, embedding2, metric="cosine")
    return distance


#  遍历文件夹中的所有.wav文件并生成嵌入




# 遍历所有嵌入向量对，并计算它们之间的计算值,以及阈值

def getLimit():

    embeddings = loadEmbeddings()

    pairwise_distances = {}
    embedding_keys = list(embeddings.keys())
    max = 0
    min = 1 

    for i in range(len(embedding_keys)):
        for j in range(i + 1, len(embedding_keys)):
            embedding1 = embeddings[embedding_keys[i]]
            embedding2 = embeddings[embedding_keys[j]]
            
            distance = calculate_euclidean_distance(embedding1, embedding2)
            if embedding_keys[i][:3] == embedding_keys[j][:3] and distance > max:
                max = distance
            if embedding_keys[i][:3] != embedding_keys[j][:3] and distance < min:
                min = distance
            pair_key = (embedding_keys[i], embedding_keys[j])
            pairwise_distances[pair_key] = distance

    print(pairwise_distances)
    print(max)
    print(min)
    #max:0.4723514],min:0.58155759



def getEmbeddingsAndSave():
    folder_path = "audio_wav"
    old_embeddings = loadEmbeddings()
    new_embeddings = {}


    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".wav") and file not in old_embeddings:
                audio_file = os.path.join(root, file)
                embedding = generate_embedding(audio_file)
                new_embeddings[file] = embedding.tolist()  # 将 ndarray 转换为列表

    # 将字典转换为 JSON 格式
    json_embeddings = json.dumps(new_embeddings, indent=4)

    # 保存 JSON 数据到文本文件
    with open("embeddings.json", "w") as json_file:
        json_file.write(json_embeddings)


def loadEmbeddings():
    # 读取保存的 JSON 文件
    if not os.path.exists("embeddings.json"):
        return {}
    with open("embeddings.json", "r") as json_file:
        embeddings = json.load(json_file)

    # 转换嵌套列表为 NumPy ndarray（如果需要的话）
    for key, value in embeddings.items():
        embeddings[key] = np.array(value)

    return embeddings


def getSingleSpeaker (file_path,start,end,limit = 0.5):
    embeddings = loadEmbeddings()
    embedding = generate_embedding(file_path,start,end)
    min = 1
    speaker = "未识别到说话人"
    for key, value in embeddings.items():
        distance = calculate_euclidean_distance(embedding, value)
        if distance < limit and distance < min:
            min = distance
            speaker = key[:3]
    return speaker



def getDiarization(file_path):
    diarization = pipeline(file_path)
    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        result = DiarizationResult(turn.start, turn.end, f"speaker_{speaker}")
        results.append(result)
    return results


def getSpeakers(file_path):
    results = getDiarization(file_path)
    for result in results:
        speaker = getSingleSpeaker(file_path,result.start_time,result.end_time)
        result.speaker = speaker
        result.start_time = round(result.start_time,1)
        result.end_time = round(result.end_time,1)
        
    json_result = json.dumps(results, default=lambda o: o.__dict__, indent=4)
    return json_result
    






if __name__ == '__main__':
    # getEmbeddingsAndSave()
    # getLimit()
    # speaker = getSpeaker("audioTest_wav/test1.wav",5.0,8.0)
    # print(speaker)
    res = getSpeakers("audioTest_wav/test1.wav")
    print(res)





