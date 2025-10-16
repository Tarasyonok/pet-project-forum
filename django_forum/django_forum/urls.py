import django.contrib.admin
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path("users/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    # path("", include("home.urls")),
    # path("forum/", include("forum.urls")),
    # path("reviews/", include("reviews.urls")),
    # path("votes/", include("votes.urls")),
    # path("leaderboards/", include("leaderboards.urls")),
    path("admin/", django.contrib.admin.site.urls),
    *static(django.conf.settings.STATIC_URL, document_root=django.conf.settings.STATIC_ROOT),
)

# handler404 = 'home.views.custom_404_view'
