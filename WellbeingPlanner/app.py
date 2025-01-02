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
    include_fitness_test = True  # Default value
    fitness_test_choice = 1  # Default value
    dark_mode = False  # Default value
    current_color = '1'  # Default calendar color

    try:
        calendar_service = initialize_calendar_service()
        calendar_id = get_or_create_calendar(calendar_service)
        calendar_list_entry = calendar_service.calendarList().get(calendarId=calendar_id).execute()

        if request.method == 'POST':
            session['include_fitness_test'] = 'include_fitness_test' in request.form
            session['fitness_test_choice'] = int(request.form.get('fitness_test_choice', 1))
            session['dark_mode'] = 'dark_mode' in request.form
            session['calendar_color'] = request.form.get('calendar_color', '1')

            if calendar_list_entry.get('colorId') != session['calendar_color']:
                calendar_list_entry['colorId'] = session['calendar_color']
                calendar_service.calendarList().update(calendarId=calendar_list_entry['id'], body=calendar_list_entry).execute()

            return redirect(url_for('index'))

        # Update session variables only if the above logic succeeds
        include_fitness_test = session.get('include_fitness_test', True)
        fitness_test_choice = session.get('fitness_test_choice', 1)
        dark_mode = session.get('dark_mode', False)
        current_color = calendar_list_entry.get('colorId', '1')

        colors = calendar_service.colors().get().execute()
        calendar_colors = {
            color_id: {
                "background": color_info["background"],
                "foreground": color_info["foreground"],
                "name": color_info.get("description", f"Color {color_id}")
            }
            for color_id, color_info in colors.get('calendar', {}).items()
        }

    except Exception as e:
        print(f"Error during settings page rendering: {e}")  # Log the error for debugging
        return render_template(
            'error.html',
            error_message=str(e)
        )

    return render_template(
        'settings.html',
        include_fitness_test=include_fitness_test,
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

    fitness_test_choice = session.get('fitness_test_choice', 1)
    include_fitness_test = session.get('include_fitness_test', True)

    def generate():
        try:
            if clear_old:
                calendar_service = initialize_calendar_service()
                calendar_id = get_or_create_calendar(calendar_service)
                yield "data: Clearing old events...\n\n"
                clear_calendar_events(calendar_service, calendar_id, datetime.min, current_date)

            yield "data: Starting wellbeing plan creation...\n\n"
            for message in wellbeing_planner(start_date, end_date, fitness_test_choice, include_fitness_test):
                yield f"data: {message}\n\n"
            yield "data: Wellbeing plan creation complete!\n\n"
        except Exception as e:
            print(f"Error during settings page rendering: {e}")  # Log the error for debugging
            return render_template(
                'error.html',
                error_message=str(e)
        )

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
