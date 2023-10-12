import whisper

model = whisper.load_model("base")
audioFile = r"/Users/coder/Project/eblab_Project/meetint_analysis/test_16k.wav"
prompt = '以下是普通话的句子。'
# verbose 输出过程 ， initial_prompt 确定语言类型
result = model.transcribe(audioFile, verbose=True, initial_prompt=prompt)
# result = model.transcribe(audioFile, verbose=True)
# print(f' 转录： \n {result["text"]}')
print(result)
