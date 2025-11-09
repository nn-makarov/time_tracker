import requests

BASE_URL = "http://localhost:8000/api"


def test_fixed():
    print("🎯 Тестирование после исправления...")

    session = requests.Session()

    # Логин
    login_data = {"login": "finaluser", "password": "finalpass123"}
    response = session.post(f"{BASE_URL}/login/", json=login_data)
    print(f"🔑 Логин: {response.status_code}")

    if response.status_code == 200:
        # Создание записи
        record_data = {
            "activity": "work",
            "duration": 120,
            "description": "Тест после исправления"
        }
        response = session.post(f"{BASE_URL}/records/", json=record_data)
        print(f"📝 Создание записи: {response.status_code}")
        if response.status_code == 201:
            print(f"✅ Успех! ID: {response.json().get('id')}")

        # Получение записей
        response = session.get(f"{BASE_URL}/records/")
        print(f"📊 Получение записей: {response.status_code}")
        if response.status_code == 200:
            records = response.json().get('records', [])
            print(f"✅ Записей: {len(records)}")


test_fixed()
