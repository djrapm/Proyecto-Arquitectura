from memory_game.models import PlayerStats
from django.contrib.auth.models import User

# Evitar duplicados
username = 'testuser'
if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(username, 'test@example.com', '1234')
    stats = PlayerStats.objects.create(user=user)
    print(stats)
else:
    print(f"El usuario '{username}' ya existe.")

