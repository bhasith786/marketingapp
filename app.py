import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds_json = os.environ.get("GOOGLE_CREDS")  # Read from environment
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("submission_list").sheet1
# ---- HOME & SERVICE ROUTES ----
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/digital_marketing')
def digital_marketing():
    return render_template('digital_marketing.html')

@app.route('/seo')
def seo():
    return render_template('SEO.html')

@app.route('/ads')
def ads():
    return render_template('ADs.html')

@app.route('/traditional_marketing')
def traditional_marketing():
    return render_template('traditional_marketing.html')

@app.route('/socialmedia')
def socialmedia():
    return render_template('socialmedia.html')

@app.route('/seo')
def seo_page():
    return render_template('SEO.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# ---- FORM SUBMISSION ----
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()

    # Save data to Google Sheet
    sheet.append_row(list(data.values()))

    form_source = data.get('form_source')
    if form_source == 'index':
        return redirect(url_for('services'))
    else: 
        return redirect(url_for('thankyou'))
    
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
