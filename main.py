from app import app

# Включаем режим разработки (аналог env FLASK_ENV=development)
app.env = 'development'
# Запускаем приложение (http-сервер)
# Будет доступно на http://localhost:8080
app.run(port=8080, host='localhost', debug=True)
