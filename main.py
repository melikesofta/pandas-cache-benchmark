import pandas as pd
import numpy as np
import pyarrow as pa
import datetime
import redis


from time import time

redisClient = redis.Redis(host='localhost', port=6379, db=0)
context = pa.default_serialization_context()


def write_df(key, df, method='redis-pyarrow', **kwargs):
    if method == 'redis-pyarrow':
        redisClient.set(key, context.serialize(
            df).to_buffer().to_pybytes(), **kwargs)

    if method == 'pickle':
        df.to_pickle('''/tmp/{file_name}.pkl'''.format(file_name=key))

    if method == 'csv':
        df.to_csv('''/tmp/{file_name}.csv'''.format(file_name=key))

    if method == 'hdf':
        df.to_hdf('''/tmp/{file_name}.h5'''.format(file_name=key), key='df')


def read_df(key, method='redis-pyarrow', **kwargs):
    if method == 'redis-pyarrow':
        return context.deserialize(redisClient.get(key))

    if method == 'pickle':
        return pd.read_pickle('''/tmp/{file_name}.pkl'''.format(file_name=key))

    if method == 'csv':
        return pd.read_csv('''/tmp/{file_name}.csv'''.format(file_name=key))

    if method == 'hdf':
        return pd.read_hdf('''/tmp/{file_name}.h5'''.format(file_name=key))


def generate_df(size='small'):
    if size == 'small':
        print('------ generating very small DF')
        return pd.DataFrame(np.random.rand(288, 144) * 100)

    print('------ generating big DF with floating numbers as values')

    return pd.DataFrame(np.random.rand(288000, 144) * 100)


def benchmark(method):
    print('--- benchmarking ' + method)
    t1 = time()

    write_df('small-df', df_small, method=method)
    t2 = time()
    print('''------ Small data - Write with {method}: {delta}'''.format(
        method=method, delta=t2-t1)
    )
    read_df('small-df', method=method)
    t3 = time()
    print('''------ Small data - Read with {method}: {delta}'''.format(
        method=method, delta=t3-t2)
    )

    write_df('big-df', df_big, method=method)
    t4 = time()
    print('''------ Big data - Write with {method}: {delta}'''.format(
        method=method, delta=t4-t3)
    )
    read_df('big-df', method=method)
    t5 = time()
    print('''------ Big data - Read with {method}: {delta}'''.format(
        method=method, delta=t5-t4)
    )


if __name__ == "__main__":
    print('--- preparing data')
    df_small = generate_df()
    df_big = generate_df(size='big')

    [benchmark(method)
     for method in ['redis-pyarrow', 'pickle', 'csv', 'hdf']]
