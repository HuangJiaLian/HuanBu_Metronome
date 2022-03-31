markings = {'Largo': [40, 60], 'Adagio': [66 ,76], 'Andante': [76, 108],
            'Allegretto': [112, 120], 'Allegro': [120, 156], 'Presto':[168, 200],
            'Prestissimo':[200, 330]}
# Function to determine the tempo markings
def tempo_marking_of(tempo):
    for key in markings.keys():
        if tempo >= markings[key][0] and tempo <= markings[key][1]:
            marking = key
            break
        else:
            marking = ''
    return marking
# Test the function
for tempo in range(30, 230, 40):
    print("The marking of {} BPM is {}.".format(tempo, tempo_marking_of(tempo)))
# --------------Output-------------------
# The marking of 30 BPM is .
# The marking of 70 BPM is Adagio.
# The marking of 110 BPM is .
# The marking of 150 BPM is Allegro.
# The marking of 190 BPM is Presto.