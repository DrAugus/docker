import os
import math
import subprocess

media_name = "input"
media_type = ".mkv"

duration_time = 120

cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {media_name}{media_type}"
obj = os.popen(cmd)
res = obj.read()
media_len = math.ceil(float(res))
# 向上取整秒数
print('视频长度为: ', media_len)

# `-an`选项会删除视频中的音频
# 120s 裁剪一段，每段视频重叠上一段的最后 10s
for i in range(0, media_len, 110):
    start_time = i
    end_time = i + duration_time
    output_name = f"master_{media_name}_{start_time}_{end_time}{media_type}"
    cmd = ["ffmpeg", "-i", f'{media_name}{media_type}', '-ss',
           f'{start_time}', '-t', f'{duration_time}', '-an', f'{output_name}']

    print(cmd)
    # 执行 ffmpeg 命令
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # 获取输出结果
    output = str(stdout.decode('utf-8'))
    error = str(stderr.decode('utf-8'))
    # 打印输出结果
    print(f'Output for run {i}: {output}')
    print(f'Error for run {i}: {error}')
