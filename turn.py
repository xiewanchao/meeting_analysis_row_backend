import os
import subprocess

# 输入文件夹包含M4A文件
input_folder = "audioTest"
# 输出文件夹用于存储WAV文件
output_folder = "audioTest_wav"
ffmpeg_path = "/Users/i588093/Documents/fudan/ffmpeg"

# 确保输出文件夹存在，如果不存在则创建它
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有M4A文件
for filename in os.listdir(input_folder):
    if filename.endswith(".m4a"):
        # 构建输入文件和输出文件的完整路径
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + ".wav")
        
        # 使用FFmpeg将M4A文件转换为WAV文件
        subprocess.call([ffmpeg_path, "-i", input_file, output_file])

print("转换完成")