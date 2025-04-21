import statistics

class StatisticsCalculator:
    def compute(self, costs):
        if not costs:
            return None

        mean = statistics.mean(costs)
        std = statistics.stdev(costs) if len(costs) > 1 else 0
        min_val = min(costs)
        max_val = max(costs)
        median = statistics.median(costs)
        range_ = max_val - min_val
        coeff_var = std / mean if mean != 0 else 0

        return (mean, std, min_val, max_val, median, range_, coeff_var)
