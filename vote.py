from pathlib import Path
import pandas as pd

folder_path = Path('./roadmap/votes')
csv_files = folder_path.glob('*.csv')

ballot_list = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    ballot = df.set_index('Task')['Vote'].to_dict()
    
    # Use csv_file.stem to extract the file name without its extension and store in the list
    ballot_list.append(ballot)

print(ballot_list)
