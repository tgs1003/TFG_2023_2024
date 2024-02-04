import pandas as pd
import os
def convert(filename):
    # Reading JSON data from a file
    with open(filename) as f:
        json_data = f.read()

    # Converting JSON data to a pandas DataFrame
    df = pd.read_json(json_data)

    # Writing DataFrame to a CSV file
    df.to_csv(filename + ".csv", index=False)


files = [f for f in os.listdir() if not os.path.isdir(f) and f.endswith('json')]
for file in files:
    convert(file)