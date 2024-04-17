import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets

from matplotlib.widgets import Slider, Button, CheckButtons, RadioButtons

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

    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

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
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

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
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1

    slider_min.on_changed(update)
    slider_max.on_changed(update)
    #slider.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query2SeverityPlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Severity"):
    rural_data = [row[:-1] for row in data[0] if row[6][0]=="R"] # Used to grab all of the values that are of rural locations
    suburban_data = [row[:-1] for row in data[0] if row[6][0]=="S"] # Used to grab all of the values that are of suburban locations
    city_data = [row[:-1] for row in data[0] if row[6][0]=="C"] # Used to grab all of the values that are of city locations

    # Preparing the date list
    rural_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in rural_data]
    suburban_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in suburban_data]
    city_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in city_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = rural_data
    line, = ax.plot(rural_dates, [row[2] for row in rural_data], label=labels[0])
    lines.append(line)
        
    value2 = suburban_data
    line, = ax.plot(suburban_dates, [row[2] for row in suburban_data], label=labels[1])
    lines.append(line)
    
    value3 = city_data
    line, = ax.plot(city_dates, [row[2] for row in city_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom = 1)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = rural_dates + suburban_dates + city_dates
    all_dates.sort()

    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query2CrashesPlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Total Crashes"):
    rural_data = [row[:-1] for row in data[0] if row[6][0]=="R"] # Used to grab all of the values that are of rural locations
    suburban_data = [row[:-1] for row in data[0] if row[6][0]=="S"] # Used to grab all of the values that are of suburban locations
    city_data = [row[:-1] for row in data[0] if row[6][0]=="C"] # Used to grab all of the values that are of city locations

    # Preparing the date list
    rural_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in rural_data]
    suburban_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in suburban_data]
    city_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in city_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = rural_data
    line, = ax.plot(rural_dates, [row[3] for row in rural_data], label=labels[0])
    lines.append(line)
        
    value2 = suburban_data
    line, = ax.plot(suburban_dates, [row[3] for row in suburban_data], label=labels[1])
    lines.append(line)
    
    value3 = city_data
    line, = ax.plot(city_dates, [row[3] for row in city_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = rural_dates + suburban_dates + city_dates
    all_dates.sort()

    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query2DistancePlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Total Distance (in miles)"):
    rural_data = [row[:-1] for row in data[0] if row[6][0]=="R"] # Used to grab all of the values that are of rural locations
    suburban_data = [row[:-1] for row in data[0] if row[6][0]=="S"] # Used to grab all of the values that are of suburban locations
    city_data = [row[:-1] for row in data[0] if row[6][0]=="C"] # Used to grab all of the values that are of city locations

    # Preparing the date list
    rural_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in rural_data]
    suburban_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in suburban_data]
    city_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in city_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = rural_data
    line, = ax.plot(rural_dates, [row[4] for row in rural_data], label=labels[0])
    lines.append(line)
        
    value2 = suburban_data
    line, = ax.plot(suburban_dates, [row[4] for row in suburban_data], label=labels[1])
    lines.append(line)
    
    value3 = city_data
    line, = ax.plot(city_dates, [row[4] for row in city_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = rural_dates + suburban_dates + city_dates
    all_dates.sort()

    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query2CityDistancePlot(data, labels=["line1", "line2", "line3"], title="Interactive Plot with Multiple Lines", y_label="Average Crash Distance From City Center (in miles)"):
    rural_data = [row[:-1] for row in data[0] if row[6][0]=="R"] # Used to grab all of the values that are of rural locations
    suburban_data = [row[:-1] for row in data[0] if row[6][0]=="S"] # Used to grab all of the values that are of suburban locations
    city_data = [row[:-1] for row in data[0] if row[6][0]=="C"] # Used to grab all of the values that are of city locations

    # Preparing the date list
    rural_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in rural_data]
    suburban_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in suburban_data]
    city_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in city_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = rural_data
    line, = ax.plot(rural_dates, [row[5] for row in rural_data], label=labels[0])
    lines.append(line)
        
    value2 = suburban_data
    line, = ax.plot(suburban_dates, [row[5] for row in suburban_data], label=labels[1])
    lines.append(line)
    
    value3 = city_data
    line, = ax.plot(city_dates, [row[5] for row in city_data], label=labels[2])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = rural_dates + suburban_dates + city_dates
    all_dates.sort()

    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        #working but with value error
        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query3SeverityPlot(data, labels=["line1", "line2", "line3", "line4", "line5", "line6"], title="Interactive Plot with Multiple Lines", y_label="Severity"):
    zerototen_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that are take place with a speed of 0-10 miles per hour
    tentotwenty_data = [row[:-1] for row in data[0] if row[5][0]=="1"] # Used to grab all of the values that take place with a speed of 10-20 miles per hour
    twentytothirty_data = [row[:-1] for row in data[0] if row[5][0]=="2"] # Used to grab all of the values that take place with a speed of 20-30 miles per hour
    thirtytofourty_data = [row[:-1] for row in data[0] if row[5][0]=="3"] # Used to grab all of the values that take place with a speed of 30-40 miles per hour
    fourtytofifty_data = [row[:-1] for row in data[0] if row[5][0]=="4"] # Used to grab all of the values that take place with a speed of 40-50 miles per hour
    overfifty_data = [row[:-1] for row in data[0] if row[5][0]=="5"] # Used to grab all of the values that take place at over 50 miles per hour
        
    # Preparing the date list
    zerototen_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zerototen_data]
    tentotwenty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in tentotwenty_data]
    twentytothirty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in twentytothirty_data]
    thirtytofourty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in thirtytofourty_data]
    fourtytofifty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fourtytofifty_data]
    overfifty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in overfifty_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zerototen_data
    line, = ax.plot(zerototen_dates, [row[2] for row in zerototen_data], label=labels[0])
    lines.append(line)
        
    value2 = tentotwenty_data
    line, = ax.plot(tentotwenty_dates, [row[2] for row in tentotwenty_data], label=labels[1])
    lines.append(line)
    
    value3 = twentytothirty_data
    line, = ax.plot(twentytothirty_dates, [row[2] for row in twentytothirty_data], label=labels[2])
    lines.append(line)

    value4 = thirtytofourty_data
    line, = ax.plot(thirtytofourty_dates, [row[2] for row in thirtytofourty_data], label=labels[3])
    lines.append(line)

    value5 = fourtytofifty_data
    line, = ax.plot(fourtytofifty_dates, [row[2] for row in fourtytofifty_data], label=labels[4])
    lines.append(line)

    value6 = overfifty_data
    line, = ax.plot(overfifty_dates, [row[2] for row in overfifty_data], label=labels[5])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom = 1)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zerototen_dates + tentotwenty_dates + twentytothirty_dates + thirtytofourty_dates + fourtytofifty_dates + overfifty_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)


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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query3CrashesPlot(data, labels=["line1", "line2", "line3", "line4", "line5", "line6"], title="Interactive Plot with Multiple Lines", y_label="Total Crashes"):
    zerototen_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that are take place with a speed of 0-10 miles per hour
    tentotwenty_data = [row[:-1] for row in data[0] if row[5][0]=="1"] # Used to grab all of the values that take place with a speed of 10-20 miles per hour
    twentytothirty_data = [row[:-1] for row in data[0] if row[5][0]=="2"] # Used to grab all of the values that take place with a speed of 20-30 miles per hour
    thirtytofourty_data = [row[:-1] for row in data[0] if row[5][0]=="3"] # Used to grab all of the values that take place with a speed of 30-40 miles per hour
    fourtytofifty_data = [row[:-1] for row in data[0] if row[5][0]=="4"] # Used to grab all of the values that take place with a speed of 40-50 miles per hour
    overfifty_data = [row[:-1] for row in data[0] if row[5][0]=="5"] # Used to grab all of the values that take place at over 50 miles per hour
        
    # Preparing the date list
    zerototen_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zerototen_data]
    tentotwenty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in tentotwenty_data]
    twentytothirty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in twentytothirty_data]
    thirtytofourty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in thirtytofourty_data]
    fourtytofifty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fourtytofifty_data]
    overfifty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in overfifty_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zerototen_data
    line, = ax.plot(zerototen_dates, [row[3] for row in zerototen_data], label=labels[0])
    lines.append(line)
        
    value2 = tentotwenty_data
    line, = ax.plot(tentotwenty_dates, [row[3] for row in tentotwenty_data], label=labels[1])
    lines.append(line)
    
    value3 = twentytothirty_data
    line, = ax.plot(twentytothirty_dates, [row[3] for row in twentytothirty_data], label=labels[2])
    lines.append(line)

    value4 = thirtytofourty_data
    line, = ax.plot(thirtytofourty_dates, [row[3] for row in thirtytofourty_data], label=labels[3])
    lines.append(line)

    value5 = fourtytofifty_data
    line, = ax.plot(fourtytofifty_dates, [row[3] for row in fourtytofifty_data], label=labels[4])
    lines.append(line)

    value6 = overfifty_data
    line, = ax.plot(overfifty_dates, [row[3] for row in overfifty_data], label=labels[5])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zerototen_dates + tentotwenty_dates + twentytothirty_dates + thirtytofourty_dates + fourtytofifty_dates + overfifty_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)


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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query3DistancePlot(data, labels=["line1", "line2", "line3", "line4", "line5", "line6"], title="Interactive Plot with Multiple Lines", y_label="Distance Affected (in miles)"):
    zerototen_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that are take place with a speed of 0-10 miles per hour
    tentotwenty_data = [row[:-1] for row in data[0] if row[5][0]=="1"] # Used to grab all of the values that take place with a speed of 10-20 miles per hour
    twentytothirty_data = [row[:-1] for row in data[0] if row[5][0]=="2"] # Used to grab all of the values that take place with a speed of 20-30 miles per hour
    thirtytofourty_data = [row[:-1] for row in data[0] if row[5][0]=="3"] # Used to grab all of the values that take place with a speed of 30-40 miles per hour
    fourtytofifty_data = [row[:-1] for row in data[0] if row[5][0]=="4"] # Used to grab all of the values that take place with a speed of 40-50 miles per hour
    overfifty_data = [row[:-1] for row in data[0] if row[5][0]=="5"] # Used to grab all of the values that take place at over 50 miles per hour
        
    # Preparing the date list
    zerototen_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zerototen_data]
    tentotwenty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in tentotwenty_data]
    twentytothirty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in twentytothirty_data]
    thirtytofourty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in thirtytofourty_data]
    fourtytofifty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fourtytofifty_data]
    overfifty_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in overfifty_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zerototen_data
    line, = ax.plot(zerototen_dates, [row[4] for row in zerototen_data], label=labels[0])
    lines.append(line)
        
    value2 = tentotwenty_data
    line, = ax.plot(tentotwenty_dates, [row[4] for row in tentotwenty_data], label=labels[1])
    lines.append(line)
    
    value3 = twentytothirty_data
    line, = ax.plot(twentytothirty_dates, [row[4] for row in twentytothirty_data], label=labels[2])
    lines.append(line)

    value4 = thirtytofourty_data
    line, = ax.plot(thirtytofourty_dates, [row[4] for row in thirtytofourty_data], label=labels[3])
    lines.append(line)

    value5 = fourtytofifty_data
    line, = ax.plot(fourtytofifty_dates, [row[4] for row in fourtytofifty_data], label=labels[4])
    lines.append(line)

    value6 = overfifty_data
    line, = ax.plot(overfifty_dates, [row[4] for row in overfifty_data], label=labels[5])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zerototen_dates + tentotwenty_dates + twentytothirty_dates + thirtytofourty_dates + fourtytofifty_dates + overfifty_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)


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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query4SeverityPlot(data, labels=["line1", "line2", "line3", "line4"], title="Interactive Plot with Multiple Lines", y_label="Severity"):
    zero_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that contain 0 traffic conditions
    onetofour_data = [row[:-1] for row in data[0] if row[5][0]=="1"] # Used to grab all of the values that contain 1-4 traffic conditions
    fivetoeight_data = [row[:-1] for row in data[0] if row[5][0]=="5"] # Used to grab all of the values that contain 5-8 traffic conditions
    nine_data = [row[:-1] for row in data[0] if row[5][0]=="9"] # Used to grab all of the values that contain 9+ traffic conditions
    
    # Preparing the date list
    zero_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zero_data]
    onetofour_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in onetofour_data]
    fivetoeight_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fivetoeight_data]
    nine_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in nine_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    #for i, label in enumerate(labels, start=2):  # Start from the third column
    value1 = zero_data
    line, = ax.plot(zero_dates, [row[2] for row in zero_data], label=labels[0])
    lines.append(line)
        
    value2 = onetofour_data
    line, = ax.plot(onetofour_dates, [row[2] for row in onetofour_data], label=labels[1])
    lines.append(line)
    
    value3 = fivetoeight_data
    line, = ax.plot(fivetoeight_dates, [row[2] for row in fivetoeight_data], label=labels[2])
    lines.append(line)

    value4 = nine_data
    line, = ax.plot(nine_dates, [row[2] for row in nine_data], label=labels[3])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom = 1)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zero_dates + onetofour_dates + fivetoeight_dates + nine_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query4CrashesPlot(data, labels=["line1", "line2", "line3", "line4"], title="Interactive Plot with Multiple Lines", y_label="Total Crashes"):
    zero_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that contain 0 traffic conditions
    onetofour_data = [row[:-1] for row in data[0] if row[5][0]=="1"] # Used to grab all of the values that contain 1-4 traffic conditions
    fivetoeight_data = [row[:-1] for row in data[0] if row[5][0]=="5"] # Used to grab all of the values that contain 5-8 traffic conditions
    nine_data = [row[:-1] for row in data[0] if row[5][0]=="9"] # Used to grab all of the values that contain 9+ traffic conditions
    
    # Preparing the date list
    zero_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zero_data]
    onetofour_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in onetofour_data]
    fivetoeight_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fivetoeight_data]
    nine_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in nine_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zero_data
    line, = ax.plot(zero_dates, [row[3] for row in zero_data], label=labels[0])
    lines.append(line)
        
    value2 = onetofour_data
    line, = ax.plot(onetofour_dates, [row[3] for row in onetofour_data], label=labels[1])
    lines.append(line)
    
    value3 = fivetoeight_data
    line, = ax.plot(fivetoeight_dates, [row[3] for row in fivetoeight_data], label=labels[2])
    lines.append(line)

    value4 = nine_data
    line, = ax.plot(nine_dates, [row[3] for row in nine_data], label=labels[3])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zero_dates + onetofour_dates + fivetoeight_dates + nine_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1

    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query4DistancePlot(data, labels=["line1", "line2", "line3", "line4"], title="Interactive Plot with Multiple Lines", y_label="Distance Affected by Crash (in miles)"):
    zero_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that contain 0 traffic conditions
    onetofour_data = [row[:-1] for row in data[0] if row[5][0]=="1"] # Used to grab all of the values that contain 1-4 traffic conditions
    fivetoeight_data = [row[:-1] for row in data[0] if row[5][0]=="5"] # Used to grab all of the values that contain 5-8 traffic conditions
    nine_data = [row[:-1] for row in data[0] if row[5][0]=="9"] # Used to grab all of the values that contain 9+ traffic conditions
    
    # Preparing the date list
    zero_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zero_data]
    onetofour_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in onetofour_data]
    fivetoeight_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fivetoeight_data]
    nine_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in nine_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zero_data
    line, = ax.plot(zero_dates, [row[4] for row in zero_data], label=labels[0])
    lines.append(line)
        
    value2 = onetofour_data
    line, = ax.plot(onetofour_dates, [row[4] for row in onetofour_data], label=labels[1])
    lines.append(line)
    
    value3 = fivetoeight_data
    line, = ax.plot(fivetoeight_dates, [row[4] for row in fivetoeight_data], label=labels[2])
    lines.append(line)

    value4 = nine_data
    line, = ax.plot(nine_dates, [row[4] for row in nine_data], label=labels[3])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zero_dates + onetofour_dates + fivetoeight_dates + nine_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)

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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1

    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])
        #btn = Button(btn_ax, labels[i])
        #btn.on_clicked(lambda event, line=line: toggle_line_visibility(line))

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()


def Query5SeverityPlot(data, labels=["line1", "line2", "line3", "line4", "line5", "line6"], title="Interactive Plot with Multiple Lines", y_label="Severity"):
    zerototwo_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that are 0-2 miles from an airport
    twotofour_data = [row[:-1] for row in data[0] if row[5][0]=="2"] # Used to grab all of the values that are 2-4 miles from an airport
    fourtosix_data = [row[:-1] for row in data[0] if row[5][0]=="4"] # Used to grab all of the values that are 4-6 miles from an airport
    sixtoeight_data = [row[:-1] for row in data[0] if row[5][0]=="6"] # Used to grab all of the values that are 6-8 miles from an airport
    eighttoten_data = [row[:-1] for row in data[0] if row[5][0]=="8"] # Used to grab all of the values that are 8-10 miles from an airport
    overten_data = [row[:-1] for row in data[0] if row[5][0]=="O"] # Used to grab all of the values that over 10 miles from an airport
        
    # Preparing the date list
    zerototwo_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zerototwo_data]
    twotofour_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in twotofour_data]
    fourtosix_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fourtosix_data]
    sixtoeight_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in sixtoeight_data]
    eighttoten_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in eighttoten_data]
    overten_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in overten_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zerototwo_data
    line, = ax.plot(zerototwo_dates, [row[2] for row in zerototwo_data], label=labels[0])
    lines.append(line)
        
    value2 = twotofour_data
    line, = ax.plot(twotofour_dates, [row[2] for row in twotofour_data], label=labels[1])
    lines.append(line)
    
    value3 = fourtosix_data
    line, = ax.plot(fourtosix_dates, [row[2] for row in fourtosix_data], label=labels[2])
    lines.append(line)

    value4 = sixtoeight_data
    line, = ax.plot(sixtoeight_dates, [row[2] for row in sixtoeight_data], label=labels[3])
    lines.append(line)

    value5 = eighttoten_data
    line, = ax.plot(eighttoten_dates, [row[2] for row in eighttoten_data], label=labels[4])
    lines.append(line)

    value6 = overten_data
    line, = ax.plot(overten_dates, [row[2] for row in overten_data], label=labels[5])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom = 1)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zerototwo_dates + twotofour_dates + fourtosix_dates + sixtoeight_dates + eighttoten_dates + overten_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)


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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query5CrashesPlot(data, labels=["line1", "line2", "line3", "line4", "line5", "line6"], title="Interactive Plot with Multiple Lines", y_label="Total Crashes"):
    zerototwo_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that are 0-2 miles from an airport
    twotofour_data = [row[:-1] for row in data[0] if row[5][0]=="2"] # Used to grab all of the values that are 2-4 miles from an airport
    fourtosix_data = [row[:-1] for row in data[0] if row[5][0]=="4"] # Used to grab all of the values that are 4-6 miles from an airport
    sixtoeight_data = [row[:-1] for row in data[0] if row[5][0]=="6"] # Used to grab all of the values that are 6-8 miles from an airport
    eighttoten_data = [row[:-1] for row in data[0] if row[5][0]=="8"] # Used to grab all of the values that are 8-10 miles from an airport
    overten_data = [row[:-1] for row in data[0] if row[5][0]=="O"] # Used to grab all of the values that over 10 miles from an airport
        
    # Preparing the date list
    zerototwo_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zerototwo_data]
    twotofour_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in twotofour_data]
    fourtosix_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fourtosix_data]
    sixtoeight_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in sixtoeight_data]
    eighttoten_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in eighttoten_data]
    overten_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in overten_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zerototwo_data
    line, = ax.plot(zerototwo_dates, [row[3] for row in zerototwo_data], label=labels[0])
    lines.append(line)
        
    value2 = twotofour_data
    line, = ax.plot(twotofour_dates, [row[3] for row in twotofour_data], label=labels[1])
    lines.append(line)
    
    value3 = fourtosix_data
    line, = ax.plot(fourtosix_dates, [row[3] for row in fourtosix_data], label=labels[2])
    lines.append(line)

    value4 = sixtoeight_data
    line, = ax.plot(sixtoeight_dates, [row[3] for row in sixtoeight_data], label=labels[3])
    lines.append(line)

    value5 = eighttoten_data
    line, = ax.plot(eighttoten_dates, [row[3] for row in eighttoten_data], label=labels[4])
    lines.append(line)

    value6 = overten_data
    line, = ax.plot(overten_dates, [row[3] for row in overten_data], label=labels[5])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zerototwo_dates + twotofour_dates + fourtosix_dates + sixtoeight_dates + eighttoten_dates + overten_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)


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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()

def Query5DistancePlot(data, labels=["line1", "line2", "line3", "line4", "line5", "line6"], title="Interactive Plot with Multiple Lines", y_label="Distance Affected (in miles)"):
    zerototwo_data = [row[:-1] for row in data[0] if row[5][0]=="0"] # Used to grab all of the values that are 0-2 miles from an airport
    twotofour_data = [row[:-1] for row in data[0] if row[5][0]=="2"] # Used to grab all of the values that are 2-4 miles from an airport
    fourtosix_data = [row[:-1] for row in data[0] if row[5][0]=="4"] # Used to grab all of the values that are 4-6 miles from an airport
    sixtoeight_data = [row[:-1] for row in data[0] if row[5][0]=="6"] # Used to grab all of the values that are 6-8 miles from an airport
    eighttoten_data = [row[:-1] for row in data[0] if row[5][0]=="8"] # Used to grab all of the values that are 8-10 miles from an airport
    overten_data = [row[:-1] for row in data[0] if row[5][0]=="O"] # Used to grab all of the values that over 10 miles from an airport
        
    # Preparing the date list
    zerototwo_dates= [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in zerototwo_data]
    twotofour_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in twotofour_data]
    fourtosix_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in fourtosix_data]
    sixtoeight_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in sixtoeight_data]
    eighttoten_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in eighttoten_data]
    overten_dates = [np.datetime64(f"{year}-{month:02d}") for year, month, *_ in overten_data]

    # Creating figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

    # Plotting each set of data with its corresponding label
    lines = []
    value1 = zerototwo_data
    line, = ax.plot(zerototwo_dates, [row[4] for row in zerototwo_data], label=labels[0])
    lines.append(line)
        
    value2 = twotofour_data
    line, = ax.plot(twotofour_dates, [row[4] for row in twotofour_data], label=labels[1])
    lines.append(line)
    
    value3 = fourtosix_data
    line, = ax.plot(fourtosix_dates, [row[4] for row in fourtosix_data], label=labels[2])
    lines.append(line)

    value4 = sixtoeight_data
    line, = ax.plot(sixtoeight_dates, [row[4] for row in sixtoeight_data], label=labels[3])
    lines.append(line)

    value5 = eighttoten_data
    line, = ax.plot(eighttoten_dates, [row[4] for row in eighttoten_data], label=labels[4])
    lines.append(line)

    value6 = overten_data
    line, = ax.plot(overten_dates, [row[4] for row in overten_data], label=labels[5])
    lines.append(line)

    ax.set_xlabel('Date')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    # Slider for time range setup
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    all_dates = zerototwo_dates + twotofour_dates + fourtosix_dates + sixtoeight_dates + eighttoten_dates + overten_dates
    all_dates.sort()
    axmin = plt.axes([0.1, 0.1, 0.45, 0.03], facecolor=axcolor)
    axmax = plt.axes([0.1, 0.15, 0.45, 0.03], facecolor=axcolor)
    slider_min = Slider(ax=axmin, label='Min Time', valmin=0, valmax=len(all_dates) - 1, valinit=0, valstep=1)
    slider_max = Slider(ax=axmax, label='Max Time', valmin=0, valmax=len(all_dates) - 1, valinit=len(all_dates) - 1, valstep=1)


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
        fig.canvas.flush_events()

        slider_max.valmin=max_pos - 1
        slider_min.valmax=min_pos + 1


    slider_min.on_changed(update)
    slider_max.on_changed(update)
    

    # Buttons for toggling line visibility
    for i, line in enumerate(lines):
        btn_ax = plt.axes([0, 0, 0, 0])

    legend = ax.legend()
    map_legend_to_ax = {}  # Will map legend lines to original lines.

    pickradius = 5  # Points (Pt). How close the click needs to be to trigger an event.

    for legend_line, ax_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(pickradius)  # Enable picking on the legend line.
        map_legend_to_ax[legend_line] = ax_line

    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legend_line = event.artist

        # Do nothing if the source of the event is not a legend line.
        if legend_line not in map_legend_to_ax:
            return

        ax_line = map_legend_to_ax[legend_line]
        visible = not ax_line.get_visible()
        ax_line.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


    fig.canvas.mpl_connect('pick_event', on_pick)

    # Works even if the legend is draggable. This is independent from picking legend lines.
    legend.set_draggable(False)

    plt.show()