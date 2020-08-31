import sys, subprocess
modules_installed = False
try:
    import speech_recognition as _, moviepy as _, librosa as _, pydub as _
    modules_installed = True
except:
    modules_installed = False
    subprocess.call(f'{sys.executable} -m pip install --upgrade --user speechrecognition moviepy librosa pydub')
    modules_installed = True
finally:
    print('Successfully Installed All Requirements' if modules_installed else 'All Requirements are not installed successfully')
    # subprocess.call(f'{sys.executable} script.py')