from typing import List, Tuple
import random
import matplotlib.pyplot as plt
import csv



class Rectangle:
    def __init__(self, width: float, height: float, id: int, brand: str):
        self.width = width
        self.height = height
        self.x = 0.0  # Bottom-left corner x-coordinate
        self.y = 0.0  # Bottom-left corner y-coordinate
        self.rotated = False  # Indicates if the rectangle is rotated
        self.id = id  # Unique identifier for the rectangle
        self.brand = brand  # Brand associated with the rectangle

    def __repr__(self):
        return (f"Rectangle(id={self.id}, width={self.width}, height={self.height}, "
                f"x={self.x}, y={self.y}, rotated={self.rotated}, brand={self.brand})")

    def rotate(self):
        # Swap width and height to represent a 90-degree rotation
        self.width, self.height = self.height, self.width
        self.rotated = not self.rotated


class Bin:
    def __init__(self, bin_width: float, bin_height: float, priority_brands: List[str] = None):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.placed_rectangles = []
        self.priority_brands = priority_brands or []  # Default: no priority brands

    def can_place(self, rect: Rectangle, x: float, y: float) -> bool:
        if x + rect.width > self.bin_width or y + rect.height > self.bin_height:
            return False

        for placed in sorted(self.placed_rectangles, key=lambda r: r.x):
            if placed.x > x + rect.width:
                break
            if (x < placed.x + placed.width and x + rect.width > placed.x and
                    y < placed.y + placed.height and y + rect.height > placed.y):
                return False
        return True

    def place_rectangle(self, rect: Rectangle) -> bool:
        if self.priority_brands and rect.brand not in self.priority_brands:
            return False

        x_candidates = {0.0}
        y_candidates = {0.0}
        for placed in self.placed_rectangles:
            x_candidates.add(placed.x + placed.width)
            y_candidates.add(placed.y + placed.height)
        x_candidates = sorted(x_candidates)
        y_candidates = sorted(y_candidates)

        original_width, original_height = rect.width, rect.height

        for x in x_candidates:
            if x + original_width > self.bin_width:
                continue
            for y in y_candidates:
                if y + original_height > self.bin_height:
                    continue
                if self.can_place(rect, x, y):
                    rect.x, rect.y = x, y
                    rect.rotated = False
                    self.placed_rectangles.append(rect)
                    return True

        rect.rotate()
        for x in x_candidates:
            if x + rect.width > self.bin_width:
                continue
            for y in y_candidates:
                if y + rect.height > self.bin_height:
                    continue
                if self.can_place(rect, x, y):
                    rect.x, rect.y = x, y
                    self.placed_rectangles.append(rect)
                    return True

        rect.width, rect.height = original_width, original_height
        rect.rotated = False
        return False

    def visualize_packing(self, bin_id: int):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.bin_width)
        ax.set_ylim(0, self.bin_height)
        ax.set_aspect('equal')
        ax.set_title(f"Bin {bin_id} Packing Visualization")

        for rect in self.placed_rectangles:
            color = (random.random(), random.random(), random.random())
            ax.add_patch(plt.Rectangle(
                (rect.x, rect.y), rect.width, rect.height,
                edgecolor='black', facecolor=color, lw=1))
            ax.text(rect.x + rect.width/2, rect.y + rect.height/2,
                    f"{rect.id}\n{rect.brand}", ha='center', va='center', fontsize=8)
        plt.show()

class BinPacking:
    def __init__(self, bin_sizes: List[Tuple[float, float]]):
        self.bin_sizes = bin_sizes
        self.bins = []

    def create_bins(self, bin_priority_brands: List[List[str]]):
        for (w, h), brands in zip(self.bin_sizes, bin_priority_brands):
            self.bins.append(Bin(w, h, brands))

    def pack_rectangles(self, rectangles: List[Rectangle]):
        brand_groups = defaultdict(list)
        for rect in rectangles:
            brand_groups[rect.brand].append(rect)

        for bin in self.bins:
            priority_rects = []
            for brand in bin.priority_brands:
                priority_rects.extend(brand_groups.get(brand, []))
            priority_rects.sort(key=lambda r: r.width * r.height, reverse=True)
            for rect in priority_rects[:]:
                if bin.place_rectangle(rect):
                    brand_groups[rect.brand].remove(rect)

        remaining = [r for brand in brand_groups.values() for r in brand]
        remaining.sort(key=lambda r: r.width * r.height, reverse=True)

        for rect in remaining[:]:
            placed = False
            for bin in self.bins:
                if bin.place_rectangle(rect):
                    placed = True
                    remaining.remove(rect)
                    break
            if not placed:
                print(f"Could not place Rectangle {rect.id} ({rect.brand})")

    def calculate_utilization(self):
        total = sum(b.bin_width * b.bin_height for b in self.bins)
        used = sum(r.width * r.height for b in self.bins for r in b.placed_rectangles)
        return used / total * 100 if total != 0 else 0

    def export_results(self, filename="packing_results.csv"):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Bin ID", "Rectangle ID", "Brand", "Width", "Height", "X", "Y", "Rotated"])
            for i, bin in enumerate(self.bins, 1):
                for rect in bin.placed_rectangles:
                    writer.writerow([
                        f"Bin {i}", rect.id, rect.brand,
                        rect.width, rect.height, rect.x, rect.y, rect.rotated
                    ])

    def count_brands_in_bins(self):
        """Count the number of bins each brand is placed in."""
        brand_bins = {}
        for i, bin in enumerate(self.bins, start=1):
            for rect in bin.placed_rectangles:
                if rect.brand not in brand_bins:
                    brand_bins[rect.brand] = set()
                brand_bins[rect.brand].add(f"Bin {i}")

        # Convert set to count
        for brand, bins in brand_bins.items():
            print(f"Brand {brand} is placed in {len(bins)} bins: {', '.join(bins)}.")

    def calculate_utilization_per_bin(self):
        """Calculate and display the utilization for each bin."""
        for i, bin in enumerate(self.bins, start=1):
            used_area = sum(r.width * r.height for r in bin.placed_rectangles)
            total_area = bin.bin_width * bin.bin_height
            utilization = (used_area / total_area) * 100
            print(f"Bin {i} utilization: {utilization:.2f}%.")




