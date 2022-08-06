from time import perf_counter

s = perf_counter()

import os
import moviepy.editor as mp
import speech_recognition as sr
import librosa
from pydub import AudioSegment
from pydub.silence import split_on_silence
import socket

VIDEO_DIRECTORY = os.path.join(os.getcwd(), 'youtube', '')
AUDIO_DIRECTORY = os.path.join(os.getcwd(), 'youtube_audios', '')
TEXT_DIRECTORY  = os.path.join(os.getcwd(), 'youtube_text', '')
TEMP_DIRECTORY = os.path.join(os.getcwd(), 'tmp', '')
VERBOSE = 1
SHUT_DOWN = 0 # 0 or False -> Wont SHUTDOWN, 1 or True -> WILL SHUTDOWN AFTER THE FULL CODE IS EXECUTED SUCESSFULLY
START = 51
END = 51

class VerboseError(IOError): pass

def time_taken(s, e):
    '''
        s: starting time
        e: ending time
    '''
    t = e - s
    string = ''
    if t > 60:
        string = f'Time Taken: {int(t/(60*60))} hour(s), {int(t/60)%60} minute(s), {int(t%60)} second(s), {int((t%1)*1e3)} millisecond(s)' if t > 60*60 else f'Time Taken: {int(t/60)%60} minute(s), {int(t)%60} second(s), {int((t%1)*1e3)} millisecond(s)'
    else:
        string = f'Time Taken: {int((t%1)*1e3)} millisecond(s) {int(((t%1)*1e6)%1e3)} microsecond(s) {int(((t%1)*1e9)%1e3)} nanosecond(s)' if t < 1 else f'Time Taken: {int(t%60)} second(s), {int((t%1)*1e3)} millisecond(s) {int(((t%1)*1e6)%1e3)} microsecond(s)'
    return string

def store_time(s, e, verbose=2, file='time.txt'):
    '''
        NOTE: REQUIRED Library to be Imported before applying this function: import os
        s: starting time.
        e: ending time.
        verbose: level of print information.
        file: file in which the time information should be saved in.
    '''
    if not os.path.isfile(file):
        try:
            with open(file, 'w') as f:
                f.write(str(e - s))
                f.close()
        except Exception as exception:
            if verbose == 2:
                print(exception)

            if verbose == 0 or verbose == 1 or verbose == 2 or verbose == None:
                print(e - s)
    
    else:
        try:
            with open(file, 'r') as f:
                t = float(f.read())
                f.close()

            with open(file, 'w') as f:
                f.write(str(float(t) + (e - s)))
                f.close()

        except Exception as exception:
            if verbose == 2:
                print(exception)

            if verbose == 0 or verbose == 1 or verbose == 2:
                print(e - s)

print('Process Started')

try:
    if not (VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2 or VERBOSE == None):
        raise VerboseError('VERBOSE can have value of either 0 or 1 or 2')
    
    if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
        if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
            print('No Internet Connection')
    else:
        if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
            print(f'Internet Connection Found Successfully at {socket.gethostbyname(socket.gethostname())}')
    
    if not os.path.isdir(VIDEO_DIRECTORY):
        raise FileNotFoundError('VIDEO DIRECTORY does not exist')
    
    if not os.path.isdir(AUDIO_DIRECTORY):
        os.mkdir(AUDIO_DIRECTORY)
    
    if not os.path.isdir(TEXT_DIRECTORY):
        os.mkdir(TEXT_DIRECTORY)
    
    if not os.path.isdir(TEMP_DIRECTORY):
        os.mkdir(TEMP_DIRECTORY)
    
    n = len(os.listdir(VIDEO_DIRECTORY))
    
    for i, file in enumerate(os.listdir(VIDEO_DIRECTORY)[START-1:n if END == -1 else END]):
        if VERBOSE == 1 or VERBOSE == 2:
            print(f'{START+i}/{n if END == -1 else END} Processing: {file=}.')
        
        try:
            if not os.path.isdir(TEMP_DIRECTORY):
                os.mkdir(TEMP_DIRECTORY)
            
            s1 = perf_counter()
            
            filename = file.replace('.mp4', '')
            
            video = mp.VideoFileClip(f'{VIDEO_DIRECTORY}{file}')
            
            if os.path.isfile(f'{TEXT_DIRECTORY}{filename}_1.txt') or os.path.isfile(f'{TEXT_DIRECTORY}{filename}_2.txt') or os.path.isfile(f'{TEXT_DIRECTORY}{filename}_3.txt') or os.path.isfile(f'{TEXT_DIRECTORY}{filename}_4.txt') or os.path.isfile(f'{TEXT_DIRECTORY}{filename}_5.txt') or os.path.isfile(f'{TEXT_DIRECTORY}{filename}_6.txt') or os.path.isfile(f'{TEXT_DIRECTORY}{filename}.txt'):
                continue
            
            if not os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.wav'):
                video.audio.write_audiofile(f'{AUDIO_DIRECTORY}{filename}.wav')
            
            if not os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.mp3'):
                video.audio.write_audiofile(f'{AUDIO_DIRECTORY}{filename}.mp3')
            
            if socket.gethostbyname(socket.gethostname()) != '127.0.0.1':
                ad = AudioSegment.from_wav(f'{AUDIO_DIRECTORY}{filename}.wav')
                
                chunks = split_on_silence(ad, min_silence_len=500)
                chunk_silent = AudioSegment.silent(50)
                
                c = 0
                result1, result2, result3 = '', '', ''
                
                for c_n, chunk in enumerate(chunks):
                    audio_chunk = chunk_silent + chunk + chunk_silent
                    
                    fn = f'{TEMP_DIRECTORY}chunk_{c}.wav'
                    
                    c += 1
                    
                    audio_chunk.export(fn, 'wav', bitrate='192k')
                    
                    r = sr.Recognizer()
                    with sr.AudioFile(fn) as source:
                        audio = r.record(source)
                    
                    g = False
                    try:
                        result1 += (' ' + r.recognize_google(audio))
                        g = True
                    except Exception as exception:
                        if VERBOSE == 2:
                            print(exception)
                        g = False
                    finally:
                        # if VERBOSE == 1:
                        #     print('Successful with Google API:' if g else 'Not Successful with Google API:', end='\r')
                        if VERBOSE == 2:
                            print('Successful with Google API' if g else 'Not Successful with Google API')
                        
                    sphinx = False
                    try:
                        result2 += (' ' + r.recognize_sphinx(audio))
                        sphinx = True
                    except Exception as exception:
                        if VERBOSE == 2:
                            print(exception)
                        sphinx = True
                    finally:
                        if VERBOSE == 2:
                            print('Successful with Sphinx API' if sphinx else 'Not Successful with Sphinx API')
                    
                    ibm = False
                    try:
                        result3 += (' ' + r.recognize_ibm(audio, 'alvynabranches@gmail.com', 'Aabs@2020'))
                        ibm = True
                    except Exception as exception:
                        if VERBOSE == 2:
                            print(exception)
                        ibm = False
                    finally:
                        if VERBOSE == 2:
                            print('Successful with IBM API' if ibm else 'Not Successful with IBM API')
                    
                    if VERBOSE == 1:
                        print(f'{c_n+1:4} Chunks Done.', end='\r')
                    elif VERBOSE == 2:
                        print(f'{c_n+1} Chunks Done.')
                if VERBOSE == 1:
                    print()
                
                with open(f'{TEXT_DIRECTORY}{filename}_1.txt', 'w') as f:
                    f.write(result1)
                    f.close()
                
                with open(f'{TEXT_DIRECTORY}{filename}_2.txt', 'w') as f:
                    f.write(result2)
                    f.close()
                
                with open(f'{TEXT_DIRECTORY}{filename}_3.txt', 'w') as f:
                    f.write(result3)
                    f.close()
                
                r = sr.Recognizer()
                with sr.AudioFile(f'{AUDIO_DIRECTORY}{filename}.wav') as source:
                    audio = r.record(source)
                
                g = False
                try:
                    result1 = r.recognize_google(audio)
                    g = True
                except Exception as exception:
                    if VERBOSE == 2:
                        print(exception)
                    g = False
                finally:
                    if VERBOSE == 1:
                        pass
                    elif VERBOSE == 2:
                        print('Successful with Google API' if g else 'Not Successful with Google API')
                
                sphinx = False
                try:
                    result2 = r.recognize_sphinx(audio)
                    sphinx = True
                except Exception as exception:
                    if VERBOSE == 2:
                        print(exception)
                    sphinx = False
                finally:
                    if VERBOSE == 2:
                        print('Successful with Sphinx API' if sphinx else 'Not Successful with Sphinx API')
                
                ibm = False
                try:
                    result3 = r.recognize_ibm(audio,'alvynabranches@gmail.com', 'Aabs@2020')
                    ibm = True
                except Exception as exception:
                    if VERBOSE == 2:
                        print(exception)
                    ibm = False
                finally:
                    if VERBOSE == 2:
                        print('Successful with IBM API' if ibm else 'Not Successful with IBM API')
                
                with open(f'{TEXT_DIRECTORY}{filename}_4.txt', 'w') as f: 
                    f.write(result1)
                    f.close()
                
                with open(f'{TEXT_DIRECTORY}{filename}_5.txt', 'w') as f:
                    f.write(result2)
                    f.close()
                with open(f'{TEXT_DIRECTORY}{filename}_6.txt', 'w') as f: 
                    f.write(result3)
                    f.close()
                if os.path.isfile(f'{TEXT_DIRECTORY}{filename}_1.txt') and os.path.isfile(f'{TEXT_DIRECTORY}{filename}_2.txt') and os.path.isfile(f'{TEXT_DIRECTORY}{filename}_3.txt') and os.path.isfile(f'{TEXT_DIRECTORY}{filename}_4.txt') and os.path.isfile(f'{TEXT_DIRECTORY}{filename}_5.txt') and os.path.isfile(f'{TEXT_DIRECTORY}{filename}_6.txt'):
                    if os.path.isfile(f'{AUDIO_DIRECTORY}{filename}.wav'):
                        os.remove(f'{AUDIO_DIRECTORY}{filename}.wav')
            else:
                if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
                    print('No Internet Connection')

        except Exception as exception:
            if VERBOSE == 2:
                print(exception)
        finally:
            if os.path.isdir(TEMP_DIRECTORY):
                for files in os.listdir(TEMP_DIRECTORY):
                    if os.path.isfile(TEMP_DIRECTORY + files):
                        os.remove(TEMP_DIRECTORY + files)

            e1 = perf_counter()

            if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
                print(f'{START+i}/{n if END == -1 else END} Done: {file=}.')

            if VERBOSE == 1 or VERBOSE == 2:
                print(time_taken(s1, e1))

except KeyboardInterrupt as ki:
    if VERBOSE == 2:
        print(ki)
except VerboseError as ve:
    print(ve)
except InterruptedError as ie:
    if VERBOSE == 2:
        print(ie)
except OSError as ose:
    if VERBOSE == 2:
        print(ose)
except FileNotFoundError as fee:
    if VERBOSE == 2:
        print(fee)
    
    e = perf_counter()

    if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
        print(time_taken(s, e))

    store_time(s, e, VERBOSE)

    if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
        print(f'Total {time_taken(0, float(open("time.txt", "r").read()))}')

    raise FileNotFoundError('VIDEO DIRECTORY does not exist')

except Exception as exception:
    if VERBOSE == 2:
        print(exception)
finally:
    try:
        if os.path.isdir(TEMP_DIRECTORY):
            os.removedirs(TEMP_DIRECTORY)
    except Exception as exception:
        if VERBOSE == 1 or VERBOSE == 2:
            print(f'TEMP DIRECTORY cannot be removed: {exception}')

    for file in os.listdir(TEXT_DIRECTORY):
        try:
            if os.path.getsize(TEXT_DIRECTORY + file) == 0:
                os.remove(TEXT_DIRECTORY + file)
        except Exception as exception:
            if VERBOSE == 2:
                print(exception)

    # EXTRA CODE HERE

    e = perf_counter()

    if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
        print(time_taken(s, e))

    store_time(s, e, VERBOSE)

    if VERBOSE == 0 or VERBOSE == 1 or VERBOSE == 2:
        print(f'Total {time_taken(0, float(open("time.txt", "r").read()))}')

    if SHUT_DOWN == 1 or SHUT_DOWN == True:
        os.system('shutdown /s /t 15')