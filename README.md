# AI Interview Coach

A desktop app that helps you prepare for technical job interviews. It combines a career profile, resume builder, learning tracker, and mock interviews with feedback and analytics. Built with **Python**, **Tkinter**, and **SQLite**, using only the standard library.

> The feedback is rule-based (expected keywords and answer length). It does not call any external AI service.

## Features

- **Dashboard:** performance summary and recommendations
- **Profile:** your details and skills
- **Resume:** build a resume with projects and experience
- **Certifications:** track the certifications you have or are working toward
- **Learning:** topics per role, with progress tracking
- **Mock Interview:** role-specific questions with scored feedback on each answer and a final result
- **Analytics:** track interview scores over time
- **Roles covered:** SOC Analyst, Python Developer, Software Developer, Data Analyst, Network Security Engineer

## Requirements

- Python 3.8 or newer
- Tkinter (included with the standard Python installers on Windows and macOS; on some Linux systems install it with `sudo apt install python3-tk`)

No third-party packages are needed.

## How to Run

```bash
git clone https://github.com/tabassumbanugitthub/AI-Interview-Coach.git
cd AI-Interview-Coach
python AI_COACH.py
```

The database (`ai_interview_coach.db`) is created automatically on first run.

## Screenshots

*Add screenshots of the dashboard, a mock interview, and the analytics page here.*

## Project Structure

```
AI-Interview-Coach/
├── AI_COACH.py   # Question bank, SQLite layer, and GUI
├── README.md
├── LICENSE
└── .gitignore
```

## Future Improvements

- Split the question bank, database, and GUI into separate modules
- Add more roles and questions
- Smarter answer scoring
- Export the resume as PDF

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
