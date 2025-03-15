from flask import Blueprint, request, jsonify

from ..services.facebook_bot import FacebookBot


jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")

from flask import Blueprint, request, jsonify

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")

# Example of mapping job types to social media services
social_media_services = {
    "facebook": FacebookBot,
    # "instagram": InstagramBot(),
    # "tiktok": TiktokBot(),
}

@jobs_bp.route("/execute-jobs", methods=["GET"])
def execute_jobs():
    data = job

    
    if not data or "platform" not in data:
        return jsonify({"error": "Missing required 'platform' field"}), 400
    
    platform = data["platform"]
    
    if platform not in social_media_services:
        return jsonify({"error": f"Unsupported platform: {platform}"}), 400
    
    try:
        social_media_services[platform].execute_job(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jobs_bp.route("/<int:user_id>", methods=["GET"])
def get_running_jobs(user_id):
    
    return 'helloworld'


job = {
    "platform": "facebook",
    'job_type':'page_reply',
    "config": "single_accounts_to_multiple_posts", 
    "account": {  
        "email": "nnamdisolomon1@gmail.com",
        "password": "97Chocho@"
    },
    "target": [
        {
            "url": "https://www.facebook.com/marvinachi",  
            "required_number_of_replies": 1, 
            "replies": [ 
                "Chai!",
                # "We appreciate your feedback!",
                # "Glad you liked our post!",
                # "Stay tuned for more updates!",
                # "Have a great day!"
            ]
        },
        {
            "url": "https://web.facebook.com/enews",
            "required_number_of_replies": 3,
            "replies": [
                "Interesting perspective!",
                "Thanks for sharing your thoughts!",
                "We value your opinion!"
            ]
        }
    ]
}
