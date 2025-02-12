import matplotlib.pyplot as plt
import csv
import pandas as pd

def read_yard_names(file_path, sheet_name, column_name):
    # Read yard names from an Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df[column_name].tolist()

def visualize_bins_from_csv(filename, yard_names):
    # Read the CSV file
    bins_data = {}
    brand_colors = {}  # Dictionary to store colors for each brand
    color_palette = plt.cm.tab20.colors  # Use a predefined color palette
    color_index = 0  # Track the index for the color palette

    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            bin_id = row["Bin ID"]
            bin_index = int(bin_id.replace("Bin ", "")) - 1  # Adjust index to match yard_names
            bin_name = yard_names[bin_index] if 0 <= bin_index < len(yard_names) else bin_id
            rect_id = row["Rectangle ID"]
            brand = row["Brand"]
            width = float(row["Width"])
            height = float(row["Height"])
            x = float(row["X"])
            y = float(row["Y"])
            rotated = row["Rotated"] == "True"

            if bin_id not in bins_data:
                bins_data[bin_id] = {
                    "name": bin_name,
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
        ax.set_title(f"{data['name']} Layout")

        legend_patches = []  # For storing legend entries

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

            # Add legend entry only once for each brand
            if not any(p.get_label() == brand for p in legend_patches):
                legend_patches.append(
                    plt.Line2D([0], [0], color=brand_colors[brand], lw=4, label=brand)
                )

        # Add legend to the plot
        ax.legend(handles=legend_patches, title="Brands", loc="upper right")

        # Auto-adjust the axis limits
        ax.autoscale()
        ax.set_xlabel("Width")
        ax.set_ylabel("Height")

        plt.show()


# Example usage
initial_file_path = r"C:\Users\zhuqiu\Desktop\最后一搜船_整体\第二次模型的输入数据0.xlsx"
yard_names = read_yard_names(initial_file_path, sheet_name='Yard_Areas', column_name='yard_names')
visualize_bins_from_csv(r"C:\Users\zhuqiu\Desktop\最后一搜船_整体\唯一的文件_第二阶段布局\阶段二布局.csv", yard_names)
