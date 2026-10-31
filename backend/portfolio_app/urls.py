from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ChangePasswordView,
    CommentViewSet,
    ContactMessageViewSet,
    CustomTokenObtainPairView,
    EducationViewSet,
    ExperienceViewSet,
    LogoutView,
    MeView,
    PostViewSet,
    ProfileDetailView,
    ProjectViewSet,
    SkillViewSet,
    TagViewSet,
    dashboard_stats,
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'education', EducationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'contact', ContactMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', __import__('rest_framework_simplejwt.views', fromlist=['TokenRefreshView']).TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', MeView.as_view(), name='me'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
]
