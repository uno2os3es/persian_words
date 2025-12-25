import numpy as np
import time


# Example Fitness function (replace with your own logic)
def Fitness_multi(x):
    """
    x: population matrix (Camel_Caravan x Dim)
    Returns:
        Fit: array of fitness values
        x_best: best solution vector
        ind: indices sorted by fitness
    """
    # Example: Sphere function (sum of squares)
    Fit = np.sum(x**2, axis=1)
    ind = np.argsort(Fit)
    x_best = x[ind[0], :]
    return Fit[ind], x_best, ind


def camel_algorithm():
    x_min, x_max = -32, 32
    Dim = 10
    RUN = 1
    Total_Journey_Steps = 1000
    Camel_Caravan = 50
    Visibility = 0.1
    Tmin, Tmax = 30, 60

    Fit_opt = np.zeros(RUN)

    for run in range(RUN):
        best_iter = 1
        # Initial population
        x_old = (x_max - x_min) * np.random.rand(Camel_Caravan, Dim) + x_min
        Fit, x_best, ind = Fitness_multi(x_old)
        Fit_old = Fit[0]
        old_best = x_best
        x_old = x_old[ind, :]
        v = np.random.rand(Camel_Caravan)

        # Iterations
        for i in range(1, Total_Journey_Steps + 1):
            T = np.random.uniform(Tmin, Tmax, (Camel_Caravan, Dim))
            End = 1 - (T - Tmin) / (Tmax - Tmin)
            x = np.zeros_like(x_old)

            for j in range(Camel_Caravan):
                if v[j] > Visibility:
                    x[j, :] = x_old[j, :] + End[j, :] * (old_best - x_old[j, :])
                else:
                    x[j, :] = (x_max - x_min) * np.random.rand(Dim) + x_min

            Fit, x_best, ind = Fitness_multi(x)

            if Fit[0] < Fit_old:
                best_iter = i
                old_best = x_best
                Fit_old = Fit[0]

            x_old = x
            v = np.random.rand(Camel_Caravan)

        Best_Iter = best_iter
        X_best = x_best
        Fit_opt[run] = Fit_old

    Best_Cost = Fit_opt
    return Best_Cost, X_best, Best_Iter


if __name__ == '__main__':
    start = time.time()
    Best_Cost, X_best, Best_Iter = camel_algorithm()
    print('Best Cost:', Best_Cost)
    print('Best Solution:', X_best)
    print('Best Iteration:', Best_Iter)
    print('Elapsed time:', time.time() - start)
