#!/bin/bash

# -c:v copy和-c:a copy表示视频和音频都不进行重编码 直接复制到输出文件中
# -f segment表示以分段的方式进行裁剪
# -segment_time 120表示每个分段的时长为2分钟
# -segment_start_time 0表示从视频的起始位置开始进行分段
# -segment_format mkv表示生成mkv格式的分段视频文件
# -reset_timestamps 1表示重置时间戳
# -movflags +faststart表示生成的mkv文件可以进行快速启动
# -avoid_negative_ts 1表示避免生成负时间戳
# -segment_list output.m3u8和-segment_list_type m3u8表示生成m3u8播放列表文件，并指定其格式为m3u8
split_video(){
    ffmpeg -i input.mkv \
        -c:v copy \
        -c:a copy \
        -f segment \
        -segment_time 120 \
        -segment_list output.m3u8 \
        -segment_list_type m3u8 \
        -segment_format mkv \
        -reset_timestamps 1 \
        -movflags +faststart \
        -avoid_negative_ts 1 \
        -segment_time_delta 10 \
        output_%03d.mkv
}

split_video


# 最后，需要将每段视频的开始时间和结束时间进行调整，以满足重叠的需求。这可以通过手动编辑m3u8播放列表文件来完成。