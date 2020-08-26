import sys, subprocess

try:
    import speech_recognition as _, moviepy as _
except:
    subprocess.call(f'{sys.executable} -m pip install --upgrade --user speechrecognition moviepy')
finally:
    subprocess.call(f'{sys.executable} script.py')