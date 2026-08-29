#!/usr/bin/env python3
"""
cushion-foam-guide.py — Pick the right cushion foam density for commercial outdoor furniture

The #1 "it went flat" complaint about outdoor sofas is foam density. This tool
maps foam density (kg/m³) to real use, so you can spec commercial-grade cushions.

Usage:
    python3 cushion-foam-guide.py 28        # explain a foam density
    python3 cushion-foam-guide.py --spec    # print a commercial cushion spec
"""
import argparse

def explain(density):
    d = float(density)
    if d < 20:
        return "Very soft — indoor comfort foam. Flattens fast under daily outdoor use."
    if d < 25:
        return "Standard residential — okay for occasional use, sags after a season of daily sitting."
    if d < 30:
        return "Mid-range — good residential/light commercial. Acceptable for covered hospitality."
    if d < 35:
        return "Commercial grade — holds shape under daily hotel/resort use. This is the range we spec."
    if d <= 40:
        return "High density commercial — premium support, long life, firmer feel. For heavy daily use."
    return "Very high density — feels firm; usually overkill unless it's a high-traffic public space."

def spec():
    return """Commercial outdoor cushion spec (what we ship at SOLAIREVA):

• Foam: 30-35 kg/m³ high-resilience (HR) polyurethane
• Core: denser than the comfort layer — resists sag
• Wrap: quick-dry polyester fiber, not cotton (cotton holds water)
• Cover: solution-dyed outdoor fabric, 300+ hours UV tested
• Zipper: stainless or plastic coil — never metal teeth that rust
• Drying: cushions should drain and dry in under 24h

Questions for the supplier:
1. Foam density in kg/m³? (a number, not 'high quality')
2. Is it HR foam or standard? (HR recovers, standard sags)
3. Water-resistant fabric or waterproof? (outdoor breathable beats vinyl in heat)
4. UV rating of the cover fabric in hours?
5. How does the cushion drain after rain?
"""

def main():
    parser = argparse.ArgumentParser(description="Spec commercial-grade outdoor furniture cushion foam.")
    parser.add_argument("density", nargs="?", type=float, help="foam density in kg/m³ to explain")
    parser.add_argument("--spec", action="store_true", help="print a commercial cushion spec")
    args = parser.parse_args()

    if args.spec:
        print(spec())
        return

    if not args.density:
        print("Usage: python3 cushion-foam-guide.py 30  (or --spec)")
        return

    print(f"Foam density {args.density} kg/m³")
    print("  → " + explain(args.density))
    print("\nRun with --spec for the full commercial cushion spec + supplier questions.")

if __name__ == "__main__":
    main()
