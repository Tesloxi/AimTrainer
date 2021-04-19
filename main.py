#!/usr/bin/python3
# -*- coding: utf-8 -*

"""AimTrainer game with pygame."""

import os
import tkinter as tk

from pygame import *
from random import randint, randrange

init()

# Setup main display

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

WIDTH = screen_width // 2
HEIGHT = screen_height // 2

win_x = screen_width // 2 - WIDTH // 2
win_y = screen_height // 2 - HEIGHT // 2

os.environ["SDL_VIDEO_WINDOW_POS"] = str(win_x) + ',' + str(win_y)
win = display.set_mode((WIDTH, HEIGHT)) # main window
rect = win.get_rect()
display.set_caption("AimTrainer")
display.set_icon(image.load("target.png"))

# Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts

BUTTON_FONT = font.SysFont('calibri', 60)
TITLE_FONT = font.SysFont('calibri', 80)
HITS_FONT = font.SysFont('calibri', 40)

# Menu display settings

title = TITLE_FONT.render("Aim Trainer", 1, WHITE)
title_rect = title.get_rect(center = (rect.centerx, rect.h // 4))

play_button = BUTTON_FONT.render("PLAY", 1, WHITE)
play_button_rect = play_button.get_rect(center = rect.center)

def display_menu(surface):
    surface.blit(title, title_rect)
    surface.blit(play_button, play_button_rect)

class Target:
    """"""

    def __init__(self, image_path):
        self.image_path = image_path
        self.w = self.h = randrange(20, 80, 5)
        self.image = transform.scale(image.load(self.image_path), (self.w, self.h))
        self.rect = self.image.get_rect()

    def new_pos(self):
        """Generate a new position and size"""

        self.w = self.h = randrange(20, 80, 5)
        self.image = transform.scale(image.load(self.image_path), (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, rect.w - self.w)
        self.rect.y = randint(0, rect.h - self.h)
        
# Game settings

hits = 0
chrono_start = 0
time_elapsed = 0

# Setup game loop

FPS = 60
clock = time.Clock()
run = True
play = False
end = False

while run:
    clock.tick(FPS)    

    display_menu(win)
    display.update()

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1:
                pos = mouse.get_pos()
                if play_button_rect.collidepoint(pos):
                    play = True
                    target = Target("target.png")
                    target.new_pos()
                    chrono_start = time.get_ticks()

    while play:
        clock.tick(FPS)

        time_elapsed = int((time.get_ticks() - chrono_start) / 1000)

        time_text = HITS_FONT.render("TIME: " + str(time_elapsed) + "s", 1, WHITE)
        time_rect = time_text.get_rect(center = (rect.centerx // 2, rect.h // 10))
        hits_text = HITS_FONT.render("HITS: " + str(hits), 1, WHITE)
        hits_rect = hits_text.get_rect(center = (rect.centerx, rect.h // 10))
        win.fill(BLACK)
        win.blit(time_text, time_rect)
        win.blit(hits_text, hits_rect)
        win.blit(target.image, target.rect)
        display.update()

        if time_elapsed >= 30:
            play = False
            end = True
            win.blit(play_button, play_button_rect)
            display.update()

        for e in event.get():
            if e.type == QUIT:
                play = False
                run = False
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    pos = mouse.get_pos()
                    if target.rect.collidepoint(pos):
                        win.fill(BLACK)
                        target.new_pos()
                        hits += 1
    
    while end:
        clock.tick(FPS)

        win.fill(BLACK)

        for e in event.get():
            if e.type == QUIT:
                end = False
                run = False
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    pos = mouse.get_pos()
                    if play_button_rect.collidepoint(pos):
                        end = False
                        play = True
                        hits = 0
                        chrono_start = time.get_ticks()
                        time_elapsed = 0
                        
quit()