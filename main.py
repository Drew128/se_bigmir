from selenium import webdriver
import logging


class Spider:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
        self.driver.implicitly_wait(10)

    def __del__(self):
        self.driver.close()


class PassportBigmir(Spider):
    def fill_login(self, login):
        login_form = self.driver.find_element_by_xpath('//input[@id="login"]')
        login_form.click()
        login_form.send_keys(login)

    def fill_password(self, password):
        password_form = self.driver.find_element_by_xpath('//input[@id="password"]')
        password_form.click()
        password_form.send_keys(password)

        password_conf_form = self.driver.find_element_by_xpath('//input[@id="password_conf"]')
        password_conf_form.click()
        password_conf_form.send_keys(password)

    def fill_secret_question(self, seq_qn_option=1, seq_qn_a='pizza'):
        secret_qn_dropdown = self.driver.find_element_by_xpath('//select[@id="secret_qn"]')
        secret_qn_dropdown.click()

        secret_qn_options = secret_qn_dropdown.find_element_by_xpath(f'./option[@value="{seq_qn_option}"]')
        secret_qn_options.click()

        secret_a_form = self.driver.find_element_by_xpath('//input[@id="secret_a"]')
        secret_a_form.click()
        secret_a_form.send_keys(seq_qn_a)

    def push_agree_button(self):
        rules_agree_checkbox = self.driver.find_element_by_xpath('//input[@id="rules_agree_id"]')
        rules_agree_checkbox.click()

    def recaptcha(self):
        frames = self.driver.find_elements_by_tag_name("iframe")
        recaptcha_active_frames = [each for each in frames if each.is_displayed() and
                                   each.get_attribute('src').startswith("https://www.google.com/recaptcha/api2/anchor")]
        return recaptcha_active_frames

    def check_recaptcha(self):
        captcha = self.recaptcha()
        solved_list = dict()
        if captcha:
            for frame in captcha:
                self.driver.switch_to.frame(frame)
                elem = self.driver.find_element_by_xpath('//span[@role="checkbox"]')
                solved_list.update({frame: elem.get_attribute('aria-checked')})
        self.driver.switch_to.default_content()
        return solved_list

    def push_submit_button(self):
        submit_button = self.driver.find_element_by_xpath('//input[@id="submit"]')
        submit_button.click()

    def check_alerts(self):
        alert_messages = []
        alerts = self.driver.find_elements_by_xpath('//div[@class="text_left"]')
        if alerts:
            for alert in alerts:
                [alert_messages.append(each.text) for each in alert.find_elements_by_xpath('./b')]
                [alert_messages.append(elem.get_attribute('innerHTML'))
                 for elem in alert.find_elements_by_xpath('./div')]
        return alert_messages

    def reg_page_bigmir(self, login, password):
        self.driver.get("https://passport.bigmir.net/registration/")
        logging.debug('get("https://passport.bigmir.net/registration/")')
        self.fill_login(login)
        logging.debug('fill_login')
        self.fill_password(password)
        logging.debug('fill_password')
        self.fill_secret_question()
        logging.debug('fill_secret_question')
        self.push_agree_button()
        logging.debug('push_agree_button')
        logging.debug(f'recaptcha solved: {self.check_recaptcha().values()}')
        self.push_submit_button()
        logging.debug('push_submit_button')
        alerts = ''.join(self.check_alerts())
        logging.debug(f"Alerts: {alerts}")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, filename='app.log', filemode='w')
    firefox = PassportBigmir()
    firefox.reg_page_bigmir(login="login", password="password")