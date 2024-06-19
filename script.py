import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
text_to_send = "I’m writing to you from the ALL DAY JOY Superfoods team. We offer $1000 to the affiliate who generates the most sales plus other gifts!  We're excited about the possibility of collaborating with you! Our functional drinks are part of a new healthy trend, and we believe your support can help us skyrocket! 🚀 We can send you videos designed to generate great sales — all you need to do is post them. Plus, you'll earn a 25% commission from each sale. Thank you for considering this opportunity!"
product_href = ""
def send_email(to_email, subject, body):
    smtpObj = smtplib.SMTP('smtp.mail.ru', 25)
    smtpObj.starttls()
    smtpObj.login('alekseiionov912@mail.ru', 'ggewQ6xqxnLsmGEYgat7')
    msg = MIMEMultipart()
    msg['From'] = 'alekseiionov912@mail.ru'
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    try:
        text = msg.as_string()
        smtpObj.sendmail("alekseiionov912@mail.ru", f"{to_email}", text)
    except:
        print(f"Failed to send email to {to_email}")

# Извлечение email из текста профиля


def extract_email(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text)
    return emails


def get_all_elements(already_sent):
    global cnt
    cnt = 0
    counting = 0
    while True:
        collabs = driver.find_elements(By.CLASS_NAME, f'sc-hzhJZQ.eSyGBZ.cursor-pointer')
        global texts
        while cnt != len(collabs):
            time.sleep(2.5)
            collabs = driver.find_elements(By.CLASS_NAME, f'sc-hzhJZQ.eSyGBZ.cursor-pointer')
            collab = collabs[cnt]
            try:
                counting += 1
                if counting < 110:
                    window_handles = driver.window_handles
                    main_window_handle = driver.current_window_handle
                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", collab)
                    name = collab.find_element(By.XPATH, '//*[@data-e2e="fbc99397-6043-1b37"]')
                    if name.text in already_sent:
                        print("Skipping: ", name.text)
                        cnt += 1
                        continue
                    driver.execute_script("arguments[0].click();", collab)
                    cnt += 1
                    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    window_handles = driver.window_handles
                    driver.switch_to.window(window_handles[-1])
                    # Собрать данные с новой страницы
                    time.sleep(5)
                    discription = driver.find_element(By.CLASS_NAME, 'text-body-s-regular.break-words.whitespace-pre-wrap')
                    emails = extract_email(discription.text)
                    print(discription.text)
                    # Если найден email, отправка сообщения
                    if emails:
                        email = emails[0]  # Берём первый найденный email
                        subject = "Hello Dear Creator!"
                        body = "I’m writing to you from the ALL DAY JOY Superfoods team. We offer $1000 to the affiliate who generates the most sales plus other gifts!  We're excited about the possibility of collaborating with you! Our functional drinks are part of a new healthy trend, and we believe your support can help us skyrocket! 🚀 We can send you videos designed to generate great sales — all you need to do is post them. Plus, you'll earn a 25% commission from each sale. Thank you for considering this opportunity!"
                        send_email(email, subject, body)
                    else:
                        print("No email found in the profile")
                    
                    handles_before = driver.window_handles
                    if (counting < 50):
                        msg = driver.find_element(By.CLASS_NAME, 'alliance-icon.alliance-icon-Message')
                        time.sleep(0.5)
                        msg.click()
                        time.sleep(10)

                        handles_after = driver.window_handles
                        new_handle = [handle for handle in handles_after if handle not in handles_before][0]
                        driver.switch_to.window(new_handle)

                        skip = driver.find_element(By.XPATH, '//*[@id="___reactour"]/div[4]/div/div[2]/div/span[1]/button')
                        skip.click()
                        time.sleep(2)
                        ok = driver.find_element(By.XPATH, '//*[@id="___reactour"]/div[4]/div/div[2]/div[2]/span/span/button')
                        ok.click()
                        time.sleep(1)
                        message = driver.find_element(By.CLASS_NAME, 'index-module_textarea__Xgm4v')
                        message.send_keys(f'{text_to_send}')
                        time.sleep(1)
                        send = driver.find_element(By.XPATH, '//*[@id="im_sdk_ui_sdk_chat_input"]/div[2]/div/button')
                        send.click()
                        target_text = "Products"
                        class_name = "arco-space-item"
                        xpath = f'//div[@class="{class_name}" and text()="{target_text}"]'
                        element = driver.find_element(By.XPATH, xpath)
                        element.click()
                        time.sleep(1)
                        send = driver.find_elements(By.XPATH, '//*[@data-e2e="02ac77bb-7ae6-5fd5"]')[0]
                        ActionChains(driver).move_to_element(send).perform()
                        send = driver.find_element(By.XPATH, '//*[@data-e2e="a7fd9ff4-af7c-a295"]')
                        send.click()
                    # Вернуться назад
                    window_handles = driver.window_handles
                    for handle in window_handles:
                        if handle != main_window_handle:
                            driver.switch_to.window(handle)
                            driver.close()
                    driver.switch_to.window(main_window_handle)
                else:
                    break
            except Exception as e:
                print(f"Encountered an exception: {e}")
                return False


# Функция для сбора информации с новой страницы и возврата назад
def collect_info_from_element(element):
    try:
        print(f"Collecting info from element...")
        # Кликнуть на элемент
        driver.execute_script("arguments[0].setAttribute('target','_self');", element)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(5)  # Подождать загрузку новой страницы
        xpath = '//*[@id="creator-detail-profile-container"]/div[2]/div[2]/div/button[2]'
        # Собрать данные с новой страницы
        msg = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].setAttribute('target','_self');", msg)
        driver.execute_script("arguments[0].click();", msg)
        time.sleep(15)
        # Вернуться назад
        driver.execute_script("window.history.go(-2)")
        time.sleep(3)  # Подождать загрузку предыдущей страницы
    except Exception as e:
        print(f"Encountered an exception: {e}")

already_sent = []
cnt = 0
offset = 0
def get_people(class_name):
    collabs = driver.find_elements(By.CLASS_NAME, f'{class_name}')
    global cnt
    global offset
    counter = len(collabs)
    if (offset != 0):
        counter = counter - offset
    else:
        offset = len(collabs)
    for i in range(counter):
        time.sleep(3)
        collabs = driver.find_elements(By.CLASS_NAME, f'{class_name}')
        collab = collabs[i]
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", collab)
            driver.execute_script("arguments[0].click();", collab)
            cnt += 1
            time.sleep(3)
            
            parent_divs = driver.find_elements(By.CLASS_NAME, 'text-neutral-text1.text-body-m-medium.cursor-pointer')
            for parent in parent_divs:
                # Find the child element with the specified class
                child_elements = parent.find_elements(By.CLASS_NAME, 'arco-typography')
                for element in child_elements:
                    already_sent.append(element.text)
            
            returnaly = driver.find_element(By.CLASS_NAME, 'm4b-breadcrumb-item-str')
            returnaly.click()
        except Exception as e:
            print(f"Encountered an exception: {e}")
            return False
    return True

driver = webdriver.Chrome()
driver.get("https://seller-us-accounts.tiktok.com/account/login")
username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "TikTok_Ads_SSO_Login_Email_Input"))
    )
username.send_keys('sasacuvpilo@gmail.com')
time.sleep(2)
password = driver.find_element(By.ID, "TikTok_Ads_SSO_Login_Pwd_Input")
password.send_keys('ChAD91285858?!')
time.sleep(40)

driver.get("https://affiliate-us.tiktok.com/connection/target-invitation?source_from=seller_affiliate_landing&shop_region=US&tab=1")
time.sleep(5)
#class="arco-modal-close-icon"
try:
    try:
        x_path = "/html/body/div[6]/div[2]/div/div[2]/span"
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
        #driver.execute_script("arguments[0].click();", first_filter)
        time.sleep(1)
        x_path = "/html/body/div[5]/div[2]/div/div[2]/span"
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
    except:
        x_path = "/html/body/div[5]/div[2]/div/div[2]/span"
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
        time.sleep(1)
        x_path = "/html/body/div[6]/div[2]/div/div[2]/span"
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
    #driver.execute_script("arguments[0].click();", first_filter.click)
    time.sleep(5)
    x_path = '//*[@id="___reactour"]/div[4]/div/div[3]/div/span[1]/button'
    first_filter = driver.find_element(By.XPATH, x_path)
    first_filter.click()
except:
    try:
        time.sleep(2)
        x_path = '//*[@id="___reactour"]/div[4]/div/div[3]/div/span[1]/button'
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
        #driver.execute_script("arguments[0].click();", first_filter)
        time.sleep(1)
        x_path = "/html/body/div[5]/div[2]/div/div[2]/span"
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
    except:
        time.sleep(2)
        x_path = '//*[@id="___reactour"]/div[4]/div/div[3]/div/span[1]/button'
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
        time.sleep(1)
        x_path = "/html/body/div[6]/div[2]/div/div[2]/span"
        first_filter = driver.find_element(By.XPATH, x_path)
        first_filter.click()
#driver.execute_script("arguments[0].click();", first_filter)
time.sleep(3)

while not get_people('cursor-pointer.arco-table-tr'):
    time.sleep(1)
time.sleep(3)
div_col = driver.find_element(By.XPATH, f'//div[@role="tab" and @aria-controls="arco-tabs-{cnt}-panel-1"]')
second_collab = div_col.find_element(By.CLASS_NAME, 'arco-tabs-header-title-text')
actions = ActionChains(driver)
actions.move_to_element(second_collab).perform()
second_collab.click()
time.sleep(3)

while not get_people('cursor-pointer.arco-table-tr'):
    time.sleep(1)
# Print the extracted texts
for text in already_sent:
    print(text)

# Retry logic for handling StaleElementReferenceException
driver.get("https://affiliate-us.tiktok.com/connection/creator?shop_region=US")
time.sleep(5)
x_path = '/html/body/div[5]/div[2]/div/div[2]/span'
first_filter = driver.find_element(By.XPATH, x_path)
first_filter.click()
x_path = '//*[@id="content-container"]/main/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[1]/div[2]/div/label[3]/button'
first_filter = driver.find_element(By.XPATH, x_path)
first_filter.click()
time.sleep(0.5)
x_path = '//*[@id="gmv"]/div/span/button'
gmv = driver.find_element(By.XPATH, x_path)
gmv.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-5"]/div/div/li[3]'
first = driver.find_element(By.XPATH, x_path)
first.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-5"]/div/div/li[4]'
second = driver.find_element(By.XPATH, x_path)
second.click()
time.sleep(0.5)

x_path = '//*[@id="unitsSold"]/div/span/button'
units_sold = driver.find_element(By.XPATH, x_path)
units_sold.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-6"]/div/div/li[3]'
first = driver.find_element(By.XPATH, x_path)
first.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-6"]/div/div/li[4]'
second = driver.find_element(By.XPATH, x_path)
second.click()
time.sleep(0.5)

x_path = '//*[@id="content-container"]/main/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[1]/div[2]/div/label[2]/button'
followers = driver.find_element(By.XPATH, x_path)
followers.click()
time.sleep(0.5)
x_path = '//*[@id="followerAge"]/div/span/button'
age = driver.find_element(By.XPATH, x_path)
age.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-3"]/div/div/li[3]'
first = driver.find_element(By.XPATH, x_path)
first.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-3"]/div/div/li[4]'
second = driver.find_element(By.XPATH, x_path)
second.click()
time.sleep(0.5)
x_path = '//*[@id="arco-select-popup-3"]/div/div/li[5]'
third = driver.find_element(By.XPATH, x_path)
third.click()
time.sleep(0.5)
x_path = '//*[@id="followerAge"]/div/span/button'
age = driver.find_element(By.XPATH, x_path)
age.click()
time.sleep(2)
print("start")
all_elements = get_all_elements(already_sent)
print("done")
driver.quit()