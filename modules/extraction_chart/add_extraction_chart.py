import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def add_extraction_chart(tds_percent, extraction_yield):
    """
    Adds a beautiful coffee extraction chart visualization to the Streamlit app
    showing where the current brew falls on the extraction map.

    Parameters:
    tds_percent (float): The calculated TDS percentage
    extraction_yield (float): The calculated extraction yield percentage
    """
    st.markdown("### Coffee Extraction Map")

    # Use a cleaner style
    plt.style.use("seaborn-whitegrid")

    # Create figure with high-resolution and better aspect ratio
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)

    # Set background color for the plot
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")

    # Define extraction zones
    extraction_range = np.linspace(13, 26, 100)
    tds_range = np.linspace(1.0, 1.7, 100)

    # Create grid for zones
    X, Y = np.meshgrid(extraction_range, tds_range)

    # Create zone masks
    under_extracted = X < 17
    ideal_range = (X >= 17) & (X <= 22)
    over_extracted = X > 22

    # Create zone colors
    under_color = "#FFF2CC"  # Light yellow
    ideal_color = "#FFD280"  # Golden orange
    over_color = "#FCE4EC"  # Light pink

    # Add colored zones with gradient alpha for more depth
    alpha_gradient = np.ones_like(X) * 0.7
    alpha_gradient = alpha_gradient * (Y - 1.0) / 0.7  # More transparent at bottom

    # Plot zones with alpha transparency for gradient effect
    ax.imshow(
        np.flipud(under_extracted),
        extent=[13, 17, 1.0, 1.7],
        aspect="auto",
        alpha=0.6,
        cmap=plt.cm.colors.ListedColormap([under_color]),
    )
    ax.imshow(
        np.flipud(ideal_range),
        extent=[17, 22, 1.0, 1.7],
        aspect="auto",
        alpha=0.7,
        cmap=plt.cm.colors.ListedColormap([ideal_color]),
    )
    ax.imshow(
        np.flipud(over_extracted),
        extent=[22, 26, 1.0, 1.7],
        aspect="auto",
        alpha=0.6,
        cmap=plt.cm.colors.ListedColormap([over_color]),
    )

    # Add zone dividers
    ax.axvline(x=17, color="#CCCCCC", linestyle="-", linewidth=1.5, alpha=0.8)
    ax.axvline(x=22, color="#CCCCCC", linestyle="-", linewidth=1.5, alpha=0.8)

    # Add horizontal strength dividers
    ax.axhline(y=1.15, color="#CCCCCC", linestyle="-", linewidth=1, alpha=0.5)
    ax.axhline(y=1.35, color="#CCCCCC", linestyle="-", linewidth=1, alpha=0.5)
    ax.axhline(y=1.45, color="#CCCCCC", linestyle="-", linewidth=1, alpha=0.5)

    # Plot brewing ratio lines
    for coffee_dose in [50, 55, 60, 65, 70, 75, 80, 85, 90]:
        # Create more accurate ratio curves
        x_range = np.linspace(13, 26, 100)

        # Calculate y-values based on real extraction principles
        # This is a simplified model of the relationship
        # Adjust the formula to match your specific chart if needed
        y_values = []
        for x in x_range:
            # This formula approximates the diagonal lines in the coffee chart
            # Each line corresponds to a different coffee dose
            ratio_factor = coffee_dose / 60.0  # Normalize around 60g as reference
            y = 1.0 + (x - 13) * 0.04 * ratio_factor
            y_values.append(min(y, 1.7))  # Cap at max 1.7

        # Plot the ratio line with gradient color
        (line,) = ax.plot(x_range, y_values, linewidth=2.5, alpha=0.8)
        line.set_color("#E53935")  # Consistent deep red color

        # Add label at the end of the line
        # Find where the line intersects with the right edge of the plot
        if y_values[-1] <= 1.65:  # Only if the line ends within the visible area
            ax.text(
                26.2,
                y_values[-1],
                f"{coffee_dose}g",
                fontsize=10,
                color="#E53935",
                fontweight="bold",
                verticalalignment="center",
                horizontalalignment="left",
            )

    # Add zone labels with styled text boxes
    def add_zone_label(
        x,
        y,
        text,
        rotation=0,
        fontsize=10,
        weight="normal",
        color="#333333",
        bg_color=None,
    ):
        if bg_color:
            bbox = dict(boxstyle="round,pad=0.4", fc=bg_color, ec="none", alpha=0.7)
        else:
            bbox = None
        ax.text(
            x,
            y,
            text,
            fontsize=fontsize,
            rotation=rotation,
            ha="center",
            va="center",
            fontweight=weight,
            color=color,
            bbox=bbox,
        )

    # Add zone labels
    add_zone_label(15, 1.55, "STRONG\nUNDER-DEVELOPED", fontsize=9)
    add_zone_label(15, 1.25, "UNDER-DEVELOPED", fontsize=10)
    add_zone_label(15, 1.05, "WEAK\nUNDER-DEVELOPED", fontsize=9)

    add_zone_label(19.5, 1.55, "STRONG", fontsize=9)
    add_zone_label(
        19.5,
        1.35,
        "IDEAL\nOPTIMUM BALANCE",
        fontsize=12,
        weight="bold",
        color="#000000",
        bg_color="#FFCC80",
    )
    add_zone_label(19.5, 1.05, "WEAK", fontsize=9)

    add_zone_label(24, 1.55, "STRONG\nBITTER", fontsize=9)
    add_zone_label(24, 1.25, "BITTER", fontsize=10)
    add_zone_label(24, 1.05, "WEAK\nBITTER", fontsize=9)

    # Add title at the top with styled text
    plt.figtext(
        0.5,
        0.97,
        "Brewing Ratio | Grams per One Liter",
        fontsize=16,
        color="#E53935",
        fontweight="bold",
        ha="center",
    )

    # Set axis labels with more styling
    ax.set_xlabel(
        "EXTRACTION | Solubles Yield — percent",
        fontsize=12,
        fontweight="bold",
        labelpad=10,
    )
    ax.set_ylabel(
        "STRENGTH | Solubles Concentration — percent",
        fontsize=12,
        fontweight="bold",
        labelpad=10,
    )

    # Style the ticks and gridlines
    ax.tick_params(axis="both", which="major", labelsize=10, colors="#333333", length=5)
    ax.grid(True, color="#E0E0E0", linestyle="-", linewidth=0.8, alpha=0.7)

    # Set axis limits with a bit of padding
    ax.set_xlim(13, 26.5)
    ax.set_ylim(1.0, 1.7)

    # Add custom tick marks
    plt.xticks(np.arange(13, 27, 1))
    plt.yticks(
        [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65]
    )

    # Add border around the plot
    for spine in ax.spines.values():
        spine.set_color("#AAAAAA")
        spine.set_linewidth(1.5)

    # Plot the current brew point if values are provided
    if tds_percent and extraction_yield:
        tds_value = tds_percent / 100  # Convert percentage to decimal

        # Create the marker with a halo effect
        ax.plot(
            extraction_yield,
            tds_value,
            "o",
            markersize=14,
            markerfacecolor="#1976D2",
            markeredgecolor="white",
            markeredgewidth=2.5,
            zorder=10,
            alpha=0.9,
        )

        # Add a pulsing circle around the point (optional visual effect)
        for size in [18, 22]:
            ax.plot(
                extraction_yield,
                tds_value,
                "o",
                markersize=size,
                markerfacecolor="none",
                markeredgecolor="#1976D2",
                markeredgewidth=1.5,
                zorder=9,
                alpha=0.3,
            )

        # Add elegant annotation for current brew
        brew_status = (
            "Under-extracted"
            if extraction_yield < 17
            else "Over-extracted"
            if extraction_yield > 22
            else "Ideal"
        )

        # Adjust text position based on point location to avoid going off-chart
        x_offset = -2.5 if extraction_yield > 24 else 1.5
        y_offset = -0.15 if tds_value > 1.6 else 0.1

        ax.annotate(
            f"Current Brew\n{tds_percent:.2f}% TDS\n{extraction_yield:.2f}% EY\n{brew_status}",
            xy=(extraction_yield, tds_value),
            xytext=(extraction_yield + x_offset, tds_value + y_offset),
            arrowprops=dict(
                facecolor="#333333",
                shrink=0.05,
                width=1.5,
                headwidth=8,
                alpha=0.7,
                connectionstyle="arc3,rad=0.2",
            ),
            fontsize=10,
            fontweight="bold",
            bbox=dict(
                fc="white",
                ec="#CCCCCC",
                alpha=0.9,
                boxstyle="round,pad=0.5,rounding_size=0.2",  # Fixed: removed duplicate boxstyle
            ),
        )

    # Add a slight padding around the figure
    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.94])

    # Show in Streamlit with proper sizing
    st.pyplot(fig)

    # Add an explanation below the chart
    st.markdown(
        """
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; font-size: 14px; margin-top: 15px;">
        <h4 style="margin-top: 0;">How to Use This Chart:</h4>
        <p>This chart maps your coffee extraction based on the Total Dissolved Solids (TDS) percentage and Extraction Yield:</p>
        <ul>
            <li><strong>Horizontal axis:</strong> Extraction Yield (13-26%)</li>
            <li><strong>Vertical axis:</strong> TDS/Strength (1.0-1.7%)</li>
            <li><strong>Diagonal red lines:</strong> Different coffee-to-water ratios (grams of coffee per liter)</li>
            <li><strong>Colored zones:</strong> Flavor profiles from under-developed to bitter</li>
        </ul>
        <p>The blue marker shows where your current brew falls on the chart.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
