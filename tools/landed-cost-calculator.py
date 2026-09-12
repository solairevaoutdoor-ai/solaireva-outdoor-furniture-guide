#!/usr/bin/env python3
"""
landed-cost-calculator.py — What does a container of outdoor furniture really cost, landed?

Importers comparing quotes from China furniture factories forget the costs between
the FOB price and the warehouse door. This tool builds the full landed cost so you
can compare suppliers apples-to-apples.

Usage:
    python3 landed-cost-calculator.py --fob 18000 --freight 5500 --duty-pct 5.4 --container 40hq
    python3 landed-cost-calculator.py            # interactive
"""
import argparse

def estimate_insurance(cargo_value, pct=0.004):
    """Insurance is typically 0.3-0.5% of cargo value."""
    return cargo_value * pct

def main():
    parser = argparse.ArgumentParser(description="Estimate full landed cost of a furniture container from China.")
    parser.add_argument("--fob", type=float, help="FOB value in USD (what the factory charges)")
    parser.add_argument("--freight", type=float, help="freight + insurance to destination, USD")
    parser.add_argument("--duty-pct", type=float, default=5.4, help="import duty percentage (default 5.4, varies by HTS)")
    parser.add_argument("--local", type=float, default=800, help="destination charges: terminal, customs, inland, USD")
    args = parser.parse_args()

    fob = args.fob
    if not fob:
        try:
            fob = float(input("FOB value (factory price, USD): "))
            freight = float(input("Freight to destination (USD): "))
            duty_pct = float(input("Import duty % (e.g. 5.4): ") or 5.4)
            local = float(input("Destination charges (terminal/customs/inland, USD): ") or 800)
        except (EOFError, KeyboardInterrupt, ValueError):
            print("Try: python3 landed-cost-calculator.py --fob 18000 --freight 5500 --duty-pct 5.4")
            return
    else:
        freight = args.freight
        duty_pct = args.duty_pct
        local = args.local

    duty = fob * (duty_pct / 100.0)
    insurance = estimate_insurance(fob + freight)
    landed = fob + freight + duty + insurance + local

    print(f"\nLanded cost breakdown (USD)")
    print("-" * 45)
    print(f"FOB (factory):            ${fob:>12,.2f}")
    print(f"Freight:                  ${freight:>12,.2f}")
    print(f"Insurance (0.4%):         ${insurance:>12,.2f}")
    print(f"Import duty ({duty_pct}%):       ${duty:>12,.2f}")
    print(f"Destination charges:      ${local:>12,.2f}")
    print("-" * 45)
    print(f"TOTAL LANDED:             ${landed:>12,.2f}")
    print(f"Landed vs FOB premium:    {((landed/fob)-1)*100:>10.1f}%")
    print("""
Notes:
- Import duty from China varies by HTS code and country — confirm with a customs broker.
- This is a planning estimate, not a quote. Peak season (Aug-Nov) freight runs high.
- Ask the factory for FOB and honest packed dimensions so freight is quoted accurately.
""")

if __name__ == "__main__":
    main()
