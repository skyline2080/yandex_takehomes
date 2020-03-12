from itertools import tee, takewhile

def chars_are_equal(current_next_chars):
    current_char, next_char = current_next_chars
    return current_char == next_char

def char_freq_gen(it):
    try:
        it1, it2 = tee(it)
        current_char = next(it2)
        current_next_chars_it = zip(it1, it2)
        sequence_equal_chars = list(takewhile(chars_are_equal, current_next_chars_it))
        sequence_length = len(sequence_equal_chars) + 1
        
        yield current_char, sequence_length
        yield from char_freq_gen(it1)
        
    except StopIteration:
        pass

def convert_to_string(it):
    for char, freq in it:
        yield f"{char}{freq}"

def encode(string):
    return "".join(
                convert_to_string(
                    char_freq_gen(
                        string
            )
        )
    )

def test():
    string = "AAAAAAAAABBBBBBAAAAAAABBBBBCCCCCCDDDDDDEEEEEFFFFFFFFFAAAAAABBBB"
    print(string)
    print(encode(string))