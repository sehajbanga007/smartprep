from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.HealthView.as_view()),
    path("topics/", views.TopicsView.as_view()),
    path("practice-sets/", views.PracticeSetCreateView.as_view()),
    path("practice-sets/<str:attempt_id>/", views.PracticeSetDetailView.as_view()),
    path("practice-sets/<str:attempt_id>/submit/", views.SubmitView.as_view()),
    path("results/<str:attempt_id>/", views.ResultView.as_view()),
    path("leaderboard/", views.LeaderboardView.as_view()),
    path("stats/", views.StatsView.as_view()),
    path("external-trivia/", views.ExternalTriviaView.as_view()),
]
