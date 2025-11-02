import requests
import json

BASE_URL = "http://127.0.0.1:8000"
session = requests.Session()

print("🚀 Тестируем классовую вьюху...")

# 1. Вход
print("\n1. 🔐 Вход в систему:")
login_resp = session.post(f"{BASE_URL}/api/login/", json={
    "login": "testuser", 
    "password": "12345"
})
print("Вход:", login_resp.json())

# 2. Создаем момент с описанием
print("\n2. ⏰ Создание момента с описанием:")
record_resp = session.post(f"{BASE_URL}/api/records/", json={
    "activity": "study",
    "description": "Изучаем классовые вьюхи Django!"  # 🔹 ОПИСАНИЕ
})
print("Создан момент:", record_resp.json())

# 3. ТЕСТИРУЕМ КЛАССОВУЮ ВЬЮХУ (GET запрос)
print("\n3. 📊 Тестируем классовую вьюху (GET /api/records/):")
records_resp = session.get(f"{BASE_URL}/api/records/")  # 🔹 GET запрос
print("Все моменты:", records_resp.json())

print("\n✅ Тест классовой вьюхи завершен!")