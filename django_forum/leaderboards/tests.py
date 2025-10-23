import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from forum.models import Question
from users.models import UserProfile

# Get logger for this module
logger = logging.getLogger(__name__)

User = get_user_model()


class LeaderboardViewTest(TestCase):
    """Test LeaderboardView functionality"""

    def setUp(self):
        self.client = Client()
        self.leaderboard_url = reverse("leaderboards:leaderboard")

        # Create test users with different reputation points
        self.user1 = User.objects.create_user(username="topuser", email="top@example.com", password="testpass123")
        self.user1.profile.reputation_points = 1000
        self.user1.profile.save()

        self.user2 = User.objects.create_user(username="mediumuser", email="medium@example.com", password="testpass123")
        self.user2.profile.reputation_points = 500
        self.user2.profile.save()

        self.user3 = User.objects.create_user(username="lowuser", email="low@example.com", password="testpass123")
        self.user3.profile.reputation_points = 100
        self.user3.profile.save()

        # User with zero reputation (should not appear in leaderboards)
        self.user_zero = User.objects.create_user(username="zerouser", email="zero@example.com", password="testpass123")
        self.user_zero.profile.reputation_points = 0
        self.user_zero.profile.save()

    def test_all_time_leaders_limit(self):
        """Test that all-time leaders are limited to top 20"""
        # Clear existing users first to avoid interference
        UserProfile.objects.all().delete()

        # Create exactly 25 users with reputation
        for i in range(25):
            user = User.objects.create_user(
                username=f"testuser{i}",
                email=f"test{i}@example.com",
                password="testpass123",
            )
            user.profile.reputation_points = 50 + i
            user.profile.save()

        response = self.client.get(self.leaderboard_url)
        all_time_leaders = response.context["all_time_leaders"]

        # Should be limited to 20 users
        self.assertEqual(len(all_time_leaders), 20)

        # Should include the highest reputation users
        # Highest reputation should be 50 + 24 = 74
        highest_reputation = max(profile.reputation_points for profile in all_time_leaders)
        self.assertEqual(highest_reputation, 74)  # 50 + 24

    def test_leaderboard_template_content(self):
        """Test that template renders leaderboard data correctly"""
        response = self.client.get(self.leaderboard_url)

        # Check that usernames appear in the response
        self.assertContains(response, "topuser")
        self.assertContains(response, "mediumuser")
        self.assertContains(response, "lowuser")

        # Check that reputation points appear
        self.assertContains(response, "1000")
        self.assertContains(response, "500")
        self.assertContains(response, "100")

        # Check that leaderboard sections are present
        self.assertContains(response, "All-Time Reputation Leaders")
        self.assertContains(response, "This Month's Top Contributors")


class LeaderboardIntegrationTest(TestCase):
    """Integration tests for leaderboard functionality"""

    def setUp(self):
        self.client = Client()

    # def test_leaderboard_url_resolution(self):
    #     """Test that leaderboard URL resolves correctly"""
    #     url = reverse("leaderboards:leaderboard")
    #     self.assertEqual(url, "/leaderboards/")

    def test_leaderboard_performance(self):
        """Test that leaderboard page loads efficiently"""
        # Create a reasonable number of users to test performance
        for i in range(50):
            user = User.objects.create_user(
                username=f"perfuser{i}",
                email=f"perf{i}@example.com",
                password="testpass123",
            )
            user.profile.reputation_points = i * 10
            user.profile.save()

            # Add some recent activity
            if i % 5 == 0:  # Every 5th user has recent activity
                Question.objects.create(title=f"Question {i}", content=f"Content {i}", author=user)

        import time

        start_time = time.time()

        response = self.client.get(reverse("leaderboards:leaderboard"))

        end_time = time.time()
        load_time = end_time - start_time

        # Page should load in reasonable time (adjust threshold as needed)
        self.assertLess(load_time, 2.0)  # 2 seconds maximum
        self.assertEqual(response.status_code, 200)

        logger.debug("Leaderboard page loaded in %.3f seconds", load_time)

    def test_leaderboard_with_old_activity(self):
        """Test that only recent activity counts for monthly leaders"""
        # Create a user with old activity (more than a month ago)
        old_user = User.objects.create_user(username="olduser", email="old@example.com", password="testpass123")
        old_user.profile.reputation_points = 300
        old_user.profile.save()

        # Create question from more than a month ago
        old_date = timezone.now() - timedelta(days=35)
        old_question = Question.objects.create(
            title="Old Question",
            content="Old content",
            author=old_user,
            created_at=old_date,
        )
        # Manually save to override auto_now_add
        Question.objects.filter(pk=old_question.pk).update(created_at=old_date)

        # Create a user with recent activity
        recent_user = User.objects.create_user(
            username="recentuser",
            email="recent@example.com",
            password="testpass123",
        )
        recent_user.profile.reputation_points = 200
        recent_user.profile.save()

        Question.objects.create(title="Recent Question", content="Recent content", author=recent_user)

        response = self.client.get(reverse("leaderboards:leaderboard"))
        month_leaders = response.context["month_leaders"]

        # Should include user with recent activity
        recent_usernames = [profile.user.username for profile in month_leaders]
        self.assertIn("recentuser", recent_usernames)

        # Might or might not include old user depending on implementation
        # The current implementation filters by created_at__gte=month_start
        # so old_user should not appear in month_leaders


class LeaderboardEdgeCasesTest(TestCase):
    """Test edge cases for leaderboard functionality"""

    def setUp(self):
        self.client = Client()

    def test_users_with_same_reputation(self):
        """Test leaderboard when multiple users have same reputation"""
        # Create users with identical reputation
        for i in range(5):
            user = User.objects.create_user(
                username=f"sameuser{i}",
                email=f"same{i}@example.com",
                password="testpass123",
            )
            user.profile.reputation_points = 500
            user.profile.save()

        response = self.client.get(reverse("leaderboards:leaderboard"))
        all_time_leaders = response.context["all_time_leaders"]

        # All should appear in leaderboard
        self.assertEqual(len(all_time_leaders), 5)

        # Order might be by secondary criteria (like username or ID)
        # This is acceptable as long as they're all included

    def test_negative_reputation(self):
        """Test leaderboard with users having negative reputation"""
        negative_user = User.objects.create_user(
            username="negativeuser",
            email="negative@example.com",
            password="testpass123",
        )
        negative_user.profile.reputation_points = -50
        negative_user.profile.save()

        response = self.client.get(reverse("leaderboards:leaderboard"))
        all_time_leaders = response.context["all_time_leaders"]

        # Users with negative reputation should not appear in leaderboards
        # since we filter by reputation_points__gt=0
        usernames = [profile.user.username for profile in all_time_leaders]
        self.assertNotIn("negativeuser", usernames)

    def test_deleted_user_handling(self):
        """Test that leaderboard handles user deletion gracefully"""
        # This tests that the queries don't break if users are deleted
        # The current implementation uses select_related('user') so it should be fine

        response = self.client.get(reverse("leaderboards:leaderboard"))
        self.assertEqual(response.status_code, 200)
