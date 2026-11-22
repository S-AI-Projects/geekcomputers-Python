__author__ = "vamsi"

try:
    import pandas as pd  # pandas library to read csv file
except ImportError:
    pd = None

try:
    from matplotlib import pyplot as plt  # matplotlib library to visualise the data
    from matplotlib import style

    style.use("ggplot")
except ImportError:
    plt = None


def read_from_csv(filepath=r"..\SalesData.csv", show_plot=False):
    """Reads SalesData CSV file, extracts coordinate vectors, and visualizes sales.

    Decisive State Transition:
        Transforms raw serialized CSV text on disk into structured tabular rows
        within a pandas DataFrame, then projects the distinct 'SalesID' and
        'ProductPrice' series into discrete numeric coordinate arrays (x, y) for
        trend plotting.

    Preconditions (source citations from ReadFromCSV.py baseline):
        - Line 2: `import pandas as pd` loads tabular processing engine.
        - Line 11: `df = pd.read_csv(...)` ingests CSV data from disk.
        - Lines 12-14: `x = df['SalesID']` extracts identifier axis.
        - Line 15: `y = df['ProductPrice']` extracts metric axis.
        - Lines 16-20: Configures labels, title, and renders visualization.

    Args:
        filepath (str): Path to CSV data file.
        show_plot (bool): If True, invokes `plt.show()`. Default False for headless runs.

    Returns:
        dict: Processed intermediate and output data:
            {"df": DataFrame, "x": list, "y": list}
    """
    if pd is None:
        raise RuntimeError("pandas is required to run read_from_csv")

    df = pd.read_csv(filepath)

    x = [int(v) for v in df["SalesID"].tolist()]
    y = [float(v) for v in df["ProductPrice"].tolist()]

    if show_plot and plt is not None:
        plt.xlabel("SalesID")
        plt.ylabel("ProductPrice")
        plt.title("Sales Analysis")
        plt.plot(x, y)
        plt.show()

    return {"df": df, "x": x, "y": y}


# Alias for exact matching with issue title
ReadFromCSV = read_from_csv


def main():
    read_from_csv(filepath=r"..\SalesData.csv", show_plot=True)


if __name__ == "__main__":
    main()
