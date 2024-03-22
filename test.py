import numpy as np
import pandas as pd
from TD import TD

# test various model parameter values for the sarsa model
epsilon_values = [0.1, 0.075, 0.05] 
gamma_values = [1, 0.9, 0.5, 0.25]
alpha_values = [0.1, 0.5, 0.9]

df = pd.DataFrame(columns=["epsilon", "gamma", "alpha", "mean", "sd"])

for epsilon in epsilon_values:
    for gamma in gamma_values:
        for alpha in alpha_values:
            # run simulation
            e = TD(alpha=alpha, gamma=gamma, epsilon=epsilon)
            data = e.train(1000, save_name="TD_folder/%s %s %s" % (alpha, gamma, epsilon), verbose=False)

            # append to df
            df.loc[len(df.index)] = [epsilon, gamma, alpha, data[0], data[1]]
            print("completed run with alpha %s gamma %s epsilon %s" % (alpha, gamma, epsilon))



print(df)
df.to_csv("./TD_data")

# run the simulations for 