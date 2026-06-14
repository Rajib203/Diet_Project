def get_diet_plan(health_data):
    """
    Returns a personalized diet plan based on the user's ML predictions and goal.
    """
    goal = health_data.goal
    risk = health_data.disease_risk
    
    # Base plans
    plans = {
        'Weight Loss': {
            'Breakfast': ['Oats with Fruits', 'Boiled Egg', 'Green Tea'],
            'Lunch': ['Brown Rice', 'Grilled Chicken', 'Mixed Vegetables', 'Salad'],
            'Dinner': ['Vegetable Soup', 'Paneer / Tofu', 'Steamed Veggies'],
            'Tips': [
                'Maintain a caloric deficit',
                'Prioritize high-protein meals',
                'Avoid processed sugar entirely',
                'Drink at least 3-4 liters of water'
            ]
        },
        'Maintenance': {
            'Breakfast': ['Whole Wheat Toast', 'Peanut Butter', 'Milk', 'Apple'],
            'Lunch': ['Rice/Roti', 'Dal', 'Chicken/Fish Curry', 'Salad'],
            'Dinner': ['Roti', 'Mixed Veg Curry', 'Curd'],
            'Tips': [
                'Keep macros balanced daily',
                'Maintain consistent meal timings',
                'Limit processed foods',
                'Stay adequately hydrated'
            ]
        },
        'Weight Gain': {
            'Breakfast': ['Banana Shake', 'Oats with Dry Fruits', 'Eggs/Paneer'],
            'Lunch': ['Rice & Dal', 'Chicken breast', 'Potato Salad', 'Curd'],
            'Dinner': ['Pasta/Rice', 'Meat/Tofu', 'Avocado', 'Mixed Veggies'],
            'Tips': [
                'Focus on calorie-dense whole foods',
                'Eat 5-6 smaller meals per day',
                'Increase healthy fats (nuts, avocados)',
                'Consume protein before bed'
            ]
        }
    }
    
    plan = plans.get(goal, plans['Maintenance'])
    
    # Adjust tips and meals dynamically based on disease_risk (ML output)
    if risk in ["Obesity Type I", "Obesity Type II", "Obesity Type III"]:
        plan['Tips'] = [
            'Consult a healthcare provider before starting intense diets',
            'Focus on low-impact, sustainable caloric deficits',
            'Completely eliminate sugary drinks and snacks',
            'Increase dietary fiber to improve satiety'
        ]
        plan['Dinner'] = ['Clear Soup', 'Grilled Veggies', 'Lean Protein Portion']
    elif risk in ["Overweight Level I", "Overweight Level II"]:
        plan['Tips'].insert(0, 'Replace simple carbs with complex carbs (e.g. quinoa, oats)')
        plan['Tips'].append('Implement intermittent fasting (14:10) if comfortable')
    elif risk == "Insufficient Weight":
        plan['Tips'].insert(0, 'Incorporate liquid calories (shakes/smoothies) to boost intake')
        plan['Tips'].append('Ensure a surplus of at least 300-500 kcal daily')
        
    return plan

def get_workout_plan(health_data):
    """
    Returns a personalized workout plan durations (in minutes) based on ML predictions.
    """
    risk = health_data.disease_risk
    goal = health_data.goal
    
    # Default baseline
    workout_plan = {
        'brisk_walking': 30,
        'cardio': 20,
        'strength': 30,
        'stretching': 10,
        'meditation': 10
    }
    
    if risk in ["Obesity Type II", "Obesity Type III"]:
        # High impact cardio is bad for joints here
        workout_plan['brisk_walking'] = 45
        workout_plan['cardio'] = 0
        workout_plan['strength'] = 20
        workout_plan['stretching'] = 20
        workout_plan['meditation'] = 15
    elif risk in ["Obesity Type I", "Overweight Level II", "Overweight Level I"]:
        workout_plan['brisk_walking'] = 40
        workout_plan['cardio'] = 20
        workout_plan['strength'] = 30
        workout_plan['stretching'] = 15
    elif risk == "Insufficient Weight" or goal == 'Weight Gain':
        workout_plan['brisk_walking'] = 15
        workout_plan['cardio'] = 10
        workout_plan['strength'] = 45
        workout_plan['stretching'] = 10
    else: # Normal
        if goal == 'Weight Loss':
            workout_plan['cardio'] += 15
            workout_plan['brisk_walking'] += 15
        elif goal == 'Weight Gain':
            workout_plan['strength'] += 15
            workout_plan['cardio'] = 10
            
    return workout_plan
