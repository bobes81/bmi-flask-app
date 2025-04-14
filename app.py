from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import codecs

app = Flask(__name__)

# Google Sheets setup
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# Získání proměnné jako string
creds_json = os.getenv("GOOGLE_CREDS_JSON")

# Odstraň uvozovky, pokud Heroku přidalo ""
if creds_json.startswith('"') and creds_json.endswith('"'):
    creds_json = creds_json[1:-1]

# Dekóduj escapované znaky (např. \n -> nový řádek)
creds_json = codecs.decode(creds_json, 'unicode_escape')

# Převeď na Python slovník
creds_dict = json.loads(creds_json)

# Autorizace Google Sheets API
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("bmi-results").sheet1


def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
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
        return "Muscle Building", "Combine strength training with high protein intake and proper rest."

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height_cm = float(request.form["height"])

            if weight <= 0 or height_cm <= 0:
                return render_template("index.html", error="Please enter positive values.")

            bmi = calculate_bmi(weight, height_cm)
            category, advice = get_bmi_category(bmi)

            sheet.append_row([weight, height_cm, bmi, category])

            return render_template("result.html", bmi=bmi, category=category, advice=advice)
        except ValueError:
            return render_template("index.html", error="Invalid input. Please enter numbers only.")

    return render_template("index.html")

# Přidání kódu pro nastavení portu na Renderu
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
