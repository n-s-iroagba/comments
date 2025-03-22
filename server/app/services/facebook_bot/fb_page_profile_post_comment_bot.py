import logging
import re
import time
import json
from .fb_actions import FbActions
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FbPageProfilePostCommentBot(FbActions):
    config = {}
    completed_jobs_file = "completed_jobs.json"  # File to store completed jobs

    def __init__(self):
        super().__init__()
        FbPageProfilePostCommentBot.config['multiple_page'] = self.execute_multiple_page
        self.completed_jobs = self.load_completed_jobs()

    def load_completed_jobs(self):
        """Load completed jobs from file."""
        try:
            with open(self.completed_jobs_file, "r") as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return set()

    def save_completed_jobs(self):
        """Save completed jobs to file."""
        with open(self.completed_jobs_file, "w") as f:
            json.dump(list(self.completed_jobs), f)

    def execute_job(self, job):
        job_id = f"{job['target']}_{job['message']}"  # Unique job identifier
        if job_id in self.completed_jobs:
            logger.info(f"Skipping already completed job: {job_id}")
            return

        logger.info(f"Executing job: {job}")
        if job['config'] not in FbPageProfilePostCommentBot.config:
            raise ValueError(f"Invalid job config: {job['config']}")

        try:
            FbPageProfilePostCommentBot.config[job['config']](self, job)
            self.completed_jobs.add(job_id)
            self.save_completed_jobs()  # Save after successful execution
        except Exception as e:
            logger.error(f"Job failed: {e}")

    def execute_multiple_page(self, driver, jobs):
        for job in jobs:
            self.process_job(driver, job)

    def process_job(self, driver, job):
        job_id = f"{job['target']}_{job['message']}"  # Unique job identifier
        if job_id in self.completed_jobs:
            logger.info(f"Skipping already completed job: {job_id}")
            return

        logger.info(f"Processing job for target: {job['target']}")
        self.get_page(driver, job['target'])
        self.open_post(driver)

        # Fetch comments
        logger.info("Fetching comments...")
        self.show_comments(driver, job['number_of_target_profiles'])
        comments = self.get_comments(driver)
        logger.info(f"Found {len(comments)} comments.")

        if not comments:
            logger.warning("No comments found. Skipping reply process.")
            return

        number_of_tenative_profiles = min(job['number_of_target_profiles'], len(comments) - 1)  # Exclude poster
        logger.info(f"{number_of_tenative_profiles} tentative profiles found.")

        for i in range(number_of_tenative_profiles):
            retry_count = 0
            while retry_count < 3:  # Max 3 retries
                try:
                    comment = comments[i]
                    
                    # Check if comment is from the original poster
                    isPosterComment = self.get_element_in_element(
                        comment,
                        By.CSS_SELECTOR,
                        f'div[aria-label*="Comment by {job["name"]} "]'
                    )
                    if isPosterComment:
                        logger.info(f"Skipping comment {i+1}: Comment by original poster: {job['name']}.")
                        break  # No retry needed, just skip

                    # Extract commenter name
                    commenter = self.get_element_in_element(comment, By.CSS_SELECTOR, 'div[aria-label^="Comment by"]')
                    name = commenter.find_element(By.CSS_SELECTOR, 'span.xt0psk2 a').text
                    logger.info(f"Replying to comment {i+1} by {name}")

                    # Replace ((name)) placeholder in message
                    message = re.sub(r'\(\(name\)\)', name, job['message'])

                    # Click profile link and comment
                    profile_link = self.get_element_in_element(comment, By.CSS_SELECTOR, 'a[href*="/profile.php?id="]')
                    profile_url = profile_link.get_attribute("href")
                    logger.info(f"Opening profile of {name}: {profile_url}")

                    driver.get(profile_url)
                    self.open_post(driver)
                    self.comment_on_post(driver, message)

                    # Successfully processed the comment
                    logger.info(f"Successfully replied to comment {i+1} by {name}")
                    break  # Exit retry loop

                except Exception as e:
                    retry_count += 1
                    logger.error(f"Error replying to comment {i+1} (Attempt {retry_count}/3): {e}")
                    time.sleep(2)  # Wait before retrying

                    if retry_count == 3:
                        logger.error(f"Max retries reached for comment {i+1}. Skipping...")

        # Mark job as completed
        self.completed_jobs.add(job_id)
        self.save_completed_jobs()


# ---- Mock Jobs Data ----
mock_jobs = [
    {
        "config": "multiple_page",
        "target": "https://www.facebook.com/samplepage",
        "name": "John Doe",
        "message": "Hello ((name)), thanks for your comment!",
        "number_of_target_profiles": 3
    },
    {
        "config": "multiple_page",
        "target": "https://www.facebook.com/samplepage2",
        "name": "Jane Doe",
        "message": "Hey ((name)), appreciate your feedback!",
        "number_of_target_profiles": 2
    }
]
