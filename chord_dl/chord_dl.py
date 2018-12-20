import pygame
import pygame.midi
import pandas
import msvcrt

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
            if kb.decode() == "r":
                chord = []
    #コードを返す
    return chord

def loop():
    try:
        with open("data/index.txt",mode="r") as data:
            ind = int(data.read())
    except FileNotFoundError:
        ind = 0
        
    chords = []
    print("Press d to end a section. reset button:r")

    while True:
        cho = input_chord()
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

        if msvcrt.kbhit():
            kb = msvcrt.getch()
            if kb.decode() == "d":
                print("end section")
                break
            if kb.decode() == "r":
                print("chords are reseted")
                chords = []

    ind += 1
    with open("data/index.txt",mode="w") as data:
        data.write(ind)

    #データフレームにする
    df = pandas.DataFrame(chords,
                          columns=["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0",
                                   "C1","C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1"])
    df.to_csv("data/data/"+str(ind)+".csv")

print("press q to quit.")
while True:
    loop()
    if msvcrt.kbhit():
        kb = msvcrt.getch()
        if kb.decode() == "q":
            break
