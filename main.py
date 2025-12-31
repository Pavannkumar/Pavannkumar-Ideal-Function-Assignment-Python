import pandas as pd
import numpy as np
import math
from sqlalchemy import create_engine
from exceptions import DataValidationError, MappingError
from visualization import visualize
# Base function class
class BaseFunction:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def deviation(self, other_y):
        return abs(self.y - other_y)

#  a training function used for least-squares fitting
class TrainingFunction(BaseFunction):
    def max_deviation(self, ideal_y):
        return abs(self.y - ideal_y).max()


#  an ideal reference function
class IdealFunction(BaseFunction):
    def squared_error(self, training_y):
        return ((training_y - self.y) ** 2).sum()


#  a test data point.
class TestFunction(BaseFunction):
    def is_assignable(self, ideal_y, max_dev):
        return abs(self.y - ideal_y) <= max_dev




# Main Logic
def main():
    try:
        # Load datasets
        training_df = pd.read_csv("train.csv")
        ideal_df = pd.read_csv("ideal.csv")
        test_df = pd.read_csv("test.csv")

        if training_df.empty or ideal_df.empty or test_df.empty:
            raise DataValidationError("One or more datasets are empty")

        # Create SQLite database
        engine = create_engine("sqlite:///functions.db")

        training_df.to_sql("training_data", engine, if_exists="replace", index=False)
        ideal_df.to_sql("ideal_functions", engine, if_exists="replace", index=False)

        
        # Select best ideal functions
        chosen_ideals = []
        max_deviations = []

        for train_col in ["y1", "y2", "y3", "y4"]:
            min_error = float("inf")
            best_ideal = None
            max_dev = 0

            for i in range(1, 51):
                ideal_col = f"y{i}"
                error = ((training_df[train_col] - ideal_df[ideal_col]) ** 2).sum()

                if error < min_error:
                    min_error = error
                    best_ideal = i
                    max_dev = abs(training_df[train_col] - ideal_df[ideal_col]).max()

            chosen_ideals.append(best_ideal)
            max_deviations.append(max_dev)

        
        # Map test data
        mapped_rows = []

        for _, row in test_df.iterrows():
            x_val = row["x"]
            y_val = row["y"]

            for idx, ideal_idx in enumerate(chosen_ideals):
                ideal_y = ideal_df.loc[ideal_df["x"] == x_val, f"y{ideal_idx}"]

                if ideal_y.empty:
                    continue

                delta = abs(y_val - ideal_y.values[0])

                if delta <= max_deviations[idx] * math.sqrt(2):
                    mapped_rows.append({
                        "x": x_val,
                        "y": y_val,
                        "delta_y": delta,
                        "ideal_function": ideal_idx
                    })
                    break

        if not mapped_rows:
            raise MappingError("No test data could be mapped")

        test_mapping_df = pd.DataFrame(mapped_rows)
        test_mapping_df.to_sql("test_mapping", engine, if_exists="replace", index=False)

        
        # Visualization     
        visualize(training_df, ideal_df, test_mapping_df, chosen_ideals)

        print("Program executed successfully")
        print("Database created: functions.db")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
