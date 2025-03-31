from pathlib import Path
import pandas as pd

import starvote
from starvote import hashed_ballots_tiebreaker
import json
from collections import defaultdict

def get_votes(votes_dir):
    folder_path = Path(votes_dir)
    csv_files = folder_path.glob('*.csv')

    ballot_list = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        ballot = df.set_index('Task')['Vote'].to_dict()
        ballot_list.append(ballot)
    print(ballot_list)
    return ballot_list

def starvote_election(ballot_list, seats=1):
    results = starvote.election(
        method=starvote.star if seats < 2 else starvote.allocated,
        ballots=ballot_list,
        seats=seats,
        tiebreaker=hashed_ballots_tiebreaker,
        maximum_score=100,
    )
    print(json.dumps(results, indent=4))
    return results

def generate_avg_table(ballot_list, tasks_path):
    aggregated_values = defaultdict(list)

    for ballot in ballot_list:
        for key, value in ballot.items():
            if not value.is_integer():
                raise Exception(f"Ballot vote {key} is not an integer")
            value = max(0, min(value, 100)) # 0-100
            aggregated_values[key].append(value)

    # Compute the average for each key and store in a dictionary
    averages = {key: round(sum(values) / len(values)) for key, values in aggregated_values.items()}
    averages_df = pd.DataFrame(list(averages.items()), columns=["Task", "Priority"])
    averages_df.set_index("Task", drop=False, inplace=True)

    print(averages_df.to_string(index=False, header=False))
    print("Averages for each key:", averages)

    tasks_df = pd.read_csv(tasks_path)
    tasks_df["Priority"] = 0
    tasks_df.set_index("Task", drop=False, inplace=True)
# drop=False,
    tasks_df.update(averages_df)
    tasks_df.sort_values(by='Priority', ascending=False, inplace=True)
    tasks_df.reset_index(drop=True)
    
    print(averages_df)
    print(tasks_df)
    return tasks_df

def run_election(votes_dir, seats, tasks_path):
    ballot_list = get_votes(votes_dir)
    starvote_winners = starvote_election(ballot_list, seats)
    avg_table = generate_avg_table(ballot_list, tasks_path)
    return {"avg_table": avg_table, "winners": starvote_winners}

run_election('./roadmap/votes', 2, "./roadmap/tasks.csv")
