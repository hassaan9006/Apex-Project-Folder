from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Creates the data/ folder automatically if it doesn't exist
os.makedirs('data', exist_ok=True)


# ─────────────────────────────────────────
# STATIC ROUTES — just render the HTML page
# ─────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/trainers')
def trainers():
    return render_template('trainers.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')


# ─────────────────────────────────────────
# FUNCTIONAL ROUTES — handle form submissions
# ─────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    # GET = user visits the page, just show the form
    # POST = user submitted the form, save the data
    if request.method == 'POST':
        name  = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        age   = request.form['age']
        plan  = request.form['plan']
        # Save to CSV
        with open('data/members.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, phone, age, plan, datetime.now()])
        return redirect(url_for('thankyou'))
    return render_template('register.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name       = request.form['name']
        email      = request.form['email']
        class_type = request.form['class_type']
        date       = request.form['date']
        time       = request.form['time']
        with open('data/bookings.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, class_type, date, time, datetime.now()])
        return redirect(url_for('thankyou'))
    return render_template('booking.html')


@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    result   = None
    category = None
    if request.method == 'POST':
        weight = float(request.form['weight'])        # in kg
        height = float(request.form['height']) / 100  # convert cm to metres
        bmi_value = weight / (height ** 2)            # BMI formula
        result = round(bmi_value, 1)
        # Determine category
        if bmi_value < 18.5:
            category = "Underweight"
        elif bmi_value < 25:
            category = "Normal Weight"
        elif bmi_value < 30:
            category = "Overweight"
        else:
            category = "Obese"
    # Pass result and category back into the HTML page
    return render_template('bmi.html', result=result, category=category)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name    = request.form['name']
        email   = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        with open('data/feedback.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, subject, message, datetime.now()])
        return redirect(url_for('thankyou'))
    return render_template('contact.html')


@app.route('/transformation', methods=['GET', 'POST'])
def transformation():
    if request.method == 'POST':
        name     = request.form['name']
        duration = request.form['duration']
        story    = request.form['story']
        with open('data/transformations.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, duration, story, datetime.now()])
        return redirect(url_for('thankyou'))
    return render_template('transformation.html')


# ─────────────────────────────────────────
# SHARED
# ─────────────────────────────────────────

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
