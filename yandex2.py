from collections import deque

def seq (num_elements_required):
    initial_values = [0, 1, 2]
    yield from initial_values

    running_seq = deque(initial_values, maxlen=3)

    nums_elements_yielded = len(initial_values)

    for _ in range(nums_elements_yielded, num_elements_required):
        new_elem = running_seq[-1] + running_seq[-3]
        running_seq.append(new_elem)
        yield new_elem


