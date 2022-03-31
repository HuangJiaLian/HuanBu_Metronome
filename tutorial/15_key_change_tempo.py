import time
import tkinter as tk
from tkinter import Frame
import simpleaudio

strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
sub_strong_beat = simpleaudio.WaveObject.from_wave_file('sub_strong_beat.wav')

theme_colors = {'bg': '#52767D', 'text':'#FFFFE6', 'label_bg':'#3D998D', 'scale_through':'#A3CEC5'}
theme_fonts = ['Helvetica']
tempo_range = [30, 230]
defaults = {'tempo': 120, 'scale_length': 550}

# The main window
window = tk.Tk()
window.title('Metronome')
window.geometry('900x300')

# Three frames are created
leftFrame = Frame(window)
leftFrame.config(bg=theme_colors['bg'])
leftFrame.pack(side='left',fill='both')

midFrame = Frame(window)
midFrame.pack(side='left', fill='both')

rightFrame = Frame(window)
rightFrame.pack(side='left', fill='both', expand=1)

# In left frame
time_signatures = {1: [' 2 / 4', (2, 4)], 2: [' 3 / 4',(3 ,4)], 3: [' 4 / 4',(4, 4)], 4: [' 2 / 2',(2, 2)],
                   5: [' 6 / 8',(6, 8)], 6: [' 9 / 8',(9, 8)], 7: ['12/ 8',(12, 8)],
                   8: [' * / 4',(-1, 4)], 9: [' * / 2',(-1,2)], 10: [' * / 8',(-1,8)]}
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
    global ON 
    if event.char == ' ':
        ON = not ON
    elif event.char == 't':
        tap_estimate()
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

window.bind("<Key>",key_pressed)
window.bind('<Down>', arrow_down)
window.bind('<Up>', arrow_up)
window.bind('<Left>', arrow_left)
window.bind('<Right>', arrow_right)

window.after(interval_ms, play)
window.mainloop()