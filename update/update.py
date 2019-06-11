import pandas as pd

from engine.engine import engine

df = pd.read_sql('select * from greedy', engine)


#