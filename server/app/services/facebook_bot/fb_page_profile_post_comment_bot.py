import logging
import re
from .fb_actions import FbActions
from selenium.webdriver.common.by import By

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FbPageProfilePostCommentBot(FbActions):
    config = {}

    def __init__(self):
        super().__init__()
        FbPageProfilePostCommentBot.config['multiple_page'] = self.execute_multiple_page

    def execute_job(self, job):
        logger.info(f"Executing job: {job}")

        if job['config'] not in FbPageProfilePostCommentBot.config:
            raise ValueError(f"Invalid job config: {job['config']}")

        FbPageProfilePostCommentBot.config[job['config']](self, job)

    def execute_multiple_page(self, driver, jobs):
        for job in jobs:
            logger.info(f"Processing job for target: {job['target']}")

            # Open the page and post
            self.get_page(driver, job['target'])
            self.open_post(driver)

            # Fetch comments
            logger.info("Fetching comments...")
            self.show_comments(driver, job['number_of_target_profiles'])
            comments = self.get_comments(driver)
            logger.info(f"Found {len(comments)} comments.")

            if not comments:
                logger.warning("No comments found. Skipping reply process.")
                continue

            number_of_tenative_profiles = min(job['number_of_target_profiles'], len(comments) - 1)  # Exclude the poster
            logger.info(f"{number_of_tenative_profiles} tentative profiles found.")

            for i in range(number_of_tenative_profiles):
                comment = comments[i]
                try:
                    # Check if comment is from the original poster
                    isPosterComment = self.get_element_in_element(
                        comment,
                        By.CSS_SELECTOR,
                        f'div[aria-label*="Comment by {job["target_name"]} "]'
                    )
                    if isPosterComment:
                        logger.info(f"Skipping comment {i+1}: Comment by original poster: {job['target_name']}.")
                        continue

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

                except Exception as e:
                    logger.error(f"Error replying to comment {i+1}: {e}")

# ---- Mock Jobs Data ----
mock_jobs = [
    {
        "config": "multiple_page",
        "target": "https://www.facebook.com/samplepage",
        "target_name": "John Doe",
        "message": "Hello ((name)), thanks for your comment!",
        "number_of_target_profiles": 3
    },
    {
        "config": "multiple_page",
        "target": "https://www.facebook.com/samplepage2",
        "target_name": "Jane Doe",
        "message": "Hey ((name)), appreciate your feedback!",
        "number_of_target_profiles": 2
    }
]
