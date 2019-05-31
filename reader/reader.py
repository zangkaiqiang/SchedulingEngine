import pandas as pd
import ast
from engine.engine import engine


def read():
    df = pd.read_sql('select service_id,attr from caring_plan_item', engine)
    df['attr'] = df['attr'].apply(lambda x: ast.literal_eval(x))

    df['expect_from'] = df.attr.apply(lambda x: x['expect_from'])
    df['expect_to'] = df.attr.apply(lambda x: x['expect_to'])
