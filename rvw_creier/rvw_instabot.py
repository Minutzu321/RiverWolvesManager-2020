from selenium import webdriver
from time import sleep


class InstaBot:
    def __init__(self, username, pw):
        self.status = 0
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Accept')]")\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        sleep(2)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(7)
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Allow All Cookies')]")\
                .click()
            sleep(4)
        except: pass
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                .click()
            sleep(4)
        except: pass
        self.driver.get_screenshot_as_file(f"scs.png")
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                .click()
            sleep(4)
        except: pass
        self.status = 1
        

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names(False)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names(True)
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_names(self, f):
        sleep(2)
        if f:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
        else:
            scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(5)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def close(self):
        self.driver.close()


my_bot = InstaBot('-', '-')
my_bot.get_unfollowers()
my_bot.close()
