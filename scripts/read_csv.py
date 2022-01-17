from network.models import NetworkEdge, NetworkNode
import pandas as pd

def read_csv():
    G_df = pd.read_csv('got-edges.csv')
    N_df = pd.read_csv('got-nodes.csv')
    return G_df, N_df

def to_sql(df):
    for row in df:
        _, created = NetworkEdge.objects.get_or_create(
            Source=row[0],
            Target=row[1],
            Weight=row[2],
        )

if __name__ =="__main__":
    G, N = read_csv()
    to_sql(G)

