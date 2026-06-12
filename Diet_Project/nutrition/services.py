def get_diet_plan(goal):
    """
    Returns a sample diet plan based on the user's goal.
    """
    plans = {
        'Weight Loss': {
            'Breakfast': ['Oats with Fruits', 'Boiled Egg', 'Green Tea'],
            'Lunch': ['Brown Rice', 'Grilled Chicken', 'Mixed Vegetables', 'Salad'],
            'Dinner': ['Vegetable Soup', 'Paneer / Tofu', 'Steamed Veggies'],
            'Tips': ['Drink 3-4 liters of water daily', 'Avoid junk food', 'Exercise for 30 mins daily', 'Sleep 7-8 hours daily']
        },
        'Maintenance': {
            'Breakfast': ['Whole Wheat Toast', 'Peanut Butter', 'Milk', 'Apple'],
            'Lunch': ['Rice/Roti', 'Dal', 'Chicken/Fish Curry', 'Salad'],
            'Dinner': ['Roti', 'Mixed Veg Curry', 'Curd'],
            'Tips': ['Drink 3-4 liters of water daily', 'Maintain physical activity', 'Limit processed sugar']
        },
        'Weight Gain': {
            'Breakfast': ['Banana Shake', 'Oats with Dry Fruits', 'Eggs/Paneer'],
            'Lunch': ['Rice & Dal', 'Chicken breast', 'Potato Salad', 'Curd'],
            'Dinner': ['Pasta/Rice', 'Meat/Tofu', 'Avocado', 'Mixed Veggies'],
            'Tips': ['Eat calorie dense foods', 'Include strength training', 'Have frequent meals', 'Drink 3-4 liters of water daily']
        }
    }
    
    return plans.get(goal, plans['Maintenance'])
