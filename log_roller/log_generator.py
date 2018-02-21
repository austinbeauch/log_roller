import random

f = open('log_1.log', 'w+')

time_dict = {'h': '04', 'm': '20', 's': '00'}
level = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
obj = ['Mainframe', 'Server', 'CPU', 'Battery', 'Human']
measurement = ['voltage', 'current', 'capacitance', 'love']

dx = 1
for i in range(100000):
    time_dict['s'] = str("0" + str(int(time_dict['s']) + 1)) if int(time_dict['s']) < 9 \
        else str(int(time_dict['s']) + dx)
    if int(time_dict['s']) == 99:
        time_dict['s'] = '00'
        time_dict['m'] = str("0" + str(int(time_dict['m']) + 1)) if int(time_dict['m']) < 9 \
            else str(int(time_dict['m']) + dx)
        if time_dict['m'] == '60':
            time_dict['m'] = '00'
            time_dict['h'] = str("0" + str(int(time_dict['h']) + 1)) if int(time_dict['h']) < 9 \
                else str(int(time_dict['h']) + dx)
            if time_dict['h'] == '24':
                time_dict['h'] = '00'
    time = "{}:{}.{}".format(time_dict['h'], time_dict['m'], time_dict['s'])
    output = '{}|{}|{}_{}: {}\n'.format(time,
                                        random.choice(level),
                                        random.choice(obj),
                                        random.choice(measurement),
                                        round(random.random()*10, 3))
    f.write(output)

f.close()
