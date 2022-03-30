# http://c.biancheng.net/tkinter/scale-widget.html
# https://ritza.co/articles/note-generator-article/
# https://py2app.readthedocs.io/en/latest/tutorial.html
# https://www.pythonguis.com/tutorials/packaging-pyqt5-applications-pyinstaller-macos-dmg/
# https://cloudconvert.com/

import time, simpleaudio, os
import tkinter as tk
from tkinter import Frame, PhotoImage, Menu, messagebox

basedir = os.path.dirname(__file__)

num_counts_en = ['0','1','2','3','4','5','6','7','8','9']
num_counts_cn = ['零','壹','贰','叁','肆','伍','陆','柒','捌','玖']

num_counts = num_counts_en

speeds_en = {
    'Largo': [40, 60],
    'Adagio': [66 ,76],
    'Andante': [76, 108],
    'Allegretto': [112, 120],
    'Allegro': [120, 156],
    'Presto':[168, 200],
    'Prestissimo':[200, 330],
}

speeds_cn = {
    '最缓板': [40, 60],
    '柔板': [66 ,76],
    '行板': [76, 108],
    '小快板': [112, 120],
    '快板': [120, 156],
    '急板':[168, 200],
    '最急板':[200, 330],
}



speeds = speeds_cn

window =tk.Tk()
window.title('Huanbu Metronome')


#创建一个执行函数，点击下拉菜单中命令时执行
def show_usage() :
    messagebox.showinfo(title='Usage', message='Shortcuts are strongly recommended.\nSpace:\tPlay/Pause\nM:\t\tMode Change\nT:\t\tTap Estimate\nUp/Right:\tTempo+\nDown/Left:\tTempo-')

mainmenu = Menu(window)


filemenu = Menu (mainmenu, tearoff=False)
filemenu.add_command (label="Useage", command=show_usage,accelerator="U")
filemenu.add_command (label="Quit",command=window.quit, accelerator="Q")
mainmenu.add_cascade (label="Help",menu=filemenu)
window.config (menu=mainmenu)


window.geometry('912x325')
theme_colors = ['#ffffff','#52767D']
theme_fonts = ['Helvetica']
window["background"] = theme_colors[0]
scale_length = 550


leftFrame = Frame(window, height=300)
leftFrame.config(bg="#52767D")
leftFrame.pack(side='left',fill='both')

midFrame = Frame(window)
midFrame.pack(side='left', fill='both')

rightFrame = Frame(window)
rightFrame.pack(side='left', fill='both', expand=1)
 
ON = False
bpm = 120
delay = 60/bpm
count = 0
beat = 0


mode = [4, 4]

speed_range = [30, 230]

wave_a = simpleaudio.WaveObject.from_wave_file(os.path.join(basedir,'metronome.wav'))
wave_b = simpleaudio.WaveObject.from_wave_file(os.path.join(basedir,'metronomeup.wav'))
wave_c = simpleaudio.WaveObject.from_wave_file(os.path.join(basedir,'metronomeup_2.wav'))

def metronome():
    time_t1 = time.time()
    global ON, bpm, count, mode, beat, wave_a, wave_b, time_list, tap, count_label
    if len(time_list) > 0 and time_t1 - time_list[-1] > 3: 
        time_list = []
    delay = (60/bpm)/(mode[1]/4)
    if ON:
        count += 1
        # -1/4, 4/4 , or 3/4
        if mode[1] == 4:
            if mode[0] != -1:
                wave_a.play() if count != 1 else wave_b.play()
            else:
                wave_a.play()
        # 6/8
        if mode[1] == 8:
            if count == 1:
                wave_b.play()
            elif count == 4:
                wave_c.play()
            else:
                wave_a.play()
        # print(beat, count)
        # count_label['text'] = num_counts[count]
        count_label['text'] = str(count)
        if count >= mode[0] and mode[0] > 0:
            count = 0
            beat += 1
    window.after(int((delay - (time.time() - time_t1))*1000), metronome)


def update_bpm(value):
    global bpm, ON
    bpm = int(value)
    update_speed_name()

def key_pressed(event):
    global ON, mode_var, modes, scale
    if event.char == ' ':
        ON = not ON
        scale.set(bpm) 
    # Loop through modes
    elif event.char == 'm':
        mode_var.set((mode_var.get() + 1)%len(modes))
    # Taping 
    elif event.char == 't':
        tap_callback()
    elif event.char == 'u':
        show_usage()
    elif event.char == 'q':
        exit()
        

def arrow_down(event):
    global scale, bpm, speed_range
    if bpm - 1 >=  speed_range[0]:
        bpm -= 1
    scale.set(bpm) 
    update_speed_name()

def arrow_up(event):
    global scale, bpm
    if bpm + 1 <= speed_range[1]:
        bpm += 1
    scale.set(bpm) 
    update_speed_name()

def arrow_left(event):
    global scale, bpm, speed_range
    if bpm - 10 >= speed_range[0]:
        bpm -= 10
    else:
        bpm -= (bpm-speed_range[0])
    scale.set(bpm) 
    update_speed_name()

def arrow_right(event):
    global scale, bpm
    if bpm + 10 <= speed_range[1]:
        bpm += 10
    else:
        bpm +=(speed_range[1]-bpm)
    scale.set(bpm) 
    update_speed_name()



def update_speed_name():
    global scale, bpm, speed_label, mark_label, speeds
    speed_label['text'] = '{}'.format(bpm)
    for key in speeds.keys():
        if bpm >= speeds[key][0] and bpm <= speeds[key][1]:
            mark_label['text'] =  '{}'.format(key)
            break
        else:
            mark_label['text'] =  ''
    # print(window.winfo_width(), window.winfo_height())



modes = [('\u2009*/4', 0), ('4/4',1), ('3/4',2), ('2/4', 3), ('6/8',4)]
mode_var = tk.IntVar(leftFrame)
for name, num in modes:
    radio_button = tk.Radiobutton(leftFrame,text = name, variable = mode_var, value =num, fg='#FFFFE6',bg='#52767D', anchor='w', font=(theme_fonts[0], 17))
    # Select 4/4 by default
    if name == '4/4':
        radio_button.select()
    radio_button.pack(fill='x')

# When new mode selected
# run this function
def mode_var_callback(*args):
    global mode, count 
    selection = mode_var.get()
    if selection == 0:
        mode = [-1, 4]
    elif selection == 1:
        mode = [4, 4]
    elif selection == 2:
        mode = [3, 4]
    elif selection == 3:
        mode = [2, 4]       
    elif selection == 4:
        mode = [6, 8]
    count = 0

# When mode_var changes call callback
mode_var.trace("w", mode_var_callback)

languages=[('EN', 0), ('CN', 1)]
language_var = tk.IntVar(leftFrame)
for name, num in languages:
    radio_button = tk.Radiobutton(leftFrame,text = name, variable = language_var, value =num, fg='#FFFFE6',bg='#52767D', anchor='w', font=(theme_fonts[0], 17))
    if name == 'CN':
        radio_button.select()
    radio_button.pack(fill='x')


def language_var_callback(*args):
    global speeds, speeds_en, speeds_cn
    selection = language_var.get()
    if selection == 0:
        speeds = speeds_en
    elif selection == 1:
        speeds = speeds_cn
    update_speed_name()


language_var.trace("w", language_var_callback)

# label_play = tk.Label(leftFrame, text='帮助', fg='#FFFFE6', bg=window["background"], anchor='w')
# # play_button = tk.Button(leftFrame,image=play_img, borderwidth=0)   
# label_play.pack(side='top',fill='x') 

scale = tk.Scale(midFrame,
             label='',
             from_=speed_range[0],
             to= speed_range[1],
             orient=tk.HORIZONTAL,
             length=scale_length,
             showvalue=0,
             troughcolor = '#A3CEC5',
             bd = 0,
             activebackground = '#FFFFE6',
             bg = '#3D998D',
             sliderlength = 30,
            #  tickinterval=20, 
             font=(theme_fonts[0]),   
             command=update_bpm)
# scale.set(bpm)
scale.pack(side='bottom',fill='both', expand='0')

# Label to show tempo
# speed_label =tk.Label(midFrame, text='Press Space', font=(theme_fonts[0], 90, 'bold'),
#                       justify='center', fg = '#FFFFE6', bg ='#3D998D', anchor='s')
# speed_label.pack(fill='both', expand=1)

# mark_label =tk.Label(midFrame, text='To Start', font=(theme_fonts[0], 90, 'bold'),
#                       justify='center', fg = '#FFFFE6', bg ='#3D998D', anchor='n')
# mark_label.pack(fill='both', expand=1)

speed_label =tk.Label(midFrame, text='按空格', font=(theme_fonts[0], 90, 'bold'),
                      justify='center', fg = '#FFFFE6', bg ='#3D998D', anchor='s')
speed_label.pack(fill='both', expand=1)

mark_label =tk.Label(midFrame, text='开始', font=(theme_fonts[0], 90, 'bold'),
                      justify='center', fg = '#FFFFE6', bg ='#3D998D', anchor='n')
mark_label.pack(fill='both', expand=1)

# Keyboard interrupt
window.bind("<Key>",key_pressed)
window.bind('<Down>', arrow_down)
window.bind('<Up>', arrow_up)
window.bind('<Left>', arrow_left)
window.bind('<Right>', arrow_right)

tab_count = 0
time_list = []
new_flag = False
def tap_callback():
    global time_list, bpm, scale
    new_flag = True
    time_list.append(time.time())
    print(time_list)
    if len(time_list) > 1:
        if time_list[-1] - time_list[-2] > 3:
            time_list = []
        else:
            if len(time_list) < 6:
                interval = (time_list[-1] - time_list[0]) / (len(time_list) - 1)
            else:
                # Use the last 5 intervals to estimate tempo
                interval = (time_list[-1] - time_list[-6]) / (6 - 1)
            bpm = int(60/interval)
            if bpm > speed_range[-1]:
                bpm = speed_range[-1]
            scale.set(bpm) 
            update_speed_name()
    print(bpm)

count_label =tk.Label(rightFrame, text=num_counts[0], fg='#FFFFE6', bg ='#52767D', width=3, font=(theme_fonts[0], 180, 'bold'), justify='left')
count_label.pack(fill='both', expand=1)



window.after(1, metronome)
window.mainloop()