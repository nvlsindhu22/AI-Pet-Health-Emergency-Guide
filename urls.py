from django.urls import path
from .views import home, register, user_login, user_logout, base_view, pet_health, emergency, ai_training, analyze_symptoms, analyze_skin

urlpatterns = [
    path("", home, name="home"),  
    path("register/", register, name="register"),  
    path("login/", user_login, name="login"),  
    path("logout/", user_logout, name="logout"),  
    path("base/", base_view, name="base"),  
    path("pet-health/", pet_health, name="pet_health"),
    path("emergency/", emergency, name="emergency"),
    path("ai-training/", ai_training, name="ai_training"),
    path("api/pets/analyze_symptoms/", analyze_symptoms, name="analyze_symptoms"),
    path("api/pets/analyze_skin/", analyze_skin, name="analyze_skin"),
]
