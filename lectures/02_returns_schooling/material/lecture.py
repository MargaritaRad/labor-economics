#!/usr/bin/env python
""" This module allows to simulate an observed sample based on the accouting identity model."""
import statsmodels.formula.api as smf
import pandas as pd
import numpy as np

kappa = 1.0
rho_0 = 0.075
P_0 = 239.15215950404396
rho_s = 0.1250
T = 55
num_agents = 1000


def log_observed_earnings(s, x):
    """This function simulates logarithmic earnings directly from the accounting-identify model."""
    rslt = 0
    rslt += np.log(P_0) - kappa
    rslt += rho_s * s
    rslt += (rho_0 * kappa + (rho_0*kappa)/ (2 * T) + kappa / T) * x
    rslt -= (rho_0 * kappa / (2 * T)) * (x ** 2) + np.random.normal(scale=0.1)

    return rslt


def store_dataset(data, fname='data.mincer.pkl'):
    """This function stores the dataset."""
    columns = ['Identifier', 'Age', 'Earnings', 'Schooling', 'Experience']
    df = pd.DataFrame(data, columns=columns)
    df.set_index('Identifier', inplace=True)
    df.to_pickle(fname)



if __name__ == '__main__':
    #
    # data = []
    # for i in range(num_agents):
    #     s = np.random.choice(range(10, 16))
    #     x = np.random.choice(range(1, T))
    #     y = log_observed_earnings(s, x)
    #
    #     age = s + x + 6
    #
    #     data += [[i, age, np.exp(y), s, x]]
    #
    # store_dataset(data)
    from scipy.stats import norm


    eval_point, s = 1.0, 0.1

    conditional_expectation(eval_point, s)

