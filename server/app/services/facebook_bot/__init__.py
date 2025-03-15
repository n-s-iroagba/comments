from .fb_page_profile_post_comment_bot import FbPageProfilePostCommentBot
from .fb_page_comment_reply_bot import FbPageCommentReplyBot


social_media_services = {
    "page_reply":FbPageCommentReplyBot ,
    'page_profile_comment': FbPageProfilePostCommentBot
    # "page_single_post_comment": InstagramBot(),
    # "page_conversational_comment_reply": TiktokBot(),
    # "page_conversational_post_comments": InstagramBot(),
}

class FacebookBot:
    def execute_job(job):
        job_type = job['job_type']
        service = social_media_services[job_type]()
        service.execute_job(job)
       


