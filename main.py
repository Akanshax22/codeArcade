# main.py
from pygame import mixer
import pygame
from menu import menu
from intro import intro
from select_module import run_select_module


# Run the modules
intro()
pygame.mixer.init()
mixer.music.load("Background.mp3")
mixer.music.play(-1)
menu()
run_select_module() 

