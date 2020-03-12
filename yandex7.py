import collections
from itertools import takewhile

def push_creator(window_length, occurence_threshold):
    current_window = collections.deque(maxlen=window_length)
    current_window_counter = collections.Counter()
    seen_suspects = set()

    def occurence_threshold_exceeded(element_count_pair):
        _, occurence_count = element_count_pair
        return occurence_count > occurence_threshold

    def fst(seq):
        return seq[0]

    def push(item):
        if len(current_window) == current_window.maxlen:
            current_window_counter.subtract(fst(current_window))
        current_window.append(item)
        current_window_counter.update(item)

        it = takewhile(occurence_threshold_exceeded, current_window_counter.most_common())

        for suspect, _ in it:
            if suspect not in seen_suspects:
                seen_suspects.add(suspect)
                yield suspect, current_window

    return push

def suspects_gen(stream):
    push = push_creator(window_length = 10, occurence_threshold = 3)
    for item in stream:
        yield from push(item)

def test():
    import random
    stream = map(chr, (random.randint(97,102) for _ in range(1, 100)))

    for line in suspects_gen(stream):
        print(line)
