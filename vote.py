from pathlib import Path
import pandas as pd

import starvote
from starvote import hashed_ballots_tiebreaker
import json
from collections import defaultdict

folder_path = Path('./roadmap/votes')
csv_files = folder_path.glob('*.csv')

ballot_list = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    ballot = df.set_index('Task')['Vote'].to_dict()
    ballot_list.append(ballot)

print(ballot_list)

# Vote
seats = 1

results = starvote.election(
    method=starvote.star if seats < 2 else starvote.allocated,
    ballots=ballot_list,
    seats=seats,
    tiebreaker=hashed_ballots_tiebreaker,
    maximum_score=100,
)

print(json.dumps(results, indent=4))

aggregated_values = defaultdict(list)

for ballot in ballot_list:
    for key, value in ballot.items():
        aggregated_values[key].append(value)

# Step 2: Compute the average for each key and store in a dictionary
averages = {key: round(sum(values) / len(values)) for key, values in aggregated_values.items()}
averages_df = pd.DataFrame(list(averages.items()), columns=["Task", "Priority"])
averages_df.set_index("Task", drop=False, inplace=True)

print(averages_df.to_string(index=False, header=False))

print("Averages for each key:", averages)

tasks_df = pd.read_csv("./roadmap/tasks.csv")
tasks_df["Priority"] = 0
tasks_df.set_index("Task", drop=False, inplace=True)

tasks_df.update(averages_df)

print(averages_df)
print(tasks_df)
