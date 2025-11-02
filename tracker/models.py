from django.db import models
from django.contrib.auth.models import User

class TimeRecord(models.Model):
    ACTIVITY_CHOICES = [
        ('work', 'Работа'),
        ('study', 'Учеба'),
        ('sport', 'Спорт'),
        ('rest', 'Отдых'),
        ('meal', 'Еда'),
        ('sleep', 'Сон'),
        ('reading', 'Чтение'),
        ('gaming', 'Игры'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True)
    duration = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.activity}"