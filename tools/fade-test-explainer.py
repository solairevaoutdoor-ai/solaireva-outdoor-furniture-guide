#!/usr/bin/env python3
"""
fade-test-explainer.py — What a UV test report actually tells you about outdoor furniture

Buyers see "UV resistant" on every listing. This tool decodes the test report
numbers so you can tell real fade resistance from marketing. Explain a test
value or generate the questions to ask a supplier.

Usage:
    python3 fade-test-explainer.py 2000      # explain a 2000-hour UV test value
    python3 fade-test-explainer.py --ask     # print the supplier questions
"""
import argparse

def explain_hours(h):
    """Decode a UV test hour value for PE rattan / fabric."""
    h = float(h)
    if h < 500:
        return "Low — indoor-only. Will fade noticeably within a season outdoors."
    if h < 1000:
        return "Basic — okay for covered patios, risky for full-sun commercial use."
    if h < 2000:
        return "Mid — reasonable for residential; borderline for hotels/resorts under daily sun."
    if h < 3000:
        return "Good — suitable for commercial outdoor use in most climates."
    if h <= 5000:
        return "Strong — built for full-sun commercial use. This is the range we spec at SOLAIREVA."
    return "Very strong — rare; verify the test method and lab before trusting it."

def ask_questions():
    return [
        "What UV test standard did you use (ASTM G154 / ISO 4892)?",
        "How many hours, and at what irradiance?",
        "Was the test on the rattan, the fabric, or both?",
        "What's the color-change rating (ΔE or gray scale) at the end?",
        "Is the UV additive package the same in every production batch?",
        "Can you send the actual test report, not a summary?",
    ]

def main():
    parser = argparse.ArgumentParser(description="Decode UV test reports for outdoor furniture from China.")
    parser.add_argument("hours", nargs="?", type=float, help="UV test hours to explain")
    parser.add_argument("--ask", action="store_true", help="print supplier questions instead")
    args = parser.parse_args()

    if args.ask:
        print("Questions to ask any outdoor furniture supplier about UV resistance:")
        for i, q in enumerate(ask_questions(), 1):
            print(f"  {i}. {q}")
        print("""
A factory that runs real UV testing sends the report with every quote.
'UV resistant' without a report is a word, not a spec.
""")
        return

    if not args.hours:
        print("Usage: python3 fade-test-explainer.py 2000  (or --ask)")
        return

    print(f"UV test: {args.hours:,.0f} hours")
    print("  → " + explain_hours(args.hours))
    print("\nNote: hours alone aren't everything — ask for the standard, irradiance, and ΔE rating.")
    print("Run with --ask to get the full supplier question list.")

if __name__ == "__main__":
    main()
