def calculate_calories(protein, fat, carbs):
    """Macro based calorie fomrula"""
    return (protein * 4) + (fat * 9) + (carbs * 4)

def main():
    # Példa ételek előre megadva
    daily_intake = [
        {"food": "Chicken breast (100g)", "protein": 23, "fat": 1.5, "carbs": 0, "calories": calculate_calories(23, 1.5, 0)},
        {"food": "Rice (100g)", "protein": 2.7, "fat": 0.3, "carbs": 28, "calories": calculate_calories(2.7, 0.3, 28)},
        {"food": "Egg (1 db)", "protein": 6, "fat": 5, "carbs": 0.6, "calories": calculate_calories(6, 5, 0.6)},
        {"food": "Apple (150g)", "protein": 0.5, "fat": 0.3, "carbs": 20, "calories": calculate_calories(0.5, 0.3, 20)}
    ]

    while True:
        food = input("Étel neve (vagy nyomj Entert a kilépéshez): ")
        if not food:
            break
        
        protein = float(input("Protein (g): "))
        fat = float(input("Fat (g): "))
        carbs = float(input("Carb (g): "))
        
        calories = calculate_calories(protein, fat, carbs)
        daily_intake.append({"food": food, "protein": protein, "fat": fat, "carbs": carbs, "calories": calories})
    
    # Összesítés
    total_protein = sum(item["protein"] for item in daily_intake)
    total_fat = sum(item["fat"] for item in daily_intake)
    total_carbs = sum(item["carbs"] for item in daily_intake)
    total_calories = sum(item["calories"] for item in daily_intake)

    print("\n Sum of daily intake :")
    print(f"Protein: {total_protein}g")
    print(f"Fat: {total_fat}g")
    print(f"Carb: {total_carbs}g")
    print(f"Calorie: {total_calories} kcal")

if __name__ == "__main__":
    main()
