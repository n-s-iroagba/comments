import logging
import time

from ..driver import create_driver
from .fb_actions import FbActions
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FbPageCommentReplyBot(FbActions):

    config = {}
    completed_jobs = set()  # Store completed jobs to avoid duplication
    MAX_RETRIES = 3  # Number of retries before skipping a job
    selectors = {
        "post": (By.XPATH, "//a[contains(@href, '/p/') or contains(@href, '/reel/')]"),
        "show_comments": (By.CSS_SELECTOR, 'div[aria-label*="Comment"]'),
        "comments": (By.CSS_SELECTOR, 'div[aria-label*="Comment by"]'),
        "comment_box": (By.CSS_SELECTOR, '[aria-label*="Reply to"]'),
        "toggle": (By.XPATH, "//span[text()='Most relevant']"),
        "full_comments_div": (By.CSS_SELECTOR, '[role*= "complementary"]'),
        "all_comments": (By.XPATH, "//span[text()='All comments']"),
        "view_more_comments": (By.XPATH, "//span[text()='View more comments']"),
        "reply_button": (By.XPATH, "//div[text()='Reply']")
    }
    def __init__(self):
        super().__init__()
        FbPageCommentReplyBot.config['single_accounts_to_multiple_posts'] = self.execute_single_accounts_to_multiple_posts

    def execute_job(self, job):
        job_id = job.get("id")  # Assuming each job has a unique ID
        if job_id in self.completed_jobs:
            logger.info(f"Skipping already completed job: {job_id}")
            return

        logger.info(f"Executing job: {job_id}")

        if job['config'] not in FbPageCommentReplyBot.config:
            raise ValueError(f"Invalid job config: {job['config']}")

        retries = 2
        while retries < self.MAX_RETRIES:
            try:
                FbPageCommentReplyBot.config[job['config']](job)
                self.completed_jobs.add(job_id)  # Mark job as completed
                logger.info(f"Job {job_id} completed successfully.")
                return  # Exit loop if job succeeds
            except Exception as e:

                retries += 1
                logger.error(f"Error executing job {job_id} (Attempt {retries}/{self.MAX_RETRIES}): {e}")
                time.sleep(2 ** retries)  # Exponential backoff
        logger.error(f"Job {job_id} failed after {self.MAX_RETRIES} attempts. Skipping.")
    
    def execute_url_job(self, target, driver):
        logger.info(f"Navigating to page: {target['url']}")
        self.get_page(driver, target['url'])

        logger.info("Opening post...")
        self.open_post(driver)

        logger.info("About to show the comments")
        
        self.show_comments(driver, target['number_of_replies'])

        logger.info("Replying to comments...")
        self.reply_to_comments(driver, target)

    def execute_single_accounts_to_multiple_posts(self, job):
        logger.info("Creating WebDriver instance...")
        driver = create_driver()
        try:
            logger.info("Logging in...")
            self.login(driver, job['account'])

            for target in job['target']:
                logger.info(f"Processing target: {target['url']}")
                self.execute_url_job(target, driver)
        finally:
            logger.info("Quitting WebDriver...")
            driver.quit()
