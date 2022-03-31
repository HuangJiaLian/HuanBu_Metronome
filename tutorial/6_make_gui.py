import tkinter as tk
from tkinter import Frame

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
# Time signature options
time_signatures = [('*/4', 0),  ('4/4',1), ('3/4',2), ('2/4',3), ('6/8',4)]
mode_var = tk.IntVar(leftFrame)
for name, num in time_signatures:
    radio_button = tk.Radiobutton(leftFrame,text = name, variable = mode_var, value = num, fg=theme_colors['text'],bg=theme_colors['bg'], anchor='w', font=(theme_fonts[0], 17))
    if name == '4/4': # Select 4/4 by default
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
             font=(theme_fonts[0]))
scale.set(defaults['tempo'])
scale.pack(side='bottom',fill='both', expand='0')

# In right frame
# Label to show click number in a measure
count_label =tk.Label(rightFrame, text='0', fg=theme_colors['text'], bg =theme_colors['bg'], width=3, font=(theme_fonts[0], 180, 'bold'), justify='left')
count_label.pack(fill='both', expand=1)

window.mainloop()