from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Card(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='memory_game/cards/', default='cards/gohan.png')
    is_matched = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PlayerStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    average_time = models.FloatField(default=0.0)
    most_played_level = models.CharField(max_length=50, default='Básico')

    def __str__(self):
        return f"Stats: {self.user.username}"


class GameSession(models.Model):
    LEVEL_CHOICES = (
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    score = models.IntegerField(default=0)
    attempts_remaining = models.IntegerField(default=0)
    pairs_found = models.IntegerField(default=0)
    duration_seconds = models.FloatField(default=0.0)
    win = models.BooleanField(default=False)
    date_played = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_played']

    def __str__(self):
        return f"{self.user.username} - {self.level} - {self.date_played:%Y-%m-%d %H:%M}"


# -----------------------------
# Señal única para crear stats
# -----------------------------
@receiver(post_save, sender=User)
def create_or_update_player_stats(sender, instance, created, **kwargs):
    if created:
        PlayerStats.objects.create(user=instance)
    else:
        PlayerStats.objects.get_or_create(user=instance)

    
    
