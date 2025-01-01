from flask import Flask, render_template, request, jsonify, Response
from datetime import datetime
from main import wellbeing_planner

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    start_date_str = request.form.get('start_date')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date_str = request.form.get('end_date')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    try:
        if not start_date or not end_date:
            raise ValueError("Start date and end date are required.")
        if end_date < start_date:
            raise ValueError("End date must be on or after start date.")
        if start_date.date() < datetime.now().date():
            raise ValueError("Start date must be today or in the future.")

        return jsonify({'message': 'Starting plan creation...', 'type': 'success'})
    except Exception as e:
        return jsonify({'message': str(e), 'type': 'danger'}), 400

@app.route('/progress')
def progress():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except (TypeError, ValueError):
        return Response("data: Invalid date format\n\n", mimetype='text/event-stream')

    def generate():
        try:
            for message in wellbeing_planner(start_date, end_date):
                yield f"data: {message}\n\n"
            yield "data: Wellness plan creation complete!\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
