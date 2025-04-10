def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "Increase healthy calories, try strength training with supervision."
    elif 18.5 <= bmi < 25:
        return "Normal weight", "Maintain your routine, mix cardio and bodyweight training."
    elif 25 <= bmi < 30:
        return "Overweight", "Focus on cardio and a balanced diet, aim for consistency."
    elif 30 <= bmi < 35:
        return "Obese", "Prioritize low-impact cardio and consult a healthcare provider."
    else:
        return "Muscle Building", "Monitor body composition; combine weight training with rest and high protein intake."

def main():
    print("Welcome to the Fitness BMI Calculator! 💪\n")
    
    try:
        weight = float(input("Enter your weight in kg: "))
        height = float(input("Enter your height in meters: "))
        
        if weight <= 0 or height <= 0:
            print("Please enter positive values.")
            return
        
        bmi = calculate_bmi(weight, height)
        category, advice = get_bmi_category(bmi)
        
        print(f"\nYour BMI is: {bmi}")
        print(f"Category: {category}")
        print(f"Advice: {advice}")
        
    except ValueError:
        print("Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    main()
