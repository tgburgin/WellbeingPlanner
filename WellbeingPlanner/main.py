# Imports
from calendar_functions.auth import get_or_create_calendar, initialize_calendar_service
from calendar_functions.tools import add_daily_activities, add_reminder, add_weekly_activities, clear_calendar_events
from config.settings import CARDIO_WORKOUTS, DAILY_ACTIVITIES, WEEKLY_ACTIVITIES

# Constants
cardio_workouts = CARDIO_WORKOUTS
daily_activities = DAILY_ACTIVITIES
weekly_activities = WEEKLY_ACTIVITIES


# Main script
def wellbeing_planner(start_date, end_date, fitness_test_choice=1, include_fitness_test=True):
    try:
        yield "Initializing calendar service..."
        calendar_service = initialize_calendar_service()

        yield "Getting or creating calendar..."
        calendar_id = get_or_create_calendar(calendar_service)

        yield f"Clearing calendar events from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}..."
        clear_calendar_events(calendar_service, calendar_id, start_date, end_date)

        yield "Adding daily activities..."
        add_daily_activities(calendar_service, calendar_id, start_date, end_date, DAILY_ACTIVITIES)

        yield "Adding weekly activities..."
        add_weekly_activities(calendar_service, calendar_id, start_date, end_date, WEEKLY_ACTIVITIES, CARDIO_WORKOUTS, fitness_test_choice, include_fitness_test)

        yield "Adding reminder for future planning..."
        add_reminder(calendar_service, calendar_id, end_date)

        yield "Wellbeing plan created successfully!"
    except Exception as e:
        yield f"Error: {str(e)}"
        print(f"Error during wellbeing planner execution: {e}")

if __name__ == "__main__":
    # Run the main script
    wellbeing_planner()