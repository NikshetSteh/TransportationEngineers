import json


def get_key(item):
    if isinstance(item, dict):
        # if 'id' in item:
            # return item['id']
        if 'authenticator' in item:
            return item['authenticator']
        elif 'identity' in item:
            return item['identity']
        elif 'name' in item:
            return item['name']
        elif 'clientScope' in item:
            return item['clientScope']
        elif 'client' in item:
            return item['client']
        elif 'flowAlias' in item:
            return item['flowAlias']
        elif 'alias' in item:
            return item['alias']
        else:
            print(item)
            raise Exception('No key found')
        # elif 'users' in item:
        #     return item['users']
        # else:
        #     print(item)

    return item


def sort_arrays_in_json(data):
    """
    Recursively traverse the JSON data and sort all arrays.
    """
    if isinstance(data, list):
        # If the current element is a list, sort it and recursively process its elements
        # try:
        if len(data) > 1:
            data.sort(key=get_key)
        # except Exception as e:
        #     print(data)
        # Recursively process each item in the list
        for item in data:
            sort_arrays_in_json(item)
    elif isinstance(data, dict):
        # If the current element is a dictionary, recursively process its values
        for key, value in data.items():
            data[key] = sort_arrays_in_json(value)
    return data


def sort_json_file(input_file, output_file):
    """
    Reads a JSON file, sorts all arrays within it, and writes the sorted JSON to an output file.
    """
    try:
        # Read the input JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Sort all arrays in the JSON data
        sorted_data = sort_arrays_in_json(data)

        # Write the sorted JSON data to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(sorted_data, file, indent=4, ensure_ascii=False)

        print(f"All arrays have been sorted and saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{input_file}' contains invalid JSON.")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")


# Example usage
if __name__ == "__main__":
    input_file = "input.json"  # Replace with your input JSON file path
    output_file = "output.json"  # Replace with your desired output JSON file path
    sort_json_file(input_file, output_file)