from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

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
    return render_template('seo.html')

@app.route('/ads')
def ads():
    return render_template('ads.html')

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
    # Use flat=False to capture multiple checkbox values as a list
    data = request.form.to_dict(flat=False)

    # Convert checkbox list to comma-separated string for CSV
    if 'location' in data:
        if isinstance(data['location'], list):
            data['location'] = ', '.join(data['location'])

    file_exists = os.path.isfile('submissions.csv')
    with open('submissions.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    form_source = data.get('form_source', ['index'])[0]

    if form_source == 'index':
        return redirect(url_for('services'))
    elif form_source in ['traditional_marketing', 'socialmedia','seo']:
        return redirect(url_for('thankyou'))
    else:
        return redirect(url_for('thankyou'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
