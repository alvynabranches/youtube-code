try:
    import selenium as _, pandas as _, youtube_dl as _
except:
    import sys, subprocess
    subprocess.call(f'{sys.executable} -m pip install --upgrade --user selenium beautifulsoup4 youtube_dl')
    sys.exit()

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from warnings import filterwarnings
import os
from time import perf_counter
from youtube_dl import YoutubeDL
filterwarnings('ignore')

URL = 'https://www.youtube.com/c/LordsonRoch/videos'
START = 1
END = -1
BATCH_SIZE = 1
MAX_ITERATIONS = 1000

# START = int(input('Enter the starting value: '))
# END = int(input('Enter the ending value: '))
# BATCH_SIZE = int(input('Enter the batch size: '))
# MAX_ITERATIONS = int(input('Enter the max iterations: '))

s = perf_counter()
opts = ChromeOptions()
opts.headless = False
if os.path.isfile('links.xlsx'):
    df = pd.read_excel('links.xlsx')
    print('File Exists')
else:
    df = pd.DataFrame(columns=['links'])

driver = Chrome(executable_path='chromedriver.exe', options=opts)
driver.maximize_window()
driver.get()
driver.implicitly_wait(30)

for _ in range(MAX_ITERATIONS):
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    driver.implicitly_wait(100)

try:
    for element in driver.find_elements_by_id('items'):
        soup = BeautifulSoup(element.get_attribute('innerHTML'), 'html.parser')
        for link in soup.find_all('a', href=True):
            url = 'https://www.youtube.com' + str(link['href'])
            if 'watch' in str(link['href']):
                df = df.append({'links': url}, ignore_index=True).drop_duplicates()
except Exception as e:
    print(e)
finally:
    driver.close()
    df.to_excel('links.xlsx', index=False)

e = perf_counter()
print(f'Time taken for extracting the links: {e-s:4.3f} seconds')

# Downloading Part

s = perf_counter()
df = pd.read_excel('links.xlsx')
def download_ytvid(vid_url:list):
    with YoutubeDL({}) as ydl:
        ydl.download(vid_url)

def download_ytvids(video_link_list:list, start:int=1, end:int=1, batch_size:int=1, custom_link=None):
    all_batches = []
    start -= 1
    end = len(df['links']) if end == -1 else end
    for i in range(start, end+1, batch_size):
        # if video_link_list[i*batch_size:(i+1)*batch_size] != []:
        try:
            print(video_link_list[i*batch_size : (i+1)*batch_size])
        except:
            print(i*batch_size, (i+1)*batch_size)
            if os.path.isfile('not_completed.xlsx'):
                df = pd.read_excel('not_completed.xlsx')
                print('File Exists')
                df.append({'not_completed': video_link_list[i*batch_size : (i+1)*batch_size]}, ignore_index=True)
                df.to_excel('not_completed.xlsx')
            else:
                df = pd.DataFrame(columns=['not_completed'])
                df.append({'not_completed': video_link_list[i*batch_size : (i+1)*batch_size]}, ignore_index=True)
                df.to_excel('not_completed.xlsx')
e = perf_counter()
print(f'Time taken for load the file: {e-s:4.3f} seconds')

s = perf_counter()
download_ytvids(df['links'].values, start=START, end=END, batch_size=1)
e = perf_counter()
print(f'Time taken for downloading the videos: {e-s:4.3f} seconds')