
from faker import Faker
# from datetime import datetime, timedelta

# from src.models.SocialMediaAccount import SocialMedia
# from src.models.comment_group import CommentGroup
# from src.models.job import Job
# from src.models.link import Link
# from src.models.transaction import Transaction

from app.models.user import User
from app.models import db
from server.app.main import create_app
app = create_app()
# db.init_app(app)
app.app_context().push()

# Initialize Faker
fake = Faker()

def seed_users(num_users=10):
    """Seed users into the database."""
    for _ in range(num_users):
        user = User(
            contactType=fake.random_element(elements=("email", "phone")),
            contactID=fake.email() if fake.boolean() else fake.phone_number(),
            username=fake.user_name(),
            password=fake.password()
        )
        db.session.add(user)
    db.session.commit()
    print(f"Seeded {num_users} users.")

# def seed_social_medias(num_social_medias=20):
#     """Seed social media accounts into the database."""
#     users = User.query.all()
#     platforms = ["Facebook", "Twitter", "Instagram", "LinkedIn", "YouTube"]

#     for _ in range(num_social_medias):
#         social_media = SocialMedia(
#             platform=fake.random_element(elements=platforms),
#             password=fake.password(),
#             username=fake.user_name(),
#             user_id=fake.random_element(elements=users).id
#         )
#         db.session.add(social_media)
#     db.session.commit()
#     print(f"Seeded {num_social_medias} social media accounts.")

# def seed_links(urls,num_links=4):
#     """Seed links into the database."""
#     social_medias = SocialMedia.query.all()

#     for i in range(num_links):
#         link = Link(
#             url=urls(i),
#             social_media_id=fake.random_element(elements=social_medias).id  # Assign a random social media ID
#         )
#         db.session.add(link)
#     db.session.commit()
#     print(f"Seeded {num_links} links.")

# def seed_transactions(num_transactions=50):
#     """Seed transactions into the database."""
#     users = User.query.all()

#     for _ in range(num_transactions):
#         transaction = Transaction(
#             date=fake.date_time_between(start_date="-30d", end_date="now"),
#             amount=fake.random_number(digits=3, fix_len=True),
#             user_id=fake.random_element(elements=users).id
#         )
#         db.session.add(transaction)
#     db.session.commit()
#     print(f"Seeded {num_transactions} transactions.")

# def seed_jobs(num_jobs=30):
#     """Seed jobs into the database."""
#     links = Link.query.all()
#     comment_groups = CommentGroup.query.all()

#     for _ in range(num_jobs):
#         job = Job(
#             link_id=fake.random_element(elements=links).id,
#             numberOfComments=fake.random_number(digits=2),
#             comment_group_id=fake.random_element(elements=comment_groups).id
#         )
#         db.session.add(job)
#     db.session.commit()
#     print(f"Seeded {num_jobs} jobs.")

# def seed_comment_groups(num_comment_groups=10):
#     """Seed comment groups into the database."""
#     for _ in range(num_comment_groups):
#         comment_group = CommentGroup()
#         db.session.add(comment_group)
#     db.session.commit()
#     print(f"Seeded {num_comment_groups} comment groups.")

# def seed_comments(num_comments=100):
#     """Seed comments into the database."""
#     users = User.query.all()
#     comment_groups = CommentGroup.query.all()

#     for _ in range(num_comments):
#         comment = Comment(
#             content=fake.sentence(),
#             user_id=fake.random_element(elements=users).id,
#             # comment_group_id=fake.random_element(elements=comment_groups).id
#         )
#         db.session.add(comment)
#     db.session.commit()
#     print(f"Seeded {num_comments} comments.")


def seed_all():
    """Seed all data into the database."""
    seed_users()
    # seed_social_medias()
    # seed_transactions()
    # seed_links()
    # seed_comment_groups()
    # seed_jobs()
    # seed_comments()
    print("Database seeding completed.")

if __name__ == "__main__":
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Seed the database
    seed_all()