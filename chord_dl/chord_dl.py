import pygame
import os
import pygame.midi
import pandas
import msvcrt


os.makedirs("data", exist_ok=True)
os.makedirs("data/data", exist_ok=True)

pygame.init()
pygame.midi.init()

print("MIDI IDs")
for i in range(pygame.midi.get_count()):
    print("%d: %s"%(i,pygame.midi.get_device_info(i)))
input_id = int(input("input ID: "))
i = pygame.midi.Input(input_id)

#一個コードを入力する
def input_chord():
    chord = []
    print("Press n to input next chord. reset button:r")
    while True:
        if i.poll():
            midi_events = i.read(10)
            if midi_events[0][0][0] == 144:
                chord.append(midi_events[0][0][1])
            chord = list(set(chord))
            print("\r temporary inputs: ",chord,end="")

        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == "n":
                print("\n input chord: ",chord)
                break
            elif kb.decode() == "r":
                chord = []
                print("reset chord")
            elif kb.decode() == "d":
                return "d"
            elif kb.decode() == "0":
                return "0"
            elif kb.decode() == "q":
                return "q"
    #コードを返す
    return chord

def loop():
    try:
        with open("data/index.txt",mode="r") as data:
            ind = int(data.read())
    except FileNotFoundError:
        ind = 0
    
    chords = []
    print("press q to quit.")
    print("Press d to end a section. reset button:0")

    while True:
        cho = input_chord()
        if cho == "d":
            print("end section")
            break
        elif cho == "0":
            print("chords are reseted")
            chords = []
            continue
        elif cho == "q":
            return "q"
        elif len(cho) == 0:
            print("input a chord")
            continue

        #そろえる
        min_of_ch = min(cho)
        oct_ch = min_of_ch//12
        cho = list(map(lambda x:x - (oct_ch*12),cho))
        #ダミー変数的に
        cho_dum = [0 for i in range(24)]
        for i in range(24):
            if i in cho:
                cho_dum[i] = 1
            else:
                cho_dum[i] = 0
        chords.append(cho_dum)

    ind += 1
    with open("data/index.txt",mode="w") as data:
        data.write(str(ind))

    #データフレームにする
    df = pandas.DataFrame(chords,
                          columns=["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0",
                                   "C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1"])
    df.to_csv("data/data/"+str(ind)+".csv")

    return None


while True:
    ret = loop()
    if ret == "q":
        print("quit")
        break