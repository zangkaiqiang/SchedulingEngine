import pandas as pd
import sqlalchemy
import ast

def read():
    engine = sqlalchemy.create_engine('mysql+pymysql://icare:ginkodrop@172.16.0.27:4000/dolphin-dev?charset=utf8')
    df = pd.read_sql('select service_id,attr from caring_plan_item',engine)
    df['attr'] = df['attr'].apply(lambda x:ast.literal_eval(x))

    df['expect_from'] = df.attr.apply(lambda x:x['expect_from'])
    df['expect_to'] = df.attr.apply(lambda x:x['expect_to'])
