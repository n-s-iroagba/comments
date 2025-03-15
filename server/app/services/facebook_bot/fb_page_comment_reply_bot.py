import logging
import time

from ..driver import create_driver
from .fb_actions import FbActions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FbPageCommentReplyBot(FbActions):

    config = {}
    completed_jobs = set()  # Store completed jobs to avoid duplication
    MAX_RETRIES = 3  # Number of retries before skipping a job

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

        retries = 0
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
