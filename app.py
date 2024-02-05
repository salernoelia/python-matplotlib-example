import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button
import json

def plot_cube(ax, x, y, z, color):
    ax.bar3d(x, y, 0, 1, 1, z, shade=True, color=color)

def create_3d_cube_graph(data_points, height_variable):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scale_factor = 1e-11  # Adjust this scale factor as needed
    spacing_factor = 2.0  # Adjust this spacing factor as needed

    for i, data_point in enumerate(data_points):
        try:
            area_habitat = float(data_point.get("Area_Habitat", 0))
            x = (i % 3) * spacing_factor
            y = (i // 3) * spacing_factor

            # Toggle height based on the selected variable
            if height_variable == "Above_ground_current_storage":
                z = float(data_point.get("Above_ground_current_storage", 0)) * scale_factor
            elif height_variable == "Above_ground_potential_storage":
                z = float(data_point.get("Above_ground_potential_storage", 0)) * scale_factor
            elif height_variable == "Normalized_above_ground_current_storage":
                z = float(data_point.get("Normalized_above_ground_current_storage", 0)) * scale_factor
            elif height_variable == "Normalized_above_ground_potential_storage":
                z = float(data_point.get("Normalized_above_ground_potential_storage", 0)) * scale_factor
            else:
                raise ValueError(f"Invalid height variable: {height_variable}")

            color = data_point.get("color", "b")
            plot_cube(ax, x, y, z, color)
        except (ValueError, TypeError) as e:
            print(f"Skipping data point due to error: {e}")

    ax.set_xlabel('X Axis (Index % 3 * spacing_factor)')
    ax.set_ylabel('Y Axis (Index // 3 * spacing_factor)')
    ax.set_zlabel(f'Z Axis ({height_variable} * scale_factor)')

    return fig, ax

def on_button_click(label):
    global height_variable
    height_variable = label  # Use the button's text as the height variable
    fig, ax = create_3d_cube_graph(data, height_variable)
    plt.draw()

if __name__ == "__main__":
    # Read data from the JSON file
    with open("data.json", "r") as json_file:
        data = json.load(json_file)

    height_variable = "Above_ground_potential_storage"  # Default height variable

    # Create initial 3D cube graph
    fig, ax = create_3d_cube_graph(data, height_variable)
    
def create_button(ax, label):
    button = Button(ax, label)
    button.on_clicked(lambda event: on_button_click(label))
    return button

ax_button = plt.axes([0.01, 0.01, 0.1, 0.05])
button_current = Button(ax_button, 'Above_ground_current_storage')
button_current.on_clicked(lambda event: on_button_click(button_current.label.get_text()))

ax_button = plt.axes([0.12, 0.01, 0.1, 0.05])
button_potential = Button(ax_button, 'Above_ground_potential_storage')
button_potential.on_clicked(lambda event: on_button_click(button_potential.label.get_text()))

ax_button = plt.axes([0.23, 0.01, 0.1, 0.05])
button_normalized_current = Button(ax_button, 'Normalized_above_ground_current_storage')
button_normalized_current.on_clicked(on_button_click)

ax_button = plt.axes([0.34, 0.01, 0.1, 0.05])
button_normalized_potential = Button(ax_button, 'Normalized_above_ground_potential_storage')
button_normalized_potential.on_clicked(on_button_click)

plt.show()
