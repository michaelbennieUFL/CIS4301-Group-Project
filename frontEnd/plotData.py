import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def plot(data, labels=["line1", "line2"], title="Interactive Plot with Multiple Lines", y_label="Value"):
    # Preparing the date list
    dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in data[0]]

    # Creating figure and axis
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    for i, label in enumerate(labels, start=2):  # Start from the third column
        values = [entry[i] for entry in data[0]]
        line, = ax.plot(dates, values, label=label)
        lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    axmin = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(dates) - 1, valinit=len(dates) - 1, valstep=1)

    # Update function for the sliders
    def update(val):
        min_pos = int(slider_min.val)
        max_pos = int(slider_max.val)
        ax.set_xlim(dates[min_pos], dates[max_pos])
        fig.canvas.draw_idle()
        slider_max.valmin=slider_min.val+1
        slider_min.valmax=slider_max.val-1

    slider_min.on_changed(update)
    slider_max.on_changed(update)

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0.76, 0.05 - i*0.05, 0.1, 0.04])
        btn = Button(btn_ax, labels[i])
        btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    def toggle_line_visibility(line):
        line.set_visible(not line.get_visible())
        fig.canvas.draw_idle()

    plt.show()