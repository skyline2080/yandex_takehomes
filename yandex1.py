from collections import Counter

def most_common_max(values):
    counter = Counter(values)
    max_occurance = max(counter.values())
    max_occurance_values = ( 
        value for value, num_occurence in counter.items() 
            if num_occurence == max_occurance )

    return max(max_occurance_values)