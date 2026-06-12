from django.shortcuts import render, redirect
from .forms import PredictionForm
from .models import HealthData
from .ml_service import predict_health_metrics
from nutrition.services import get_diet_plan

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
        
    diet_plan = get_diet_plan(data.goal)
    water_intake = round(data.weight * 0.033, 1) # ~33ml per kg of body weight
        
    context = {
        'data': data,
        'diet_plan': diet_plan,
        'water_intake': water_intake
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
