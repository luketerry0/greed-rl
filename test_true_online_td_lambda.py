import multiprocessing 
import itertools
from online_td_lambda import TrueOnlineTDLambda
import pandas as pd
import numpy as np

# tests online_td_lambda with various params

alpha_values = [0.1, 0.25, 0.5, 0.75, 0.9]
gamma_values = [0.9, 1]
lambda_values = [0.1, 0.5, 0.9]
epsilon_values = [0.1, 0.01]

processes = []

q = multiprocessing.Queue()
processes = []
rets = []


for params in itertools.product(alpha_values, gamma_values, lambda_values, epsilon_values):
    alpha, gamma, _lambda, epsilon = params
    agent = TrueOnlineTDLambda(GAMMA=gamma, ALPHA=alpha,EPSILON=epsilon,LAMBDA=_lambda)

    p = multiprocessing.Process(target=agent.evaluate, args=(10, q))
    processes.append(p)
    p.start()
    "starting process..."

for p in processes:
    ret = q.get() # will block
    rets.append(ret)

for p in processes:
    p.join()

# compile results
df = pd.DataFrame(columns=["mean", "sd", "alpha", "gamma", "epsilon", "lambda"])

for run in rets:
    run_df = pd.DataFrame({"mean": [np.mean(run[0])], "sd": [np.std((run[1]))], "alpha": [run[2]], "gamma": [run[3]], "epsilon": [run[4]], "lambda": [run[5]]})
    df = pd.concat([df, run_df], ignore_index=True)
    df.to_csv("test.csv")
print(df)
