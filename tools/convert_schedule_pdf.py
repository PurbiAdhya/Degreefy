#!/usr/bin/env python3
"""Convert Spring Hill's traditional undergraduate schedule PDF to Degreefy CSV.

Usage:
    python tools/convert_schedule_pdf.py data/source/fall-2026-schedule.pdf \
        --output data/semester_schedule.csv --catalog data/courses.csv
"""
from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pdfplumber


def group_words_by_top(words: list[dict[str, Any]], tolerance: float = 1.3) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for word in sorted(words, key=lambda item: (item["top"], item["x0"])):
        for group in reversed(groups[-3:]):
            if abs(group["top"] - word["top"]) <= tolerance:
                count = len(group["words"])
                group["words"].append(word)
                group["top"] = (group["top"] * count + word["top"]) / (count + 1)
                break
        else:
            groups.append({"top": word["top"], "words": [word]})
    for group in groups:
        group["words"].sort(key=lambda item: item["x0"])
    return groups


def load_catalog(path: Path | None) -> dict[str, dict[str, str]]:
    if not path or not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return {row["code"].strip(): row for row in csv.DictReader(handle) if row.get("code")}


def iso_date(value: str) -> str:
    return datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d") if value else ""


def extract_schedule(pdf_path: Path, catalog: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with pdfplumber.open(pdf_path) as document:
        for page in document.pages:
            groups = group_words_by_top(page.extract_words(use_text_flow=False, keep_blank_chars=False))
            current_term: dict[str, Any] | None = None

            for index, group in enumerate(groups):
                text = " ".join(word["text"] for word in group["words"])
                if "TRADITIONAL UNDERGRADUATE" in text:
                    match = re.search(
                        r"(FALL|SPRING|SUMMER)\s+(\d{4})\s+([A-Z0-9]+)\s+"
                        r"(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})",
                        text,
                    )
                    if match:
                        current_term = {
                            "term": f"{match.group(1).title()} {match.group(2)}",
                            "term_code": match.group(3),
                            "start_date": iso_date(match.group(4)),
                            "end_date": iso_date(match.group(5)),
                        }

                words = group["words"]
                left = [word for word in words if word["x0"] < 92]
                if not (
                    len(left) >= 3
                    and re.fullmatch(r"[A-Z]{2,4}", left[0]["text"])
                    and re.fullmatch(r"\d{3}", left[1]["text"])
                    and re.fullmatch(r"\d{2}", left[2]["text"])
                ):
                    continue

                def column_text(min_x: float, max_x: float) -> str:
                    return " ".join(word["text"] for word in words if min_x <= word["x0"] < max_x).strip()

                instructor = comments = ""
                if index + 1 < len(groups):
                    next_group = groups[index + 1]
                    if 8 <= next_group["top"] - group["top"] <= 16:
                        instructor = " ".join(
                            word["text"] for word in next_group["words"] if 90 <= word["x0"] < 276
                        ).strip()
                        comments = " ".join(
                            word["text"] for word in next_group["words"] if word["x0"] >= 276
                        ).strip()

                course_code = f'{left[0]["text"]} {left[1]["text"]}'
                section = left[2]["text"]
                title = column_text(92, 272)
                credit_text = column_text(272, 292)
                if not credit_text:
                    attached_credit = re.match(r"^(.*?)([0-9])$", title)
                    if attached_credit and attached_credit.group(1).strip():
                        title = attached_credit.group(1).strip()
                        credit_text = attached_credit.group(2)
                    elif course_code in catalog:
                        credit_text = catalog[course_code].get("credits", "0")
                    else:
                        credit_text = "0"

                building = column_text(344, 384)
                room = column_text(384, 424)
                modality = "Online" if building == "OLC" or room == "OLC" else "In person"
                record = {
                    **(current_term or {"term": "", "term_code": "", "start_date": "", "end_date": ""}),
                    "section_id": f'{course_code.replace(" ", "")}-{section}',
                    "course_code": course_code,
                    "section": section,
                    "course_title": title or catalog.get(course_code, {}).get("title", course_code),
                    "credit_hours": int(float(credit_text or 0)),
                    "days": column_text(424, 454).replace(" ", ""),
                    "begin_time": column_text(454, 512),
                    "end_time": column_text(512, 575),
                    "modality": modality,
                    "building": building,
                    "room": room,
                    "location": " ".join(part for part in (building, room) if part),
                    "instructor": instructor,
                    "comments": comments,
                    "registered": int(column_text(292, 314) or 0),
                    "capacity": int(column_text(314, 344) or 0),
                }
                records.append(record)
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Official traditional undergraduate schedule PDF")
    parser.add_argument("--output", type=Path, default=Path("data/semester_schedule.csv"))
    parser.add_argument("--catalog", type=Path, default=Path("data/courses.csv"))
    args = parser.parse_args()

    catalog = load_catalog(args.catalog)
    rows = extract_schedule(args.pdf, catalog)
    if not rows:
        raise SystemExit("No schedule rows were found. Confirm that the PDF uses the expected SHC layout.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "term", "term_code", "start_date", "end_date", "section_id", "course_code", "section",
        "course_title", "credit_hours", "days", "begin_time", "end_time", "modality", "building",
        "room", "location", "instructor", "comments", "registered", "capacity",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} sections to {args.output}")


if __name__ == "__main__":
    main()
