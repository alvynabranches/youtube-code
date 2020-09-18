try:
    import pytesseract as _
except:
    import os, sys, subprocess
    subprocess.call(f'{sys.executable} -m pip install pytesseract')
    # os.system(f'{sys.executable} {__file__}')
    
import os
from PIL import Image
import pytesseract as tess

def image_text(image:str):
    img = Image.open(image)
    return tess.image_to_string(img, nice=2)

def image_file(filename:str):
    with open(filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '') + '.txt', 'wb') as f:
        text = image_text(filename)
        text = text.replace('\n\n\n\n', '\n')
        text = text.replace('\n\n \n', '\n')
        text = text.replace('\n\n', '\n')
        text = text.replace('\n    \n', '\n')
        text = text.replace('\n  \n  \n \n', '\n')
        text = text.replace(' \n \n     \n      \n  \n', '\n')
        text = text.replace('\\', '')
        f.write(bytes(text, 'utf-16'))
        f.close()
        
def folder_image_text(img_path:str):
    for file in os.listdir(img_path):
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            image_file(os.path.join(img_path, file))
            
folder_image_text('images', 'text_files')