import pandas as pd
from json import load

with open('data.json', 'r') as f:
    data = load(f)
    df = pd.io.json.json_normalize(data)
    print(df)
    df.to_excel('sunp_0-2043.xlsx', index=True, sheet_name='data')
