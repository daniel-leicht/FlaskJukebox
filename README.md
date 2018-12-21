# FlaskJukebox
Python/Flask web based MP3 library player, excellent for RaspberryPi based jukeboxes.
(FlaskJukebox was tested and works with Python 3)

![FlaskJukeBox on RPi](https://i.imgur.com/nYxdhvN.jpg "FlaskJukebox on RaspberryPi with a 3.5inch touchscreen")

## Raspberry Pi stuff 
To auto start chrome and point it to FlaskJukeBox, add the following lines to /home/pi/.config/lxsession/LXDE-pi/autostart (tested on pi3):
```
@amixer set PCM -- -100
@sudo nohup python3 /home/pi/FlaskJukebox/FlaskJukebox.py &
@xset s off
@xset -dpms
@xset s noblank
@amixer cset numid=3 1
@chromium-browser --app=http://127.0.0.1/ --start-fullscreen --disable-restore-session-state --noerrdialogs --disable-translate --no-first-run --fast --fast-start --disable-infobars --disk-cache-dir=/dev/null
```
Change the /home/pi/FlaskJukebox/ to the path of FlaskJukebox

To hide the mouse cursor (good for touchscreens) in /etc/lightdm/lightdm.conf, uncomment:
```
#xserver-command=X
```
and change it to:
```
xserver-command=X -nocursor
```
