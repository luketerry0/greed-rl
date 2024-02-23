import numpy as np
import pandas as pd
from sarsa import SARSA

# test various model parameter values for the sarsa model
epsilon_values = [0.1, 0.01, 0.0001]
gamma_values = [1, 0.9]
alpha_values = [0.1, 0.01, 0.0001]
score_discount_factor_values = [(1/1000000), (1/100000), (1/10)]

df = pd.DataFrame(columns=["epsilon", "gamma", "alpha", "sdf", "mean", "sd"])

for epsilon in epsilon_values:
    for gamma in gamma_values:
        for alpha in alpha_values:
            for sdf in score_discount_factor_values:
                # run simulation
                e = SARSA(alpha=alpha, gamma=gamma, epsilon=epsilon, score_discount_factor=sdf)
                data = e.train(100000, save_name="old/%s %s %s %s" % (alpha, gamma, epsilon, sdf), verbose=False)

                # append to df
                df.loc[len(df.index)] = [epsilon, gamma, alpha, sdf, data[0], data[1]]
                print("completed run with alpha %s gamma %s epsilon %s sdf %s" % (alpha, gamma, epsilon, sdf))



print(df)
df.to_csv("./simulation_data")

# run the simulations for 