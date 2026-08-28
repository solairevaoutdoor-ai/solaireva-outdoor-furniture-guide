#!/usr/bin/env python3
"""
container-calculator.py — How many pieces of outdoor furniture fit in a shipping container?

A practical tool for importers and wholesale buyers calculating how much patio furniture
fits in a 20HQ / 40HQ container from China. Uses real loadable volumes (not theoretical
cubic capacity) because carton shape and bracing cost you space.

Usage:
    python3 container-calculator.py                       # interactive
    python3 container-calculator.py --length 60 --width 55 --height 40 --container 40hq
    python3 container-calculator.py --file cartons.csv    # one carton spec per line
"""
import argparse
import csv
import sys

# Real-world loadable volumes (m3) for furniture containers from China.
# These are below the theoretical cubic capacity because of carton waste + bracing.
CONTAINERS = {
    "20gp": 28.0,
    "20hq": 28.5,
    "40gp": 58.0,
    "40hq": 68.0,
    "45hq": 78.0,
}

def carton_volume_m3(length_cm, width_cm, height_cm):
    """Volume of one carton in cubic metres."""
    return (length_cm * width_cm * height_cm) / 1_000_000.0

def pieces_per_container(vol_m3, container_key, utilization=0.85):
    """
    Estimate how many cartons fit. We use ~85% utilization: cartons of
    outdoor furniture never pack at 100% because of mixed sizes and bracing.
    """
    loadable = CONTAINERS.get(container_key)
    if loadable is None:
        raise ValueError(f"Unknown container: {container_key}. Use one of {list(CONTAINERS)}")
    return int((loadable * utilization) / vol_m3)

def main():
    parser = argparse.ArgumentParser(description="Estimate how many outdoor furniture cartons fit in a container from China.")
    parser.add_argument("--length", type=float, help="carton length in cm")
    parser.add_argument("--width", type=float, help="carton width in cm")
    parser.add_argument("--height", type=float, help="carton height in cm")
    parser.add_argument("--container", default="40hq", choices=list(CONTAINERS), help="container type")
    parser.add_argument("--file", help="CSV with columns: length,width,height")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            reader = csv.DictReader(f)
            print(f"{'carton(cm)':<20} {'m3':<8} {'pieces/'+args.container.upper()}")
            print("-" * 45)
            for row in reader:
                l, w, h = float(row["length"]), float(row["width"]), float(row["height"])
                v = carton_volume_m3(l, w, h)
                p = pieces_per_container(v, args.container)
                print(f"{f'{l}x{w}x{h}':<20} {v:<8.3f} {p}")
            return

    if not (args.length and args.width and args.height):
        print("Interactive mode: enter carton size in cm (commercial outdoor furniture packing):")
        try:
            l = float(input("  Carton length (cm): "))
            w = float(input("  Carton width (cm): "))
            h = float(input("  Carton height (cm): "))
        except (EOFError, KeyboardInterrupt):
            print("No input. Try: python3 container-calculator.py --length 60 --width 55 --height 40 --container 40hq")
            return
    else:
        l, w, h = args.length, args.width, args.height

    v = carton_volume_m3(l, w, h)
    print(f"\nCarton: {l:.0f} x {w:.0f} x {h:.0f} cm = {v:.3f} m³")
    print(f"{'Container':<8} {'Loadable m³':<12} {'Pieces (85% util)':<18}")
    print("-" * 40)
    for key, loadable in CONTAINERS.items():
        p = pieces_per_container(v, key)
        print(f"{key.upper():<8} {loadable:<12} {p}")

    print(f"""
Notes:
- 85% utilization is a realistic average for mixed outdoor furniture cartons.
- For a single SKU repeat, utilization can reach ~90%+.
- Add ~5% for bracing if the factory uses full container bracing.
- Actual count depends on the packing standard of the furniture factory you choose.
  Ask your supplier for their measured loadable volume — a real factory will give it.
""")

if __name__ == "__main__":
    main()
