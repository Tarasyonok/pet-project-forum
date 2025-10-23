# management/commands/populate_fake_data.py
import random

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from faker import Faker

from votes.models import Vote
from forum.models import Answer, Question
from reviews.models import CourseReview

User = get_user_model()


class Command(BaseCommand):
    help = "Populates database with fake data for all models"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=50,
            help="Number of users to create",
        )
        parser.add_argument(
            "--questions",
            type=int,
            default=100,
            help="Number of questions to create",
        )

    def handle(self, *args, **options):
        fake = Faker()
        user_count = options["users"]
        questions_count = options["questions"]

        self.stdout.write("Starting data population...")

        # Create users with profiles
        users = self.create_users(fake, user_count)

        # Create questions
        questions = self.create_questions(fake, questions_count, users)

        # Create answers
        answers = self.create_answers(fake, questions, users)

        # Create reviews
        reviews = self.create_reviews(fake, users)

        # Create votes
        self.create_votes(users, questions, answers, reviews)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created:\n"
                f"- {len(users)} users\n"
                f"- {len(questions)} questions\n"
                f"- {len(answers)} answers\n"
                f"- {len(reviews)} reviews\n"
                f"- {Vote.objects.count()} votes",
            ),
        )

    def create_users(self, fake, count):
        users = []
        for i in range(count):
            try:
                # Determine role (mostly students, few admins)
                role = User.Role.ADMIN if i < 3 else User.Role.STUDENT

                user = User.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.unique.email(),
                    password="testpass123",
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    role=role,
                )
                users.append(user)

                # Update profile
                profile = user.profile
                profile.bio = fake.paragraph() if random.random() > 0.3 else ""
                profile.birthday = (
                    fake.date_of_birth(
                        minimum_age=18,
                        maximum_age=70,
                    )
                    if random.random() > 0.4
                    else None
                )
                profile.reputation_points = random.randint(0, 500)
                profile.save()

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error creating user: {e}"))

        return users

    def create_questions(self, fake, count, users):
        questions = []

        for _ in range(count):
            question = Question.objects.create(
                title=fake.sentence()[:199],
                content="\n".join(fake.paragraphs(nb=random.randint(2, 5))),
                author=random.choice(users),
                is_solved=random.random() > 0.7,  # 30% chance of being solved
            )
            questions.append(question)
        return questions

    def create_answers(self, fake, questions, users):
        answers = []
        for question in questions:
            # Create 1-8 answers per question
            num_answers = random.randint(1, 8)
            question_answers = []

            for _ in range(num_answers):
                answer = Answer.objects.create(
                    question=question,
                    content="\n".join(fake.paragraphs(nb=random.randint(1, 4))),
                    author=random.choice(users),
                    is_accepted=False,
                )
                question_answers.append(answer)
                answers.append(answer)

            # Mark one answer as accepted if question is solved
            if question.is_solved and question_answers:
                accepted_answer = random.choice(question_answers)
                accepted_answer.mark_accepted()  # This handles reputation points

        return answers

    def create_reviews(self, fake, users):
        reviews = []
        course_names = [
            "Python Bootcamp",
            "Django Mastery",
            "React Fundamentals",
            "JavaScript Pro",
            "Data Science",
            "Web Development",
            "Mobile App Development",
            "Cloud Engineering",
            "DevOps Course",
        ]

        # Ensure each user reviews 2-5 courses
        for user in users:
            num_reviews = random.randint(2, 5)
            user_courses = random.sample(course_names, num_reviews)

            for course in user_courses:
                review = CourseReview.objects.create(
                    author=user,
                    title=fake.sentence(),
                    content="\n".join(fake.paragraphs(nb=random.randint(2, 4))),
                    rating=random.randint(1, 5),
                    course_name=course,
                )
                reviews.append(review)

        return reviews

    def create_votes(self, users, questions, answers, reviews):
        voteable_objects = questions + answers + reviews

        for user in users:
            # Each user votes on 20-40 random objects
            objects_to_vote = random.sample(
                voteable_objects,
                min(random.randint(20, 40), len(voteable_objects)),
            )

            for obj in objects_to_vote:
                # Skip if user is the author
                if hasattr(obj, "author") and obj.author == user:
                    continue

                vote_type = random.choices(
                    ["up", "down"],
                    weights=[0.7, 0.3],  # 70% upvotes, 30% downvotes
                )[0]

                Vote.objects.get_or_create(
                    user=user,
                    content_type=ContentType.objects.get_for_model(obj),
                    object_id=obj.id,
                    defaults={"vote_type": vote_type},
                )

                # Update reputation points based on votes
                if vote_type == "up" and hasattr(obj, "author"):
                    obj.author.profile.reputation_points += 1
                    obj.author.profile.save()
