import sys
import pandas as pd
from src.sessions.session_client import get_session
from src.lib.data_client import get_datafields

s = get_session()
df = get_datafields(s, region="CHN", dataset_id="other561")
if df.empty:
    print("No fields found for other561 in CHN.")
else:
    print("Found fields:")
    print(df[['id', 'type', 'description']].head(10))
    df.to_csv("other561_fields.csv", index=False)
