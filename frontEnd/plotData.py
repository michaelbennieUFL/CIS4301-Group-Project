import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons

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

def Query1SeverityPlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Severity"):
    towards_data = [row[:-1] for row in data[0] if row[5][0]=="t"] # Used to grab all of the values that are towards the vehicle
    against_data = [row[:-1] for row in data[0] if row[5][0]=="a"] # Used to grab all of the values against the vehicle
    perpendicular_data = [row[:-1] for row in data[0] if row[5][0]=="p"] # Used to grab all of the values perpendicular to the vehicle
    
    # Preparing the date list
    towards_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in towards_data]
    against_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in against_data]
    perpendicular_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in perpendicular_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    #for i, label in enumerate(labels, start=2):  # Start from the third column
    value1 = towards_data
    line, = ax.plot(towards_dates, [row[2] for row in towards_data], label=labels[0])
    lines.append(line)
        
    value2 = against_data
    line, = ax.plot(against_dates, [row[2] for row in against_data], label=labels[1])
    lines.append(line)
    
    value3 = perpendicular_data
    line, = ax.plot(perpendicular_dates, [row[2] for row in perpendicular_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom = 1)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = towards_dates + against_dates + perpendicular_dates
    all_dates.sort()
    #min_date = min(all_dates)
    #max_date = max(all_dates)
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)
    #slider = Slider(ax=ax_slider, label='Select Date Range', valmin=min_date, valmax=max_date, valinit=[min_date, max_date], valstep=np.timedelta64(1, 'D'))


    # Update function for the sliders
    def update(val):
        min_pos = int(slider_min.val)
        max_pos = int(slider_max.val)

        if abs(min_pos - max_pos) <= 3:
            return

        min_dates = all_dates[min_pos]
        max_dates = all_dates[max_pos]
        ax.set_xlim(min_dates, max_dates)
        fig.canvas.draw_idle()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1

        #min_val, max_val = slider.val
        #ax.set_xlim(min_val, max_val)
        #fig.canvas.draw_idle()

    slider_min.on_changed(update)
    slider_max.on_changed(update)
    #slider.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    line_visibility = [True, True, True]  # Initialize line visibility status

    def toggle_line_visibility(line_visibility):
        index = labels.index(line_visibility)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()

    ax_check = plt.axes([0.6, 0.001, 0.3, 0.3])
    plot_buttons = CheckButtons(ax_check, labels, line_visibility)
    plot_buttons.on_clicked(toggle_line_visibility)

    plt.show()

def Query1CrashesPlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Total Crashes"):
    towards_data = [row[:-1] for row in data[0] if row[5][0]=="t"] # Used to grab all of the values that are towards the vehicle
    against_data = [row[:-1] for row in data[0] if row[5][0]=="a"] # Used to grab all of the values against the vehicle
    perpendicular_data = [row[:-1] for row in data[0] if row[5][0]=="p"] # Used to grab all of the values perpendicular to the vehicle
    
    # Preparing the date list
    towards_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in towards_data]
    against_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in against_data]
    perpendicular_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in perpendicular_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    #for i, label in enumerate(labels, start=2):  # Start from the third column
    value1 = towards_data
    line, = ax.plot(towards_dates, [row[3] for row in towards_data], label=labels[0])
    lines.append(line)
        
    value2 = against_data
    line, = ax.plot(against_dates, [row[3] for row in against_data], label=labels[1])
    lines.append(line)
    
    value3 = perpendicular_data
    line, = ax.plot(perpendicular_dates, [row[3] for row in perpendicular_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = towards_dates + against_dates + perpendicular_dates
    all_dates.sort()
    #min_date = min(all_dates)
    #max_date = max(all_dates)
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)
    #slider = Slider(ax=ax_slider, label='Select Date Range', valmin=min_date, valmax=max_date, valinit=[min_date, max_date], valstep=np.timedelta64(1, 'D'))


    # Update function for the sliders
    def update(val):
        min_pos = int(slider_min.val)
        max_pos = int(slider_max.val)

        if abs(min_pos - max_pos) <= 3:
            return

        min_dates = all_dates[min_pos]
        max_dates = all_dates[max_pos]
        ax.set_xlim(min_dates, max_dates)
        fig.canvas.draw_idle()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1

        #min_val, max_val = slider.val
        #ax.set_xlim(min_val, max_val)
        #fig.canvas.draw_idle()

    slider_min.on_changed(update)
    slider_max.on_changed(update)
    #slider.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    line_visibility = [True, True, True]  # Initialize line visibility status

    def toggle_line_visibility(line_visibility):
        index = labels.index(line_visibility)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()

    ax_check = plt.axes([0.6, 0.001, 0.3, 0.3])
    plot_buttons = CheckButtons(ax_check, labels, line_visibility)
    plot_buttons.on_clicked(toggle_line_visibility)

    plt.show()

def Query1DistancePlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Distance Affected by Crash (in miles)"):
    towards_data = [row[:-1] for row in data[0] if row[5][0]=="t"] # Used to grab all of the values that are towards the vehicle
    against_data = [row[:-1] for row in data[0] if row[5][0]=="a"] # Used to grab all of the values against the vehicle
    perpendicular_data = [row[:-1] for row in data[0] if row[5][0]=="p"] # Used to grab all of the values perpendicular to the vehicle
    
    # Preparing the date list
    towards_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in towards_data]
    against_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in against_data]
    perpendicular_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in perpendicular_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    #for i, label in enumerate(labels, start=2):  # Start from the third column
    value1 = towards_data
    line, = ax.plot(towards_dates, [row[4] for row in towards_data], label=labels[0])
    lines.append(line)
        
    value2 = against_data
    line, = ax.plot(against_dates, [row[4] for row in against_data], label=labels[1])
    lines.append(line)
    
    value3 = perpendicular_data
    line, = ax.plot(perpendicular_dates, [row[4] for row in perpendicular_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = towards_dates + against_dates + perpendicular_dates
    all_dates.sort()
    #min_date = min(all_dates)
    #max_date = max(all_dates)
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)
    #slider = Slider(ax=ax_slider, label='Select Date Range', valmin=min_date, valmax=max_date, valinit=[min_date, max_date], valstep=np.timedelta64(1, 'D'))


    # Update function for the sliders
    def update(val):
        min_pos = int(slider_min.val)
        max_pos = int(slider_max.val)

        if abs(min_pos - max_pos) <= 3:
            return

        min_dates = all_dates[min_pos]
        max_dates = all_dates[max_pos]
        ax.set_xlim(min_dates, max_dates)
        fig.canvas.draw_idle()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1

        #min_val, max_val = slider.val
        #ax.set_xlim(min_val, max_val)
        #fig.canvas.draw_idle()

    slider_min.on_changed(update)
    slider_max.on_changed(update)
    #slider.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    line_visibility = [True, True, True]  # Initialize line visibility status

    def toggle_line_visibility(line_visibility):
        index = labels.index(line_visibility)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()

    ax_check = plt.axes([0.6, 0.001, 0.3, 0.3])
    plot_buttons = CheckButtons(ax_check, labels, line_visibility)
    plot_buttons.on_clicked(toggle_line_visibility)

    plt.show()