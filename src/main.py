import os
import re

LOG_DIRECTORY = 'logs/'
x2 = 0
NCORES = 3


def stats(tot, number, volt):
    """
    Calculates running x mean, along with variance from running total of square x values

    :param tot: total battery voltages for mean
    :param number: total amount of voltages collected
    :param volt: new input voltage
    :return: x average, varaince
    """
    global x2
    x_bar = tot / number
    x2 += volt**2
    try:
        # variance with accuracy of <= 1e-12, as compared to against np.variance
        var = ((x2/number) - x_bar**2)
    except ZeroDivisionError:
        var = 0

    return x_bar, var


def parser(filename):
    """
    Parses a textfile in search of battery current information

    :param filename: File to be parsed
    :return:
    """
    maximum = 0
    log_data = open(filename, 'r')
    for line in log_data:
        m = re.search('current: (\d+\.\d*)', line)
        if m is None:
            continue  # no battery information in this line
        voltage = float(m.group(1))
        if voltage > maximum:
            maximum = voltage

    return maximum


def downloader(filename):
    """
    Stored files on my UVic web space. Downloads with wget and moves to /logs directory.
    Of course this would be changed if an actual server was specified

    :param filename: Full filename for downloading
    """
    if not os.path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)
    os.system('wget https://web.uvic.ca/~austinb/%s' % filename)
    os.rename(filename, 'logs/%s' % filename)


def worker(f):
        # downloader line can be excluded as files are stored locally.
        downloader(f)
        log_file = LOG_DIRECTORY + f
        return parser(log_file)


if __name__ == '__main__':
    log_numbers = [1]
    count = 0
    total = 0
    ave = 0
    variance = 0
    async_result = None
    for i in log_numbers:
        file = 'log_{}.log'.format(i)
        maxi = worker(file)
        count += 1
        total += maxi
        ave, variance = stats(total, count, maxi)
    print("Current average: {} ; Current variance: {}".format(ave, variance))
