import os
import threading
import uuid

from flask import Flask, request, send_file, make_response, jsonify
from flask_cors import CORS

import video_converter

app = Flask(__name__)
CORS(app)


@app.route("/convertVideo/<newFormat>", methods=["POST"])
def convertVideo(newFormat):
    global videos_status
    if request.method == 'POST':
        f = next(iter(request.files.values()))

        tmp_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(f.filename)
        f.save(tmp_filename)

        new_filename = str(uuid.uuid4())

        videos_status.update({new_filename: False})

        thread1 = threading.Thread(target=video_converter.convert_video,
                                   args=(newFormat, tmp_filename, new_filename, videos_status))
        thread1.start()

        return jsonify(uuid=new_filename)


@app.route("/putWatermark/<operations>", methods=["POST"])
def putWatermark(operations):
    global videos_status
    if request.method == 'POST':
        files = iter(request.files.values())
        image = next(files)
        video = next(files)

        tmp_video_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(video.filename)
        tmp_image_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(image.filename)

        video.save(tmp_video_filename)
        image.save(tmp_image_filename)

        new_filename = str(uuid.uuid4())
        videos_status.update({new_filename: False})

        thread1 = threading.Thread(target=video_converter.put_watermark,
                                   args=(
                                   tmp_video_filename, tmp_image_filename, new_filename, videos_status, operations))
        thread1.start()

        return jsonify(uuid=new_filename)


@app.route("/editVideo/<operations>", methods=["POST"])
def simpleEditVideo(operations):
    global videos_status
    if request.method == 'POST':
        f = next(iter(request.files.values()))
        tmp_filename = str(uuid.uuid4()) + '.' + video_converter.video_extension(f.filename)
        f.save(tmp_filename)

        new_filename = str(uuid.uuid4())

        videos_status.update({new_filename: False})

        thread1 = threading.Thread(target=video_converter.simple_edit_video,
                                   args=(tmp_filename, operations, new_filename, videos_status))

        thread1.start()

        return jsonify(uuid=new_filename)


@app.route("/downloadVideo/<user_uuid>", methods=["POST"])
def downloadVideo(user_uuid):
    global videos_status
    if request.method == 'POST':
        if videos_status.get(user_uuid, False) is True:
            for fname in os.listdir('.'):
                if fname.startswith(user_uuid):
                    response = make_response(send_file("/backend/" + fname, attachment_filename=fname))
                    # response = make_response(send_file(fname, attachment_filename=fname))
                    response.headers['x-suggested-filename'] = fname
                    return response
    return "not found"


@app.route("/status/<user_uuid>", methods=["POST"])
def status(user_uuid):
    global videos_status
    if request.method == 'POST':
        if videos_status.get(user_uuid, False) == True:
            return str("100")
        elif videos_status.get(user_uuid, False) == -1:
            return "error", 410
        if videos_status.get(user_uuid, False) != False:
            percent = videos_status.get(user_uuid)
            return str(percent)
    return "0"


if __name__ == '__main__':
    open_sockets = {}
    videos_status = {}
    app.run(host="0.0.0.0", debug=True)
