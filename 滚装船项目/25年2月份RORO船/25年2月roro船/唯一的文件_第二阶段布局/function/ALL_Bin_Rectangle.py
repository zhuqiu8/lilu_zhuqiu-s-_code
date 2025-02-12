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
        # Check if the rectangle fits within the bin at (x, y)
        if x + rect.width > self.bin_width or y + rect.height > self.bin_height:
            return False

        # Check for overlap with already placed rectangles
        for placed in self.placed_rectangles:
            if not (
                x + rect.width <= placed.x or
                x >= placed.x + placed.width or
                y + rect.height <= placed.y or
                y >= placed.y + placed.height
            ):
                return False

        return True

    def place_rectangle(self, rect: Rectangle) -> bool:
        step = 0.1  # Define step size for placement to handle floating-point coordinates

        # Try to place the rectangle in its original orientation
        y = 0.0
        while y < self.bin_height:
            x = 0.0
            while x < self.bin_width:
                if self.can_place(rect, x, y):
                    rect.x = x
                    rect.y = y
                    self.placed_rectangles.append(rect)
                    return True
                x += step
            y += step

        # Try to place the rectangle after rotating it
        rect.rotate()
        y = 0.0
        while y < self.bin_height:
            x = 0.0
            while x < self.bin_width:
                if self.can_place(rect, x, y):
                    rect.x = x
                    rect.y = y
                    self.placed_rectangles.append(rect)
                    return True
                x += step
            y += step

        # Restore original orientation if placement fails
        rect.rotate()
        return False

    def visualize_packing(self, bin_id: int):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.bin_width)
        ax.set_ylim(0, self.bin_height)
        ax.set_aspect('equal')
        ax.set_title(f"Bin {bin_id} Packing Visualization")

        for rect in self.placed_rectangles:
            rect_color = (random.random(), random.random(), random.random())
            ax.add_patch(
                plt.Rectangle((rect.x, rect.y), rect.width, rect.height, edgecolor="black", facecolor=rect_color, lw=1)
            )
            ax.text(
                rect.x + rect.width / 2,
                rect.y + rect.height / 2,
                f"{rect.id}\n{rect.brand}",
                color="black",
                ha="center",
                va="center",
                fontsize=8
            )

        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.show()


class BinPacking:
    def __init__(self, bin_sizes: List[Tuple[float, float]]):
        self.bin_sizes = bin_sizes  # List of (width, height) for different bins
        self.bins = []

    def create_bins(self, bin_priority_brands: List[List[str]]):
        for (width, height), priority_brands in zip(self.bin_sizes, bin_priority_brands):
            self.bins.append(Bin(width, height, priority_brands))

    def pack_rectangles(self, rectangles: List[Rectangle]) -> None:
        # Sort rectangles by height (descending) for better packing efficiency
        rectangles.sort(key=lambda r: max(r.width, r.height), reverse=True)

        # 按堆场优先品牌数量排序
        self.bins.sort(key=lambda bin: len(bin.priority_brands), reverse=True)

        # Assign priority brands first
        for bin in self.bins:
            for brand in bin.priority_brands:
                for rect in [r for r in rectangles if r.brand == brand]:
                    if bin.place_rectangle(rect):
                        rectangles.remove(rect)

        # Assign remaining rectangles
        for rect in rectangles:
            placed = False
            for bin in self.bins:
                if bin.place_rectangle(rect):
                    placed = True
                    break

            if not placed:
                print(f"Rectangle {rect.id} ({rect.brand}) could not be placed.")

    def calculate_utilization(self) -> float:
        used_area = sum(
            sum(r.width * r.height for r in bin.placed_rectangles) for bin in self.bins
        )
        total_area = sum(bin.bin_width * bin.bin_height for bin in self.bins)
        return used_area / total_area * 100

    def visualize_all_bins(self):
        for i, bin in enumerate(self.bins):
            bin.visualize_packing(i + 1)

    def export_results(self, filename="packing_results.csv"):
        """Export the packing results to a CSV file."""
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Bin ID", "Rectangle ID", "Brand", "Width", "Height", "X", "Y", "Rotated"])

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
                        rect.rotated
                    ])

        print(f"Results exported to {filename}.")

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





