import ffmpeg
import subprocess

def convert_video(format, filename, new_filename, video_status):
    # filename_without_ext = filename.split('.')[0]
    new_filename_with_ext = new_filename + '.' + format
    ffmpeg.input(filename) \
        .output(new_filename_with_ext) \
        .run()

    video_status.update({new_filename: True})
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


def simple_edit_video(filename, operations, new_filename, video_status):
    tmp_filename = new_filename + '.' + video_extension(filename)
    stream = ffmpeg.input(filename)
    if 'hflip' in operations:
        stream = stream.hflip()
    if 'vflip' in operations:
        stream = stream.vflip()
    if 'trim_from' in operations and 'trim_to' in operations:
        from_frame = int(get_text_before_colon(operations.split('trim_from,')[1]))
        to_frame = int(get_text_before_colon(operations.split('trim_to,')[1]))
        stream = stream.trim(start_frame = from_frame, end_frame = to_frame)
    elif 'trim_from' in operations:
        from_frame = int(get_text_before_colon(operations.split('trim_from,')[1]))
        # stream = stream.trim(start_frame=from_frame)
        stream = stream.trim(start=from_frame)
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
        stream = stream.drawtext(text_to_add, x = x, y = y, fontsize=30, fontcolor=font_color)

    stream = stream.setpts('PTS-STARTPTS')
    stream.output(tmp_filename) \
        .run()

    video_status.update({new_filename: True})
    return tmp_filename

def watermark(filename, operations, new_filename, video_status):
    tmp_filename = new_filename + '.' + video_extension(filename)

    print(subprocess.run(['ffmpeg', '-y', '-i', filename, '-i', 'rejestracje-us-de.jpg',
                                   '-filter_complex', "[1][0]scale2ref=h=ow/mdar:w=iw/4[#A logo][movie];[#A logo]format=argb,colorchannelmixer=aa=0.5[#B logo transparent];[movie][#B logo transparent]overlay=(main_w-w)-(main_w*0.1):(main_h-h)-(main_h*0.1)", tmp_filename]))

    video_status.update({new_filename: True})
    return tmp_filename

def get_text_before_colon(text):
    return text.split(',')[0]

def video_extension(filename):
    return filename.split('.')[1]


def video_name(filename):
    return filename.split('.')[0]
