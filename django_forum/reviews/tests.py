# reviews/tests.py
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from reviews.forms import CourseReviewForm
from reviews.models import CourseReview

# Get logger for this module
logger = logging.getLogger(__name__)

User = get_user_model()


class CourseReviewModelTest(TestCase):
    """Test CourseReview model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.review = CourseReview.objects.create(
            author=self.user,
            title="Great Course!",
            content="This course was amazing and very informative.",
            rating=5,
            course_name="Django Masterclass",
        )

    def test_review_creation(self):
        """Test review creation with all fields"""
        self.assertEqual(self.review.author, self.user)
        self.assertEqual(self.review.title, "Great Course!")
        self.assertEqual(self.review.content, "This course was amazing and very informative.")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.course_name, "Django Masterclass")
        self.assertIsNotNone(self.review.created_at)
        self.assertIsNotNone(self.review.updated_at)

    def test_review_string_representation(self):
        """Test review string representation"""
        expected_str = f"Django Masterclass - ⭐⭐⭐⭐⭐ by {self.user.username}"
        self.assertEqual(str(self.review), expected_str)

    def test_review_absolute_url(self):
        """Test get_absolute_url method"""
        expected_url = reverse("reviews:review_detail", kwargs={"pk": self.review.pk})
        self.assertEqual(self.review.get_absolute_url(), expected_url)

    def test_get_rating_stars_method(self):
        """Test get_rating_stars method"""
        self.assertEqual(self.review.get_rating_stars(), "⭐⭐⭐⭐⭐")

        # Test with different ratings
        review2 = CourseReview.objects.create(
            author=self.user,
            title="Average Course",
            content="This course was okay.",
            rating=3,
            course_name="Python Basics",
        )
        self.assertEqual(review2.get_rating_stars(), "⭐⭐⭐")

    def test_review_ordering(self):
        """Test that reviews are ordered by creation date (newest first)"""
        # Create another review
        review2 = CourseReview.objects.create(
            author=self.user,
            title="Newer Review",
            content="Newer content",
            rating=4,
            course_name="React Fundamentals",
        )

        reviews = CourseReview.objects.all()
        self.assertEqual(reviews[0], review2)  # Newest first
        self.assertEqual(reviews[1], self.review)  # Older second

    def test_rating_choices_validation(self):
        """Test that rating is within valid range"""
        # Test valid ratings
        for rating in [1, 2, 3, 4, 5]:
            review = CourseReview(
                author=self.user,
                title=f"Test Review {rating}",
                content="Test content",
                rating=rating,
                course_name=f"Course {rating}",
            )
            try:
                review.full_clean()  # This should not raise ValidationError
            except ValidationError:
                self.fail(f"Rating {rating} should be valid")

    def test_rating_display(self):
        """Test that rating choices display correctly"""
        self.assertEqual(self.review.get_rating_display(), "⭐⭐⭐⭐⭐")

        review2 = CourseReview.objects.create(
            author=self.user,
            title="Two Star Review",
            content="Not great.",
            rating=2,
            course_name="Basic HTML",
        )
        self.assertEqual(review2.get_rating_display(), "⭐⭐")


class CourseReviewFormTest(TestCase):
    """Test CourseReviewForm validation and functionality"""

    def test_valid_review_form(self):
        """Test form with valid data"""
        form_data = {
            "course_name": "Django Masterclass",
            "title": "Excellent Course!",
            "content": "This course was very comprehensive and well-structured.",
            "rating": 5,
        }
        form = CourseReviewForm(data=form_data)

        if not form.is_valid():
            logger.debug("Form validation failed with errors: %s", form.errors)

        self.assertTrue(form.is_valid())

    def test_review_form_with_empty_course_name(self):
        """Test form with empty course name"""
        form_data = {"course_name": "", "title": "Test Title", "content": "Test content", "rating": 4}
        form = CourseReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("course_name", form.errors)

    def test_review_form_with_empty_title(self):
        """Test form with empty title"""
        form_data = {"course_name": "Test Course", "title": "", "content": "Test content", "rating": 4}
        form = CourseReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_review_form_with_empty_content(self):
        """Test form with empty content"""
        form_data = {"course_name": "Test Course", "title": "Test Title", "content": "", "rating": 4}
        form = CourseReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_review_form_with_invalid_rating(self):
        """Test form with invalid rating"""
        form_data = {
            "course_name": "Test Course",
            "title": "Test Title",
            "content": "Test content",
            "rating": 6,  # Invalid rating
        }
        form = CourseReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_review_form_widget_attributes(self):
        """Test that form widgets have correct attributes"""
        form = CourseReviewForm()

        course_name_widget = form.fields["course_name"].widget
        title_widget = form.fields["title"].widget
        content_widget = form.fields["content"].widget
        rating_widget = form.fields["rating"].widget

        self.assertEqual(course_name_widget.attrs.get("class"), "form-control")
        self.assertEqual(course_name_widget.attrs.get("placeholder"), "e.g., Django Masterclass, Python Basics...")

        self.assertEqual(title_widget.attrs.get("class"), "form-control")
        self.assertEqual(title_widget.attrs.get("placeholder"), "Brief summary of your review...")

        self.assertEqual(content_widget.attrs.get("class"), "form-control")
        self.assertEqual(content_widget.attrs.get("placeholder"), "Share your experience with this course...")
        self.assertEqual(content_widget.attrs.get("rows"), 5)

        self.assertEqual(rating_widget.attrs.get("class"), "form-check-inline")


class ReviewListViewTest(TestCase):
    """Test ReviewListView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.review1 = CourseReview.objects.create(
            author=self.user,
            title="First Review",
            content="First review content",
            rating=5,
            course_name="Django Masterclass",
        )
        self.review2 = CourseReview.objects.create(
            author=self.user,
            title="Second Review",
            content="Second review content",
            rating=4,
            course_name="Python Basics",
        )
        self.list_url = reverse("reviews:review_list")

    def test_review_list_view_get(self):
        """Test GET request to review list view"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_list.html")
        self.assertEqual(len(response.context["reviews"]), 2)
        self.assertFalse(response.context["is_search"])

    def test_review_list_search(self):
        """Test review list with search query"""
        response = self.client.get(self.list_url, {"q": "Django"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["reviews"]), 1)
        self.assertEqual(response.context["reviews"][0], self.review1)
        self.assertEqual(response.context["query"], "Django")
        self.assertTrue(response.context["is_search"])

    def test_review_list_search_multiple_fields(self):
        """Test review list search across multiple fields"""
        # Search by course name
        response = self.client.get(self.list_url, {"q": "Python"})
        self.assertEqual(len(response.context["reviews"]), 1)
        self.assertEqual(response.context["reviews"][0], self.review2)

        # Search by title
        response = self.client.get(self.list_url, {"q": "Second"})
        self.assertEqual(len(response.context["reviews"]), 1)
        self.assertEqual(response.context["reviews"][0], self.review2)

    def test_review_list_search_no_results(self):
        """Test review list search with no matching results"""
        response = self.client.get(self.list_url, {"q": "nonexistent"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["reviews"]), 0)
        self.assertEqual(response.context["results_count"], 0)

    def test_review_list_vote_counts(self):
        """Test that vote counts are calculated for each review"""
        response = self.client.get(self.list_url)

        for review in response.context["reviews"]:
            self.assertEqual(review.upvotes, 0)
            self.assertEqual(review.downvotes, 0)
            self.assertEqual(review.vote_count, 0)


class ReviewDetailViewTest(TestCase):
    """Test ReviewDetailView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.review = CourseReview.objects.create(
            author=self.user,
            title="Test Review",
            content="Test review content",
            rating=5,
            course_name="Test Course",
        )
        self.detail_url = reverse("reviews:review_detail", kwargs={"pk": self.review.pk})

    def test_review_detail_view_get(self):
        """Test GET request to review detail view"""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_detail.html")
        self.assertEqual(response.context["review"], self.review)

    def test_review_detail_vote_counts(self):
        """Test that vote counts are calculated"""
        response = self.client.get(self.detail_url)
        review = response.context["review"]

        self.assertEqual(review.upvotes, 0)
        self.assertEqual(review.downvotes, 0)
        self.assertEqual(review.vote_count, 0)

    def test_review_detail_user_vote_anonymous(self):
        """Test user_vote is None for anonymous users"""
        response = self.client.get(self.detail_url)
        review = response.context["review"]

        self.assertIsNone(review.user_vote)

    def test_review_detail_user_vote_authenticated(self):
        """Test user_vote for authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.detail_url)
        review = response.context["review"]

        # Initially no vote
        self.assertIsNone(review.user_vote)

    def test_review_detail_nonexistent(self):
        """Test accessing non-existent review"""
        nonexistent_url = reverse("reviews:review_detail", kwargs={"pk": 999})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class ReviewCreateViewTest(TestCase):
    """Test ReviewCreateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.create_url = reverse("reviews:review_create")

    # def test_login_required(self):
    #     """Test that login is required to create review"""
    #     response = self.client.get(self.create_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.create_url}")

    def test_authenticated_access(self):
        """Test authenticated user can access review creation"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_form.html")
        self.assertIsInstance(response.context["form"], CourseReviewForm)

    def test_review_creation(self):
        """Test successful review creation"""
        self.client.login(username="testuser", password="testpass123")

        form_data = {
            "course_name": "New Test Course",
            "title": "New Test Review",
            "content": "New test review content",
            "rating": 4,
        }

        response = self.client.post(self.create_url, data=form_data)

        # Should redirect to review detail
        review = CourseReview.objects.get(title="New Test Review")
        expected_url = reverse("reviews:review_detail", kwargs={"pk": review.pk})
        self.assertRedirects(response, expected_url)

        # Check review was created with correct author
        self.assertEqual(review.author, self.user)
        self.assertEqual(review.course_name, "New Test Course")
        self.assertEqual(review.rating, 4)


class ReviewUpdateViewTest(TestCase):
    """Test ReviewUpdateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.review = CourseReview.objects.create(
            author=self.user,
            title="Original Title",
            content="Original content",
            rating=3,
            course_name="Original Course",
        )
        self.update_url = reverse("reviews:review_update", kwargs={"pk": self.review.pk})

    # def test_login_required(self):
    #     """Test that login is required to update review"""
    #     response = self.client.get(self.update_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.update_url}")

    def test_owner_required(self):
        """Test that only review owner can update it"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 404)  # Should return 404 for non-owner

    def test_owner_can_update(self):
        """Test that review owner can update it"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_form.html")

    def test_successful_update(self):
        """Test successful review update"""
        self.client.login(username="testuser", password="testpass123")

        form_data = {
            "course_name": "Updated Course",
            "title": "Updated Title",
            "content": "Updated content",
            "rating": 5,
        }

        response = self.client.post(self.update_url, data=form_data)

        # Should redirect to review detail
        expected_url = reverse("reviews:review_detail", kwargs={"pk": self.review.pk})
        self.assertRedirects(response, expected_url)

        # Check review was updated
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, "Updated Title")
        self.assertEqual(self.review.content, "Updated content")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.course_name, "Updated Course")


class ReviewDeleteViewTest(TestCase):
    """Test ReviewDeleteView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.review = CourseReview.objects.create(
            author=self.user,
            title="Review to delete",
            content="Content to delete",
            rating=2,
            course_name="Course to delete",
        )
        self.delete_url = reverse("reviews:review_delete", kwargs={"pk": self.review.pk})

    # def test_login_required(self):
    #     """Test that login is required to delete review"""
    #     response = self.client.get(self.delete_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.delete_url}")

    def test_owner_required(self):
        """Test that only review owner can delete it"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)

    def test_owner_can_delete(self):
        """Test that review owner can delete it"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.delete_url)

        # Debug: Check what's in the context
        if hasattr(response, "context") and response.context is not None:
            logger.debug("Context data: %s", dict(response.context))
            if "object" in response.context:
                logger.debug("Object in context: %s", response.context["object"])
            if "review" in response.context:
                logger.debug("Review in context: %s", response.context["review"])

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_confirm_delete.html")

        # Check that the context contains the review with proper ID
        if hasattr(response, "context") and response.context is not None:
            self.assertIn("object", response.context)
            self.assertEqual(response.context["object"], self.review)
            # Also check if 'review' is in context (some views use different context names)
            if "review" in response.context:
                self.assertEqual(response.context["review"], self.review)

    def test_successful_deletion(self):
        """Test successful review deletion"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.delete_url)

        # Should redirect to review list
        self.assertRedirects(response, reverse("reviews:review_list"))

        # Check review was deleted
        with self.assertRaises(CourseReview.DoesNotExist):
            CourseReview.objects.get(pk=self.review.pk)


class UserReviewListViewTest(TestCase):
    """Test UserReviewListView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        # Create reviews for testuser
        self.review1 = CourseReview.objects.create(
            author=self.user,
            title="First User Review",
            content="First user review content",
            rating=5,
            course_name="Course One",
        )
        self.review2 = CourseReview.objects.create(
            author=self.user,
            title="Second User Review",
            content="Second user review content",
            rating=3,
            course_name="Course Two",
        )
        # Create review for other user (should not appear)
        CourseReview.objects.create(
            author=self.other_user,
            title="Other User Review",
            content="Other user content",
            rating=4,
            course_name="Other Course",
        )
        self.user_reviews_url = reverse("reviews:user_reviews", kwargs={"username": "testuser"})

    def test_user_review_list_view_get(self):
        """Test GET request to user review list view"""
        response = self.client.get(self.user_reviews_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/user_reviews.html")
        self.assertEqual(len(response.context["reviews"]), 2)
        self.assertEqual(response.context["profile_user"], self.user)

    def test_user_review_list_only_shows_user_reviews(self):
        """Test that only reviews by specified user are shown"""
        response = self.client.get(self.user_reviews_url)

        reviews = response.context["reviews"]
        self.assertEqual(len(reviews), 2)
        # All reviews should belong to testuser
        for review in reviews:
            self.assertEqual(review.author, self.user)

    def test_user_review_list_vote_counts(self):
        """Test that vote counts are calculated"""
        response = self.client.get(self.user_reviews_url)

        for review in response.context["reviews"]:
            self.assertEqual(review.upvotes, 0)
            self.assertEqual(review.downvotes, 0)
            self.assertEqual(review.vote_count, 0)

    def test_user_review_list_average_rating(self):
        """Test that average rating is calculated correctly"""
        response = self.client.get(self.user_reviews_url)

        # Average of ratings 5 and 3 is 4.0
        self.assertEqual(response.context["average_rating"], 4.0)

    def test_user_review_list_no_reviews(self):
        """Test user with no reviews"""
        user_without_reviews_url = reverse("reviews:user_reviews", kwargs={"username": "otheruser"})
        response = self.client.get(user_without_reviews_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["reviews"]), 1)  # otheruser has 1 review
        self.assertEqual(response.context["profile_user"], self.other_user)
        self.assertIn("average_rating", response.context)

    def test_user_review_list_nonexistent_user(self):
        """Test accessing reviews for non-existent user"""
        nonexistent_url = reverse("reviews:user_reviews", kwargs={"username": "nonexistent"})
        response = self.client.get(nonexistent_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["reviews"]), 0)
        self.assertIsNone(response.context["profile_user"])


class URLTests(TestCase):
    """Test URL patterns and their accessibility"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.review = CourseReview.objects.create(
            author=self.user,
            title="Test Review",
            content="Test content",
            rating=4,
            course_name="Test Course",
        )

    def test_reviews_urls(self):
        """Test all reviews app URLs are accessible"""
        # Public URLs
        public_urls = [
            reverse("reviews:review_list"),
            reverse("reviews:review_detail", kwargs={"pk": self.review.pk}),
            reverse("reviews:user_reviews", kwargs={"username": "testuser"}),
        ]

        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    # def test_protected_urls_redirect_when_anonymous(self):
    #     """Test protected URLs redirect anonymous users to login"""
    #     protected_urls = [
    #         reverse("reviews:review_create"),
    #         reverse("reviews:review_update", kwargs={"pk": self.review.pk}),
    #         reverse("reviews:review_delete", kwargs={"pk": self.review.pk}),
    #     ]
    #
    #     for url in protected_urls:
    #         response = self.client.get(url)
    #         self.assertEqual(response.status_code, 302)  # Redirect to login
    #         self.assertTrue(response.url.startswith("/users/login/"))


class IntegrationTests(TestCase):
    """Test complete user flows and integration"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

        # Create an initial review for the unique constraint test
        self.initial_review = CourseReview.objects.create(
            author=self.user,
            title="Initial Review",
            content="Initial content",
            rating=4,
            course_name="Django Masterclass",
        )

    def test_complete_review_flow(self):
        """Test complete flow: create review -> view it -> update it -> delete it"""
        self.client.login(username="testuser", password="testpass123")

        # Step 1: Create review
        review_data = {
            "course_name": "Integration Test Course",
            "title": "Integration Test Review",
            "content": "Integration test review content",
            "rating": 5,
        }
        response = self.client.post(reverse("reviews:review_create"), data=review_data)
        review = CourseReview.objects.get(title="Integration Test Review")

        # Verify creation
        self.assertEqual(review.author, self.user)
        self.assertEqual(review.course_name, "Integration Test Course")

        # Step 2: View review
        response = self.client.get(reverse("reviews:review_detail", kwargs={"pk": review.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["review"], review)

        # Step 3: Update review
        update_data = {
            "course_name": "Updated Integration Course",
            "title": "Updated Integration Review",
            "content": "Updated integration test review content",
            "rating": 4,
        }
        response = self.client.post(reverse("reviews:review_update", kwargs={"pk": review.pk}), data=update_data)

        # Verify update
        review.refresh_from_db()
        self.assertEqual(review.title, "Updated Integration Review")
        self.assertEqual(review.rating, 4)

        # Step 4: Delete review
        response = self.client.post(reverse("reviews:review_delete", kwargs={"pk": review.pk}))

        # Verify deletion
        self.assertRedirects(response, reverse("reviews:review_list"))
        with self.assertRaises(CourseReview.DoesNotExist):
            CourseReview.objects.get(pk=review.pk)
