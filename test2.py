import numpy as np
import pandas as pd
from MC import MC

# test various model parameter values for the sarsa model
epsilon_values = [0.1, 0.01, 0.0001]
gamma_values = [1, 0.9]

df = pd.DataFrame(columns=["epsilon", "gamma", "mean", "sd"])

for epsilon in epsilon_values:
    for gamma in gamma_values:
        # run simulation
        e = MC(gamma=gamma, epsilon=epsilon)
        data = e.train(100, save_name="jose/%s %s" % (gamma, epsilon), verbose=False)
        # append to df
        df.loc[len(df.index)] = [epsilon, gamma, data[0], data[1]]
        print("completed run with gamma %s epsilon %s" % (gamma, epsilon))



print(df)
df.to_csv("./simulation_data")

# run the simulations for