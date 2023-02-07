from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('currentuser/', CurrentUserViewSet.as_view(
        {
            'get': 'list',
            'put': 'update',
            'delete': 'destroy'
        }), name='current_user'),
    path('photo/', PhotoAPIList.as_view(), name='photo'),
    path('photo/<int:pk>', PhotoAPIUpdate.as_view(), name='photo_detail'),
    path('photodelete/<int:pk>', PhotoAPIDestroy.as_view(), name='photo_delete'),

    # path('auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    re_path('', include('social_django.urls', namespace='social')),
    path('githubauth/', githubauth),
]
