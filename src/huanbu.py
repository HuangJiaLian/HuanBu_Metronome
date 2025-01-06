import time, os
import tkinter as tk
from tkinter import messagebox
from tkinter import Frame
import simpleaudio

basedir = os.path.dirname(__file__)
strong_beat = simpleaudio.WaveObject.from_wave_file(os.path.join(basedir,'strong_beat.wav'))
weak_beat = simpleaudio.WaveObject.from_wave_file(os.path.join(basedir,'weak_beat.wav'))
sub_strong_beat = simpleaudio.WaveObject.from_wave_file(os.path.join(basedir,'sub_strong_beat.wav'))

theme_colors = {'bg': '#52767D', 'text':'#FFFFE6', 'label_bg':'#3D998D', 'scale_through':'#A3CEC5'}
theme_fonts = ['Helvetica']
tempo_range = [30, 230]
defaults = {'tempo': 120, 'scale_length': 550}

# The main window
window = tk.Tk()
window.title('Huanbu Metronome')
window.geometry('900x300')

###########################
# Help message
###########################
# Create the menu bar
menu_bar = tk.Menu(window)

# Add the Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
def show_help_overview():
    messagebox.showinfo("Help - User Guide", 
        "Welcome to Huanbu Metronome!\n\n"
        "Here are some tips to help you use the application:\n"
        "1. Hover over different areas of the app to see helpful tooltips.\n"
        "2. Use the slider to adjust the tempo.\n"
        "3. Select a time signature from the left-hand side.\n"
        "4. The beat counter is displayed on the right.\n"
        "5. Press 't' to tap tempo, 'space' to start/stop the metronome.")
help_menu.add_command(label="User guide", command=show_help_overview)

# Three frames are created
leftFrame = Frame(window)
leftFrame.config(bg=theme_colors['bg'])
leftFrame.pack(side='left',fill='both')

midFrame = Frame(window)
midFrame.pack(side='left', fill='both')

rightFrame = Frame(window)
rightFrame.pack(side='left', fill='both', expand=1)

# In left frame
time_signatures = {0: [' 2 / 4', (2, 4)], 1: [' 3 / 4',(3 ,4)], 2: [' 4 / 4',(4, 4)], 3: [' 2 / 2',(2, 2)],
                   4: [' 6 / 8',(6, 8)], 5: [' 9 / 8',(9, 8)], 6: ['12/ 8',(12, 8)],
                   7: [' * / 4',(-1, 4)], 8: [' * / 2',(-1,2)], 9: [' * / 8',(-1,8)]}

ts_mode = tk.IntVar(leftFrame)
for mode in time_signatures.keys():
    radio_button = tk.Radiobutton(leftFrame, text = time_signatures[mode][0], variable = ts_mode,
                    value = mode, fg=theme_colors['text'],
                    bg=theme_colors['bg'], anchor='w', font=(theme_fonts[0], 17))
    if time_signatures[mode][-1] == (4, 4): # Select 4/4 by default
        radio_button.select()
    radio_button.pack(fill='x')

# In middle frame
# Label to show tempo 
tempo_label =tk.Label(midFrame, text='120', font=(theme_fonts[0], 90, 'bold'),
                      justify='center', fg = theme_colors['text'], bg = theme_colors['label_bg'], anchor='s')
tempo_label.pack(fill='both', expand=1)

marking_label =tk.Label(midFrame, text='Allegretto', font=(theme_fonts[0], 90, 'bold'),
                      justify='center', fg = theme_colors['text'], bg = theme_colors['label_bg'], anchor='n')
marking_label.pack(fill='both', expand=1)

markings = {'Largo': [40, 60], 'Adagio': [66 ,76], 'Andante': [76, 108],
            'Allegretto': [112, 120], 'Allegro': [120, 156], 'Presto':[168, 200],
            'Prestissimo':[200, 330]}

#markings = {'最缓板': [40, 60], '柔板': [66 ,76], '行板': [76, 108], 
#             '小快板': [112, 120], '快板': [120, 156],'急板':[168, 200],
#             '最急板':[200, 330]}

# Variable for the scale value
scale_var = tk.IntVar(midFrame)


# Function to determine the tempo markings
def tempo_marking_of(tempo):
    for key in markings.keys():
        if tempo >= markings[key][0] and tempo <= markings[key][1]:
            marking = key
            break
        else:
            marking = ''
    return marking

# When scale changes 
def update(*args):
    global scale_var, time_signature, interval_ms, tempo, tempo_label, marking_label
    tempo = scale_var.get()
    interval_ms = int((60/tempo) * (4/time_signature[-1]) * 1000)
    tempo_label['text'] = '{}'.format(tempo)
    marking = tempo_marking_of(tempo)
    marking_label['text'] = '{}'.format(marking)

# Use a scale to show the tempo range
scale = tk.Scale(midFrame,
             from_=tempo_range[0],
             to= tempo_range[1],
             orient=tk.HORIZONTAL,
             length=defaults['scale_length'],
             showvalue=0,
             troughcolor = theme_colors['scale_through'],
             bd = 0,
             activebackground = theme_colors['text'],
             bg = theme_colors['label_bg'],
             sliderlength = 30,
             width = 25,
             font=(theme_fonts[0]),
             variable=scale_var,
             command=update)
scale.set(defaults['tempo'])
scale.pack(side='bottom',fill='both', expand='0')

# In right frame
# Label to show click number in a measure
count_label =tk.Label(rightFrame, text='0', fg=theme_colors['text'], bg =theme_colors['bg'], width=3, font=(theme_fonts[0], 180, 'bold'), justify='left')
count_label.pack(fill='both', expand=1)


# When time signature mode changes
def update_time_signature(*args):
    global temp, time_signature, count, interval_ms
    time_signature = time_signatures[ts_mode.get()][-1]
    interval_ms = int((60/tempo) * (4/time_signature[-1]) * 1000)
    count = 0
ts_mode.trace('w', update_time_signature)

#####################
# Create a label for the tooltip
tooltip_label = tk.Label(midFrame, text='', font=(theme_fonts[0], 14),
                         justify='center', fg=theme_colors['text'], bg=theme_colors['label_bg'])
tooltip_label.pack(side='bottom', fill='x')

# Function to show the tooltip
def show_tooltip(event):
    tooltip_label.config(text='Drag the slider or use the ARROW keys to adjust the tempo')

# Function to hide the tooltip
def hide_tooltip(event):
    tooltip_label.config(text='')

# Function to show tooltip for the right region
def show_right_tooltip(event):
    tooltip_label.config(text='Press SPACE to start/pause')

# Function to hide tooltip for the right region
def hide_right_tooltip(event):
    tooltip_label.config(text='')

# Function to show tooltip for the left frame
def show_left_tooltip(event):
    tooltip_label.config(text='Select a time signature or use M key to change')

# Function to hide tooltip for the left frame
def hide_left_tooltip(event):
    tooltip_label.config(text='')

# Function to show tooltip for the center frame
def show_tempo_tooltip(event):
    tooltip_label.config(text='Tap T continuously along with your own beat to estimate the tempo')

# Function to hide tooltip for the left frame
def hide_tempo_tooltip(event):
    tooltip_label.config(text='')
#####################

# Time signature selection implementation
time_signature = time_signatures[ts_mode.get()][-1]
tempo = 120
interval_ms = int((60/tempo) * (4/time_signature[-1]) * 1000)
count = 0
ON = True
def play():
    global count, time_signature, count_label, ON
    if ON:
        count += 1
        count_label['text'] = '{}'.format(count)
        if time_signature[0] == -1:
            strong_beat.play()
        else:
            if count == 1:
                strong_beat.play()
            else:
                if time_signature[-1] == 8 and count % 3 == 1:
                    sub_strong_beat.play()
                else:
                    weak_beat.play()
        if count == time_signature[0]:
            count = 0
    window.after(interval_ms, play)

time_list = []
def tap_estimate():
    global time_list, scale
    time_list.append(time.time())
    list_len = len(time_list)
    N = 6
    if list_len > 1:
        # If two time far away from each other 
        # throw away the former times, only left the last one
        if time_list[-1] - time_list[-2] > 2:
            time_list = time_list[-1:]
        else:
            if list_len < N:
                interval = (time_list[-1] - time_list[0]) / (list_len - 1)
            else:
                interval = (time_list[-1] - time_list[-N]) / (N - 1)
            tempo = int(60/interval)
            scale.set(tempo)
    else:
        # Keep tapping 
        pass 
    # print(time_list)


def key_pressed(event):
    global ON, ts_mode, time_signatures
    if event.char == ' ':
        ON = not ON
    elif event.char == 't':
        tap_estimate()
    elif event.char =='m':
        ts_mode.set((ts_mode.get() + 1)%len(time_signatures))
    elif event.char == 'q':
        exit()

def arrow_down(event):
    global tempo, scale, tempo_range
    if tempo -1 >= tempo_range[0]:
        tempo -= 1
    scale.set(tempo)

def arrow_up(event):
    global tempo, scale, tempo_range
    if tempo +1 <= tempo_range[-1]:
        tempo += 1
    scale.set(tempo)

def arrow_left(event):
    global tempo, scale, tempo_range
    if tempo - 10 >= tempo_range[0]:
        tempo -= 10
    else:
        tempo -= (tempo-tempo_range[0])
    scale.set(tempo) 

def arrow_right(event):
    global tempo, scale, tempo_range
    if tempo + 10 <= tempo_range[1]:
        tempo += 10
    else:
        tempo += (tempo_range[1]-tempo)
    scale.set(tempo) 

# Bind the slider to show/hide the tooltip
scale.bind("<Enter>", show_tooltip)
scale.bind("<Leave>", hide_tooltip)
# Bind the right region (count_label) to show/hide the tooltip
count_label.bind("<Enter>", show_right_tooltip)
count_label.bind("<Leave>", hide_right_tooltip)

# Bind the left frame to show/hide the tooltip
leftFrame.bind("<Enter>", show_left_tooltip)
leftFrame.bind("<Leave>", hide_left_tooltip)

# Bind the tempo label to show/hide the tooltip
tempo_label.bind("<Enter>", show_tempo_tooltip)
tempo_label.bind("<Leave>", hide_tempo_tooltip)

marking_label.bind("<Enter>", show_tempo_tooltip)
marking_label.bind("<Leave>", hide_tempo_tooltip)

window.bind("<Key>",key_pressed)
window.bind('<Down>', arrow_down)
window.bind('<Up>', arrow_up)
window.bind('<Left>', arrow_left)
window.bind('<Right>', arrow_right)

# Display the menu bar
window.config(menu=menu_bar)
window.after(interval_ms, play)
window.mainloop()
