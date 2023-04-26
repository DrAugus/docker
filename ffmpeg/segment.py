import os
import math
import subprocess


def print_list(l):
    print('len: ', len(l))
    for i in l:
        print(i)


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
# 文件路径
media_from_dir_path = [
    v[:v.rfind("/") + 1] for v in media_from_dir_files]
# 不带路径不带文件类型 只有文件名
media_from_dir_filename = [v[v.rfind("/") + 1:v.rfind(".")]
                           for v in media_from_dir_files]


print('>>> media_from_dir_files')
print_list(media_from_dir_files)

print('>>> media_from_dir_path')
print_list(media_from_dir_path)

print('>>> media_from_dir_filename')
print_list(media_from_dir_filename)


duration_time = 120


def slice_media(from_path, media_name, media_type):
    src_file = f'{from_path}{media_name}{media_type}'

    # 视频时长
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \
        {src_file}"
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
        cmd = ["ffmpeg", "-i", f'{src_file}', '-ss',
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
        output_log = f'Output for run {i}: {output}'
        output_error = f'Error for run {i}: {error}'
        print(output_log)
        print(output_error)
        # 打开文件并以追加模式写入内容
        with open('output.log', 'a') as f:
            print(output_log, file=f)
        with open('error.log', 'a') as f:
            print(output_error, file=f)


for i in range(len(media_from_dir_filename)):
    filename = media_from_dir_filename[i]
    filepath = media_from_dir_path[i]
    media_type = ".mkv"
    slice_media(filepath, filename, media_type)
