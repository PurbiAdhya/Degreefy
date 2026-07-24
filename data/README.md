# Degreefy CSV data folder

Place this `data` folder beside `index.html` in a GitHub repository and publish the repository with GitHub Pages. Degreefy loads `./data/*.csv` automatically. You can also point the setup wizard to a raw GitHub folder URL such as:

`https://raw.githubusercontent.com/USERNAME/REPOSITORY/main/data`

## Files

- `programs.csv`: one row per major or minor, including a `requirements_file` path such as `programs/computer-science.csv`. Add all Spring Hill programs here.
- `programs/<program_id>.csv`: one requirements file per major or minor; the filename is listed in `programs.csv`.
- `requirements.csv`: optional combined fallback file when per-program files are not used.
- `courses.csv`: course titles, credits, academic areas, prerequisites, and corequisites.
- `offerings.csv`: current-semester offerings and projected typical Fall/Spring/Summer offerings.
- `core_requirements.csv`: Spring Hill core requirements.

## Prerequisite syntax

In `courses.csv`, separate prerequisite groups with semicolons. Separate alternatives within one group with vertical bars.

- `MTH 121;PHL 101|PHL 190` means **MTH 121 AND (PHL 101 OR PHL 190)**.
- The same syntax is used for `corequisites`.

## Requirement criteria

For a direct required course, fill `course_code` and leave `criteria_type` blank.

For choices or electives:

- `criteria_type`: `choice` or `elective`
- `choices`: eligible course codes separated by `|`
- `prefixes`: eligible prefixes separated by `|`
- `min_level`, `max_level`, and `min_credits`: numeric eligibility rules

## Offerings

Use `status=current` with a `year` for the actual current semester. Use `status=typical` with a blank year for projected recurring offerings. Degreefy uses typical offerings for scheduling warnings and current rows for the “Current semester” filter.

Acadeum is selected within the semester planner rather than in these files. Any Acadeum selection remains a planner warning until “Department approved” is checked.
