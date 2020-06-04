import os
import re
import subprocess

import ffmpeg


def convert_video(format, filename, new_filename, video_status):
    try:
        new_filename_with_ext = new_filename + '.' + format
        stream = ffmpeg.input(filename) \
            .output(new_filename_with_ext)

        nb_frame = frame_number(filename)

        process = return_with_progress(stream)

        update_progress(new_filename, video_status, process, nb_frame)

        is_video_file_created(new_filename_with_ext, video_status, new_filename)
    except:
        video_status.update({new_filename: -1})

    return new_filename


def get_xy_text_position(position):
    if position == 'Top left':
        return ("10", "10")
    elif position == 'Top right':
        return ("w-tw-10", "10")
    elif position == 'Bottom left':
        return ("10", "h-th-10")
    else:
        return ("w-tw-10", "h-th-10")


def return_with_progress(stream_spec):
    args = ffmpeg.compile(stream_spec)
    return subprocess.Popen(
        args, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    )


def frame_number(file_video):
    result = ffmpeg.probe(file_video)
    return int(result['streams'][0]['nb_frames'])


def update_progress(new_filename, video_status, process, nb_frame):
    for line in process.stdout:
        if line.startswith("frame"):
            print(line)
            current_frame = int(re.split(r"frame=\s*([0-9]*)\s.*", line)[1])
            percent = int((current_frame / nb_frame) * 100)
            video_status.update({new_filename: percent})


def simple_edit_video(filename, operations, new_filename, video_status):
    tmp_filename = new_filename + '.' + video_extension(filename)
    try:
        stream = ffmpeg.input(filename)
        if 'hflip' in operations:
            stream = stream.hflip()
        if 'vflip' in operations:
            stream = stream.vflip()
        if 'trim_from' in operations and 'trim_to' in operations:
            from_frame = int(get_text_before_colon(operations.split('trim_from,')[1]))
            to_frame = int(get_text_before_colon(operations.split('trim_to,')[1]))
            stream = stream.trim(start_frame=from_frame, end_frame=to_frame)
        elif 'trim_from' in operations:
            from_frame = int(get_text_before_colon(operations.split('trim_from,')[1]))
            stream = stream.trim(start_frame=from_frame)
        elif 'trim_to' in operations:
            to_frame = int(get_text_before_colon(operations.split('trim_to,')[1]))
            stream = stream.trim(end_frame=to_frame)
        if 'text_to_add' in operations:
            text_to_add = get_text_before_colon(operations.split('text_to_add,')[1])
            text_position = get_text_before_colon(operations.split('text_position,')[1])
            if ',' in text_to_add:
                text_to_add = text_to_add.split(',')[0]
            font_color = get_text_before_colon(operations.split('font_color,')[1])
            (x, y) = get_xy_text_position(text_position)
            stream = stream.drawtext(text_to_add, x=x, y=y, fontsize=30, fontcolor=font_color)

        stream = stream.setpts('PTS-STARTPTS')
        stream = stream.output(tmp_filename)

        nb_frame = frame_number(filename)

        process = return_with_progress(stream)

        update_progress(new_filename, video_status, process, nb_frame)

        is_video_file_created(tmp_filename, video_status, new_filename)

    except:
        video_status.update({new_filename: -1})

    return tmp_filename


def watermark_position(position):
    if position == 'Top left':
        return "(main_w*0.1):(main_h*0.1)"
    elif position == 'Top right':
        return "(main_w-w)-(main_w*0.1):(main_h*0.1)"
    elif position == 'Bottom left':
        return "(main_w*0.1):(main_h-h)-(main_h*0.1)"
    else:
        return "(main_w-w)-(main_w*0.1):(main_h-h)-(main_h*0.1)"


def put_watermark(video_filename, image_filename, new_filename, video_status, operations):
    tmp_filename = new_filename + '.' + video_extension(video_filename)

    try:
        string_position = get_text_before_colon(operations.split('position,')[1])
        opacity = get_text_before_colon(operations.split('opacity,')[1])
        position = watermark_position(string_position)

        nb_frame = frame_number(video_filename)

        process = subprocess.Popen(['ffmpeg', '-y', '-i', video_filename, '-i', image_filename,
                                    '-filter_complex',
                                    f"[1][0]scale2ref=h=ow/mdar:w=iw/4[#A logo][movie];[#A logo]format=argb,colorchannelmixer=aa={opacity}[#B logo transparent];[movie][#B logo transparent]overlay={position}",
                                    tmp_filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True)

        update_progress(new_filename, video_status, process, nb_frame)

        is_video_file_created(tmp_filename, video_status, new_filename)

    except:
        video_status.update({new_filename: -1})
    return tmp_filename


def get_text_before_colon(text):
    return text.split(',')[0]


def video_extension(filename):
    return filename.split('.')[1]


def video_name(filename):
    return filename.split('.')[0]


def is_video_file_created(file_name, video_status, uuid):
    if os.path.isfile(file_name) and os.path.getsize(file_name) > 200:
        video_status.update({uuid: True})
    else:
        video_status.update({uuid: -1})
