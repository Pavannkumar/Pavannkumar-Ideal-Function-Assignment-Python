from bokeh.plotting import figure, show
from bokeh.models import HoverTool
from bokeh.io import output_file

# Visualizes training data, ideal functions, and mapped test data
def visualize(training_df, ideal_df, test_mapping_df, chosen_ideals):
    output_file("function_mapping.html")

    p = figure(
        title="Training Data, Ideal Functions, and Test Data Mapping",
        x_axis_label="x",
        y_axis_label="y",
        width=900,
        height=600
    )

    # Plot training data
    colors = ["blue", "green", "orange", "purple"]
    for i, col in enumerate(["y1", "y2", "y3", "y4"]):
        p.circle(
            training_df["x"],
            training_df[col],
            size=5,
            color=colors[i],
            legend_label=f"Training {col}"
        )

    # Plot chosen ideal functions
    for i, ideal_idx in enumerate(chosen_ideals):
        y_col = f"y{ideal_idx}"
        p.line(
            ideal_df["x"],
            ideal_df[y_col],
            line_width=2,
            color=colors[i],
            legend_label=f"Ideal {y_col}"
        )

    # Plot mapped test data
    p.cross(
        test_mapping_df["x"],
        test_mapping_df["y"],
        size=8,
        color="red",
        legend_label="Mapped Test Data"
    )

    p.add_tools(HoverTool(
        tooltips=[
            ("x", "@x"),
            ("y", "@y"),
            ("Δy", "@delta_y"),
            ("Ideal func", "@ideal_function")
        ]
    ))

    p.legend.click_policy = "hide"
    show(p)
