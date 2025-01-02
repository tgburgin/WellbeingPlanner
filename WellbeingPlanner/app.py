from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response
from datetime import datetime
from main import wellbeing_planner
from calendar_functions.tools import clear_calendar_events, get_fitness_test_choices
from calendar_functions.auth import initialize_calendar_service, get_or_create_calendar

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    calendar_service = initialize_calendar_service()
    calendar_id = get_or_create_calendar(calendar_service)

    if request.method == 'POST':
        session['fitness_test_choice'] = int(request.form.get('fitness_test_choice', 1))
        session['dark_mode'] = 'dark_mode' in request.form
        session['calendar_color'] = request.form.get('calendar_color', '1')

        print(f"Updating calendar color to {session['calendar_color']}")

        calendar_list_entry = calendar_service.calendarList().get(calendarId=calendar_id).execute()
        calendar_list_entry['colorId'] = session['calendar_color']
        calendar_service.calendarList().update(calendarId=calendar_list_entry['id'], body=calendar_list_entry).execute()
                
        return redirect(url_for('index'))

    fitness_test_choice = session.get('fitness_test_choice', 1)
    dark_mode = session.get('dark_mode', False)

    calendar = calendar_service.calendars().get(calendarId=calendar_id).execute()
    current_color = calendar.get('colorId', '1')

    colors = calendar_service.colors().get().execute()
    calendar_colors = {
        color_id: {
            "background": color_info["background"],
            "foreground": color_info["foreground"],
            "name": color_info.get("description", f"Color {color_id}")
        }
        for color_id, color_info in colors.get('calendar', {}).items()
    }

    return render_template(
        'settings.html',
        fitness_tests=get_fitness_test_choices(),
        fitness_test_choice=fitness_test_choice,
        dark_mode=dark_mode,
        calendar_color=current_color,
        calendar_colors=calendar_colors
    )


@app.route('/progress')
def progress():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    clear_old = request.args.get('clear_old') == 'true'

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        current_date = datetime.now()
    except ValueError:
        return Response("data: Invalid date format\n\n", mimetype='text/event-stream')

    def generate():
        try:
            if clear_old:
                calendar_service = initialize_calendar_service()
                calendar_id = get_or_create_calendar(calendar_service)
                yield "data: Clearing old events...\n\n"
                clear_calendar_events(calendar_service, calendar_id, datetime.min, current_date)

            yield "data: Starting wellbeing plan creation...\n\n"
            for message in wellbeing_planner(start_date, end_date):
                yield f"data: {message}\n\n"
            yield "data: Wellbeing plan creation complete!\n\n"
        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
