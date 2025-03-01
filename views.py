from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
import os
import joblib
import numpy as np
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from tensorflow.keras.models import load_model
from PIL import Image
import pandas as pd
from django.conf import settings
from django.contrib.auth.models import User


# ✅ Home Page
def home(request):
    return render(request, "home.html")

# ✅ User Registration
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists."})

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "Email is already registered."})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect("login")

    return render(request, "register.html")

# ✅ User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("base")  # Redirect to base.html after login
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

# ✅ User Logout
def user_logout(request):
    logout(request)
    return redirect("home")  # Redirect to home after logout

# ✅ Base Page (After Login)
@login_required
def base_view(request):
    return render(request, "base.html")

# ✅ Other Protected Pages
@login_required
def pet_health(request):
    return render(request, "pet_health.html")

@login_required
def emergency(request):
    return render(request, "emergency.html")

@login_required
def ai_training(request):
    return render(request, "ai_training.html")

# ✅ Load trained symptom model
symptom_model = joblib.load(os.path.join(settings.BASE_DIR, "models/symptom_model.pkl"))
vectorizer = joblib.load(os.path.join(settings.BASE_DIR, "models/symptom_vectorizer.pkl"))
disease_info_dict = joblib.load(os.path.join(settings.BASE_DIR, "models/disease_info.pkl"))

# ✅ Load trained skin disease model
skin_model = load_model(os.path.join(settings.BASE_DIR, "models/skin_disease_model.h5"))

# ✅ AI Symptom Analysis API
@api_view(["POST"])
def analyze_symptoms(request):
    symptoms = request.data.get("symptoms", "").strip().lower()

    if not symptoms:
        return JsonResponse({"error": "No symptoms provided"}, status=400)

    symptoms_list = [s.strip() for s in symptoms.split(",")]
    symptoms_input = " ".join(symptoms_list)

    symptoms_vectorized = vectorizer.transform([symptoms_input])
    predicted_disease = symptom_model.predict(symptoms_vectorized)[0]

    disease_info = disease_info_dict.get(predicted_disease, {})

    if not disease_info:
        return JsonResponse({"error": "Disease information not found"}, status=404)

    ai_insights = {
        "Disease": predicted_disease,
        "Severity": disease_info["severity"],
        "Treatment": disease_info["treatment"],
        "Diagnosis": disease_info["diagnosis"],
    }

    return JsonResponse({"diagnosis": predicted_disease, "ai_insights": ai_insights})

# ✅ AI Skin Disease Detection API
@api_view(["POST"])
def analyze_skin(request):
    try:
        skin_image = request.FILES.get("skin_image")
        if not skin_image:
            print("❌ No skin image received!")
            return JsonResponse({"error": "No skin image provided"}, status=400)

        print(f"✅ Received file: {skin_image.name}")

        # Define uploads directory path
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)  # Ensure directory exists

        # Save file properly
        file_path = os.path.join(upload_dir, skin_image.name)
        with open(file_path, "wb+") as destination:
            for chunk in skin_image.chunks():
                destination.write(chunk)

        print(f"✅ Image saved at: {file_path}")

        # Load image and preprocess
        img = Image.open(file_path).convert("RGB").resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = img_array.reshape(1, 224, 224, 3)

        print("✅ Image processed successfully!")

        # Make prediction
        prediction = skin_model.predict(img_array)
        predicted_class = np.argmax(prediction)
        print(f"✅ Prediction Output: {prediction}, Class: {predicted_class}")

        # Mock disease labels and treatments
        disease_labels = ["Healthy", "Fungal Infection", "Mange", "Allergic Reaction"]
        treatments = {
            "Healthy": "No treatment required. Keep up regular pet care!",
            "Fungal Infection": "Apply antifungal cream and consult a vet.",
            "Mange": "Use medicated shampoo and visit a vet for prescription medication.",
            "Allergic Reaction": "Avoid allergens, give antihistamines, and seek veterinary advice."
        }

        predicted_disease = disease_labels[predicted_class] if predicted_class < len(disease_labels) else "Unknown"
        recommended_treatment = treatments.get(predicted_disease, "Consult a veterinarian for accurate diagnosis.")

        print(f"✅ Predicted Disease: {predicted_disease}, Treatment: {recommended_treatment}")

        return JsonResponse({
            "skin_disease": predicted_disease,
            "ai_insights": {"Treatment": recommended_treatment}
        })
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return JsonResponse({"error": f"Failed to analyze image: {str(e)}"}, status=500)
