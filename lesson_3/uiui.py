with open(input()) as f:
    datafirst = f.readlines()

with open(input()) as f:
    datasecond = f.readlines()

color = input()

for i in datafirst:
    if i.split()[-1] == color:
        color = int(i.split()[0])
        break

output = []

for i in datasecond[int(color) - 1].split():
    try:
        output.append(datafirst[int(i) - 1].split()[-1])

    except IndexError:
        output = ['Error']
        break

with open('regards.txt', 'w') as f:
    f.write('\n'.join(output))
