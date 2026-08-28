#!/usr/bin/env python3
"""
moq-estimator.py — What's a realistic MOQ for wholesale outdoor furniture from China?

For importers asking "what's the MOQ for patio furniture from a China factory?".
This gives realistic ranges by product type and customization level, so you know
whether a supplier's MOQ is fair or a red flag.

Usage:
    python3 moq-estimator.py                        # interactive
    python3 moq-estimator.py --product sofa --custom oem
"""
import argparse

# Realistic MOQ guidance for wholesale outdoor furniture factories in China.
# Stock models can be low; OEM/ODM needs volume to justify tooling + new SKUs.
MOQ_GUIDE = {
    "sofa":        {"stock": "1-2 containers or mixed container", "oem": "full container", "odm": "full container + design fee"},
    "dining_set":  {"stock": "mixed container OK",               "oem": "full container", "odm": "full container + design fee"},
    "lounge":      {"stock": "1-2 containers",                   "oem": "full container", "odm": "full container + design fee"},
    "umbrella":    {"stock": "mixed container OK",               "oem": "high (volume-based)", "odm": "negotiable"},
    "fire_pit":    {"stock": "mixed container OK",               "oem": "high (volume-based)", "odm": "negotiable"},
    "daybed":      {"stock": "1-2 containers",                   "oem": "full container", "odm": "full container + design fee"},
}

def estimate(product, custom):
    custom = custom.lower()
    row = MOQ_GUIDE.get(product)
    if not row:
        # fallback generic
        return {
            "stock": "mixed container usually OK",
            "oem": "usually a full container",
            "odm": "full container + design/tooling fee",
        }
    return row

def main():
    parser = argparse.ArgumentParser(description="Estimate realistic MOQ for wholesale outdoor furniture from China factories.")
    parser.add_argument("--product", choices=list(MOQ_GUIDE) + ["other"], default=None)
    parser.add_argument("--custom", choices=["stock", "oem", "odm"], default="stock",
                        help="stock = factory models; oem = your spec; odm = design + make")
    args = parser.parse_args()

    product = args.product
    if not product:
        print("Interactive mode — pick a product type:")
        for i, p in enumerate(list(MOQ_GUIDE) + ["other"]):
            print(f"  {i+1}. {p}")
        try:
            idx = int(input("  Number: ")) - 1
            product = list(MOQ_GUIDE)[idx] if idx < len(MOQ_GUIDE) else "other"
        except (EOFError, KeyboardInterrupt, ValueError):
            product = "other"

    row = estimate(product, args.custom)
    print(f"\nProduct: {product} | Customization: {args.custom.upper()}")
    print("-" * 50)
    print(f"Stock models (factory catalog): {row['stock']}")
    print(f"OEM (your spec, their build):   {row['oem']}")
    print(f"ODM (they design + build):      {row['odm']}")
    print("""
Key questions to ask any outdoor furniture supplier about MOQ:
1. Is the MOQ per model or per container? (a mixed container of stock models is common)
2. What changes with OEM/ODM — tooling, new SKU admin, packaging?
3. Can the first order mix models to hit the container, then repeat per-SKU?
4. Does the MOQ change with a deposit or annual volume commitment?

A real furniture factory answers these with numbers. A trading company hedges.
""")

if __name__ == "__main__":
    main()
