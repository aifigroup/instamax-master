import time
from flask import session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-extentions')
        self.options.add_argument('--enable-popup-blocking')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=self.options)


    def closeBrowser(self):
        self.driver.close()


    def login(self):
        try:
            driver = self.driver
            driver.get("https://www.instagram.com/")
            time.sleep(2)
            login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
            login_button.click()
            time.sleep(2)
            user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
            user_name_elem.clear()
            user_name_elem.send_keys(self.username)
            passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
            passworword_elem.clear()
            passworword_elem.send_keys(self.password)
            passworword_elem.send_keys(Keys.RETURN)
            time.sleep(2)
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
            except:
                pass
            driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[1]/a/span').click()
            return True
        except:
            return False

    def login2(self):
        try:
            driver = self.driver
            driver.get("https://www.instagram.com/")
            time.sleep(2)
            login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
            login_button.click()
            time.sleep(1)
            user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
            user_name_elem.clear()
            user_name_elem.send_keys(self.username)
            passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
            passworword_elem.clear()
            passworword_elem.send_keys(self.password)
            passworword_elem.send_keys(Keys.RETURN)
            try:
                try:
                    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
                except:
                    driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
            except:
                pass

            return True
        except:
            return False


    def pending_request_count(self):
        driver = self.driver
        # import ipdb; ipdb.set_trace()
        try:
            time.sleep(2)
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
            except:
                driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
        except:
            pass
        driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[2]/a/span").click()
        time.sleep(2)

        try:
            try:
                pending_count = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "JRHhD")))
                pending_count_requests = int(pending_count.text)

                return pending_count_requests
            except:
                pending_count = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "JRHhD")))
                pending_count = pending_count.text[:-1]
                pending_count_requests = int(pending_count)

                return 1000
        except:
            return "No request to accept"


    # def accept_pending_requests(self, request_accept_count):
    #
    #     driver = self.driver
    #     var1 = int(request_accept_count/15)
    #     var2 = request_accept_count%15
    #     counter = 0
    #
    #     # import ipdb; ipdb.set_trace()
    #     try:
    #         if var1 > 0:
    #             for j in range(0, var1):
    #                 try:
    #                     try:
    #                         driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
    #                     except:
    #                         driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    #                 except:
    #                     pass
    #
    #                 try:
    #                     driver.find_element_by_xpath(
    #                         "/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[2]/a/span").click()
    #                 except:
    #                     pass
    #
    #                 WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "M_9ka"))).click()
    #
    #                 for i in range(1, 16):
    #
    #                     xpath_for_confirm = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div[{count}]/div[3]/div/div[1]/button'.format(count=i)
    #                     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_for_confirm))).click()
    #                     time.sleep(0.5)
    #                     counter+= 1
    #                     session['accepted_count'] = request_accept_count
    #                     # session['request_accepted_counter'] = i
    #                     session['request_accepted_counter'] = counter
    #                     session['request_accepted_counter_demo'] = counter
    #                 time.sleep(4)
    #                 driver.find_element_by_xpath(
    #                     '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div').click()
    #
    #             print(request_accept_count)
    #             return "{} Requests Accepted".format(request_accept_count)
    #
    #         if not var2 == 0:
    #             try:
    #                 try:
    #                     driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
    #                 except:
    #                     driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    #             except:
    #                 pass
    #             WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "M_9ka"))).click()
    #             try:
    #                 for i in range(1, var2+1):
    #                     xpath_for_confirm = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div[{count}]/div[3]/div/div[1]/button'.format(
    #                         count=i)
    #                     WebDriverWait(driver, 5).until(
    #                         EC.presence_of_element_located((By.XPATH, xpath_for_confirm))).click()
    #                     session['accepted_count'] = request_accept_count
    #                     # session['request_accepted_counter'] = i
    #                     session['request_accepted_counter'] = counter
    #                     session['request_accepted_counter_demo'] = counter
    #                 return "{} Requests Accepted".format(request_accept_count)
    #
    #             except:
    #                 return "No request to accept"
    #     except:
    #         return "All requests Accepted"

    def accept_pending_requests(self, request_accept_count):

        # driver = self.driver
        # var1 = int(request_accept_count/15)
        # var2 = request_accept_count%15
        # counter = 0

        # import ipdb; ipdb.set_trace()

        for i in range(300):
            # print(i)
            # if (i % 5 == 0):
            session["request_accepted_counter_demo"] = i
            session.modified = True
            time.sleep(0.05)
            print(session["request_accepted_counter_demo"])

        # try:
        #     if var1 > 0:
        #         for j in range(0, var1):
        #             try:
        #                 try:
        #                     driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
        #                 except:
        #                     driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
        #             except:
        #                 pass
        #
        #             try:
        #                 driver.find_element_by_xpath(
        #                     "/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[2]/a/span").click()
        #             except:
        #                 pass
        #
        #             WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "M_9ka"))).click()
        #
        #             for i in range(1, 16):
        #
        #                 xpath_for_confirm = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div[{count}]/div[3]/div/div[1]/button'.format(count=i)
        #                 WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_for_confirm))).click()
        #                 time.sleep(0.5)
        #                 counter+= 1
        #                 session['accepted_count'] = request_accept_count
        #                 # session['request_accepted_counter'] = i
        #                 session['request_accepted_counter'] = counter
        #                 session['request_accepted_counter_demo'] = counter
        #             time.sleep(4)
        #             driver.find_element_by_xpath(
        #                 '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div').click()
        #
        #         print(request_accept_count)
        #         return "{} Requests Accepted".format(request_accept_count)
        #
        #     if not var2 == 0:
        #         try:
        #             try:
        #                 driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/button[2]').click()
        #             except:
        #                 driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
        #         except:
        #             pass
        #         WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "M_9ka"))).click()
        #         try:
        #             for i in range(1, var2+1):
        #                 xpath_for_confirm = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/div/div[1]/div/div[{count}]/div[3]/div/div[1]/button'.format(
        #                     count=i)
        #                 WebDriverWait(driver, 5).until(
        #                     EC.presence_of_element_located((By.XPATH, xpath_for_confirm))).click()
        #                 session['accepted_count'] = request_accept_count
        #                 # session['request_accepted_counter'] = i
        #                 session['request_accepted_counter'] = counter
        #                 session['request_accepted_counter_demo'] = counter
        #             return "{} Requests Accepted".format(request_accept_count)
        #
        #         except:
        #             return "No request to accept"
        # except:
        #     return "All requests Accepted"