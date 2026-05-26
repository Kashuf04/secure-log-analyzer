from collections import defaultdict

# SPLIT PHASE
def split_data(lines, chunk_size=2):

    chunks = []

    for i in range(0, len(lines), chunk_size):

        chunks.append(lines[i:i + chunk_size])

    return chunks


# MAP PHASE
def map_function(chunk):

    mapped = []

    for line in chunk:

        parts = line.strip().split()

        if len(parts) < 4:
            continue

        try:
            # Extract hour
            time_part = parts[1]
            hour = time_part.split(":")[0]

            mapped.append((f"Hour_{hour}", 1))

            # Extract status code
            status_code = parts[-1]

            if status_code in ['404', '500']:

                mapped.append((status_code, 1))

        except:
            continue

    return mapped


# SHUFFLE PHASE
def shuffle_function(mapped_data):

    shuffled = defaultdict(list)

    for key, value in mapped_data:

        shuffled[key].append(value)

    return shuffled


# REDUCE PHASE
def reduce_function(shuffled_data):

    reduced = {}

    for key, values in shuffled_data.items():

        reduced[key] = sum(values)

    return reduced


# COMPLETE MAPREDUCE PROCESS
def run_mapreduce(filepath):

    with open(filepath, 'r') as file:

        lines = file.readlines()

    # Split
    chunks = split_data(lines)

    # Map
    mapped_results = []

    for chunk in chunks:

        mapped_results.extend(map_function(chunk))

    # Shuffle
    shuffled = shuffle_function(mapped_results)

    # Reduce
    reduced = reduce_function(shuffled)

    return reduced