from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import PredictionForm
from .models import HealthData
from .ml_service import predict_health_metrics
from nutrition.services import get_diet_plan, get_workout_plan
from django.utils import timezone


# To convert UTC datetime to Local datetime (in India)
def get_local_datetime(dt):
   local_time = timezone.localtime(dt.created_at)
   local_time = local_time.strftime("%d/%m/%Y %H:%M:%S %Z")    
   return local_time


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

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
            health_data.prediction_confidence = predictions['prediction_confidence']
            
            # Assign user and name
            health_data.user = request.user if request.user.is_authenticated else None
            health_data.name = "Guest" if not request.user.is_authenticated else (request.user.get_full_name() or request.user.username)
            
            health_data.save()
            
            # Save non-model inputs to session for rendering on result page
            request.session['food_preference'] = request.POST.get('food_preferences', 'Non-Vegetarian')
            request.session['daily_steps'] = request.POST.get('daily_steps', '8000')
            request.session['sleep_duration'] = request.POST.get('sleep_duration', '8')
            
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
    
    # Get values from session for UI items not in DB (or default them)
    diet_type = request.session.get('food_preference', 'choices')
    daily_steps = request.session.get('daily_steps', '1000')
    sleep_duration_val = request.session.get('sleep_duration', '8')
    
    # Format sleep hours
    sleep_hours_map = {
        '4': '< 5 hours',
        '6': '5-6 hours',
        '8': '7-8 hours',
        '9': '> 8 hours'
    }
    sleep_hours = sleep_hours_map.get(sleep_duration_val, '7-8 hours')

    # BMI Category
    bmi = data.bmi
    bmi_category = "Normal Weight"
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal Weight"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"

    # Meal Plan text
    breakfast = ", ".join(diet_plan.get('Breakfast', []))
    lunch = ", ".join(diet_plan.get('Lunch', []))
    dinner = ", ".join(diet_plan.get('Dinner', []))
    
    # Snacks recommendation based on goal
    if data.goal == 'Weight Loss':
        snacks = "Green Tea / Cucumber slices with Hummus"
    elif data.goal == 'Weight Gain':
        snacks = "Peanut Butter banana toast / Protein shake"
    else:
        snacks = "Mixed Nuts / Fruit Yogurt"

    # Recommended Foods (unique list of all foods in meals)
    recommended_foods = list(set(diet_plan.get('Breakfast', []) + diet_plan.get('Lunch', []) + diet_plan.get('Dinner', [])))
        
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
        'workout_plan': workout_plan,
        
        # New Context variables required by result.html template
        'bmi': bmi,
        'bmi_category': bmi_category,
        'calories': data.calories,
        'protein': data.protein,
        'carbs': data.carbs,
        'fat': data.fat,
        'water': water_intake,
        'diet_type': diet_type,
        'recommended_foods': recommended_foods,
        'breakfast': breakfast,
        'lunch': lunch,
        'snacks': snacks,
        'dinner': dinner,
        'daily_steps': daily_steps,
        'sleep_hours': sleep_hours,
        'prediction_confidence': data.prediction_confidence
    }
    return render(request, 'result.html', context)

def history_view(request):
    history = HealthData.objects.all().order_by('-created_at')
    
    return render(request, 'history.html', {'history': history})

def delete_prediction(request, pk):
    try:
        data = HealthData.objects.get(pk=pk)
        data.delete()
    except HealthData.DoesNotExist:
        pass
    return redirect('history')

def inputs_view(request, pk):
    try:
        data = HealthData.objects.get(pk=pk)
    except HealthData.DoesNotExist:
        return redirect('history')
    
    return render(request, 'inputs.html', {'data': data})

# Force reload

def api_predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Since ML service expects an object with attributes, we create a dummy object
            class DummyData:
                pass
            
            hd = DummyData()
            hd.age = data.get('age')
            hd.weight = data.get('weight')
            hd.height = data.get('height')
            hd.gender = data.get('sex', 'Male')
            
            # Map activity float multiplier to choice labels
            activity_val = data.get('activity', 1.55)
            try:
                activity_float = float(activity_val)
            except (ValueError, TypeError):
                activity_float = 1.55
                
            activity_map = {
                1.2: 'Sedentary',
                1.375: 'Lightly Active',
                1.55: 'Moderate',
                1.725: 'Very Active',
                1.9: 'Extra Active'
            }
            activity_level_str = activity_map.get(activity_float, 'Moderate')
            
            hd.activity_level = activity_level_str
            hd.goal = data.get('goal', 'Maintenance')
            
            predictions = predict_health_metrics(hd)
            
            bmi = predictions['bmi']
            bmi_category = "Normal Weight"
            if bmi < 18.5: bmi_category = "Underweight"
            elif bmi < 25: bmi_category = "Normal Weight"
            elif bmi < 30: bmi_category = "Overweight"
            else: bmi_category = "Obese"
            
            # Simple mock risks based on BMI
            risks = []
            if bmi >= 30:
                risks = [
                    {'label': 'Heart Disease', 'level': 'high'},
                    {'label': 'Diabetes Type II', 'level': 'high'},
                    {'label': 'Hypertension', 'level': 'high'}
                ]
            elif bmi >= 25:
                risks = [
                    {'label': 'Heart Disease', 'level': 'med'},
                    {'label': 'Diabetes Type II', 'level': 'med'},
                    {'label': 'Hypertension', 'level': 'med'}
                ]
            else:
                risks = [
                    {'label': 'Heart Disease', 'level': 'low'},
                    {'label': 'Diabetes Type II', 'level': 'low'},
                    {'label': 'Hypertension', 'level': 'low'}
                ]

            conditions = data.get('conditions', ['None'])
            medical_condition = 'None'
            if isinstance(conditions, list) and conditions:
                choices = ['Diabetes', 'Hypertension', 'PCOS', 'Thyroid']
                for c in conditions:
                    if c in choices:
                        medical_condition = c
                        break

            # Save prediction to DB
            real_hd = HealthData.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name="Guest" if not request.user.is_authenticated else request.user.username,
                age=data.get('age'),
                gender=data.get('sex', 'Male'),
                height=data.get('height'),
                weight=data.get('weight'),
                activity_level=activity_level_str,
                goal=data.get('goal', 'Maintenance'),
                medical_condition=medical_condition,
                bmi=bmi,
                calories=predictions['calories'],
                protein=predictions['protein'],
                carbs=predictions['carbs'],
                fat=predictions['fat'],
                disease_risk=predictions['disease_risk'],
                prediction_confidence=predictions['prediction_confidence'],
            )

            diet_plan = get_diet_plan(real_hd)
            
            meals = [
                {
                    "time": "Breakfast",
                    "name": ", ".join(diet_plan.get("Breakfast", [])),
                    "calories": round(real_hd.calories * 0.3)
                },
                {
                    "time": "Lunch",
                    "name": ", ".join(diet_plan.get("Lunch", [])),
                    "calories": round(real_hd.calories * 0.4)
                },
                {
                    "time": "Dinner",
                    "name": ", ".join(diet_plan.get("Dinner", [])),
                    "calories": real_hd.calories - round(real_hd.calories * 0.3) - round(real_hd.calories * 0.4)
                }
            ]
            
            insights = diet_plan.get("Tips", [])

            return JsonResponse({
                'success': True,
                'id': real_hd.id,
                'created_at': real_hd.created_at.strftime('%b %d, %Y %I:%M %p'),
                'goal': real_hd.goal,
                'age': real_hd.age,
                'model_name': 'Random Forest (v1.2)',
                'target_calories': real_hd.calories,
                'bmi': bmi,
                'model_accuracy': 94,
                'prediction_confidence': real_hd.prediction_confidence,
                'bmi_category': bmi_category,
                'obesity_prediction': real_hd.disease_risk,
                'protein_g': real_hd.protein,
                'protein_pct': data.get('protein_pct', 30),
                'carb_g': real_hd.carbs,
                'carb_pct': data.get('carb_pct', 50),
                'fat_g': real_hd.fat,
                'fat_pct': 100 - data.get('protein_pct', 30) - data.get('carb_pct', 50),
                'risks': risks,
                'meals': meals,
                'insights': insights
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def generate_weekly_meals(goal, target_calories):
    options = {
        'Weight Loss': {
            'Breakfast': [
                'Oats with Mixed Berries & Almonds',
                'Scrambled Egg Whites with Spinach',
                'Avocado toast on Whole Wheat',
                'Greek Yogurt with Chia Seeds',
                'Protein Shake with Banana',
                'Quinoa Porridge with Apple',
                'Boiled Eggs with Steamed Asparagus'
            ],
            'Lunch': [
                'Grilled Chicken Salad with Olive Oil',
                'Baked Salmon with Broccoli & Quinoa',
                'Tofu Stir-fry with Brown Rice',
                'Lentil Soup with Mixed Greens',
                'Turkey Wrap with Hummus',
                'Chickpea Salad with Lemon Dressing',
                'Grilled Cod with Sweet Potato'
            ],
            'Dinner': [
                'Steamed Veggies with Paneer',
                'Clear Chicken Soup with Cabbage',
                'Baked Chicken Breast with Zucchini',
                'Mushroom Stir-fry with Tofu',
                'Mixed Greens with Boiled Shrimp',
                'Vegetable Broth with Cottage Cheese',
                'Roasted Eggplant with Cauliflower Rice'
            ]
        },
        'Maintenance': {
            'Breakfast': [
                'Whole Wheat Toast with Peanut Butter',
                'Oatmeal with Honey & Dry Fruits',
                'Eggs Benedict with Spinach',
                'Muesli with Cold Milk & Apple',
                'Fruit Smoothie with Whey Protein',
                'Paneer bhurji with Multigrain Roti',
                'Avocado Egg Toast'
            ],
            'Lunch': [
                'Brown Rice with Dal & Mixed Veggies',
                'Chicken Curry with Rice & Cucumber Salad',
                'Fish Fillet with Roasted Potatoes',
                'Paneer Tikka Wrap with Mint Chutney',
                'Quinoa Salad with Feta & Olives',
                'Whole Wheat Pasta with Veggies',
                'Lentil Curry with Jeera Rice'
            ],
            'Dinner': [
                'Roti with Mixed Veg Curry & Curd',
                'Grilled Salmon with Quinoa & Peas',
                'Stir-fried Chicken with Vegetables',
                'Baked Tofu with Sautéed Spinach',
                'Minestrone Soup with Garlic Bread',
                'Egg Drop Soup with Mixed Veggies',
                'Stir-fry Noodles with Veggies & Shrimp'
            ]
        },
        'Weight Gain': {
            'Breakfast': [
                'Banana & Peanut Butter Shake',
                'Oats with Almonds, Raisins & Whole Milk',
                'Scrambled Eggs with Cheese & Avocado Toast',
                'Granola with Greek Yogurt & Honey',
                'Sweet Potato Pancakes with Maple Syrup',
                'Paneer Paratha with Butter & Curd',
                'Nut Butter Toast with Berries'
            ],
            'Lunch': [
                'Rice, Thick Dal, Chicken Breast & Potatoes',
                'Beef/Lamb Stew with Carrots & Potatoes',
                'Salmon Pasta with Creamy Sauce',
                'Chickpea Curry with Coconut Milk & Paratha',
                'Double Chicken Breast Wrap with Cheese',
                'Egg Curry with Ghee Rice',
                'Paneer Butter Masala with Butter Naan'
            ],
            'Dinner': [
                'Pasta with Olive Oil, Meatballs & Veggies',
                'Baked Fish with Avocado & Quinoa Pilaf',
                'Chicken Biryani with Raita',
                'Tofu & Vegetable Fried Rice with Cashews',
                'Steak with Mashed Potatoes & Butter Veggies',
                'Lentil Soup with Olive Oil & Wheat Roti',
                'Creamy Mushroom Risotto'
            ]
        }
    }
    
    goal_options = options.get(goal, options['Maintenance'])
    
    weekly_schedule = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    variations = [0, -80, 40, -120, 60, 120, -40]
    
    for i, day in enumerate(days):
        day_cals = max(1200, target_calories + variations[i])
        
        # Meal distribution: Breakfast 30%, Lunch 40%, Dinner 30%
        b_cals = round(day_cals * 0.3)
        l_cals = round(day_cals * 0.4)
        d_cals = day_cals - b_cals - l_cals
        
        weekly_schedule[day] = {
            "target_calories": day_cals,
            "meals": [
                {"time": "Breakfast", "name": goal_options['Breakfast'][i % len(goal_options['Breakfast'])], "calories": b_cals},
                {"time": "Lunch", "name": goal_options['Lunch'][i % len(goal_options['Lunch'])], "calories": l_cals},
                {"time": "Dinner", "name": goal_options['Dinner'][i % len(goal_options['Dinner'])], "calories": d_cals}
            ]
        }
        
    return weekly_schedule


def api_weekly_chart(request):
    if request.user.is_authenticated:
        latest_data = HealthData.objects.filter(user=request.user).order_by('-created_at').first()
    else:
        latest_data = HealthData.objects.filter(user__isnull=True).order_by('-created_at').first()
        
    if not latest_data:
        latest_data = HealthData.objects.order_by('-created_at').first()
        
    if not latest_data:
        return JsonResponse({
            'success': False,
            'error': 'No health metrics found. Please submit prediction first.'
        }, status=400)
        
    try:
        weekly_schedule = generate_weekly_meals(latest_data.goal, latest_data.calories)
        return JsonResponse({
            'success': True,
            'weekly_schedule': weekly_schedule
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_history_item_dict(item):
    bmi = item.bmi
    bmi_category = "Normal Weight"
    if bmi < 18.5: bmi_category = "Underweight"
    elif bmi < 25: bmi_category = "Normal Weight"
    elif bmi < 30: bmi_category = "Overweight"
    else: bmi_category = "Obese"
    
    # Risks based on BMI
    risks = []
    if bmi >= 30:
        risks = [
            {'label': 'Heart Disease', 'level': 'high'},
            {'label': 'Diabetes Type II', 'level': 'high'},
            {'label': 'Hypertension', 'level': 'high'}
        ]
    elif bmi >= 25:
        risks = [
            {'label': 'Heart Disease', 'level': 'med'},
            {'label': 'Diabetes Type II', 'level': 'med'},
            {'label': 'Hypertension', 'level': 'med'}
        ]
    else:
        risks = [
            {'label': 'Heart Disease', 'level': 'low'},
            {'label': 'Diabetes Type II', 'level': 'low'},
            {'label': 'Hypertension', 'level': 'low'}
        ]
        
    diet_plan = get_diet_plan(item)
    
    meals = [
        {
            "time": "Breakfast",
            "name": ", ".join(diet_plan.get("Breakfast", [])),
            "calories": round(item.calories * 0.3)
        },
        {
            "time": "Lunch",
            "name": ", ".join(diet_plan.get("Lunch", [])),
            "calories": round(item.calories * 0.4)
        },
        {
            "time": "Dinner",
            "name": ", ".join(diet_plan.get("Dinner", [])),
            "calories": item.calories - round(item.calories * 0.3) - round(item.calories * 0.4)
        }
    ]
    
    protein_cals = item.protein * 4
    carbs_cals = item.carbs * 4
    fat_cals = item.fat * 9
    total_cals = protein_cals + carbs_cals + fat_cals
    
    protein_pct = round((protein_cals / total_cals) * 100) if total_cals > 0 else 30
    carb_pct = round((carbs_cals / total_cals) * 100) if total_cals > 0 else 50
    fat_pct = 100 - protein_pct - carb_pct
    
    return {
        'id': item.id,
        'created_at': item.created_at.strftime('%b %d, %Y %I:%M %p'),
        'goal': item.goal,
        'age': item.age,
        'bmi': item.bmi,
        'target_calories': item.calories,
        'model_name': 'Random Forest (v1.2)',
        'model_accuracy': 94,
        'bmi_category': bmi_category,
        'obesity_prediction': item.disease_risk,
        'protein_g': item.protein,
        'protein_pct': protein_pct,
        'carb_g': item.carbs,
        'carb_pct': carb_pct,
        'fat_g': item.fat,
        'fat_pct': fat_pct,
        'risks': risks,
        'meals': meals,
        'insights': diet_plan.get('Tips', [])
    }


def api_history(request):
    try:
        if request.user.is_authenticated:
            history_qs = HealthData.objects.filter(user=request.user).order_by('-created_at')
        else:
            history_qs = HealthData.objects.all().order_by('-created_at')
            
        history_list = []
        for item in history_qs:
            history_list.append(get_history_item_dict(item))
            
        return JsonResponse({
            'success': True,
            'history': history_list
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def api_delete_history(request, pk):
    if request.method == 'POST':
        try:
            data = HealthData.objects.get(pk=pk)
            data.delete()
            return JsonResponse({'success': True})
        except HealthData.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)



