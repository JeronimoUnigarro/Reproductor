import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

class Track:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add(self, data):
        new_node = Track(data)
        if self.head is None:
            self.head = self.tail = self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def remove_current(self):
        if self.current is None:
            return
        if self.current == self.head:
            self.head = self.current.next
            if self.head:
                self.head.prev = None
        elif self.current == self.tail:
            self.tail = self.current.prev
            if self.tail:
                self.tail.next = None
        else:
            self.current.prev.next = self.current.next
            self.current.next.prev = self.current.prev

        self.current = self.current.next if self.current.next else self.tail

    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next

    def prev_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev

    def get_current_song(self):
        return self.current.data if self.current else None

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x300")
        self.playlist = DoublyLinkedList()

        pygame.mixer.init()

        self.label = tk.Label(self.root, text="No song selected", font=("Arial", 14))
        self.label.pack(pady=20)

        add_btn = tk.Button(self.root, text="Add Song", command=self.add_song)
        add_btn.pack(pady=10)

        remove_btn = tk.Button(self.root, text="Remove Song", command=self.remove_song)
        remove_btn.pack(pady=10)

        prev_btn = tk.Button(self.root, text="Previous", command=self.play_prev_song)
        prev_btn.pack(side=tk.LEFT, padx=20)

        next_btn = tk.Button(self.root, text="Next", command=self.play_next_song)
        next_btn.pack(side=tk.RIGHT, padx=20)

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.add(file_path)
            self.label.config(text=f"Added: {os.path.basename(file_path)}")

    def remove_song(self):
        current_song = self.playlist.get_current_song()
        if current_song:
            self.playlist.remove_current()
            pygame.mixer.music.stop()
            next_song = self.playlist.get_current_song()
            if next_song:
                self.label.config(text=f"Playing: {os.path.basename(next_song)}")
                pygame.mixer.music.load(next_song)
                pygame.mixer.music.play()
            else:
                self.label.config(text="No song selected")
        else:
            messagebox.showwarning("Warning", "No song to remove")

    def play_next_song(self):
        self.playlist.next_song()
        self.play_song()

    def play_prev_song(self):
        self.playlist.prev_song()
        self.play_song()

    def play_song(self):
        current_song = self.playlist.get_current_song()
        if current_song:
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()
            self.label.config(text=f"Playing: {os.path.basename(current_song)}")
        else:
            self.label.config(text="No song selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
