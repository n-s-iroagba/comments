# Assume this function exists to fetch an account from your database.
def get_social_media_account(account_id):
    # Implementation to retrieve account from your DB.
    # For demonstration, we return a dummy account dict.
    return {
        'email': f'user{account_id}@example.com',
        'password': 'your_password_here',
        'account_name': f'User {account_id}'
    }

################################################################################
# TestimonialCommentHandler: Posts a testifier comment on each post using a
# rotating list of testifier accounts, then logs in with a confirmation account
# to reply to that comment.
################################################################################
class TestimonialCommentHandler:
    def __init__(self, data, job, driver):
        # data should follow the TestimonialCommentStyle schema
        self.testifier_ids = data.get('testifierSocialMediaIds', [])
        self.confirmation_ids = data.get('ConfirmationSocialMediaIds', [])
        self.testimony_comments = data.get('testimonyComments', [])
        self.confirmation_comments = data.get('confirmationComments', [])
        self.number_of_comments = data.get('numberOfComments', 0)
        self.job = job
        self.driver = driver

    def process_comments(self, posts):
        for post in posts:
            print(f"Processing testimonial comments on post: {post}")
            # For each comment index up to number_of_comments
            for i in range(self.number_of_comments):
                # --- Post the testifier comment ---
                # Rotate through testifier accounts
                testifier_account_id = self.testifier_ids[i % len(self.testifier_ids)]
                testifier_account = get_social_media_account(testifier_account_id)
                # Initialize service and log in with testifier account
                fb_testifier_service = FaceBookJobService(self.driver, self.job, FaceBookPageService, testifier_account)
                fb_testifier_service.login()
                # Choose a comment text from the provided list
                testimony_text = self.testimony_comments[i % len(self.testimony_comments)]
                print(f"Testifier ({testifier_account['account_name']}) commenting: {testimony_text}")
                fb_testifier_service.chosen_fb_job_service.reply_to_comments(testimony_text)
                
                # --- Post the confirmation reply ---
                # Rotate through confirmation accounts similarly
                confirmation_account_id = self.confirmation_ids[i % len(self.confirmation_ids)]
                confirmation_account = get_social_media_account(confirmation_account_id)
                fb_confirmation_service = FaceBookJobService(self.driver, self.job, FaceBookPageService, confirmation_account)
                fb_confirmation_service.login()
                confirmation_text = self.confirmation_comments[i % len(self.confirmation_comments)]
                print(f"Confirmation ({confirmation_account['account_name']}) replying: {confirmation_text}")
                # Here we assume that reply_to_comments will post a reply to the most recent testifier comment.
                fb_confirmation_service.chosen_fb_job_service.reply_to_comments(confirmation_text)

################################################################################
# MultipleCommentHandler: Uses the main account to post comments until it
# reaches the configured number. Then it rotates through the provided follow-up
# accounts to comment on posts that have not yet been commented on.
################################################################################
class MultipleCommentHandler:
    def __init__(self, data, job, driver):
        # data should follow the multipleCommentStyle schema
        self.follow_up_ids = data.get('followUpAccountIds', [])
        self.comments = data.get('comments', [])
        # We'll interpret "numberOfComments" (if provided) as the maximum number of
        # comments per account before switching to the next follow-up account.
        self.number_of_comments = data.get('numberOfComments', 1)
        self.job = job
        self.driver = driver

    def process_comments(self, posts):
        # Start with the main account from the request (body.socialMediaAccountId)
        # Assume job contains the main account's details already.
        main_account = self.job.get('socialMediaAccount')
        if not main_account:
            # Fallback: retrieve main account using socialMediaAccountId
            main_account = get_social_media_account(self.job.get('socialMediaAccountId'))
        comments_posted = 0
        current_account_index = 0

        for post in posts:
            print(f"Processing multiple comments on post: {post}")
            # Decide which account to use:
            # Use the main account until it has posted self.number_of_comments,
            # then rotate through follow-up accounts.
            if comments_posted < self.number_of_comments:
                account = main_account
            else:
                # Rotate using followUpAccountIds; wrap around if needed.
                follow_up_account_id = self.follow_up_ids[current_account_index % len(self.follow_up_ids)]
                account = get_social_media_account(follow_up_account_id)
                current_account_index += 1

            fb_service = FaceBookJobService(self.driver, self.job, FaceBookPageService, account)
            fb_service.login()
            # Select a comment from the list, rotating if needed.
            comment_text = self.comments[comments_posted % len(self.comments)]
            print(f"Account ({account['account_name']}) commenting: {comment_text}")
            fb_service.chosen_fb_job_service.reply_to_comments(comment_text)
            comments_posted += 1
