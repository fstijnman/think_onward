import duckdb
import pandas as pd
from loguru import logger


def process_state_county(conn, state, county):
    if "'" in county:
        county = county.replace("'", "''")
    query = f"""
    SELECT
        state,
        county,
        customers_out,
        run_start_time
    FROM
        eaglei_data
    WHERE
        customers_out IS NOT NULL
        AND customers_out > 0
        AND state = '{state}'
        AND county = '{county}'
    ORDER BY run_start_time
    """

    df = conn.sql(query).df()
    df["group"] = (
        df["run_start_time"]
        != df["run_start_time"].shift() + pd.Timedelta("15 minutes")
    ).cumsum()

    summary = (
        df.groupby("group")
        .agg(
            {
                "state": "first",
                "county": "first",
                "run_start_time": ["first", "last"],
                "customers_out": ["min", "max", "mean"],
            }
        )
        .reset_index()
    )

    summary.columns = [
        "group",
        "state",
        "county",
        "start_time",
        "end_time",
        "min_customers",
        "max_customers",
        "avg_customers",
    ]
    summary["duration"] = summary["end_time"] - summary["start_time"]

    return summary


def get_state_county_pairs(conn):
    query = """
    SELECT DISTINCT state, county
    FROM eaglei_data
    WHERE customers_out IS NOT NULL
    ORDER BY state, county
    """
    return conn.sql(query).df()


def process_all_data(db_path):
    results = []

    with duckdb.connect(database=db_path) as conn:
        pairs = get_state_county_pairs(conn)
        total_pairs = len(pairs)

        for idx, (_, row) in enumerate(pairs.iterrows(), 1):
            logger.info(
                f"Processing {row['state']}, {row['county']} ({idx}/{total_pairs})"
            )
            summary = process_state_county(conn, row["state"], row["county"])
            results.append(summary)

    final_summary = pd.concat(results, ignore_index=True)
    final_summary["group"] = range(len(final_summary))

    return final_summary


def main(db_path):
    outage_summary = process_all_data(db_path)
    outage_summary["minutes"] = outage_summary["duration"].dt.components["minutes"]

    outage_summary = outage_summary[
        [
            "state",
            "county",
            "start_time",
            "end_time",
            "min_customers",
            "max_customers",
            "avg_customers",
            "minutes",
        ]
    ].copy()

    with duckdb.connect(database=db_path) as conn:
        conn.sql("CREATE TABLE outage_summary AS SELECT * FROM outage_summary")


if __name__ == "__main__":
    db_path = "/Users/folkert/think_onward/data/eaglei_data.duckdb"
    main(db_path)
