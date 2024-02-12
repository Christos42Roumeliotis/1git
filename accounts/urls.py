from django.urls import path
from accounts.views import LoginView, LogoutView, CreateUserView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('admin/create/', CreateUserView.as_view(), name='create'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
