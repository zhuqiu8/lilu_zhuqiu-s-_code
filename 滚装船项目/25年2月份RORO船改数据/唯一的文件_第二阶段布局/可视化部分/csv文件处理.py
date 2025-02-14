import random
import csv
def export_results(self, filename=r"完整的完整的2222.csv"):
    """Export the packing results to a CSV file with brand and placement details."""
    # 使用字典为每个品牌分配不同的颜色
    brand_colors = {}
    unique_colors = [(random.random(), random.random(), random.random()) for _ in range(len(set(r.brand for r in self.bins)))]

    for idx, brand in enumerate(set(r.brand for r in self.bins)):
        brand_colors[brand] = unique_colors[idx]

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bin ID", "Rectangle ID", "Brand", "Width", "Height", "X", "Y", "Rotated", "Color"])

        for i, bin in enumerate(self.bins, start=1):
            for rect in bin.placed_rectangles:
                writer.writerow([
                    f"Bin {i}",
                    rect.id,
                    rect.brand,
                    rect.width,
                    rect.height,
                    rect.x,
                    rect.y,
                    rect.rotated,
                    brand_colors[rect.brand]  # Add the assigned color for this brand
                ])

    print(f"Results exported to {filename}.")
