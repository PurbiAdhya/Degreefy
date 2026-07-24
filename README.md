# Degreefy

Degreefy supports two guided planning paths:

1. **Full degree journey** — plans courses semester by semester through graduation.
2. **Upcoming semester only** — uses the published section schedule, meeting times, and a weekly conflict checker.

Open `index.html` through GitHub Pages or another web server. Browsers may block CSV loading when the file is opened directly with `file://`.

## Guided setup

The workflow asks for:

1. User role: student, faculty, or staff
2. Student status: incoming, transfer, current, or returning
3. Planning goal: full degree or upcoming semester
4. Whether the student has taken the math placement test, and the result when available
5. Graduation target for full-degree planning
6. Majors and minors
7. Completed core and program courses for non-incoming students
8. Weekly unavailable times for one-semester planning
9. **Plan my journey**

## Upcoming-semester planner

The one-semester workspace includes:

- A **Needed** view containing remaining requirements that appear in the published schedule
- An **All courses** view containing every published section
- A **Plan for me** action that builds a conflict-free draft while respecting prerequisites, corequisites, routine blocks, and the 18-credit maximum
- Drag-and-drop or Add controls for changing sections
- A Monday–Friday visual schedule with class and routine blocks
- Immediate class-to-class and class-to-routine conflict warnings
- A final table with course code, days and times, credit hours, and course type
- Print/PDF and Share with advisor actions

Completed courses do not appear in the Needed list. They remain available in All courses and are classified as Retake when selected.

## Data

See `data/README.md` for the GitHub CSV structure and the automatic PDF-to-CSV schedule workflow.
