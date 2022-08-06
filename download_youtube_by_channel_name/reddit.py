import os
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome, ChromeOptions

MAX_ITERATIONS = int(10**6) # Increase / Decrease this constant to get more / less records respectively
MACHINE = 'WIN'
SCRAPE = True # If SCRAPE is False, the script wont scrape but will check for the file and read that data
FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.xlsx')
SAVE = True # Saves the data into a file if True else uses just the previous data

topics = ['node.js', 'css']

# These options work for Windows as well as replit
if SCRAPE:
    opts = ChromeOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.headless = False

# Add options according to user settings
if SCRAPE:
    if MACHINE.upper() == 'WIN' or MACHINE.upper() == 'WINDOWS':
        # Works with Windows specific on my machine
        driver = Chrome('D:/chrome_driver/chromedriver.exe', options=opts)
    else: driver = Chrome(options=opts) # Works with Replit

titles = []
if SCRAPE:
    driver.get('https://www.reddit.com/r/webdev/')
    driver.implicitly_wait(30)
    for _ in range(MAX_ITERATIONS):
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        driver.implicitly_wait(30)
        for title in driver.find_elements_by_class_name('_eYtD2XCVieq6emjKBH3m'):
            title = title.text.strip()
            if title != '':
                titles.append(title)

    driver.close()
# del MAX_ITERATIONS, driver

if MACHINE.upper() == 'WIN' or MACHINE.upper() == 'WINDOWS':
    if os.path.isfile(FILE):
        df = pd.read_excel(FILE)
        if len(titles) > 0:
            for title in titles:
                df = df.append(dict(title=title), ignore_index=True)
    else: df = pd.DataFrame(columns=['title'], data=titles)
else: df = pd.DataFrame(columns=['title'], data=titles)

df.drop_duplicates(inplace=True)

if SAVE: df.to_excel(FILE, index=False)

del titles
filtered_output = []
for title in df['title'].values.tolist():
    for topic in topics:
        title, topic = title.lower(), topic.lower()
        if topic in title or topic.replace('.', ' ') in title or topic.replace('.', ' ') in title or topic.replace('.', '') in title: 
            filtered_output.append(title)
            break
            
print(filtered_output)