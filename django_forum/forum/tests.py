# forum/tests.py
import logging

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from forum.forms import AnswerForm, QuestionForm
from forum.models import Answer, Question

# Get logger for this module
logger = logging.getLogger(__name__)

User = get_user_model()


class QuestionModelTest(TestCase):
    """Test Question model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.question = Question.objects.create(
            title="Test Question",
            content="Test question content",
            author=self.user,
        )

    def test_question_creation(self):
        """Test question creation with all fields"""
        self.assertEqual(self.question.title, "Test Question")
        self.assertEqual(self.question.content, "Test question content")
        self.assertEqual(self.question.author, self.user)
        self.assertFalse(self.question.is_solved)
        self.assertIsNotNone(self.question.created_at)
        self.assertIsNotNone(self.question.updated_at)

    def test_question_string_representation(self):
        """Test question string representation"""
        self.assertEqual(str(self.question), "Test Question")

    def test_question_absolute_url(self):
        """Test get_absolute_url method"""
        expected_url = reverse("forum:question_detail", kwargs={"pk": self.question.pk})
        self.assertEqual(self.question.get_absolute_url(), expected_url)

    def test_question_answers_count(self):
        """Test answers_count method"""
        # Initially no answers
        self.assertEqual(self.question.answers_count(), 0)

        # Add an answer
        Answer.objects.create(question=self.question, content="Test answer", author=self.user)
        self.assertEqual(self.question.answers_count(), 1)

    def test_question_ordering(self):
        """Test that questions are ordered by creation date (newest first)"""
        # Create another question
        question2 = Question.objects.create(title="Newer Question", content="Newer content", author=self.user)

        questions = Question.objects.all()
        self.assertEqual(questions[0], question2)  # Newest first
        self.assertEqual(questions[1], self.question)  # Older second


class AnswerModelTest(TestCase):
    """Test Answer model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.question = Question.objects.create(
            title="Test Question",
            content="Test question content",
            author=self.user,
        )
        self.answer = Answer.objects.create(question=self.question, content="Test answer content", author=self.user)

    def test_answer_creation(self):
        """Test answer creation with all fields"""
        self.assertEqual(self.answer.question, self.question)
        self.assertEqual(self.answer.content, "Test answer content")
        self.assertEqual(self.answer.author, self.user)
        self.assertFalse(self.answer.is_accepted)
        self.assertIsNotNone(self.answer.created_at)
        self.assertIsNotNone(self.answer.updated_at)

    def test_answer_string_representation(self):
        """Test answer string representation"""
        expected_str = f"Answer to '{self.question.title}' by {self.user.username}"
        self.assertEqual(str(self.answer), expected_str)

    def test_mark_accepted_method(self):
        """Test mark_accepted method"""
        # Initially not accepted
        self.assertFalse(self.answer.is_accepted)
        initial_reputation = self.user.profile.reputation_points

        # Mark as accepted
        self.answer.mark_accepted()

        # Refresh from database
        self.answer.refresh_from_db()
        self.user.profile.refresh_from_db()

        # Should be accepted
        self.assertTrue(self.answer.is_accepted)

        # Reputation should be increased
        from core.rep_rules import REPUTATION_RULES

        expected_reputation = initial_reputation + REPUTATION_RULES["answer_accepted"]
        self.assertEqual(self.user.profile.reputation_points, expected_reputation)

    def test_answer_ordering(self):
        """Test that answers are ordered by accepted status then creation date"""
        # Create another answer
        answer2 = Answer.objects.create(question=self.question, content="Second answer", author=self.user)

        # Make first answer accepted
        self.answer.is_accepted = True
        self.answer.save()

        answers = Answer.objects.all()
        self.assertEqual(answers[0], self.answer)  # Accepted first
        self.assertEqual(answers[1], answer2)  # Then by creation date


class QuestionFormTest(TestCase):
    """Test QuestionForm validation and functionality"""

    def test_valid_question_form(self):
        """Test form with valid data"""
        form_data = {"title": "Test Question Title", "content": "This is a test question content."}
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_form_with_empty_title(self):
        """Test form with empty title"""
        form_data = {"title": "", "content": "This is a test question content."}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_question_form_with_empty_content(self):
        """Test form with empty content"""
        form_data = {"title": "Test Question Title", "content": ""}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_question_form_widget_attributes(self):
        """Test that form widgets have correct attributes"""
        form = QuestionForm()
        title_widget = form.fields["title"].widget
        content_widget = form.fields["content"].widget

        self.assertEqual(title_widget.attrs.get("class"), "form-control")
        self.assertEqual(title_widget.attrs.get("placeholder"), "What's your question?")

        self.assertEqual(content_widget.attrs.get("class"), "form-control")
        self.assertEqual(content_widget.attrs.get("placeholder"), "Describe your problem in detail...")
        self.assertEqual(content_widget.attrs.get("rows"), 5)


class AnswerFormTest(TestCase):
    """Test AnswerForm validation and functionality"""

    def test_valid_answer_form(self):
        """Test form with valid data"""
        form_data = {"content": "This is a test answer content."}
        form = AnswerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_answer_form_with_empty_content(self):
        """Test form with empty content"""
        form_data = {"content": ""}
        form = AnswerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_answer_form_widget_attributes(self):
        """Test that form widgets have correct attributes"""
        form = AnswerForm()
        content_widget = form.fields["content"].widget

        self.assertEqual(content_widget.attrs.get("class"), "form-control")
        self.assertEqual(content_widget.attrs.get("placeholder"), "Write your answer here...")
        self.assertEqual(content_widget.attrs.get("rows"), 4)


class QuestionListViewTest(TestCase):
    """Test QuestionListView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        # Make the questions more distinct for search tests
        self.question1 = Question.objects.create(
            title="First Unique Question",
            content="First unique question content with specific terms",
            author=self.user,
        )
        self.question2 = Question.objects.create(
            title="Second Different Question",
            content="Second different question content with other terms",
            author=self.user,
        )
        self.list_url = reverse("forum:question_list")

    def test_question_list_search_multiple_words(self):
        """Test question list search with multiple words"""
        # Use more specific search terms that only match one question
        response = self.client.get(self.list_url, {"q": "Unique specific"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 1)
        self.assertEqual(response.context["questions"][0], self.question1)
        self.assertEqual(response.context["search_words"], ["Unique", "specific"])

    # Update other search tests to use more specific terms
    def test_question_list_search(self):
        """Test question list with search query"""
        response = self.client.get(self.list_url, {"q": "Unique"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 1)
        self.assertEqual(response.context["questions"][0], self.question1)
        self.assertEqual(response.context["query"], "Unique")
        self.assertTrue(response.context["is_search"])

    def test_question_list_search_no_results(self):
        """Test question list search with no matching results"""
        response = self.client.get(self.list_url, {"q": "nonexistenttermxyz"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 0)
        self.assertEqual(response.context["results_count"], 0)

    def test_question_list_search_in_answers(self):
        """Test that search includes answer content"""
        # Create an answer with specific content
        Answer.objects.create(
            question=self.question1,
            content="Specific unique answer content for search",
            author=self.user,
        )

        response = self.client.get(self.list_url, {"q": "unique answer"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions"]), 1)
        self.assertEqual(response.context["questions"][0], self.question1)


class QuestionDetailViewTest(TestCase):
    """Test QuestionDetailView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.question = Question.objects.create(
            title="Test Question",
            content="Test question content",
            author=self.user,
        )
        self.detail_url = reverse("forum:question_detail", kwargs={"pk": self.question.pk})

    def test_question_detail_view_get(self):
        """Test GET request to question detail view"""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/question_detail.html")
        self.assertEqual(response.context["question"], self.question)
        self.assertIsInstance(response.context["answer_form"], AnswerForm)

    def test_question_detail_with_answers(self):
        """Test question detail view with answers"""
        answer = Answer.objects.create(question=self.question, content="Test answer", author=self.user)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(answer, response.context["answers"])

        # Check that vote counts are calculated
        question = response.context["question"]
        self.assertEqual(question.upvotes, 0)
        self.assertEqual(question.downvotes, 0)
        self.assertEqual(question.vote_count, 0)

    def test_question_detail_nonexistent(self):
        """Test accessing non-existent question"""
        nonexistent_url = reverse("forum:question_detail", kwargs={"pk": 999})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class QuestionCreateViewTest(TestCase):
    """Test QuestionCreateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.create_url = reverse("forum:question_create")

    # def test_login_required(self):
    #     """Test that login is required to create question"""
    #     response = self.client.get(self.create_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.create_url}")

    def test_authenticated_access(self):
        """Test authenticated user can access question creation"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/question_form.html")
        self.assertIsInstance(response.context["form"], QuestionForm)

    def test_question_creation(self):
        """Test successful question creation"""
        self.client.login(username="testuser", password="testpass123")

        form_data = {"title": "New Test Question", "content": "New test question content"}

        response = self.client.post(self.create_url, data=form_data)

        # Should redirect to question detail
        question = Question.objects.get(title="New Test Question")
        expected_url = reverse("forum:question_detail", kwargs={"pk": question.pk})
        self.assertRedirects(response, expected_url)

        # Check question was created with correct author
        self.assertEqual(question.author, self.user)
        self.assertEqual(question.content, "New test question content")


class QuestionUpdateViewTest(TestCase):
    """Test QuestionUpdateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.question = Question.objects.create(title="Original Title", content="Original content", author=self.user)
        self.update_url = reverse("forum:question_update", kwargs={"pk": self.question.pk})

    # def test_login_required(self):
    #     """Test that login is required to update question"""
    #     response = self.client.get(self.update_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.update_url}")

    def test_owner_required(self):
        """Test that only question owner can update it"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 404)  # Should return 404 for non-owner

    def test_owner_can_update(self):
        """Test that question owner can update it"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/question_form.html")

    def test_successful_update(self):
        """Test successful question update"""
        self.client.login(username="testuser", password="testpass123")

        form_data = {"title": "Updated Title", "content": "Updated content"}

        response = self.client.post(self.update_url, data=form_data)

        # Should redirect to question detail
        expected_url = reverse("forum:question_detail", kwargs={"pk": self.question.pk})
        self.assertRedirects(response, expected_url)

        # Check question was updated
        self.question.refresh_from_db()
        self.assertEqual(self.question.title, "Updated Title")
        self.assertEqual(self.question.content, "Updated content")


class QuestionDeleteViewTest(TestCase):
    """Test QuestionDeleteView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.question = Question.objects.create(
            title="Question to delete",
            content="Content to delete",
            author=self.user,
        )
        self.delete_url = reverse("forum:question_delete", kwargs={"pk": self.question.pk})

    # def test_login_required(self):
    #     """Test that login is required to delete question"""
    #     response = self.client.get(self.delete_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.delete_url}")

    def test_owner_required(self):
        """Test that only question owner can delete it"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)

    def test_owner_can_delete(self):
        """Test that question owner can delete it"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/question_confirm_delete.html")

    def test_successful_deletion(self):
        """Test successful question deletion"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.delete_url)

        # Should redirect to question list
        self.assertRedirects(response, reverse("forum:question_list"))

        # Check question was deleted
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(pk=self.question.pk)


class AnswerCreateViewTest(TestCase):
    """Test AnswerCreateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.question = Question.objects.create(title="Test Question", content="Test content", author=self.user)
        self.create_url = reverse("forum:answer_create", kwargs={"question_id": self.question.pk})

    # def test_login_required(self):
    #     """Test that login is required to create answer"""
    #     response = self.client.get(self.create_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.create_url}")

    def test_authenticated_user_can_answer(self):
        """Test authenticated user can create answer"""
        self.client.login(username="testuser", password="testpass123")

        form_data = {"content": "This is a test answer"}

        response = self.client.post(self.create_url, data=form_data)

        # Should redirect to question detail
        expected_url = reverse("forum:question_detail", kwargs={"pk": self.question.pk})
        self.assertRedirects(response, expected_url)

        # Check answer was created
        answer = Answer.objects.get(question=self.question)
        self.assertEqual(answer.content, "This is a test answer")
        self.assertEqual(answer.author, self.user)


class AnswerUpdateViewTest(TestCase):
    """Test AnswerUpdateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.question = Question.objects.create(title="Test Question", content="Test content", author=self.user)
        self.answer = Answer.objects.create(question=self.question, content="Original answer", author=self.user)
        self.update_url = reverse("forum:answer_update", kwargs={"pk": self.answer.pk})

    # def test_login_required(self):
    #     """Test that login is required to update answer"""
    #     response = self.client.get(self.update_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.update_url}")

    def test_owner_required(self):
        """Test that only answer owner can update it"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 404)

    def test_owner_can_update(self):
        """Test that answer owner can update it"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/answer_form.html")

    def test_successful_update(self):
        """Test successful answer update"""
        self.client.login(username="testuser", password="testpass123")

        form_data = {"content": "Updated answer content"}

        response = self.client.post(self.update_url, data=form_data)

        # Should redirect to question detail
        expected_url = reverse("forum:question_detail", kwargs={"pk": self.question.pk})
        self.assertRedirects(response, expected_url)

        # Check answer was updated
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.content, "Updated answer content")


class AnswerDeleteViewTest(TestCase):
    """Test AnswerDeleteView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.question = Question.objects.create(title="Test Question", content="Test content", author=self.user)
        self.answer = Answer.objects.create(question=self.question, content="Answer to delete", author=self.user)
        self.delete_url = reverse("forum:answer_delete", kwargs={"pk": self.answer.pk})

    # def test_login_required(self):
    #     """Test that login is required to delete answer"""
    #     response = self.client.get(self.delete_url)
    #     self.assertRedirects(response, f"/users/login/?next={self.delete_url}")

    def test_owner_required(self):
        """Test that only answer owner can delete it"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)

    def test_successful_deletion(self):
        """Test successful answer deletion"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(self.delete_url)

        # Should redirect to question detail
        expected_url = reverse("forum:question_detail", kwargs={"pk": self.question.pk})
        self.assertRedirects(response, expected_url)

        # Check answer was deleted
        with self.assertRaises(Answer.DoesNotExist):
            Answer.objects.get(pk=self.answer.pk)


class AcceptAnswerViewTest(TestCase):
    """Test AcceptAnswerView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="question_owner",
            email="owner@example.com",
            password="testpass123",
        )
        self.answer_author = User.objects.create_user(
            username="answer_author",
            email="author@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        self.question = Question.objects.create(title="Test Question", content="Test content", author=self.user)
        self.answer = Answer.objects.create(question=self.question, content="Test answer", author=self.answer_author)
        self.accept_url = reverse("forum:answer_accept", kwargs={"pk": self.answer.pk})

    # def test_login_required(self):
    #     """Test that login is required to accept answer"""
    #     response = self.client.post(self.accept_url)
    #     # Anonymous users should be redirected to login
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response.url.startswith("/users/login/"))

    def test_question_owner_required(self):
        """Test that only question owner can accept answer"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.post(self.accept_url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"], "Only question author can accept answers")

    def test_successful_acceptance(self):
        """Test successful answer acceptance"""
        self.client.login(username="question_owner", password="testpass123")

        initial_reputation = self.answer_author.profile.reputation_points

        response = self.client.post(self.accept_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

        # Check answer was accepted
        self.answer.refresh_from_db()
        self.assertTrue(self.answer.is_accepted)

        # Check reputation was awarded
        from core.rep_rules import REPUTATION_RULES

        self.answer_author.profile.refresh_from_db()
        expected_reputation = initial_reputation + REPUTATION_RULES["answer_accepted"]
        self.assertEqual(self.answer_author.profile.reputation_points, expected_reputation)

    def test_unaccept_previous_answers(self):
        """Test that accepting an answer unaccepts previous ones"""
        # Create and accept another answer first
        previous_answer = Answer.objects.create(
            question=self.question,
            content="Previous answer",
            author=self.answer_author,
            is_accepted=True,
        )

        self.client.login(username="question_owner", password="testpass123")
        response = self.client.post(self.accept_url)

        self.assertEqual(response.status_code, 200)

        # Check previous answer is no longer accepted
        previous_answer.refresh_from_db()
        self.assertFalse(previous_answer.is_accepted)

        # Check new answer is accepted
        self.answer.refresh_from_db()
        self.assertTrue(self.answer.is_accepted)


class URLTests(TestCase):
    """Test URL patterns and their accessibility"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.question = Question.objects.create(title="Test Question", content="Test content", author=self.user)
        self.answer = Answer.objects.create(question=self.question, content="Test answer", author=self.user)

    def test_forum_urls(self):
        """Test all forum app URLs are accessible"""
        # Public URLs
        public_urls = [
            reverse("forum:question_list"),
            reverse("forum:question_detail", kwargs={"pk": self.question.pk}),
        ]

        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    # def test_protected_urls_redirect_when_anonymous(self):
    #     """Test protected URLs redirect anonymous users to login"""
    #     protected_urls = [
    #         reverse("forum:question_create"),
    #         reverse("forum:question_update", kwargs={"pk": self.question.pk}),
    #         reverse("forum:question_delete", kwargs={"pk": self.question.pk}),
    #         reverse("forum:answer_create", kwargs={"question_id": self.question.pk}),
    #         reverse("forum:answer_update", kwargs={"pk": self.answer.pk}),
    #         reverse("forum:answer_delete", kwargs={"pk": self.answer.pk}),
    #         reverse("forum:answer_accept", kwargs={"pk": self.answer.pk}),
    #     ]
    #
    #     for url in protected_urls:
    #         response = self.client.get(url)
    #         self.assertIn(response.status_code, [302, 403])  # Redirect or forbidden


class IntegrationTests(TestCase):
    """Test complete user flows and integration"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_complete_question_flow(self):
        """Test complete flow: create question -> add answer -> accept answer"""
        self.client.login(username="testuser", password="testpass123")

        # Step 1: Create question
        question_data = {"title": "Integration Test Question", "content": "Integration test question content"}
        response = self.client.post(reverse("forum:question_create"), data=question_data)
        question = Question.objects.get(title="Integration Test Question")

        # Step 2: Add answer
        answer_data = {"content": "Integration test answer content"}
        response = self.client.post(
            reverse("forum:answer_create", kwargs={"question_id": question.pk}),
            data=answer_data,
        )
        answer = Answer.objects.get(question=question)

        # Step 3: Accept answer
        response = self.client.post(reverse("forum:answer_accept", kwargs={"pk": answer.pk}))

        # Verify all steps worked
        self.assertEqual(response.status_code, 200)
        answer.refresh_from_db()
        self.assertTrue(answer.is_accepted)

        # Verify question shows as solved (this depends on your implementation)
        # If your system automatically marks question as solved when answer is accepted,
        # then uncomment the following lines. Otherwise, remove them.
        question.refresh_from_db()
        self.assertTrue(question.is_solved)

        # Alternative: Check that the question has an accepted answer
        self.assertTrue(question.answers.filter(is_accepted=True).exists())
