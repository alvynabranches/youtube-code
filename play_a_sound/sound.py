import winsound
import time

major = 9/8
minor = 10/9
semi = 16/15

start_frequency = 323.63 # This is the frequency for E4
next_frequency = start_frequency
series = [ major, minor, semi, major, minor, major, semi]
scale =  [      'c'      ,  'd' ,  'e',  'f' ,  'g' ,  'a' ,  'b' , 'c']
c = [next_frequency := next_frequency * e for e in series]

# print(f'{c=}')
# for chord in c:
#     winsound.Beep(int(chord), 500)

# happy birthday song

# double_series = series + series
end_frequency = start_frequency * 2
b_flat = end_frequency + (end_frequency - end_frequency * semi)

'''
    |Happy Birthday Song Notes|
    C C D C F E
    C C D C G F
    C C C A F F E D
    B♭ B♭ A F G F
'''

line_1 = [0, 0, 1, 0, 3, 2]
line_2 = [0, 0, 1, 0, 4, 3]
line_3 = [0, 0, 0, 5, 3, 3, 2, 1]
line_4 = [-1, -1, 5, 3, 4, 3]

song_line_1 = [c[e] for e in line_1]
song_line_2 = [c[e] for e in line_2]
song_line_3 = [c[e] for e in line_3]
song_line_4 = [b_flat if e==-1 else c[e] for e in line_4]

print(f'{c=}\n{b_flat=}\n{song_line_1=}\n{song_line_2=}\n{song_line_3=}\n{song_line_4=}')

DURATION = 500
SLEEP_DURATION = 0.5


# SONG MAIN LINES
for e in song_line_1:
    winsound.Beep(int(e), DURATION)
time.sleep(SLEEP_DURATION)
for e in song_line_2:
    winsound.Beep(int(e), DURATION)
time.sleep(SLEEP_DURATION)
for e in song_line_3:
    winsound.Beep(int(e), DURATION)
time.sleep(SLEEP_DURATION)
for e in song_line_4:
    winsound.Beep(int(e), DURATION)
