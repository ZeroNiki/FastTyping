import os
import random

BASEDIR = os.path.dirname(os.path.dirname(__file__))
text_pool = []

def load_text():
    global text_pool
    if not text_pool:
        with open(f"{BASEDIR}/test.txt", "r") as file:
            text_pool = [line.strip() for line in file.readlines()]

def start():
    load_text()
    return random.choice(text_pool)
    





