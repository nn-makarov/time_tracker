from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🔐 Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('stats/', views.get_stats, name='get_stats'),

    # 📝 Моменты - ОДИН маршрут для обоих методов
    path('records/', views.record_list, name='record-list'),  # GET и POST
    path('records/<int:record_id>/', views.delete_record, name='delete_record'),
]