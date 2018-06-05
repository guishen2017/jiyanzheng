from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from io import BytesIO
from PIL import Image

class CrackGeetCaptcha(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.url = "https://account.geetest.com/login"
        self.EMAIL = "2222222222@qq.com"
        self.PWD = "12345678"

    def open(self):
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password = self.wait.until(EC.presence_of_element_located((By.ID,"password")))
        email.clear()
        password.clear()
        email.send_keys(self.EMAIL)
        password.send_keys(self.PWD)

    def get_button(self):
        button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_radar_tip"]')))
        return button

    def get_captcha(self, name="captcha.png"):
        screen_hot = self.get_screen_hot()
        top,bottom,left,right = self.get_position()
        captcha = screen_hot.crop((left,top,right,bottom))
        captcha.save(name)
        return captcha

    def get_position(self):
        img = self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="geetest_canvas_img geetest_absolute"]')))
        location = img.location
        size = img.size
        # print(location)
        # print(size)
        # top, bottom, left, right = location['y'] + 45, location['y'] + size['height'] + 35 + 20, location['x'] + 112, location['x'] + size['width'] + 112 + 20
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screen_hot(self):
        self.browser.get_screenshot_as_file("login.png")
        screen_hot = self.browser.get_screenshot_as_png()
        screen_hot = Image.open(BytesIO(screen_hot))
        return screen_hot

    def get_slider(self):
        slide_button = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider_button"]')))
        return slide_button

    def get_gap(self, image1, image2):
        left = 70
        for i in range(left,image1.size[0]):
            for j in range(image1.size[1]):
                if self.is_pixel_equal(image1,image2,i,j):
                    left = i
                    print("找到了",left)
                    return left
        print("没有找到缺口")
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x,y]
        pixel2 = image2.load()[x,y]
        threshold = 60
        if abs(pixel1[0]-pixel2[0])>threshold and abs(pixel1[1]-pixel2[1])>threshold and abs(pixel1[2]-pixel2[2])>threshold:
            return True
        else:
            return False

    def get_trace(self, distance):
        trace = []
        t = 0.2
        current = 0
        mid = distance * 4/5
        v = 0
        while current < distance:
            if current <mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a*t
            s = v*t + 1/2*a*t*t
            s = round(s)
            current += s
            trace.append(s)
        return trace

    def move_slide(self, slide, trace):
        ActionChains(self.browser).click_and_hold(slide).perform()
        for move in trace:
            ActionChains(self.browser).move_by_offset(xoffset=move, yoffset=0).perform()
        time.sleep(1)
        ActionChains(self.browser).release().perform()

    def __del__(self):
        self.browser.close()

    def crawl(self):
        self.open()
        button = self.get_button()
        button.click()
        time.sleep(3)
        image1 = self.get_captcha("captcha1.png")
        slide_button = self.get_slider()
        slide_button.click()
        time.sleep(3)
        image2 = self.get_captcha("captcha2.png")
        gas = self.get_gap(image1, image2)
        gas -= 8
        trace = self.get_trace(gas)
        # print(trace)
        # print(sum(trace))
        self.move_slide(slide_button, trace)
        time.sleep(5)

if __name__ == "__main__":
    crawl = CrackGeetCaptcha()
    crawl.crawl()

