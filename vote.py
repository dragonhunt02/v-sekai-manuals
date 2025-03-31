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
