time_list = [1648565267.9251342, 1648565268.482229, 1648565269.013833, 1648565269.560467, 1648565270.105812, 1648565270.644593, 1648565271.175668]

def tempo_estimate(time_list):
    list_len = len(time_list)
    N = 6
    if list_len < 6:
        interval = (time_list[-1] - time_list[0]) / (list_len - 1)
    else:
        interval = (time_list[-1] - time_list[-N]) / (N - 1)
    temp = int(60/interval)
    return temp

print('The estimated tempo is {} BPM.'.format(tempo_estimate(time_list)))
# ----------- Output --------------
# The estimated tempo is 111 BPM.