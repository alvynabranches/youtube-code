from time import perf_counter, sleep

import os
import moviepy.editor as mp
import speech_recognition as sr

def time_taken(s, e):
    t = e - s
    if t > 60:
        print(f'Time Taken: {int(t / (60*60))} hour(s), {int(t / 60)} minute(s), {int(t % 60)} second(s), {int((t%1)*1000)} millisecond(s)') if t > 60*60 else print(f'Time Taken: {int(t / 60)} minute(s), {int(t % 60)} second(s), {int((t%1)*1000)} millisecond(s)')
    else:
        print(f'Time Taken: {int((t%1)*1000)} millisecond(s)') if t < 1 else print(f'Time Taken: {int(t)} second(s), {int((t%1)*1000)} millisecond(s)')
s = perf_counter()

VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'videos', '')
AUDIO_DIRECTORY = os.path.join(os.getcwd(), 'audios', '')
TEXT_DIRECTORY  = os.path.join(os.getcwd(), 'text', '')

try:
    if not os.path.isdir(VIDEO_DIRECTORY):
        raise FileNotFoundError('VIDEO DIRECTORY does not exist')
    if not os.path.isdir(AUDIO_DIRECTORY):
        os.mkdir(AUDIO_DIRECTORY)
    if not os.path.isdir(TEXT_DIRECTORY):
        os.mkdir(TEXT_DIRECTORY)
    n = len(os.listdir(VIDEO_DIRECTORY))
    for i, file in enumerate(os.listdir(VIDEO_DIRECTORY)):
        filename = file.split('.')[0]
        ext = file.split('.')[1]
        video = mp.VideoFileClip(f'{VIDEO_DIRECTORY}{filename}.{ext}')
        if os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.wav'):
            os.remove(f'{AUDIO_DIRECTORY}{filename}.wav')
        if os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.mp3'):
            os.remove(f'{AUDIO_DIRECTORY}{filename}.mp3')
        video.audio.write_audiofile(f'{AUDIO_DIRECTORY}{filename}.wav')
        video.audio.write_audiofile(f'{AUDIO_DIRECTORY}{filename}.mp3')
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_DIRECTORY + filename + '.wav') as source:
            audio = r.record(source)
        result = r.recognize_google(audio)
        if os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.txt'):
            os.remove(f'{AUDIO_DIRECTORY}{filename}.txt')
        with open(f'{TEXT_DIRECTORY}{filename}.txt', 'w') as file: 
            file.write(result)
            file.close()
        if os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.wav'):
            os.remove(f'{AUDIO_DIRECTORY}{filename}.wav')

except KeyboardInterrupt as ki:
    print(ki)
except InterruptedError as ie:
    print(ie)
except OSError as ose:
    print(ose)
except FileExistsError as fee:
    print(fee)
    e = perf_counter()
    time_taken(s, e)
    raise FileNotFoundError('VIDEO DIRECTORY does not exist')
except Exception as e:
    print(e)
finally:
    e = perf_counter()
    time_taken(s, e)