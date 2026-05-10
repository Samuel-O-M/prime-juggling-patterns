# oeis.py
# Generate b-format files from cached prime pattern data for OEIS submission.
# Writes b_{seq_name}_10000.txt files to data/ for the 10,000 term upload.
# Usage: python oeis/oeis.py

import os
import json


def main():
    # Setup paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, "data")
    data_file = os.path.join(data_dir, "patterns_data.json")

    if not os.path.exists(data_file):
        print(f"Error: Could not find data file at {data_file}")
        return

    # Load the cached JSON data
    with open(data_file, "r") as f:
        data = json.load(f)

    # The four sequences to generate b-files for
    sequences = [
        "normal_2ball",
        "multiplex_2ball",
        "colored_2ball",
        "base_state_2ball",
    ]

    for seq_name in sequences:
        if seq_name in data:
            seq_data = data[seq_name]

            # Sort keys mathematically (1, 2, 3... instead of "1", "10", "2")
            sorted_ns = sorted(seq_data.keys(), key=lambda x: int(x))

            # Write b-file format for the massive 10,000 term upload
            bfile_path = os.path.join(data_dir, f"b_{seq_name}_10000.txt")
            with open(bfile_path, "w") as f:
                for n in sorted_ns:
                    f.write(f"{n} {seq_data[n]}\n")

            print(f"Generated {bfile_path}")
        else:
            print(f"Warning: Sequence '{seq_name}' not found in {data_file}")


if __name__ == "__main__":
    main()
