import pygame
import pygame.midi
import pandas
import msvcrt

pygame.init()
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
print("input MIDI:%d" % input_id)
i = pygame.midi.Input(input_id)

def input_chord():
    chord = []
    print("Press n to input next chord.")
    while True:
        if i.poll():
            midi_events = i.read(10)
            if midi_events[[[2]]] > 0:
                chord.append(midi_events[[[1]]])

        chord = list(set(chord))
        print("\r temporary inputs: ",chord,end="")
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == "n":
                print("input chord: ",chord)
                break

    return chord

def loop():
    chords = []
    print("Press d to end a section.")
    while True:
        chords.append(input_chord())
        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == "d":
                break

