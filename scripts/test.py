

def parse_tas_input(file_content):
    lines = file_content.split('\n')
    
    # Check if the file is empty
    if not lines:
        print("Error: The input file is empty.")
        return []

    # Parse the key mappings
    try:
        key_mapping_line = next(line for line in lines if line.startswith('LogKey:'))
        key_mapping = key_mapping_line.split(':')[1].strip('#').split('|')
    except StopIteration:
        print("Error: Could not find 'LogKey:' line in the input file.")
        return []
    except IndexError:
        print("Error: 'LogKey:' line is not in the expected format.")
        return []
    
    inputs = []
    input_started = False
    for line in lines:
        
        if line == '[Input]':
            input_started = True
            continue
        if line == '[/Input]':
            break
        if input_started and line.startswith('|') and line.endswith('|'):
            frame_input = []
            for i, char in enumerate(line[1:-1]):  # Exclude the first and last '|'
                if char != '.' and i < len(key_mapping):
                    frame_input.append(key_mapping[i])
            inputs.append(tuple(frame_input))

    return inputs
with open('Input Log.txt', 'r') as file:
            file_content = file.read()
inputs = parse_tas_input(file_content)
print (inputs[220])