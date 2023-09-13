import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import  csv
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Spider_cnki():

    def __init__(self,key_word,need,filename):

        self.key_word = key_word
        self.need = need
        self.filename = filename
        self.opt = Options()
        # self.opt.add_argument('--headless')  # 启用无界面模式
        self.driver = webdriver.Chrome(options=self.opt)
    def open_cnki(self):

        self.driver.get('https://www.cnki.net/')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="txt_SearchText"]'))).send_keys(self.key_word)
        # time.sleep(random.uniform(1,2))
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/input[2]'))).click()
        # time.sleep(random.uniform(1, 2))
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div/div/a[1]'))).click()
        # time.sleep(random.uniform(1, 2))
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[1]/div/ul[1]/li[2]/a'))).click()
        # time.sleep(random.uniform(1, 2))
        text=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[1]/div[1]/span[1]/em'))).text
        print(f'找到{text}条结果')
        return text
        # time.sleep(10)


    def get_data(self):
        for i in range(1, 21):

            time.sleep(0.5)
            j = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,f'/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{i}]/td[1]'))).text
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr[{i}]/td[2]/a'))).click()
            n1 = self.driver.window_handles[-1]
            self.driver.switch_to.window(n1)

            print(f'正在获取第{j}条结果')
            title=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div[1]/h1'))).text
            name=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div[1]/h3[1]/span/a'))).text
            university =WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div[1]/h3[2]/span/a'))).text
            key_words = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div[3]/p'))).text
            abstract = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div[2]/span[2]' ))).text

            print('论文题目',title,'姓名',name,'学校',university,'关键词',key_words,'摘要',abstract,)
            with open(self.filename, 'a', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerow([title, name, university, key_words, abstract])

            # time.sleep(1)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        # time.sleep(20)


    def next(self):
        WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH,'//*[@id="PageNext"]'))).click()




if __name__ == '__main__':
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"
    print('这是一个获取知网论文信息的脚本。\n信息会被保存在本脚本所处位置下。\n直接在下面输入想要搜集的论文方向即可。')
    key_word = input('请输入您想要获取的论文关键词：')
    filename = key_word + '.csv'
    with open(filename, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(['论文题目', '姓名', '学校', '关键词', '摘要'])

    need, page = int(input("请输入想要获取的条数：")) / 20, 0
    cnik = Spider_cnki(key_word, need, filename)
    cnik.open_cnki()
    while page < need:
        cnik.get_data()
        cnik.next()
        page += 1
    # amount=(cnik.open_cnki())