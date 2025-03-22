import os
import json
import logging
import random
import time
from selenium.webdriver.common.by import By
from ..bot_actions import BotActions

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FbActions(BotActions):
    COOKIES_DIR = "cookies"

    URL = "https://www.facebook.com"

    SELECTORS = {
        "email": (By.CSS_SELECTOR, "input[aria-label='Email address or phone number']"),
        "password": (By.XPATH, "//input[@type='password' and @aria-label='Password']"),
        "submit": (By.XPATH, "//button[@type='submit']"),
        "pop_up": (By.XPATH, "//"),
        "show_comments": (By.CSS_SELECTOR, 'div[aria-label*="Comment"]'),
        "send_reply_button": (By.CSS_SELECTOR, '#focused-state-composer-submit div[aria-label="Comment"]'),
        "comment_box": (By.CSS_SELECTOR, '[aria-label*="Reply to"]'),
        "toggle": (By.XPATH, "//span[text()='Most relevant']"),
        "full_comments_div": (By.CSS_SELECTOR, 'div[role*= "complementary"]'),
        "all_comments": (By.XPATH, "//span[text()='All comments']"),
        "view_more_comments": (By.XPATH, "//span[contains(text(), 'View')]"),
        "reply_button": (By.XPATH, "//div[text()='Reply']"),
        'comments':(By.XPATH, "//div[@class='x16hk5td x12rz0ws']"),
         "post": (By.XPATH, "//a[contains(@href, '/p/') or contains(@href, '/reel/')]"),
    }

    @staticmethod
    def get_cookie_path(email):
        """Returns the cookie file path for a given user email."""
        return os.path.join(FbActions.COOKIES_DIR, f"{email.replace('@', '_').replace('.', '_')}.json")

    @staticmethod
    def load_cookies(driver, cookies_file):
        """Load cookies from a file and add them to the browser."""
        try:
            with open(cookies_file, "r") as file:
                cookies = json.load(file)
            for cookie in cookies:
                # Check if the cookie is expired
                if "expiry" in cookie and cookie["expiry"] < time.time():
                    logger.warning("Cookies are expired. Performing manual login...")
                    return False
                driver.add_cookie(cookie)
            driver.refresh()  # Refresh to apply cookies
            logger.info("Cookies loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return False

    @staticmethod
    def save_cookies(driver, cookies_file):
        """Save current cookies to a file."""
        try:
            with open(cookies_file, "w") as file:
                json.dump(driver.get_cookies(), file)
            logger.info("Cookies saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")

    def manual_login(self, driver, account):
        """Perform manual login using email and password."""
        try:
            logger.info("Performing manual login...")
            self.type_in_element(driver, *FbActions.SELECTORS["email"], account['email'])
            self.type_in_element(driver, *FbActions.SELECTORS["password"], account['password'])
            self.click_element(driver, *FbActions.SELECTORS["submit"])
            logger.info("Login successful.")
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise

    def login(self, driver, account, code=None):
        """Handle the login process, including cookie management and 2FA."""
        if not os.path.exists(FbActions.COOKIES_DIR):
            os.makedirs(FbActions.COOKIES_DIR)

        driver.get(self.URL)

        cookies_file = FbActions.get_cookie_path(account['email'])
       
        # if os.path.exists(cookies_file) and FbActions.load_cookies(driver, cookies_file):
        #     logger.info("Logged in using cookies.")
        # else:
        self.manual_login(driver, account)
        FbActions.save_cookies(driver, cookies_file)
     

    def get_page(self, driver, url):
        logger.info(f"Loading URL: {url}")
        driver.get(url)

    def open_post(self, driver):
        logger.info("Clicking on post...")
        self.click_element(driver, *FbActions.SELECTORS["post"])

    def click_most_relevant_comment_toggle(self, driver):
        logger.info("Clicking 'Most relevant' comment toggle...")
        self.click_element(driver, *FbActions.SELECTORS["toggle"])

    def change_toggle_to_all_comments(self, driver):
        logger.info("Changing toggle to 'All comments'...")
        self.click_element(driver, *FbActions.SELECTORS["all_comments"])

    def show_comments(self, driver, required_number_of_comments):
        logger.info("Showing comments section...")
        self.click_element(driver, *FbActions.SELECTORS["show_comments"])

        logger.info("Adjusting comment settings...")
        self.click_most_relevant_comment_toggle(driver)
        self.change_toggle_to_all_comments(driver)

        time.sleep(10)
        logger.info("Clicking 'View more comments' if needed...")
        comment_div = self.get_element(driver, *FbActions.SELECTORS['full_comments_div'])
        if not comment_div:
            print('no comment div')
        logger.info('Scrolling to the bottom of the comment div')
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_div)
        
        self.click_element(driver, *FbActions.SELECTORS['view_more_comments'])

        number_of_clicks = (required_number_of_comments/ 10) - 1
        if number_of_clicks > 1:
            for i in range(int(number_of_clicks)):
                logger.info(f"Clicking 'View more comments' ({i + 1}/{int(number_of_clicks)})...")
                self.scroll_to_element(driver, *FbActions.SELECTORS['full_comments_div'])
                self.click_element(driver, *FbActions.SELECTORS['view_more_comments'])

    def comment_on_post(self, driver,message):
        logger.info("Showing comments section...")
        self.click_element(driver, *FbActions.SELECTORS["show_comments"])
        comment_box =self.get_element(By.CSS_SELECTOR, '[aria-label="Comment as Nnamdi Solomon Iroagba"]')
        self.type_in_found_element(comment_box,message)
        self.click_element(driver,By.CSS_SELECTOR, '[aria-label="Comment"]')
        time.sleep(2)

        
        
    def get_comments(self, driver):
        logger.info("Retrieving comments...")
        return self.get_element(driver, *FbActions.SELECTORS["comments"], multiple=True)

    def reply_to_comment(self, driver, comment, message):
        logger.info(f"Replying to comment with message: {message}")
        try:
            reply_button = self.get_element_in_element(comment, *FbActions.SELECTORS["reply_button"])
            if reply_button:
                logger.info("Scrolling to reply button...")
                self.scroll_to_element(driver, reply_button)

                logger.info("Clicking reply button...")
                reply_button.click()

                time.sleep(random.uniform(0.5, 1.5))
            else:
                self.click_element(driver, *FbActions.SELECTORS['comment_box'])
            logger.info("Typing reply message...")
            self.type_in_element(driver, *FbActions.SELECTORS['comment_box'], message)
            
            self.click_element(driver, *FbActions.SELECTORS['send_reply_button'])
            logger.info('button clicked')
          

        except Exception as e:
            logger.error(f"Failed to reply to comment: {e}")

    def reply_to_comments(self, driver, job):
        logger.info("Fetching comments...")
        comments = self.get_comments(driver)
        logger.info(f"Found {len(comments)} comments.")

        if not comments:
            logger.warning("No comments found. Skipping reply process.")
            return

        number_of_replies = min(job['number_of_replies'], len(comments))
        logger.info(f"Replying to {number_of_replies} comments...")

        reply_count = -5  # Track successful replies
        index = 0  # Track position in comments list

        while reply_count < number_of_replies and index < len(comments):
            comment = comments[index+1]

            try:
                isPosterReplied = self.get_element_in_element(
                    comment, By.XPATH, f"//span[text()='{job['name']} replied']"
                )
                isPosterComment = self.get_element_in_element(
                    comment, By.CSS_SELECTOR, f"div[aria-label='Comment by {job['name']}']"
                )

                if isPosterComment:
                    logger.info(f"Skipping comment {index+1}: Comment by original poster {job['name']}.")
                
                elif isPosterReplied is None:
                    random_reply = random.choice(job['replies'])
                    logger.info(f"Replying to comment {index+1}/{number_of_replies} with: {random_reply}")
                    self.reply_to_comment(driver, comment, random_reply)
                    reply_count += 1  # Increment only when a reply is made
                
                else:
                    logger.info(f"Skipping comment {index+1}: Already replied by {job['name']}.")

            except Exception as e:
                logger.error(f"Error replying to comment {index+1}: {e}")

            index += 1
            driver.refresh()
            self.show_comments(driver, number_of_replies-reply_count)
            
              # Always increment index to avoid infinite loop


    

    # Note: driver.quit() should be handled outside this method.