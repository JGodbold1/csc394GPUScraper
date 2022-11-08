import pandas as pd

path = 'static/csv/gpu.csv'
results_path = 'static/csv/results.csv'

# creates a results.csv that is cleaner and does not contain headers. It is ready to scrape.
df = pd.read_csv(path)
df.to_csv(results_path, sep='\t', header=None, mode='a')

# reads results.csv into a list of split keys
with open(results_path) as fp:
    line = fp.readlines()
    # print(line)

    # Split will make it into a tuple
    # print(line[0].split())

    # Reads and prints tuples in line
    for data in line:
        print(data.split())

