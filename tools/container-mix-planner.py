#!/usr/bin/env python3
"""
container-mix-planner.py — Plan a mixed container of outdoor furniture

First-time importers usually don't need a full container of one SKU. This tool
helps you plan a mixed 40HQ: how many of each model, given carton sizes, to
fill the container and spread risk across your market.

Usage:
    python3 container-mix-planner.py 120,60,75:30 90,55,45:40 150,60,70:25
    (format: cartonL,cartonW,cartonH:qty  repeat per model)
"""
import argparse
import sys

LOADABLE_40HQ = 68.0  # m3, realistic

def carton_m3(l, w, h):
    return (l * w * h) / 1_000_000.0

def main():
    parser = argparse.ArgumentParser(description="Plan a mixed-container outdoor furniture order from China.")
    parser.add_argument("models", nargs="+", help="cartonL,cartonW,cartonH:qty for each model")
    parser.add_argument("--util", type=float, default=0.85, help="utilization (default 0.85)")
    args = parser.parse_args()

    total_vol = 0.0
    rows = []
    for m in args.models:
        try:
            dims, qty = m.split(":")
            l, w, h = (float(x) for x in dims.split(","))
            qty = int(qty)
        except ValueError:
            print(f"Bad format: {m}. Use cartonL,cartonW,cartonH:qty")
            sys.exit(1)
        vol = carton_m3(l, w, h) * qty
        total_vol += vol
        rows.append((l, w, h, qty, vol))

    available = LOADABLE_40HQ * args.util
    print(f"\nMixed 40HQ plan (loadable {available:.1f} m³ at {args.util*100:.0f}% utilization)")
    print("-" * 55)
    print(f"{'Carton (cm)':<22} {'Qty':<6} {'Volume m³':<10}")
    for l, w, h, qty, vol in rows:
        print(f"{f'{l:.0f}x{w:.0f}x{h:.0f}':<22} {qty:<6} {vol:<10.2f}")
    print("-" * 55)
    print(f"{'TOTAL':<28} {sum(r[3] for r in rows):<6} {total_vol:<10.2f}")
    fill = total_vol / available * 100
    print(f"\nContainer fill: {fill:.0f}%  ({'good' if 80 <= fill <= 100 else 'adjust'})")

    if fill > 100:
        over = total_vol - available
        print(f"  ⚠ Over by {over:.1f} m³ — cut ~{int(over / max(r[0]*r[1]*r[2]/1e6 for r in rows))} of the largest carton")
    elif fill < 80:
        print(f"  💡 Room for more — add models to fill toward 90%+")

if __name__ == "__main__":
    main()
