from django.contrib import admin
from django.urls import path, include
from accounts.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/google/', include('dj_rest_auth.registration.urls')),  # Social login
    path('dj-rest-auth/google-login/', GoogleLogin.as_view(), name='google_login'),
]