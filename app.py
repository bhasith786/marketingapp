import json
import gspread
from flask import Flask, render_template, request, redirect, url_for, render_template_string
from oauth2client.service_account import ServiceAccountCredentials
import os
import traceback

app = Flask(__name__)

# ---- GOOGLE SHEETS SETUP ----
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from environment or local
creds_json = os.environ.get("GOOGLE_CREDS")
if creds_json:
    creds_dict = json.loads(creds_json)
else:
    with open("credentials.json", "r") as f:
        creds_dict = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet (must exist)
sheet = client.open("submission_list").sheet1

# ---- ROUTES ----
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/digital_marketing')
def digital_marketing():
    return render_template('digital_marketing.html')

@app.route('/traditional_marketing')
def traditional_marketing():
    return render_template('traditional_marketing.html')

@app.route('/socialmedia')
def socialmedia():
    return render_template('socialmedia.html')

@app.route('/seo')
def seo():
    return render_template('SEO.html')

@app.route('/ads')
def ads():
    return render_template('ADs.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')



# ---- SUBMIT FORM ----
@app.route('/submit', methods=['POST'])
def submit():
    try:
        service = request.form.get("services")
        form_source = request.form.get("form_source")
        # Get all selected platforms as a list
        platforms = request.form.getlist("platf")  

        # Convert list to comma-separated string
        platforms_str = ", ".join(platforms)


        print("Form data received:", request.form)
        print("Selected service:", service)
        print("Form source:", form_source)

        row = [
            request.form.get("name", ""),
            request.form.get("phone", ""),
            request.form.get("altphone", ""),
            request.form.get("company", ""),
            service,
            request.form.get("influencers", ""),
            request.form.get("location", ""),
            platforms_str,
            request.form.get("posters", ""),
            request.form.get("weekly", ""),
            request.form.get("others_desc", ""),
            request.form.get("platforms", ""),
            request.form.get("meta_ads", ""),
            request.form.get("google_ads", "")
        ]

        print("Row to append:", row)

        # Test appending safely
        try:
            sheet.append_row(row)
        except Exception as e:
            print("Google Sheets append error:", e)
            return f"Error appending to sheet: {e}"

        # Redirect logic
        if form_source == "index":
            return redirect(url_for("services"))
        else:
            if service == "digital_marketing":
                return redirect(url_for("digital_marketing"))
            elif service == "seo":
                return redirect(url_for("seo"))
            elif service == "ads":
                return redirect(url_for("ads"))
            else:
                return redirect(url_for("thankyou"))

    except Exception as e:
        print("ERROR WHILE SUBMITTING:", e)
        traceback.print_exc()
        return "An internal error occurred. Please check the console."

# ---- VIEW SUBMISSIONS ----
@app.route('/submissions')
def submissions():
    rows = sheet.get_all_values()
    if not rows:
        return "No submissions yet."

    header = rows[0]
    data_rows = rows[1:]

    html = "<h2>Submissions</h2><table border='1' cellpadding='6' style='border-collapse:collapse'>"
    html += "<tr>" + "".join(f"<th>{c}</th>" for c in header) + "</tr>"
    for r in data_rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in r) + "</tr>"
    html += "</table>"

    return render_template_string(html)
if __name__ == '__main__': 
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)
