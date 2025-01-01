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

def get_fitness_test_choice():
    # Print options
    print("Choose the fitness test to replace the first Monday of the month:")
    print("1. 1-Mile Run")
    print("2. 5K Run")
    print("3. 10K Run")
    print("4. None")    
    
    # Get user choice
    choice = input("Enter the number corresponding to your choice: ")

    # Validate choice
    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please enter a number between 1 and 4.")
        # Recursively call the function until a valid choice is made
        return get_fitness_test_choice()

    # Return choice
    return int(choice)

def add_weekly_activities(calendar_service, calendar_id, start_date, end_date, weekly_activities, cardio_workouts):
    # Add weekly activities for each week in the date range

    fitness_test = None
    # If the date range covers the first Monday of the month, ask the user if they want to replace it with a fitness test
    if start_date.day <= 7 and 7 <= end_date.day:
        # Ask the user if they want to replace the first Monday of the month with a fitness test
        fitness_test_choice = get_fitness_test_choice()
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
        else:
            fitness_test = None

    first_monday_offset = (7 - start_date.weekday()) % 7
    first_monday = start_date + timedelta(days=first_monday_offset)

    for activity in weekly_activities:
        event_date = start_date + timedelta(days=(activity['day'] - start_date.weekday()) % 7)
        while event_date <= end_date:
            # Skip any events in the past
            if event_date < datetime.now():
                event_date += timedelta(weeks=1)
                continue

            if activity['name'].startswith("Cardio"):
                # Choose a random workout
                workout_category = random.choice(cardio_workouts)
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
                        'overrides': [
                            {'method': 'popup', 'minutes': 0}
                        ]
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
                        'overrides': [
                            {'method': 'popup', 'minutes': 0}
                        ]
                    }
                }

            # Get the event end datetime
            event_end = datetime.fromisoformat(event['end']['dateTime'])

            # Add the event to the calendar if it's not in the past
            if event_end >= datetime.now():
                calendar_service.events().insert(calendarId=calendar_id, body=event).execute()

            event_date += timedelta(weeks=1)

    print("Added weekly activities successfully!")

def get_starting_weekday():
    # Print options
    print("Choose the day of the week to start the plan:")
    print("1. Monday")
    print("2. Tuesday")
    print("3. Wednesday")
    print("4. Thursday")
    print("5. Friday")
    print("6. Saturday")
    print("7. Sunday")
    
    # Get user choice
    choice = input("Enter the number corresponding to your choice: ")

    # Validate choice
    if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
        print("Invalid choice. Please enter a number between 1 and 7.")
        # Recursively call the function until a valid choice is made
        return get_starting_weekday()

    # Return choice
    return int(choice) - 1

def get_date_range():
    # Get current date
    now = datetime.now()

    # Print options
    print("Choose a time frame:")
    print("1. 1 Week")
    print("2. 2 Weeks")
    print("3. 4 Weeks")
    print("4. 1 Month (starting from the 1st)")
    
    # Get user choice
    choice = input("Enter the number corresponding to your choice: ")

    # Validate choice
    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        # Recursively call the function until a valid choice is made
        return get_date_range()

    # Calculate start date based on choice
    if choice in ["1", "2", "3"]:
        day_choice = get_starting_weekday()
        days_difference = (int(day_choice) - now.weekday()) % 7
        start_date = datetime(now.year, now.month, now.day) + timedelta(days=days_difference)

    # Calculate end date based on choice
    if choice == "1":
        end_date = start_date + timedelta(days=6)
    elif choice == "2":
        end_date = start_date + timedelta(days=13)
    elif choice == "3":
        end_date = start_date + timedelta(days=27)
    elif choice == "4":
        next_month = now.month + 1 if now.month < 12 else 1
        year = now.year if next_month > 1 else now.year + 1
        start_date = datetime(year, next_month, 1)
        end_date = datetime(year, next_month, monthrange(year, next_month)[1])

    # Return start and end dates
    return start_date, end_date

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