#!/usr/bin/env python3
"""
shipping-estimator.py — Rough freight cost from China to major ports

A quick ballpark for importers estimating shipping costs of outdoor furniture
from China to the USA, UK, Europe, Australia, UAE and Africa. These are planning
ranges, NOT quotes — freight moves with season, fuel, and demand. Always get a
real quote from a freight forwarder (or ask the factory for their shipped-FOB history).

Usage:
    python3 shipping-estimator.py --dest usa --container 40hq
    python3 shipping-estimator.py              # interactive
"""
import argparse

# Rough all-in freight ranges (USD) South China port -> destination, 2026 planning levels.
# Peak season (Aug-Nov) runs high; off-peak lower.
FREIGHT_RANGES = {
    "usa":      {"20hq": (2800, 5500), "40hq": (4000, 7500), "note": "US West Coast cheaper than East Coast; Panama route peaks in fall"},
    "uk":       {"20hq": (2600, 5000), "40hq": (3800, 7000), "note": "Felixstowe / Southampton"},
    "europe":   {"20hq": (2600, 5200), "40hq": (3800, 7200), "note": "Rotterdam / Hamburg; Mediterranean ports vary"},
    "australia":{"20hq": (2000, 3800), "40hq": (3000, 5200), "note": "Sydney / Melbourne"},
    "uae":      {"20hq": (1500, 3000), "40hq": (2200, 4200), "note": "Jebel Ali"},
    "kenya":    {"20hq": (1800, 3400), "40hq": (2700, 4800), "note": "Mombasa"},
    "south_africa": {"20hq": (1900, 3500), "40hq": (2800, 5000), "note": "Durban / Cape Town"},
    "singapore": {"20hq": (1200, 2200), "40hq": (1800, 3200), "note": "Transhipment hub"},
    "india":    {"20hq": (1800, 3200), "40hq": (2600, 4500), "note": "Nhava Sheva / Chennai"},
}

def main():
    parser = argparse.ArgumentParser(description="Rough freight cost estimate from China to major import markets.")
    parser.add_argument("--dest", choices=list(FREIGHT_RANGES), default=None)
    parser.add_argument("--container", choices=["20hq", "40hq"], default="40hq")
    args = parser.parse_args()

    dest = args.dest
    if not dest:
        print("Interactive mode — destination:")
        dests = list(FREIGHT_RANGES)
        for i, d in enumerate(dests):
            print(f"  {i+1}. {d}")
        try:
            idx = int(input("  Number: ")) - 1
            dest = dests[idx]
        except (EOFError, KeyboardInterrupt, ValueError):
            print("No input. Use: python3 shipping-estimator.py --dest usa --container 40hq")
            return

    row = FREIGHT_RANGES[dest]
    lo, hi = row[args.container]
    print(f"\nFreight estimate: China (South China port) -> {dest.upper()}, {args.container.upper()}")
    print(f"  Range: ${lo:,} - ${hi:,} all-in")
    print(f"  Note: {row['note']}")
    print("""
Add-ons to budget beyond freight:
- Import duty from China (varies by HTS code — check with a customs broker)
- Terminal handling + customs clearance at destination
- Inland haulage (port to your warehouse)
- Insurance (~0.3-0.5% of cargo value)
- Peak season surcharges (Aug-Nov)

A good furniture factory gives you the FOB price and honest packing dimensions so
your freight forwarder can quote accurately. Ask for both in writing.
""")

if __name__ == "__main__":
    main()
