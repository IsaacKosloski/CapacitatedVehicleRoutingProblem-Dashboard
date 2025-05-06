import statistics

class StatisticsCalculator:
    def compute(self, values):
        import numpy as np

        if not values:
            return None

        values = np.array(values)
        mean = values.mean()
        std_dev = values.std()
        min_val = values.min()
        max_val = values.max()
        median = np.median(values)
        range_val = max_val - min_val
        coeff_var = std_dev / mean if mean != 0 else 0

        return {
            "mean": mean,
            "std_dev": std_dev,
            "min": min_val,
            "max": max_val,
            "median": median,
            "range": range_val,
            "coeff_var": coeff_var
        }

