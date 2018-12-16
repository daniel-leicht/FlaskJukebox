from flask import Flask, render_template, request
import pygame
import os

pygame.mixer.init(buffer=1024)
app = Flask(__name__)

if os.name != 'nt':
    pygame.init()


@app.route('/')
def index():
    play = request.args.get('play', None)
    pause_flag = request.args.get('pause', False)
    resume_flag = request.args.get('resume', False)

    if play:
        play_something()
    elif pause_flag:
        pause_music()
    elif resume_flag:
        resume_music()

    return render_template('base.html')


def pause_music():
    pygame.mixer.music.pause()


def play_something():
    file = '/home/pi/sample.mp3'
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1.0)


def resume_music():
    pygame.mixer.music.unpause()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)
