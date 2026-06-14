from django.shortcuts import render, redirect
from .forms import PredictionForm
from .models import HealthData
from .ml_service import predict_health_metrics
from nutrition.services import get_diet_plan, get_workout_plan

def home(request):
    return render(request, 'home.html')

def prediction_view(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            health_data = form.save(commit=False)
            
            # Get predictions
            predictions = predict_health_metrics(health_data)
            
            # Save predictions to model
            health_data.bmi = predictions['bmi']
            health_data.calories = predictions['calories']
            health_data.protein = predictions['protein']
            health_data.carbs = predictions['carbs']
            health_data.fat = predictions['fat']
            health_data.disease_risk = predictions['disease_risk']
            health_data.save()
            
            # Redirect to result page with ID
            return redirect('result', pk=health_data.pk)
        else:
            print("Form errors:", form.errors)
    else:
        form = PredictionForm()
    
    return render(request, 'prediction.html', {'form': form})

def result_view(request, pk):
    try:
        data = HealthData.objects.get(pk=pk)
    except HealthData.DoesNotExist:
        return redirect('prediction')
        
    diet_plan = get_diet_plan(data)
    water_intake = round(data.weight * 0.033, 1) # ~33ml per kg of body weight
    
    # Calculate percentages
    protein_cals = data.protein * 4
    carbs_cals = data.carbs * 4
    fat_cals = data.fat * 9
    total_cals = protein_cals + carbs_cals + fat_cals
    
    protein_pct = round((protein_cals / total_cals) * 100) if total_cals > 0 else 0
    carbs_pct = round((carbs_cals / total_cals) * 100) if total_cals > 0 else 0
    fat_pct = round((fat_cals / total_cals) * 100) if total_cals > 0 else 0
    
    # Ideal Weight Range (BMI 18.5 - 24.9)
    height_m = data.height / 100 if data.height > 3 else data.height
    min_weight = round(18.5 * (height_m ** 2), 1)
    max_weight = round(24.9 * (height_m ** 2), 1)
    ideal_weight_range = f"{min_weight} - {max_weight}"
    healthy_weight_goal = round((min_weight + max_weight) / 2, 1)
    
    # Health Status
    if data.disease_risk in ["Obesity Type I", "Obesity Type II", "Obesity Type III"]:
        health_status = "High Risk"
        health_status_color = "danger"
    elif data.disease_risk in ["Overweight Level I", "Overweight Level II", "Insufficient Weight"]:
        health_status = "Needs Attention"
        health_status_color = "warning"
    else:
        health_status = "Healthy"
        health_status_color = "success"
        
    # Workout Plan
    workout_plan = get_workout_plan(data)
        
    context = {
        'data': data,
        'diet_plan': diet_plan,
        'water_intake': water_intake,
        'protein_pct': protein_pct,
        'carbs_pct': carbs_pct,
        'fat_pct': fat_pct,
        'ideal_weight_range': ideal_weight_range,
        'healthy_weight_goal': healthy_weight_goal,
        'health_status': health_status,
        'health_status_color': health_status_color,
        'workout_plan': workout_plan
    }
    return render(request, 'result.html', context)

def dashboard_view(request):
    history = HealthData.objects.all().order_by('-created_at')
    
    return render(request, 'dashboard.html', {'history': history})

def delete_prediction(request, pk):
    try:
        data = HealthData.objects.get(pk=pk)
        data.delete()
    except HealthData.DoesNotExist:
        pass
    return redirect('dashboard')

def inputs_view(request, pk):
    try:
        data = HealthData.objects.get(pk=pk)
    except HealthData.DoesNotExist:
        return redirect('dashboard')
    
    return render(request, 'inputs.html', {'data': data})

# Force reload
