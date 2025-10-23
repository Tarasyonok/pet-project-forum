# users/tests.py
import logging

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from users.forms import SignUpForm, UserProfileUpdateForm, UserUpdateForm
from users.models import User, UserProfile

# Get logger for this module
logger = logging.getLogger(__name__)


class UserUpdateFormTest(TestCase):
    """Test UserUpdateForm validation and functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Old",
            last_name="Name",
        )

    def test_valid_user_update_form(self):
        """Test form with valid data"""
        form_data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_user_update_form_save(self):
        """Test form save method updates user"""
        form_data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        # Refresh from database
        self.user.refresh_from_db()

        # Check user fields were updated
        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")

    def test_invalid_email_format(self):
        """Test form with invalid email"""
        form_data = {
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "User",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class UserProfileUpdateFormTest(TestCase):
    """Test UserProfileUpdateForm validation and functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.profile = self.user.profile

    def test_valid_profile_update_form(self):
        """Test form with valid data"""
        form_data = {
            "bio": "This is my bio",
            "birthday": "1990-01-01",
        }
        form = UserProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_profile_update_form_save(self):
        """Test form save method updates profile"""
        form_data = {
            "bio": "This is my bio",
            "birthday": "1990-01-01",
        }
        form = UserProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        form.save()

        # Refresh from database
        self.profile.refresh_from_db()

        # Check profile fields were updated
        self.assertEqual(self.profile.bio, "This is my bio")
        self.assertEqual(str(self.profile.birthday), "1990-01-01")

    def test_avatar_file_validation(self):
        """Test avatar file validation"""
        # Create a valid image file
        small_img = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded_file = SimpleUploadedFile("small.png", small_img, content_type="image/png")

        form_data = {
            "bio": "Test bio",
        }

        form = UserProfileUpdateForm(
            data=form_data,
            files={"avatar": uploaded_file},
            instance=self.profile,
        )
        self.assertTrue(form.is_valid())

    def test_invalid_file_extension(self):
        """Test avatar with invalid file extension"""
        text_file = b"This is not an image file"
        uploaded_file = SimpleUploadedFile("test.txt", text_file, content_type="text/plain")

        form_data = {
            "bio": "Test bio",
        }

        form = UserProfileUpdateForm(
            data=form_data,
            files={"avatar": uploaded_file},
            instance=self.profile,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("avatar", form.errors)


class ProfileUpdateViewTest(TestCase):
    """Test ProfileUpdateView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Old",
            last_name="Name",
        )
        self.profile = self.user.profile
        self.edit_url = reverse("users:edit-profile")

    def test_login_required(self):
        """Test that login is required to access edit profile"""
        response = self.client.get(self.edit_url)

        # Should redirect to login page
        self.assertRedirects(response, f"/en/users/login/?next={self.edit_url}")

    def test_authenticated_access(self):
        """Test authenticated user can access edit profile"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_edit.html")

        # Check that both forms are in context
        self.assertIn("user_form", response.context)
        self.assertIn("profile_form", response.context)
        self.assertIn("form", response.context)

        # Check form types
        self.assertIsInstance(response.context["user_form"], UserUpdateForm)
        self.assertIsInstance(response.context["profile_form"], UserProfileUpdateForm)

    def test_successful_profile_update(self):
        """Test successful profile update"""
        self.client.login(username="testuser", password="testpass123")

        update_data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "bio": "Updated bio text",
            "birthday": "1990-01-01",
        }

        response = self.client.post(self.edit_url, data=update_data, follow=True)

        # Should redirect to profile page
        self.assertRedirects(response, reverse("users:profile", kwargs={"username": "testuser"}))

        # Check data was updated
        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.email, "updated@example.com")
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "Name")
        self.assertEqual(self.profile.bio, "Updated bio text")
        self.assertEqual(str(self.profile.birthday), "1990-01-01")

    def test_profile_update_with_avatar(self):
        """Test profile update with avatar upload"""
        self.client.login(username="testuser", password="testpass123")

        # Create a test image
        small_img = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
            b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
            b"\x02\x4c\x01\x00\x3b"
        )
        uploaded_file = SimpleUploadedFile("avatar.png", small_img, content_type="image/png")

        update_data = {
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "bio": "Bio with avatar",
        }

        response = self.client.post(self.edit_url, data=update_data, files={"avatar": uploaded_file}, follow=True)

        # Should redirect to profile page
        self.assertRedirects(response, reverse("users:profile", kwargs={"username": "testuser"}))


class SignUpViewTest(TestCase):
    """Test SignUpView functionality"""

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("users:signup")
        self.valid_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        }

    def test_signup_view_get(self):
        """Test GET request to signup view"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")
        self.assertIsInstance(response.context["form"], SignUpForm)

    def test_signup_view_post_valid_data(self):
        """Test POST request with valid data creates user"""
        response = self.client.post(self.signup_url, data=self.valid_data)

        # Should redirect to login page
        self.assertRedirects(response, reverse("users:login"))

        # User should be created
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # User should be active
        user = User.objects.get(username="newuser")
        self.assertTrue(user.is_active)

        # Profile should be created
        self.assertTrue(hasattr(user, "profile"))

    def test_signup_view_post_invalid_data(self):
        """Test POST request with invalid data"""
        invalid_data = self.valid_data.copy()
        invalid_data["password2"] = "differentpassword"  # Mismatched passwords

        response = self.client.post(self.signup_url, data=invalid_data)

        # Should return to form with errors (status 200)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

        # Check that form has errors
        self.assertContains(response, "password2", status_code=200)


class UserModelTest(TestCase):
    """Test User model functionality"""

    def setUp(self):
        self.user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass123"}

    def test_create_user(self):
        """Test creating a basic user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertEqual(user.role, User.Role.GUEST)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass123")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.role, User.Role.GUEST)

    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), "User testuser")

    def test_user_profile_auto_creation(self):
        """Test that user profile is automatically created when user is created"""
        user = User.objects.create_user(**self.user_data)

        # Profile should exist
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, UserProfile)

        # Check default values
        self.assertEqual(user.profile.reputation_points, 0)
        self.assertEqual(user.profile.bio, "")
        self.assertEqual(user.profile.avatar, "")


class UserProfileModelTest(TestCase):
    """Test UserProfile model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.profile = self.user.profile

    def test_profile_string_representation(self):
        """Test profile string representation"""
        self.assertEqual(str(self.profile), "Profile of testuser")

    def test_profile_relationship(self):
        """Test one-to-one relationship between User and UserProfile"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile, self.profile)

    def test_reputation_points_default(self):
        """Test reputation points default value"""
        self.assertEqual(self.profile.reputation_points, 0)
        self.profile.reputation_points = 100
        self.profile.save()

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.reputation_points, 100)


class LoginViewTest(TestCase):
    """Test LoginView functionality"""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse("users:login")
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_login_view_get(self):
        """Test GET request to login view"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_failed_login(self):
        """Test failed login attempt"""
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
        )

        # Should return to login page
        self.assertEqual(response.status_code, 200)
        # Check that user is not authenticated
        self.assertFalse(response.context["user"].is_authenticated)


class PublicProfileViewTest(TestCase):
    """Test PublicProfileView functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.profile_url = reverse("users:profile", kwargs={"username": "testuser"})

    def test_profile_view_accessible(self):
        """Test profile page is accessible"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/public_profile.html")
        self.assertEqual(response.context["profile_user"], self.user)

    def test_profile_view_context_data(self):
        """Test profile view context contains expected data"""
        response = self.client.get(self.profile_url)
        context = response.context

        # Check basic context variables
        self.assertEqual(context["profile_user"], self.user)
        self.assertIn("is_owner", context)

    def test_is_owner_context(self):
        """Test is_owner context variable"""
        # When not logged in
        response = self.client.get(self.profile_url)
        self.assertFalse(response.context["is_owner"])

        # When logged in as the user
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertTrue(response.context["is_owner"])

        # When logged in as different user
        User.objects.create_user(username="otheruser", email="other@example.com", password="testpass123")
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertFalse(response.context["is_owner"])

    def test_nonexistent_user_profile(self):
        """Test accessing profile of non-existent user"""
        nonexistent_url = reverse("users:profile", kwargs={"username": "nonexistent"})
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, 404)


class EdgeCaseTests(TestCase):
    """Test edge cases and error conditions"""

    def test_duplicate_email_signup(self):
        """Test that duplicate email addresses are rejected"""
        # Create first user
        User.objects.create_user(username="user1", email="duplicate@example.com", password="testpass123")

        # Try to create second user with same email
        form_data = {
            "username": "user2",
            "email": "duplicate@example.com",  # Same email
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_case_insensitive_username_login(self):
        """Test that username login is case-sensitive"""
        User.objects.create_user(
            username="TestUser",
            email="test@example.com",
            password="testpass123",  # With capital letters
        )

        # Try to login with lowercase
        client = Client()
        response = client.post(
            reverse("users:login"),
            {
                "username": "testuser",  # lowercase
                "password": "testpass123",
            },
        )

        # Should fail because usernames are case-sensitive
        self.assertFalse(response.context["user"].is_authenticated)


class URLTests(TestCase):
    """Test URL patterns and their accessibility"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_users_urls(self):
        """Test all users app URLs are accessible"""
        # Public URLs - should return 200
        public_urls = [
            reverse("users:login"),
            reverse("users:signup"),
            reverse("users:password_reset"),
            reverse("users:password_reset_done"),
            reverse("users:profile", kwargs={"username": "testuser"}),
        ]

        for url in public_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])

    def test_protected_urls_redirect_when_anonymous(self):
        """Test protected URLs redirect anonymous users to login"""
        protected_urls = [
            reverse("users:edit-profile"),
            reverse("users:password_change"),
        ]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue("/login" in response.url)
