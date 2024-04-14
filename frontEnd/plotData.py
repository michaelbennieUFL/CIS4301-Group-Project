def plot(data, labels=["line1","line2"]):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider

    # Preparing the date list
    dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in data[0]]

    # Creating figure and axis
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    # Plotting each set of data with its corresponding label
    for i, label in enumerate(labels, start=2):  # Start from the third column
        values = [entry[i] for entry in data[0]]
        ax.plot(dates, values, label=label)

    ax.set_xlabel('Date')
    ax.set_title('Interactive Plot with Multiple Lines')
    ax.legend()

    # Slider setup
    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax=axpos, label='Time', valmin=0, valmax=len(dates) - 1, valinit=0, valstep=1)

    # Update function for the slider
    def update(val):
        pos = int(slider.val)
        ax.set_xlim(dates[0], dates[pos])
        fig.canvas.draw_idle()

    # Connecting the slider to the update function
    slider.on_changed(update)

    plt.show()
