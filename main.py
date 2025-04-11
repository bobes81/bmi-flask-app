import gspread
from oauth2client.service_account import ServiceAccountCredentials

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100  # převod cm → metry
    bmi = weight / (height_m ** 2)
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

def save_to_google_sheets(weight, height_cm, bmi, category):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open("bmi-results").sheet1
        sheet.append_row([weight, height_cm, bmi, category])
    except Exception as e:
        print(f"⚠️ Failed to save to Google Sheets: {e}")

def main():
    print("Welcome to the Fitness BMI Calculator! 💪\n")
    
    try:
        weight = float(input("Enter your weight in kg: "))
        height_cm = float(input("Enter your height in centimeters: "))
        
        if weight <= 0 or height_cm <= 0:
            print("Please enter positive values.")
            return
        
        bmi = calculate_bmi(weight, height_cm)
        category, advice = get_bmi_category(bmi)
        
        print(f"\nYour BMI is: {bmi}")
        print(f"Category: {category}")
        print(f"Advice: {advice}")

        # Save to Google Sheet
        save_to_google_sheets(weight, height_cm, bmi, category)

    except ValueError:
        print("Invalid input. Please enter numbers only.")

if __name__ == "__main__":
    main()
