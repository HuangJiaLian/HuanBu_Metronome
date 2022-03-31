import simpleaudio, time 
strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
sub_strong_beat = simpleaudio.WaveObject.from_wave_file('sub_strong_beat.wav')

count = 0
while True:
    count = count + 1
    if count == 1:
        strong_beat.play()
    elif count == 4:
        sub_strong_beat.play()
    else:
        weak_beat.play()
    if count == 6:
        count = 0
    time.sleep(0.5/2)