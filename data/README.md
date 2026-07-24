# Degreefy data folder

Place this folder beside `index.html` in the GitHub repository used for GitHub Pages. Degreefy loads `./data/*.csv` automatically. The setup can also point to a raw GitHub folder URL such as:

`https://raw.githubusercontent.com/USERNAME/REPOSITORY/main/data`

## Degree and catalog files

- `programs.csv` — one row per major or minor, including its requirements-file path
- `programs/<program_id>.csv` — one requirements file per major or minor
- `requirements.csv` — optional combined fallback requirements file
- `courses.csv` — course titles, credits, areas, prerequisites, and corequisites
- `offerings.csv` — current and projected typical Fall/Spring/Summer offerings
- `core_requirements.csv` — Spring Hill core requirements

## Published semester schedule

- `semester_schedule.csv` — actual sections for the upcoming semester
- `source/*.pdf` — official schedule PDF uploaded by the college

The semester CSV includes:

`term, term_code, start_date, end_date, section_id, course_code, section, course_title, credit_hours, days, begin_time, end_time, modality, building, room, location, instructor, comments, registered, capacity`

Day codes use `M`, `T`, `W`, `R`, and `F`. Courses without fixed meeting times, including many online courses, may have blank day/time fields.

## Updating the schedule from a PDF

### Automatic GitHub workflow

1. Upload the new official PDF to `data/source/`.
2. Commit and push it to GitHub.
3. `.github/workflows/build-semester-schedule.yml` runs automatically.
4. The workflow converts the newest PDF and commits the refreshed `data/semester_schedule.csv`.

The GitHub Action installs `pdfplumber` and runs:

```bash
python tools/convert_schedule_pdf.py data/source/your-schedule.pdf \
  --output data/semester_schedule.csv \
  --catalog data/courses.csv
```

Because the college PDF is a formatted report rather than a data export, review the generated CSV after each new schedule is published. A later PDF layout change may require a small update to the converter.

## Prerequisite syntax

In `courses.csv`, separate required prerequisite groups with semicolons and alternatives within a group with vertical bars.

- `MTH 121;PHL 101|PHL 190` means **MTH 121 AND (PHL 101 OR PHL 190)**.

The same syntax is used for corequisites.

## Requirement criteria

For a direct required course, fill `course_code` and leave `criteria_type` blank.

For choices or electives:

- `criteria_type`: `choice` or `elective`
- `choices`: eligible course codes separated by `|`
- `prefixes`: eligible prefixes separated by `|`
- `min_level`, `max_level`, and `min_credits`: numeric eligibility rules

## Offerings

Use `status=current` with a year for an actual semester and `status=typical` with a blank year for projected recurring offerings. The published `semester_schedule.csv` is the source of truth for section times in the one-semester planner.

Acadeum remains part of the full-degree planner. Any Acadeum course stays flagged until departmental approval is recorded.
