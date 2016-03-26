# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
pygame.display.set_caption('Hallo Kinder, das ist das Wortratespiel')

with open('/usr/share/dict/ngerman') as f:
    germandict = f.read().splitlines()

germandict = set(map(str.upper, germandict))

RED = (250, 0, 0)
BLACK = (10, 10, 10)
GREEN = (0, 250, 0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))
screen.blit(background, (0, 0))
current_word = ''
required_start = ''
message = ''

color = BLACK

already_seen_words = []

def render_text(word, col, ypos = 0, xpos = None):
    font = pygame.font.Font(None, 36)
    text = font.render(word, 1, col)
    centerx = background.get_width() / 2 if xpos == None else xpos
    textpos = text.get_rect(centerx = centerx, centery = 18 + ypos * 36)
    background.blit(text, textpos)

def render():
    background.fill((250, 250, 250))
    render_text(current_word, color)
    render_text(message, RED, 0, 200)
    render_words_so_far()
    screen.blit(background, (0, 0))
    pygame.display.flip()

def render_words_so_far():
    length = len(already_seen_words)
    text = 'Noch kein Wort...' if length == 0 else 'Schon ' + str(length)
    if length > 0:
        text += u' Wort' if length == 1 else u' Wörter'
    render_text(text, GREEN, 1)
    cnt = 2
    for word in reversed(already_seen_words):
        render_text(word, GREEN, cnt)
        cnt = cnt + 1

current_word = 'Bitte ein Anfangswort eingeben'
render()
current_word = ''

def quit():
    pygame.quit()
    sys.exit()

def check_word():
    global color, message
    color = RED if not current_word in germandict else BLACK
    message = ''
    if current_word not in germandict:
        message = 'Das Wort kenn ich nicht...'
    if current_word in already_seen_words:
        message = 'Das Wort gab es schonmal...'
        color = RED
    if len(current_word) == 1:
        message = 'Das Wort ist zu kurz...'
        color = RED
    render()

while True:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            quit()
        elif event.type == KEYDOWN and event.key == K_BACKSPACE:
            current_word = current_word[:-1]
            check_word()
        elif event.type == KEYDOWN and event.key == K_RETURN:
            message = ''
            if len(current_word) == 0:
                continue
            check_word()
            if current_word in already_seen_words:
                continue
            if current_word not in germandict:
                continue
            if len(current_word) == 1:
                continue
            already_seen_words.append(current_word)
            required_start = current_word[-1]
            current_word = ''
            render()
        elif event.type == KEYDOWN:
            if not event.unicode.isalpha():
                continue
            current_word = (current_word + event.unicode).upper()
            if not current_word.startswith(required_start):
                current_word = current_word[:-1]
                color = RED
            check_word()
