import pandas as pd

from scheduling.ga_scheduling import evaluate_delay
from engine.engine import engine

df = pd.read_sql('select * from ga_scheduling', engine)
print(evaluate_delay(df))
