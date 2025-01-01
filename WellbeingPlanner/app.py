from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
from datetime import datetime
from main import wellbeing_planner
from calendar_functions.tools import get_fitness_test_choices

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Save settings to the session
        session['fitness_test_choice'] = int(request.form.get('fitness_test_choice', 1))
        session['dark_mode'] = 'dark_mode' in request.form
        return redirect(url_for('index'))
    
    # Retrieve current settings or defaults
    fitness_test_choice = session.get('fitness_test_choice', 1)
    dark_mode = session.get('dark_mode', False)
    fitness_tests = get_fitness_test_choices()
    
    return render_template(
        'settings.html',
        fitness_tests=fitness_tests,
        fitness_test_choice=fitness_test_choice,
        dark_mode=dark_mode
    )

@app.route('/progress')
def progress():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return Response("data: Invalid date format\n\n", mimetype='text/event-stream')

    def generate():
        try:
            yield "data: Starting wellbeing plan creation...\n\n"
            for message in wellbeing_planner(start_date, end_date):
                yield f"data: {message}\n\n"
            yield "data: Wellbeing plan creation complete!\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
