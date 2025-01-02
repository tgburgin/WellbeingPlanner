# Wellbeing Planner 🌟

**A smarter way to schedule, plan, and achieve your wellness goals!**

## About the Project

The **Wellbeing Planner** is a comprehensive tool designed to help you create customized wellness plans that integrate with Google Calendar. Whether you're looking to track fitness goals, organize your daily activities, or maintain a healthier lifestyle, this project provides an intuitive and flexible platform for success.

### Key Features

- **Interactive Calendar Integration**: Automatically syncs with Google Calendar to keep your plans organized and accessible.
- **Dark Mode Toggle**: Switch between light and dark themes for a comfortable user experience.
- **Custom Fitness Tests**: Choose from a variety of fitness tests to measure and track your progress.
- **Dynamic Date Selection**: Easily select start and end dates for your wellness plans.
- **Real-Time Updates**: Monitor progress through a live event-streaming feature.

---

## Screenshots

![Wellbeing Planner UI](assets/screenshot.png)

---

## How It Works

1. **Setup**: Authenticate your Google Calendar using OAuth 2.0.
2. **Plan**: Select your fitness test, set calendar colors, and pick a date range.
3. **Track**: Get real-time updates as your plan is built and synced to your calendar.
4. **Maintain**: Use automated reminders to stay on top of your goals.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tgburgin/wellbeing-planner.git
   cd wellbeing-planner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables for Google OAuth:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `GOOGLE_PROJECT_ID`

4. Run the app:
   ```bash
   python app.py
   ```

5. Visit `http://localhost:5000` to start planning your wellness journey!

---

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Flask (Python)
- **API Integration**: Google Calendar API

---

## Contributing

We welcome contributions! Feel free to:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

*Stay organized, stay healthy! 💪*

