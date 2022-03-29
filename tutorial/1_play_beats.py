import simpleaudio, time 

strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')

count = 0
interval = 0.5
while count < 4:
    strong_beat.play()
    count = count + 1
    time.sleep(interval)


weak_beat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
weak_beat.play()