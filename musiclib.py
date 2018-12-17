from settings import MUSIC_DIR, SHUFFLE, REPEAT
from threading import Thread
from queue import Queue, Empty
import os
import random
import pygame
from time import sleep

pygame.mixer.init(buffer=1024)
if os.name != 'nt':
    pygame.init()


class MusicLibrary(Thread):
    library = dict()
    songs_queue = Queue()
    stopped = True
    paused = False

    def run(self):
        self.scan_library()
        while True:
            pygame.mixer.music.load(self.songs_queue.get())
            self.stopped = False
            self.paused = False
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(1.0)
            while pygame.mixer.music.get_busy() and not self.stopped:
                sleep(0.2)
            self.songs_queue.task_done()
            if self.stopped:
                pygame.mixer.music.stop()

    def scan_library(self):
        for item in os.listdir(MUSIC_DIR):
            if os.path.isdir(os.path.join(MUSIC_DIR, item)):
                self.library[item] = []
        for dir_name in self.library:
            category_dir = os.path.join(MUSIC_DIR, dir_name)
            for item in os.listdir(category_dir):
                full_path = os.path.join(category_dir, item)
                if os.path.isfile(full_path) and (item.lower()[-4:] in ('.ogg', '.mp3')):
                    self.library[dir_name].append(full_path)

    def get_categories(self, empty=False):
        return [name for name in self.library if empty or self.library[name]]

    def drain_queue(self):
        while not self.songs_queue.empty():
            try:
                self.songs_queue.get(False)
            except Empty:
                continue
            else:
                self.songs_queue.task_done()

    def get_playlist(self, category=None, shuffle=SHUFFLE, repeat=REPEAT):
        playlist = []
        if category:
            for song in self.library[category]:
                playlist.append(song)
        else:
            for category in self.library:
                for song in self.library[category]:
                    playlist.append(song)

        playlist = playlist * repeat

        if shuffle:
            random.shuffle(playlist)

        return playlist

    def play_category(self, category):
        if category == 'all':
            song_list = self.get_playlist()
        else:
            song_list = self.get_playlist(category=category)
        self.stop()
        [self.songs_queue.put(song) for song in song_list]
        self.stopped = False

    def stop(self):
        self.drain_queue()
        self.stopped = True
        self.paused = False
        self.songs_queue.join()

    def pause(self):
        if pygame.mixer.music.get_busy():
            self.paused = True
            pygame.mixer.music.pause()
        else:
            self.paused = False

    def resume(self):
        if pygame.mixer.music.get_busy():
            self.paused = False
            pygame.mixer.music.unpause()

if __name__ == "__main__":
    print(MusicLibrary().get_categories())
