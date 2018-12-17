from flask import Flask, render_template, request, redirect
from musiclib import MusicLibrary


app = Flask(__name__)


music_library = MusicLibrary()
music_library.start()
jukebox_dict = {}


@app.route('/')
def index():
    play = request.args.get('play', None)
    pause_flag = request.args.get('pause', False)
    resume_flag = request.args.get('resume', False)
    stop_flag = request.args.get('stop', False)

    if play:
        music_library.play_category(play)
    elif pause_flag:
        music_library.pause()
    elif resume_flag:
        music_library.resume()
    elif stop_flag:
        music_library.stop()
    else:
        return render_template('base.html', music_library=music_library)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)
