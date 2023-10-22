from django.urls import path, re_path
from . import views

urlpatterns = [path('', views.PostView.as_view(), name='Home'),
               path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
               path('review/<int:pk>/', views.AddComments.as_view(), name='add_comments'),
               path('<int:pk>/add_likes/', views.AddLikes.as_view(), name='add_likes'),
               path('<int:pk>/del_likes/', views.DeLike.as_view(), name='del_likes'),
               path('login/', views.sign_in, name='login'),
               path('logout/', views.sign_out, name='logout'),
               path('register/', views.sign_up, name='register'),
               ]