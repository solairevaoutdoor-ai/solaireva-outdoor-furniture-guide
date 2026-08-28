#!/usr/bin/env python3
"""
sourcing-checklist.py — Generate a supplier audit checklist for China furniture factories

Prints a ready-to-use factory audit checklist for buyers sourcing outdoor furniture
from China. Output as terminal text or export to markdown for sharing with a team.

Usage:
    python3 sourcing-checklist.py                # full checklist to terminal
    python3 sourcing-checklist.py --format md --out audit.md
    python3 sourcing-checklist.py --section docs
"""
import argparse

SECTIONS = {
    "docs": {
        "title": "Documents to request",
        "items": [
            "Business license (营业执照) — registered address + 'manufacturing' scope",
            "Export license",
            "ISO 9001 certificate (if claimed)",
            "Test reports: UV stability, salt spray, load-bearing",
            "Customer references in your market",
            "Real product photos (not catalog renders) + factory video walkthrough",
        ],
    },
    "factory": {
        "title": "Factory floor (on site or live video)",
        "items": [
            "Production line actually running (not a rented showroom)",
            "Powder coating done in-house or outsourced?",
            "Welding quality — even beads, no spatter",
            "Rattan weaving density + UV additive mix",
            "Cushion foam density (commercial grade = higher density)",
            "Carton and container packing standard",
        ],
    },
    "commercial": {
        "title": "Commercial & quality terms",
        "items": [
            "MOQ: per model or per container?",
            "Payment terms: 30% deposit / 70% against B/L is standard",
            "Defect rate — a factory that measures it can quote it (e.g. 0.47%)",
            "QC stages: incoming material, in-production, pre-packing, pre-shipping",
            "Third-party inspection available (SGS / Bureau Veritas / Intertek)?",
            "Container loading photographed at every stage",
        ],
    },
}

def render(section, fmt):
    s = SECTIONS[section]
    if fmt == "md":
        lines = [f"## {s['title']}", ""]
        lines += [f"- [ ] {item}" for item in s["items"]]
        return "\n".join(lines) + "\n"
    else:
        lines = [f"== {s['title']} =="]
        lines += [f"  [ ] {item}" for item in s["items"]]
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Generate a furniture supplier audit checklist for China sourcing.")
    parser.add_argument("--format", choices=["text", "md"], default="text")
    parser.add_argument("--section", choices=list(SECTIONS), default=None,
                        help="only one section; default = all")
    parser.add_argument("--out", help="write to file instead of stdout")
    args = parser.parse_args()

    sections = [args.section] if args.section else list(SECTIONS)
    output = []
    for s in sections:
        output.append(render(s, args.format))
        if args.format == "md" and len(sections) > 1:
            output.append("---\n")
    text = "\n".join(output)

    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"Checklist written to {args.out}")
    else:
        print(text)

if __name__ == "__main__":
    main()
