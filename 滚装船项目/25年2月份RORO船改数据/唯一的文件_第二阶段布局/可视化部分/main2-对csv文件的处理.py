import matplotlib.pyplot as plt
import csv
import random

def visualize_bins_from_csv(filename):
    # Read the CSV file
    bins_data = {}
    brand_colors = {}  # Dictionary to store colors for each brand
    color_palette = plt.cm.tab20.colors  # Use a predefined color palette
    color_index = 0  # Track the index for the color palette

    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            bin_id = row["Bin ID"]
            rect_id = row["Rectangle ID"]
            brand = row["Brand"]
            width = float(row["Width"])
            height = float(row["Height"])
            x = float(row["X"])
            y = float(row["Y"])
            rotated = row["Rotated"] == "True"

            if bin_id not in bins_data:
                bins_data[bin_id] = {
                    "rectangles": [],
                }

            bins_data[bin_id]["rectangles"].append({
                "rect_id": rect_id,
                "brand": brand,
                "width": width,
                "height": height,
                "x": x,
                "y": y,
                "rotated": rotated
            })

            # Assign a unique color to each brand
            if brand not in brand_colors:
                brand_colors[brand] = color_palette[color_index % len(color_palette)]
                color_index += 1

    # Visualize each bin
    for bin_id, data in bins_data.items():
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.set_title(f"Bin {bin_id} Layout")

        for rect in data["rectangles"]:
            x = rect["x"]
            y = rect["y"]
            width = rect["width"]
            height = rect["height"]
            brand = rect["brand"]

            # Draw rectangle with a consistent color for each brand
            rect_patch = plt.Rectangle(
                (x, y), width, height, edgecolor="black",
                facecolor=brand_colors[brand], lw=1
            )
            ax.add_patch(rect_patch)

            # Add label with rectangle ID and brand
            ax.text(
                x + width / 2, y + height / 2,
                f"{rect['rect_id']}\n{brand}",
                ha="center", va="center", fontsize=8, color="black"
            )

        # Auto-adjust the axis limits
        ax.autoscale()
        ax.set_xlabel("Width")
        ax.set_ylabel("Height")

        plt.show()

# Call the function to visualize the bins
visualize_bins_from_csv(r"D:\Github\RORO_Project\OROR-PROJECT\唯一的文件_第二阶段布局\阶段二布局.csv")

