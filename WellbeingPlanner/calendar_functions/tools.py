from calendar import monthrange
from datetime import datetime, timedelta
import random

# Helper functions
def clear_calendar_events(calendar_service, calendar_id, start_date, end_date):
    # Clear all events from the start of the first day to the end of the last day
    time_max = (end_date + timedelta(days=1) - timedelta(seconds=1)).isoformat() + "Z"
    events = calendar_service.events().list(
        calendarId=calendar_id,
        timeMin=start_date.isoformat() + "Z",
        timeMax=time_max,
        singleEvents=True
    ).execute()
    for event in events.get('items', []):
        calendar_service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
        
    print(f"Cleared all calendar events from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.")

def add_daily_activities(calendar_service, calendar_id, start_date, end_date, daily_activities):
    # Add daily activities for each day in the date range
    for activity in daily_activities:
        for day_offset in range((end_date - start_date).days + 1):
            event_date = start_date + timedelta(days=day_offset)
            event_time = datetime.combine(event_date, datetime.strptime(activity['time'], "%H:%M").time())
            event = {
                'summary': activity['name'],
                'description': activity['details'],
                'start': {
                    'dateTime': event_time.isoformat(),
                    'timeZone': 'Europe/London',
                },
                'end': {
                    'dateTime': (event_time + timedelta(minutes=activity['duration'])).isoformat(),
                    'timeZone': 'Europe/London',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 0}
                    ]
                }
            }
            # Add the event to the calendar if it doesn't end in the past
            if datetime.fromisoformat(event['end']['dateTime']) >= datetime.now():
                calendar_service.events().insert(calendarId=calendar_id, body=event).execute()
    print("Added daily activities successfully!")

def get_fitness_test_choices():
    # Return the fitness test choices as a list
    return [
        {"id": 1, "name": "1-Mile Run", "details": "Run or walk 1 mile as fast as you can."},
        {"id": 2, "name": "5K Run", "details": "Run or walk 5 kilometers as fast as you can."},
        {"id": 3, "name": "10K Run", "details": "Run or walk 10 kilometers as fast as you can."}
    ]

def add_weekly_activities(calendar_service, calendar_id, start_date, end_date, weekly_activities, cardio_workouts, enabled_types, enabled_workouts, fitness_test_choice=None, include_fitness_test=True):
    fitness_test_choice = fitness_test_choice or 1  # Default to 1-Mile Run if not set
    fitness_test = None

    if not include_fitness_test:
        fitness_test_choice = 4  # Corresponds to "None" in fitness tests

    # Map fitness test choice to its details
    if fitness_test_choice == 1:
        fitness_test = {
            "name": "Baseline Cardio Fitness Test: 1-Mile Run",
            "time": "09:30",
            "duration": 20,
            "details": "Run or walk 1 mile as fast as you can."
        }
    elif fitness_test_choice == 2:
        fitness_test = {
            "name": "Baseline Cardio Fitness Test: 5K Run",
            "time": "09:30",
            "duration": 30,
            "details": "Run or walk 5 kilometers as fast as you can."
        }
    elif fitness_test_choice == 3:
        fitness_test = {
            "name": "Baseline Cardio Fitness Test: 10K Run",
            "time": "09:30",
            "duration": 60,
            "details": "Run or walk 10 kilometers as fast as you can."
        }

    filtered_cardio_workouts = [
            {
                "type": category["type"],
                "workouts": [
                    workout for workout in category["workouts"] if workout["name"] in enabled_workouts
                ]
            }
            for category in cardio_workouts if category["type"] in enabled_types
        ]

    first_monday_offset = (7 - start_date.weekday()) % 7
    first_monday = start_date + timedelta(days=first_monday_offset)

    for activity in weekly_activities:
        event_date = start_date + timedelta(days=(activity['day'] - start_date.weekday()) % 7)
        while event_date <= end_date:
            # Skip events in the past
            if event_date < datetime.now():
                event_date += timedelta(weeks=1)
                continue

            if activity['name'].startswith("Cardio") and filtered_cardio_workouts:
                # Choose a random workout
                workout_category = random.choice(filtered_cardio_workouts)
                workout = random.choice(workout_category['workouts'])
                activity_name = f"{activity['name']}: {workout['name']} ({workout_category['type']})"
                activity_description = f"{workout['details']}\n{activity['details']}"
                activity_duration = workout['duration']
            else:
                activity_name = activity['name']
                activity_description = activity['details']
                activity_duration = activity['duration']

            if event_date == first_monday and activity['day'] == 0 and fitness_test is not None:  # Monday's activity
                # Add the fitness test event instead of the regular activity
                event_time = datetime.combine(first_monday, datetime.strptime(fitness_test['time'], "%H:%M").time())
                event = {
                    'summary': fitness_test['name'],
                    'description': fitness_test['details'],
                    'start': {
                        'dateTime': event_time.isoformat(),
                        'timeZone': 'Europe/London',
                    },
                    'end': {
                        'dateTime': (event_time + timedelta(minutes=fitness_test['duration'])).isoformat(),
                        'timeZone': 'Europe/London',
                    },
                    'reminders': {
                        'useDefault': False,
                        'overrides': [{'method': 'popup', 'minutes': 0}]
                    }
                }
            else:
                event_time = datetime.combine(event_date, datetime.strptime(activity['time'], "%H:%M").time())
                event = {
                    'summary': activity_name,
                    'description': activity_description,
                    'start': {
                        'dateTime': event_time.isoformat(),
                        'timeZone': 'Europe/London',
                    },
                    'end': {
                        'dateTime': (event_time + timedelta(minutes=activity_duration)).isoformat(),
                        'timeZone': 'Europe/London',
                    },
                    'reminders': {
                        'useDefault': False,
                        'overrides': [{'method': 'popup', 'minutes': 0}]
                    }
                }

            event_end = datetime.fromisoformat(event['end']['dateTime'])

            # Add the event to the calendar if it's not in the past
            if event_end >= datetime.now():
                calendar_service.events().insert(calendarId=calendar_id, body=event).execute()

            event_date += timedelta(weeks=1)

def add_reminder(calendar_service, calendar_id, end_date):
    # Remove any old reminders first
    events = calendar_service.events().list(
        calendarId=calendar_id,
        timeMin=datetime.now().isoformat() + "Z",
        singleEvents=True
    ).execute()

    for event in events.get('items', []):
        if event.get('summary') == "Populate Next Date Range":
            calendar_service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()

    # Find the last day with events
    end_dates = [
        datetime.fromisoformat(event['end']['dateTime'][:-1])
        if 'dateTime' in event['end'] else
        datetime.fromisoformat(event['end']['date'])
        for event in events.get('items', [])
    ]

    # Find the last date
    last_event_date = max(end_dates) if end_dates else datetime.now().date()
    
    # Add a reminder event for the user to populate the next date range
    reminder_date = last_event_date
    reminder_time = datetime.combine(reminder_date, datetime.strptime("09:00", "%H:%M").time())
    reminder_event = {
        'summary': "Populate Next Date Range",
        'description': "It's time to populate the next date range for your wellness plan!",
        'start': {
            'dateTime': reminder_time.isoformat(),
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': (reminder_time + timedelta(minutes=30)).isoformat(),
            'timeZone': 'Europe/London',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 0}
            ]
        }
    }
    calendar_service.events().insert(calendarId=calendar_id, body=reminder_event).execute()
    print(f"Added reminder event for {reminder_date.strftime('%A, %d %B %Y')}.")