import os
import math
import subprocess


all_filename = []


def list_all_files(dirs):
    _files = []

    # 列出文件夹下的所有目录和文件
    l1 = os.listdir(dirs)
    # print(l1)
    all_filename.append(l1)

    for i in range(0, len(l1)):
        path = os.path.join(dirs, l1[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)

    return _files


media_from_dir = "/root/reference_videos"
media_target_dir = "/root/yingchao/master"

print(f'media_from_dir {media_from_dir}')
print(f'media_target_dir {media_target_dir}')

media_from_dir_files = list_all_files(media_from_dir)
media_from_dir_files = [v[:v.rfind(".")] for v in media_from_dir_files]

print(f'files: {media_from_dir_files}, len: {len(media_from_dir_files)}')

duration_time = 120


def slice_media(media_name, media_type):
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \
        {media_name}{media_type}"
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
               f'{start_time}', '-t', f'{duration_time}', '-an',
               f'{media_target_dir}/{output_name}']

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


for filename in media_from_dir_files:
    media_type = ".mkv"
    slice_media(filename, media_type)
