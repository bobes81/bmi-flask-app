import os
from dotenv import load_dotenv

load_dotenv()


import json
from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Setup Google Sheets API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON")

if not GOOGLE_CREDS_JSON:
    raise ValueError("Environment variable 'GOOGLE_CREDS_JSON' not set")

with open(GOOGLE_CREDS_JSON) as f:
    creds = json.load(f)

client = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_dict(creds, scope))
sheet = client.open("bmi-results").sheet1

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "Try to gain weight with a nutritious diet."
    elif 18.5 <= bmi < 25:
        return "Normal weight", "Maintain your current routine."
    elif 25 <= bmi < 30:
        return "Overweight", "Consider more activity and mindful eating."
    else:
        return "Obese", "Consult with a healthcare provider."

def save_to_sheets(bmi, category):
    try:
        sheet.append_row([str(bmi), category])
        return True
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height'])

            if weight < 30 or weight > 300 or height < 100 or height > 250:
                raise ValueError("Unrealistic input values")

            bmi = calculate_bmi(weight, height)
            category, advice = get_bmi_category(bmi)
            success = save_to_sheets(bmi, category)

            return render_template("result.html", bmi=bmi, category=category, advice=advice, success=success)

        except ValueError:
            return render_template("index.html", error="Please enter realistic height (100–250 cm) and weight (30–300 kg).")

    return render_template("index.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    print("Running in debug mode...")
    app.run(debug=True)
