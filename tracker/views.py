from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
import json

from .models import TimeRecord

# 🏠 Главная страница - ПРОСТОЙ JSON (без шаблонов)
def home(request):
    return JsonResponse({
        'message': 'Time Tracker API работает! 🚀',
        'endpoints': {
            'POST /api/register/': 'Регистрация пользователя',
            'POST /api/login/': 'Вход в систему', 
            'POST /api/logout/': 'Выход из системы',
            'POST /api/records/': 'Создание момента',
            'GET /api/records/?from=YYYY-MM-DD&to=YYYY-MM-DD': 'Получение моментов за период',
            'DELETE /api/records/{id}/': 'Удаление момента'
        },
        'activity_types': ['work', 'study', 'sport', 'rest', 'meal', 'sleep']
    })

# 🔐 Аутентификация
@csrf_exempt
def register(request):
    """POST /api/register/ - Регистрация"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['login'],
                password=data['password'],
                first_name=data.get('firstName', ''),
                last_name=data.get('lastName', '')
            )
            return JsonResponse({
                'userId': user.id, 
                'firstName': user.first_name,
                'lastName': user.last_name,
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@csrf_exempt
@login_required
def record_list(request):
    """Обрабатывает GET (получение) и POST (создание) для /api/records/"""
    
    if request.method == 'GET':
        # Ваш существующий код из get_records()
        try:
            start_date = request.GET.get('from')
            end_date = request.GET.get('to')
            
            records = TimeRecord.objects.filter(user=request.user)
            
            if start_date:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                records = records.filter(created_at__date__gte=start.date())
            
            if end_date:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                records = records.filter(created_at__date__lte=end.date())
            
            records_data = [
                {
                    'id': r.id,
                    'activity': r.activity,
                    'description': r.description,
                    'duration': r.duration,  # ⚠️ ДОБАВЬТЕ duration!
                    'timestamp': r.created_at.isoformat()
                }
                for r in records
            ]
            
            return JsonResponse({'records': records_data})
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    elif request.method == 'POST':
        # Ваш существующий код из create_record()
        try:
            data = json.loads(request.body)
            
            record = TimeRecord.objects.create(
                user=request.user,
                activity=data['activity'],
                description=data.get('description', ''),
                duration=data.get('duration', 0),
            )
            return JsonResponse({
                'id': record.id,
                'activity': record.activity,
                'description': record.description,
                'duration': record.duration,  # ⚠️ ДОБАВЬТЕ duration в ответ!
                'timestamp': record.created_at.isoformat()
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Only GET and POST methods allowed'}, status=405)

@csrf_exempt
def login_view(request):
    """POST /api/login/ - Вход в систему"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = authenticate(username=data['login'], password=data['password'])
            if user:
                login(request, user)
                return JsonResponse({
                    'userId': user.id, 
                    'firstName': user.first_name,
                    'lastName': user.last_name,
                    'status': 'success'
                })
            return JsonResponse({'error': 'Неверные логин или пароль'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
@login_required
def logout_view(request):
    """POST /api/logout/ - Выход из системы"""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# 📝 Работа с моментами
@csrf_exempt
@login_required
def create_record(request):
    """POST /api/records/ - Создание момента"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Проверяем валидность activity
           # valid_activities = ['work', 'study', 'sport', 'rest', 'meal', 'sleep']
           # if data['activity'] not in valid_activities:
           #    return JsonResponse({'error': 'Invalid activity type'}, status=400)
            
            record = TimeRecord.objects.create(
                user=request.user,
                activity=data['activity'],
                description=data.get('description', ''),
                duration=data.get('duration', 0),
            )
            return JsonResponse({
                'id': record.id,
                'activity': record.activity,
                'description': record.description,
                'timestamp': record.created_at.isoformat()
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@login_required
def get_records(request):
    """GET /api/records/ - Получение моментов"""
    if request.method == 'GET':
        try:
            start_date = request.GET.get('from')
            end_date = request.GET.get('to')
            
            records = TimeRecord.objects.filter(user=request.user)
            
            if start_date:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                records = records.filter(created_at__date__gte=start.date())
            
            if end_date:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                records = records.filter(created_at__date__lte=end.date())
            
            records_data = [
                {
                    'id': r.id,
                    'activity': r.activity,
                    'description': r.description, 
                    'timestamp': r.created_at.isoformat()
                }
                for r in records
            ]
            
            return JsonResponse({'records': records_data})
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)

@csrf_exempt
@login_required
def delete_record(request, record_id):
    """DELETE /api/records/{id}/ - Удаление момента"""
    if request.method == 'DELETE':
        try:
            record = TimeRecord.objects.get(id=record_id, user=request.user)
            record.delete()
            return JsonResponse({'status': 'deleted', 'id': record_id})
        except TimeRecord.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
    return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)

@method_decorator(login_required, name='dispatch')

@login_required 
def get_stats(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)
    start_date = request.GET.get('from')
    end_date = request.GET.get('to')
    stats = {}
    records = TimeRecord.objects.filter(user=request.user)
    total_minutes = 0
    
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        records = records.filter(created_at__date__gte=start.date())
    
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
        records = records.filter(created_at__date__lte=end.date())
    
    for record in records:
        if record.activity not in stats:
            stats[record.activity] = 0
        stats[record.activity] += record.duration
        total_minutes += record.duration
    
    return JsonResponse({'stats': stats,
                         'total_minutes': total_minutes
    })

@csrf_exempt
@login_required
def record_list(request):
    """Обрабатывает GET (получение) и POST (создание) для /api/records/"""
    
    if request.method == 'GET':
        # Используем код из get_records
        try:
            start_date = request.GET.get('from')
            end_date = request.GET.get('to')
            
            records = TimeRecord.objects.filter(user=request.user)
            
            if start_date:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                records = records.filter(created_at__date__gte=start.date())
            
            if end_date:
                end = datetime.strptime(end_date, '%Y-%m-%d')
                records = records.filter(created_at__date__lte=end.date())
            
            records_data = [
                {
                    'id': r.id,
                    'activity': r.activity,
                    'description': r.description,
                    'duration': r.duration,
                    'timestamp': r.created_at.isoformat()
                }
                for r in records
            ]
            
            return JsonResponse({'records': records_data})
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    elif request.method == 'POST':
        # Используем код из create_record
        try:
            data = json.loads(request.body)
            
            record = TimeRecord.objects.create(
                user=request.user,
                activity=data['activity'],
                description=data.get('description', ''),
                duration=data.get('duration', 0),
            )
            return JsonResponse({
                'id': record.id,
                'activity': record.activity,
                'description': record.description,
                'duration': record.duration,
                'timestamp': record.created_at.isoformat()
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Only GET and POST methods allowed'}, status=405)