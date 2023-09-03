from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import *
urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:category_id>/', items_by_category, name='items_by_category'),
]
