from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
import json

from .models import PlayerStats, GameSession

# -------------------------
# VISTAS DE AUTENTICACION
# -------------------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"¡Bienvenido {username}!")
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'memory_game/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Cuenta creada con éxito. Inicia sesión ahora.")
            return redirect('login')

    return render(request, 'memory_game/register.html')


@login_required
def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # limpia mensajes anteriores
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')


# -------------------------
# VISTAS PRINCIPALES
# -------------------------

@login_required
def home_view(request):
    return render(request, 'memory_game/home.html')


@login_required
def select_level(request):
    if request.method == 'POST':
        level = request.POST.get('level')
        return redirect('game_board', level=level)
    return render(request, 'memory_game/select_level.html')


@login_required
def game_board(request, level):
    grid_size = 4
    attempts_by_level = {'facil': 20, 'medio': 15, 'dificil': 10}
    attempts = attempts_by_level.get(level, 15)

    image_paths = [
        'memory_game/images/gokusayan.png',
        'memory_game/images/majinvegeta.png',
        'memory_game/images/bulma.png',
        'memory_game/images/piccolo.png',
        'memory_game/images/krilin.png',
        'memory_game/images/majinbu.png',
        'memory_game/images/gohan.png',
        'memory_game/images/kaio.png',
    ]

    num_pairs = 8
    selected_images = random.sample(image_paths, num_pairs)
    cards_data = selected_images * 2
    random.shuffle(cards_data)

    cards = [
        {'id': i, 'name': f'Card {i}', 'image': {'url': static(img_path)}}
        for i, img_path in enumerate(cards_data)
    ]

    return render(request, 'memory_game/game_board.html', {
        'level': level,
        'grid_size': grid_size,
        'attempts': attempts,
        'cards': cards,
    })


# -------------------------
# VISTA DE ESTADISTICAS
# -------------------------

@login_required
def stats_view(request):
    user = request.user
    pstats, _ = PlayerStats.objects.get_or_create(user=user)
    recent_games = GameSession.objects.filter(user=user).order_by('-date_played')[:20]

    context = {
        'player': user,
        'pstats': pstats,
        'recent_games': recent_games,
    }
    return render(request, 'memory_game/stats.html', context)


# -------------------------
# API PARA GUARDAR ESTADISTICAS
# -------------------------

@login_required
@csrf_exempt
def save_stats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        level = data.get('level')
        score = data.get('score', 0)
        attempts_left = data.get('attempts', 0)
        pairs_found = data.get('pairs', 0)
        duration = data.get('duration', 0)  
        win = data.get('win', False)        

        # Crear registro de partida en GameSession
        GameSession.objects.create(
            user=request.user,
            level=level,
            score=score,
            attempts_remaining=attempts_left,
            pairs_found=pairs_found,
            duration_seconds=duration,  
            win=win                     
        )

        # Actualizar estadisticas acumuladas del jugador
        stats, _ = PlayerStats.objects.get_or_create(user=request.user)

        stats.games_played += 1
        if win:
            stats.wins += 1
        else:
            stats.losses += 1

        # Actualizar promedio de tiempo
        stats.average_time = ((stats.average_time * (stats.games_played - 1)) + duration) / stats.games_played

        # Actualizar nivel mas jugado
        stats.most_played_level = level

        stats.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'})




