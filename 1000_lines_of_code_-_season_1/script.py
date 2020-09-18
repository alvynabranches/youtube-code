from time import perf_counter, sleep

s = perf_counter()

import os
import sys
import subprocess
import socket

modules_installed = False
try:
    import speech_recognition as _
    import moviepy as _
    import pydub as _
    import selenium as _
    import pandas as _
    import youtube_dl as _
    modules_installed = True
except ModuleNotFoundError:
    modules_installed = False
    subprocess.call(f'{sys.executable} -m pip install --upgrade speechrecognition moviepy pydub selenium pandas beautifulsoup4 youtube_dl xlrd')
finally:
    if modules_installed:
        print('All modules are already installed')
    else:
        os.system(f'{sys.executable} {__file__}')
        
def time_taken(s, e):
    '''
        s: starting time
        e: ending time
    '''
    t = e - s; string = ''
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