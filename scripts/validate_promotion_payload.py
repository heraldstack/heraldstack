#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "source_url",
    "signal_type",
    "observation",
    "decision_impact",
    "proposed_action",
    "confidence",
    "priority",
    "promotion_decision",
    "attribution",
    "labels",
    "project_fields",
]

SIGNAL_TYPES = {"feed", "changelog", "research"}
PRIORITIES = {"p0", "p1", "p2", "p3"}
PROMOTION = {"promote", "hold", "archive"}
SPRINT_FIT = {"now", "next", "later"}
OWNER_ENTITY = {"harald", "stratia", "myrren", "liora", "kade vox", "solan", "ellow", "orin"}


def fail(msg: str) -> None:
    print(f"error: {msg}")
    sys.exit(1)


def ensure(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


def is_uri(value: str) -> bool:
    return bool(re.match(r"^https?://", value))


def validate(payload: dict) -> None:
    for key in REQUIRED:
        ensure(key in payload, f"missing required field: {key}")

    ensure(isinstance(payload["source_url"], str) and is_uri(payload["source_url"]), "source_url must be an http/https url")
    ensure(payload["signal_type"] in SIGNAL_TYPES, "signal_type must be feed|changelog|research")
    ensure(isinstance(payload["observation"], str) and len(payload["observation"].strip()) >= 20, "observation must be at least 20 chars")
    ensure(isinstance(payload["decision_impact"], str) and len(payload["decision_impact"].strip()) >= 20, "decision_impact must be at least 20 chars")
    ensure(isinstance(payload["proposed_action"], str) and len(payload["proposed_action"].strip()) >= 20, "proposed_action must be at least 20 chars")
    ensure(isinstance(payload["confidence"], int) and 0 <= payload["confidence"] <= 100, "confidence must be integer 0..100")
    ensure(payload["priority"] in PRIORITIES, "priority must be p0|p1|p2|p3")
    ensure(payload["promotion_decision"] in PROMOTION, "promotion_decision must be promote|hold|archive")

    attribution = payload["attribution"]
    ensure(isinstance(attribution, dict), "attribution must be an object")
    ensure(attribution.get("bryanchasko") is True, "attribution.bryanchasko must be true")
    ensure(attribution.get("heraldstack") is True, "attribution.heraldstack must be true")

    labels = payload["labels"]
    ensure(isinstance(labels, list) and len(labels) >= 3, "labels must contain at least 3 items")
    ensure(any(l == "signal/feed" or l == "signal/changelog" or l == "signal/research" for l in labels), "labels must include a signal/* label")
    ensure(any(str(l).startswith("state/") for l in labels), "labels must include a state/* label")
    ensure(any(str(l).startswith("priority/") for l in labels), "labels must include a priority/* label")

    fields = payload["project_fields"]
    ensure(isinstance(fields, dict), "project_fields must be an object")
    for f in ["signal source", "signal confidence", "promotion decision", "sprint fit", "owner entity", "attribution"]:
        ensure(f in fields, f"project_fields missing: {f}")

    ensure(fields["signal source"] in SIGNAL_TYPES, "project_fields.signal source invalid")
    ensure(isinstance(fields["signal confidence"], int) and 0 <= fields["signal confidence"] <= 100, "project_fields.signal confidence invalid")
    ensure(fields["promotion decision"] in PROMOTION, "project_fields.promotion decision invalid")
    ensure(fields["sprint fit"] in SPRINT_FIT, "project_fields.sprint fit invalid")
    ensure(fields["owner entity"] in OWNER_ENTITY, "project_fields.owner entity invalid")
    ensure(fields["attribution"] == "bryanchasko+heraldstack", "project_fields.attribution must be bryanchasko+heraldstack")

    if payload["promotion_decision"] == "promote":
        ensure(payload["confidence"] >= 70, "promoted items require confidence >= 70")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("usage: validate_promotion_payload.py <payload.json>")
    path = Path(sys.argv[1])
    ensure(path.exists(), f"file not found: {path}")
    with path.open() as f:
        payload = json.load(f)
    validate(payload)
    print(f"ok: {path}")
