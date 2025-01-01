CARDIO_WORKOUTS = [
    {
    "type": "Treadmill",
    "workouts": [
        {
        "name": "Incline Power Walk",
        "duration": 30,
        "details": "Walk with an incline of 10-15%."
        },
        {
        "name": "Interval Sprints",
        "duration": 35,
        "details": "5 minute warm up. Run hard for 1 minute, walk for 2 minutes; repeat."
        },
        {
        "name": "Steady-State Jog",
        "duration": 45,
        "details": "Jog at a consistent pace."
        }
    ]
    },
    {
    "type": "Elliptical",
    "workouts": [
        {
        "name": "Resistance Intervals",
        "duration": 30,
        "details": "Alternate 2 minutes at high resistance and 1 minute at low resistance."
        },
        {
        "name": "Steady-State Endurance",
        "duration": 40,
        "details": "Maintain a consistent pace at medium resistance."
        },
        {
        "name": "High-Intensity Push",
        "duration": 35,
        "details": "Go all-out for 30 seconds at very high resistance, then recover at very low resistance for 1 minute."
        }
    ]
    },
    {
    "type": "Spin Cycle",
    "workouts": [
        {
        "name": "Hill Climb Intervals",
        "duration": 30,
        "details": "Cycle seated for 2 minutes and standing for 1 minute at high resistance."
        },
        {
        "name": "Endurance Ride",
        "duration": 45,
        "details": "Maintain a moderate pace at a consistent medium resistance."
        },
        {
        "name": "Sprint Intervals",
        "duration": 35,
        "details": "Cycle at maximum speed for 20 seconds, recover for 40 seconds; repeat."
        }
    ]
    },
    {
    "type": "Rowing Machine",
    "workouts": [
        {
        "name": "500m Intervals",
        "duration": 30,
        "details": "Row 500 meters at maximum effort, then rest for 2 minutes; repeat."
        },
        {
        "name": "Steady-State Row",
        "duration": 40,
        "details": "Maintain your natural steady stroke rate."
        },
        {
        "name": "Pyramid Workout",
        "duration": 35,
        "details": "Row for 1, 2, 3, 4, and 5 minutes, with 1-minute rests in between."
        }
    ]
    },
    {
    "type": "Stair Climber",
    "workouts": [
        {
        "name": "Interval Climbing",
        "duration": 30,
        "details": "Climb at a fast pace for 1 minute, then slow down for 2 minutes."
        },
        {
        "name": "Steady Climb",
        "duration": 40,
        "details": "Maintain a moderate pace without stopping."
        },
        {
        "name": "Double Step Challenge",
        "duration": 35,
        "details": "Take two steps at a time for 30 seconds, then one step for 1 minute."
        }
    ]
    },
    {
    "type": "Ski Erg",
    "workouts": [
        {
        "name": "Power Intervals",
        "duration": 30,
        "details": "Ski as hard as possible for 30 seconds, then recover for 1 minute."
        },
        {
        "name": "Steady Endurance",
        "duration": 45,
        "details": "Maintain a consistent stroke rate and power output."
        },
        {
        "name": "Pyramid Intervals",
        "duration": 35,
        "details": "Ski for 1, 2, 3, 4, and 5 minutes with equal rest intervals."
        }
    ]
    },
    {
    "type": "HIIT (High-Intensity Interval Training)",
    "workouts": [
        {
        "name": "Tabata Intervals",
        "duration": 30,
        "details": "20 seconds of all-out effort followed by 10 seconds of rest; repeat for 8 cycles."
        },
        {
        "name": "Bodyweight HIIT",
        "duration": 40,
        "details": "Alternate between burpees, mountain climbers, and jump squats for 1 minute each, with 30 seconds of rest between rounds."
        },
        {
        "name": "Circuit Training",
        "duration": 35,
        "details": "Rotate through treadmill sprints, rowing, and stair climbing in 5-minute blocks."
        }
    ]
    },
]

DAILY_ACTIVITIES = [
    {
        "name": "Wake Up & HRV Check",
        "time": "05:00",
        "duration": 10,
        "details": "Wake up at 5:00 AM and perform an HRV check using your wearable or app. Use this data to adjust your day’s intensity. 🛌 Start your day strong!"
    },
    {
        "name": "Cold Shower",
        "time": "06:30",
        "duration": 5,
        "details": "Take a cold shower for 2-5 minutes to stimulate your parasympathetic nervous system and improve HRV. ❄️ Embrace the chill and feel rejuvenated!"
    },
    {
        "name": "Breathwork Break",
        "time": "12:00",
        "duration": 10,
        "details": "Practice diaphragmatic breathing: inhale for 4 seconds, hold for 4 seconds, exhale for 6 seconds. 🌊 Take a moment to reset and recharge."
    },
    {
        "name": "Evening Meditation",
        "time": "20:15",
        "duration": 15,
        "details": "Meditate for 10-15 minutes focusing on relaxation and gratitude. 🙏 Reflect on your progress and feel grateful for your journey."
    },
    {
        "name": "Bedtime Routine",
        "time": "21:30",
        "duration": 0,
        "details": "Wind down and aim to be in bed by 9:30 PM to ensure quality sleep. 🌙 Tomorrow is another chance to improve!"
    },
]

WEEKLY_ACTIVITIES = [
    {
        "day": 0,  # Monday
        "name": f"Cardio",
        "time": "09:30",
        "duration": 45,
        "details": "💪 Every step gets you closer to your goal!"
    },
    {
        "day": 1,  # Tuesday
        "name": "Strength Training (Full Body)",
        "time": "09:30",
        "duration": 60,
        "details": "Full-body workout to build strength and improve cardiovascular health. 🏋️‍♂️ Stronger every day!"
    },
    {
        "day": 2,  # Wednesday
        "name": "Active Recovery: Yoga",
        "time": "09:30",
        "duration": 30,
        "details": "Gentle yoga or stretching to promote recovery and flexibility. 🧘‍♀️ Feel the tension melt away."
    },
    {
        "day": 3,  # Thursday
        "name": f"Cardio + Core",
        "time": "09:30",
        "duration": 45,
        "details": "💥 Engage your core for better performance!"
    },
    {
        "day": 4,  # Friday
        "name": "Flexibility: Pilates",
        "time": "09:30",
        "duration": 30,
        "details": "Focus on dynamic stretching and flexibility. 🦋 Flexibility is strength in disguise!"
    },
    {
        "day": 5,  # Saturday
        "name": "Rest or Gentle Walking",
        "time": "10:00",
        "duration": 20,
        "details": "Take a relaxing walk or light activity. 🌿 Recovery is just as important as effort!"
    },
    {
        "day": 6,  # Sunday
        "name": "Active Recovery: Yoga",
        "time": "10:00",
        "duration": 30,
        "details": "Gentle yoga or stretching to promote recovery and flexibility. 🧘‍♀️ Feel the tension melt away."
    },
]