import multiprocessing 
import itertools
from MC import MC
import pandas as pd
import numpy as np

# tests online_td_lambda with various params

alpha_values = [0.1, 0.25, 0.5, 0.75, 0.9]
gamma_values = [0.9, 1]
epsilon_values = [0.1, 0.01]

processes = []

q = multiprocessing.Queue()
processes = []
rets = []


for params in itertools.product(gamma_values, epsilon_values):
    gamma, epsilon = params
    agent = MC(gamma=gamma, epsilon=epsilon)

    p = multiprocessing.Process(target=agent.evaluate, args=(10000, q))
    processes.append(p)
    p.start()
    "starting process..."

for p in processes:
    ret = q.get() # will block
    rets.append(ret)

for p in processes:
    p.join()

# compile results
df = pd.DataFrame(columns=["mean", "sd", "gamma", "epsilon"])

for run in rets:
    run_df = pd.DataFrame({"mean": [np.mean(run[0])], "sd": [np.std((run[1]))], "gamma": [run[2]], "epsilon": [run[3]]})
    df = pd.concat([df, run_df], ignore_index=True)
    df.to_csv("mc_10000_runs.csv")
print(df)
