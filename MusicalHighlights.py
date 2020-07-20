import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math


def get_peaks1(lst):
    # lst2 = sorted(lst)
    # size = len(lst)
    # minpeak, maxpeak = lst2[size // 10], lst2[size * 9 // 10]
    # print(minpeak, maxpeak)
    # stackmax = []
    # stackmin = []
    # ansmin = (0, 0)
    # ansmax = (0, 0)
    # for i in range(size):
    #     if lst[i] > maxpeak:
    #         stackmax.append(i)
    #     else:
    #         if len(stackmax) > ansmax[1] - ansmax[0]:
    #             ansmax = (stackmax[0], stackmax[-1])
    #         stackmax.clear()
    #     if lst[i] < minpeak:
    #         stackmin.append(i)
    #     else:
    #         if len(stackmin) > ansmin[1] - ansmin[0]:
    #             ansmin = (stackmin[0], stackmin[-1])
    #         stackmin.clear()
    # return ansmin, ansmax
    answer = set()

    for i in range(1, len(lst)):
        if lst[i] > lst[i - 1]:
            answer.add((-get_max(i, lst) / lst[i - 1] * (get_max(i, lst) - lst[i - 1]), i - 1))
        else:
            answer.add((lst[i - 1] / get_min(i, lst) * (get_min(i, lst) - lst[i - 1]), i - 1))
    ans2 = list(set(map(lambda x: x[1], sorted(answer)[:1])))
    ans2.sort()
    return ans2[0]


def get_max(i, lst):
    while i < len(lst) and lst[i - 1] < lst[i]:
        i += 1
    if i == len(lst):
        return lst[i - 1]
    return lst[i]


def get_min(i, lst):
    while i < len(lst) and lst[i - 1] > lst[i]:
        i += 1
    if i == len(lst):
        return lst[i - 1]
    return lst[i]


types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}


def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out


def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return float("-inf")

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)


wav = wave.open("/Users/andre/Downloads/Telegram Desktop/imagine_dragons_im_so_sorry_456454131.wav",
                mode="r")  # Path to Song
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

duration = nframes / framerate
w, h = 800, 300
k = nframes // w // 32
DPI = 72
peak = 256 ** sampwidth // 2
print(duration)
content = wav.readframes(nframes)
samples = np.frombuffer(content, dtype=types[sampwidth])

plt.figure(1, figsize=(float(w) / DPI, float(h) / DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)
answer = set()
for n in range(nchannels):
    channel = samples[n::nchannels]
    channel = channel[0::k]
    mmmm = max(channel)
    print(len(channel), channel[7000:7100], type(channel))
    if nchannels == 1:
        channel = channel - peak
    tt = int(duration)
    arr2 = [0] * tt
    psec = len(channel) // tt
    for i in range(int(duration)):
        arr2[i] = sum(map(lambda x: abs(x), channel[psec * i:psec * (i + 1)])) // tt

    for i in enumerate(arr2[:120]):
        print(i)
    moments = []
    # for i in range(1, len(arr2) - 10):
    #     if arr2[i - 1] != 0 and (get_max(i, arr2) / arr2[i - 1] > 3 / 2 or get_min(i, arr2) / arr2[i - 1] < 2 / 3):
    #         moments.append(i - 1)
    #         if arr2[i] > arr2[i - 1]:
    #             answer.add((-get_max(i, arr2) / arr2[i - 1] * (get_max(i, arr2) - arr2[i - 1]), i - 1))
    #         else:
    #             answer.add((arr2[i - 1] / get_min(i, arr2) * (get_min(i, arr2) - arr2[i - 1]), i - 1))
    for i in range(3, len(arr2) - 10):
        if arr2[i] > arr2[i - 1]:
            answer.add((-get_max(i, arr2) / arr2[i - 1] * (get_max(i, arr2) - arr2[i - 1]), i - 1))
        else:
            answer.add((arr2[i - 1] / get_min(i, arr2) * (get_min(i, arr2) - arr2[i - 1]), i - 1))

    frame = max(60, tt // 5)
    # ap = set()
    # print(tt // frame + 1)
    # anp = set()
    # for i in range(tt // frame + 1):
    #     answer.add(get_peaks1(arr2[i * frame:(i + 1) * frame]) + i * frame)

    # for i in range(tt // frame):
    #     answerplacid, answernotplacid = get_peaks1(arr2[frame // 2 + i * frame:(i + 1) * frame + frame // 2])
    #     # ap.add(answerplacid[0] + frame * i)
    #     anp.add(answernotplacid[0] + frame * i)
    # print(ap, anp)
    # answer.update(ap)
    # answer.update(anp)
    axes = plt.subplot(2, 1, n + 1)
    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()
ans2 = list(set(map(lambda x: x[1], sorted(answer)[:tt // 60 + 2])))
print(ans2)
# ans2 = list(answer)
# ans2.sort()
stack = []
for i in ans2:
    if len(stack) == 0:
        stack.append(i)
    elif len(stack) > 0 and stack[-1] - i < -5:
        stack.append(i)
print(*stack)