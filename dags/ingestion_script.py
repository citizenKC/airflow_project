import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time
import os
 


def ingest_data(parquet_file, table_name):
    parquet_file = pq.ParquetFile(parquet_file)
    # trips = parquet_file.read().to_pandas()

    engine = create_engine("postgresql://admin:admin@de_postgres:5432/ny_taxi")

    # trips.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace", index=False)

    for batch in parquet_file.iter_batches(batch_size=100000):
        t_start = time()
        batch_df = batch.to_pandas()
        batch_df.columns = [c.lower() for c in batch_df.columns]
        batch_df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
        t_end = time()
        print("inserted next chunk in  %.3f seconds" % (t_end - t_start))
