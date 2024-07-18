from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import loginView, registerView, CookieTokenRefreshView, logoutView, user, RecipeRecommenderViewSet

app_name = "user"

router = DefaultRouter()
router.register(r'recommendation', RecipeRecommenderViewSet, basename='recommendation')

urlpatterns = [
    path('login', loginView),
    path('register', registerView),
    path('refresh-token', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path('user', user),
    path('', include(router.urls)),
    # path('auth/recommendation/', recommendationsView),
]
