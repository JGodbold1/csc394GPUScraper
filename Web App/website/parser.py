import pandas as pd

path = 'website/static/csv/gpu.csv'
results_path = 'website/static/csv/results.csv'

df = pd.read_csv(path)
df.to_csv(results_path, sep='\t', header=None, mode='a') # creates a results.csv that is cleaner and does not contain headers. It is ready to scrape.

with open(results_path) as fp: # reads results.csv into a list of split keys
    line = fp.readlines()
    for data in line:
        print(data.split())