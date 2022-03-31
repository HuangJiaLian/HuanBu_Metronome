import simpleaudio, time 
strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
count = 0
while True:
    count = count + 1
    if count == 1:
        strong_beat.play()
    else:
        weak_beat.play()
    if count == 4:
        count = 0
    time.sleep(0.5)