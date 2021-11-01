from io import BytesIO
from PIL import Image
import time
import requests
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from chaojiying import Chaojiying

#输入你的B站、超级鹰用户名和密码
EMAIL='email'
PASSWORD = 'passwd'
CHAOJIYING_USERNAME = 'usrname'
CHAOJIYING_PASSWORD = 'email'
CHAOJIYING_SOFT_ID = 924124
CHAOJIYING_KIND = 9004 #返回1到4个坐标
#封装函数
class CrackTouClick():
    #测试网站：采用B站登录
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
    def open(self):
        #打开网页输入用户名密码
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_touclick_button(self):
        #获取初始验证按钮
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-box > a ')))
        return button

    def pick_code(self):
        time.sleep(3)
        pick_img_label = self.browser.find_element_by_css_selector('img.geetest_item_img')  # 获取点触图片标签
        src = pick_img_label.get_attribute('src')  # 获取点触图片链接
        img_content = requests.get(src).content  # 获取图片二进制内容
        f = BytesIO()
        f.write(img_content)
        img0 = Image.open(f)
        scale = [pick_img_label.size['width'] / img0.size[0],
                 pick_img_label.size['height'] / img0.size[1]]  # 获取图片与浏览器该标签大小的比例
        cjy = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
        result = cjy.post_pic(img_content, '9005')  # 发送图片并获取结果
        if result['err_no'] == 0:
            position = result['pic_str'].split('|')
            position = [[int(j) for j in i.split(',')] for i in position]
            for items in position:  # 模拟点击
                ActionChains(self.browser).move_to_element_with_offset(pick_img_label, items[0] * scale[0], items[1] * scale[1]).click().perform()
                time.sleep(1)
            time.sleep(2)
            # 点击登录
            certern_btn = self.browser.find_element_by_css_selector('div.geetest_commit_tip')
            time.sleep(1)
            certern_btn.click()
            pic_id = result['pic_id']
        return pic_id
    def crack(self):
        self.open()
        # 点击验证按钮
        time.sleep(2)
        button = self.get_touclick_button()
        button.click()
        self.pick_code()
        pic_id=self.pick_code()
        if (self.browser.current_url == 'https://www.bilibili.com/'):
            print('登陆成功')
        else:
            self.chaojiying.report_error(pic_id)
            self.pick_code()


if __name__ == '__main__':
    crack = CrackTouClick()
    crack.crack()