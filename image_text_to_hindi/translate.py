try:
    import googletrans as _
except:
    import os, sys, subprocess
    subprocess.call(f'{sys.executable} -m pip install --user --upgrade googletrans')
    # os.system(f'{sys.executable} {__file__}')
    
from googletrans import Translator
import socket

class UnknownLanguage(IOError): pass
    
def convert(text, src_lang='english', dest_lang:tuple=('hindi', 'marathi')):
    '''
        Only works for english, hindi and marathi
    '''
    def lang_code(lang):
        if lang == 'english' or lang == 'eng' or lang == 'en':
            return 'en'
        elif lang == 'hindi' or lang == 'hin' or lang == 'hi':
            return 'hi'
        elif lang == 'marathi':
            return 'mr'
        else:
            raise UnknownLanguage('Language Not Found')
        
    all_text = dict()
    trans = Translator()
    
    all_text[src_lang] = text
    for d in dest_lang:
        d = d.lower()
        if socket.gethostbyname(socket.gethostname()):
            t = trans.translate(text, dest=lang_code(d), src=lang_code(src_lang))
        else:
            print('No Internet Connection')
        all_text[d] = {}
        all_text[d]['text'] = t.text
        all_text[d]['possible_mistakes'] = t.extra_data['possible-mistakes']
        all_text[d]['possible_translations'] = t.extra_data['possible-translations']
    return all_text

# print(convert('Hello folks, welcome to India'))