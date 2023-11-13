#selenium版本 4.15.2
#python 版本 3.12.0
#pandas 版本 2.1.2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

#通過Cloudflare的驗證
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
options.add_experimental_option('excludeSwitches',["enable-automation"])
options.add_experimental_option('useAutomationExtension',False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-extensions')
options.add_argument('--no--sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')


#爬取的網址
url = "https://www.hltv.org"
#想爬取的選手遊戲ID
player = "s1mple"
driver = webdriver.Chrome(options=options)
driver.get(url)

#跳過cloudflare驗證 使用js去另外開一個新視窗
driver.execute_script("window.open('url','_blank')")
time.sleep(5)
driver.switch_to.window(driver.window_handles[1])

#設置瀏覽器顯示為最大的大小，否則搜索框將不可見
driver.maximize_window()
# 等待最多10秒，直到所有元素可見
driver.implicitly_wait(10) 

#點選接受所有cookie
driver.find_element(By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll").click()
time.sleep(5)

#定位搜索框並輸入想要查找的選手
driver.find_element(By.XPATH,'//*[@id="navBarContainerFull"]/nav/div[1]/div[1]/div[2]/form/span/input').send_keys(player)
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="navBarContainerFull"]/nav/div[1]/div[1]/div[2]/form/span/input').send_keys(Keys.ENTER)
time.sleep(2)

#搜尋後自動點選第一個查到的結果
driver.find_element(By.XPATH,"/html/body/div[2]/div[5]/div[2]/div[1]/div[2]/table[1]/tbody/tr[2]/td/a/img").click()

# 獲取選手遊戲姓名
player_name_element = driver.find_element(By.CSS_SELECTOR,".playerNickname")
player_name = player_name_element.text

# 獲取選手真實姓名
name_element = driver.find_element(By.CSS_SELECTOR,".playerRealname")
player_realname = name_element.text

# 獲取年齡
age_element = driver.find_element(By.CSS_SELECTOR,".playerAge")
age = age_element.text

# 獲取statistics
player_stats_element = driver.find_element(By.CSS_SELECTOR,".playerpage-container")
player_stats = player_stats_element.text

# 獲取現在所在隊伍
player_current_team_elment = driver.find_element(By.CLASS_NAME,"playerTeam")
player_current_team = player_current_team_elment.text

# 創建DataFrame
data = {
    "選手遊戲ID": [player_name],
    "真實姓名": [player_realname],
    "年齡": [age],
    "statistics": [player_stats],
    "目前效力隊伍":[player_current_team]
}

df = pd.DataFrame(data)

# 將數據保存為csv檔
df.to_csv("playerinfo.csv", index=False)

# 關閉瀏覽器
driver.quit()