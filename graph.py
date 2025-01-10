from altair import Chart, Tooltip
from pandas import DataFrame


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    """
    Creates an Altair chart for visualizing data from the provided DataFrame.

    :param df: DataFrame containing the data to visualize.
    :param x: Column name for the x-axis.
    :param y: Column name for the y-axis.
    :param target: Column name to use for color encoding (e.g., target variable).
    :return: Altair Chart object.
    """
    graph = Chart(
        df,
        title=f"{y} by {x} for {target}"
    ).mark_circle(size=100).encode(
        x=x,  # X-axis
        y=y,  # Y-axis
        color=target,  # Grouped by target
        tooltip=Tooltip([x, y, target])  # Tooltip with relevant columns
    ).properties(
        width=600,  # Set chart width
        height=400,  # Set chart height
        background='#222222',  # Grey background for the theme
    ).configure_axis(
        grid=True,  # Retain grid lines
        gridColor='#444444',  # Lighter grid lines
        gridOpacity=0.6,  # Semi-transparent grid lines
        domain=True,  # Enable the axis domains (solid lines)
        domainColor='grey',  # Set the color of the solid lines
        domainWidth=1.5,  # Adjust the thickness of the solid lines
        labelFontSize=12,  # Font size for axis labels
        titleFontSize=14,  # Font size for axis titles
        labelColor='grey',  # Grey axis labels for dark background
        titleColor='grey',  # Grey axis titles for dark background
        titlePadding=20  # Move axis titles further from the axis numbers
    ).configure_title(
        fontSize=24,  # Larger font size for the chart title
        anchor='middle',  # Center the title
        color='grey'  # Title color for dark theme
    ).configure_legend(
        titleFontSize=14,  # Font size for legend title
        titleColor='grey',  # Grey legend title
        labelFontSize=12,  # Font size for legend labels
        labelColor='grey',  # Grey legend labels
        orient='right',  # Place legend to the right of the chart
    )

    return graph


# Testing Script
if __name__ == "__main__":
    import pandas as pd

    # Example data for testing
    data = {
        'Health': [100, 200, 150, 180, 220],
        'Energy': [50, 75, 60, 90, 80],
        'Sanity': [80, 70, 90, 85, 88],
        'Rarity': ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4']
    }
    df = pd.DataFrame(data)

    # Call the chart function with test inputs
    test_chart = chart(df, x='Health', y='Energy', target='Rarity')

    # Save the chart to a JSON file to ensure serialization works
    chart_json = test_chart.to_json()
    with open("test_chart.json", "w") as json_file:
        json_file.write(chart_json)
    
    print("Chart JSON serialized and saved as 'test_chart.json'.")
