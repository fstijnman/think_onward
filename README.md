# Dynamic Rhythms Challenge

### Date started: 2025-02-15

From [the challenge](https://thinkonward.com/app/c/challenges/dynamic-rhythms):

(In a nutshell) *Your task is to design a model that can effectively forecast future weather impacts on power outages. You're free to explore and experiment with various algorithms, techniques, and models to achieve accurate results.*

# Notes

## Data

There's two datasets from the challenge itself, A. Power Outages, and B. NOAA's Storm Events. All from 2014 - 2023.

### A. Power Outage Dataset

For each year, `eaglei_outages_YYYY.csv` there is the 15-minute interval data of # customers affected by a power outage per county.

| id  | fips_code | county  | state   | customers_out | run_start_time      |
| --- | --------- | ------- | ------- | ------------- | ------------------- |
| 0   | 1003      | Baldwin | Alabama | X             | 2023-01-01 00:00:00 |
|     | 1003      | Baldwin | Alabama | X             | 2023-01-01 00:15:00 |

There's some helper functions in `utils.py` provided to visualize this data.
- `plot_outages_on_map_us` - per state on a map plot
- `plot_outages_on_map_state` - per county on a map plot
- `plot_outages_ts_states` - for multiple state in time series plot
- `plot_outages_ts_years` - for one state in time series plot

### B. NOAA's Storm Events Dataset

Again, per year `StormEvents_details-ftp_v1.0_d{YYYY}_{some_id}.csv`. Here we find a begin datetime and end datetime per event.

### C. Free (and encouraged) to explore other datasets

- *NOAA's storm events dataset is public, and you can download additional datasets for longer periods. We encourage you to do so to build more robust and accurate predictive models. Additionally, NOAA's database is just one of many public datasets on storm events. We encourage you to explore other **public** datasets on storm events, power outages, meteorological weather data, and any other data you find useful for predicting storm events and power outages.*
- Some ideas on public datasets:
  - power infrastructure
  - population density

# Starter notebook

### Insights

- *In summary, when assessing the impact of storm events on power outages, it's essential to consider not just the frequency of events but also their type, severity, and duration. These factors are critical in understanding and predicting the potential disruptions to power systems.*

# Approach

- What would I define as success? From the challenge:
  - *A good model should not only capture whether and where an outage occurs, but also predict it sufficiently early to allow proactive measures. Moreover, modeling the severity and duration of outages is essential for assessing potential impacts on communities.*
  - *When designing your performance metrics, consider that a single metric may not capture all of these dimensions. You might combine specialized metrics for rare-event classification (e.g., precision-recall for imbalanced data) with lead-time accuracy (e.g., mean time-to-event error) and severity predictions (e.g., error in forecasted duration or number of customers affected). You should also incorporate location accuracy for geospatially precise predictions. Ultimately, your goal is to develop a well-rounded evaluation that reflects how reliably and how early your model can forecast significant power outages.*
- What's a good baseline?

# Scientific Research

> [A Deep Learning-Based Method for Power System Resilience Evaluation](https://arxiv.org/pdf/2501.04830)

From the paper:

*To study power system characteristics under disruptive events, two concepts, reliability and resilience, have been proposed:*
- **Reliability**: Reliability emphasizes adequacy and security. Adequacy refers to the uninterrupted power supply, ensuring continuous service to end-users, while security is the capability to withstand unexpected disruptions, such as sudden power loss caused by component failure and adverse weather.
- **Resilience**: Resilience relates to the system’s capability to maintain power supply during highly disruptive events, such as hurricanes, earthquakes, flooding, and cyberphysical attacks.

Reliability typically addresses high-probability, low-impact (HPLI)
events, whereas resilience focuses on low-probability, high-impact (LPHI) events.

# Miscellaneous notes for later

- These events are rare
- What's the timeframe for which we need to predict? Days, weeks? At the time of the weather impact itself?
- What causes a power outage irt weather? What causes extreme weather events?
  - Causally: extreme weather events -> extreme weather -> power outage
- I found this in a [description](https://smc-datachallenge.ornl.gov/eagle/) of Eaglei data: *This dataset has been collected from utility’s public outage maps using an ETL process. Note that the number of “customers” does not necessarily equate to the number of people affected, as a “customer” reported by a utility could be one meter, one building, etc. Also included is the coverage of each state for each year included in the dataset.*

# Loading data

Im using duckdb to ingest the csvs and speed things up.

# Explorative Data Analysis

### Findings:
- `customers_out`: this can contain 0's and nulls, indicating that there would either be data missing or no apparent outage
- `run_start_time`: I feel there could be missing data around new years for some counties. In the top 10 in terms of duration, I see two counties that have a start time on the 1st of January at `2022-01-01 00:00:00`. Need to check if thats a coincidence.

| county      | state      | customers_out | run_start_time      |
| ----------- | ---------- | ------------- | ------------------- |
| Los Angeles | California | 5894          | 2021-12-31 00:00:00 |
| Los Angeles | California | 6677          | 2022-01-01 00:00:00 |


### Duration Analysis:

1. Find the longest consecutive outage in a single county (tracking same customer count)

| state         | county       | start_time          | end_time            | min_customers | max_customers | avg_customers | duration          |
| :------------ | :----------- | :------------------ | :------------------ | ------------: | ------------: | ------------: | :---------------- |
| Massachusetts | Hampden      | 2022-01-01 00:00:00 | 2022-08-23 18:30:00 |             1 |         23142 |       215.161 | 234 days 18:30:00 |
| California    | Los Angeles  | 2022-05-31 13:30:00 | 2022-10-18 23:00:00 |             1 |         93099 |       2027.89 | 140 days 09:30:00 |
| California    | Los Angeles  | 2020-07-12 11:15:00 | 2020-10-20 10:45:00 |             1 |         65931 |       2349.69 | 99 days 23:30:00  |
| New Jersey    | Morris       | 2022-05-15 11:45:00 | 2022-08-19 17:15:00 |             4 |         27353 |       132.137 | 96 days 05:30:00  |
| Arkansas      | Arkansas     | 2022-05-07 05:15:00 | 2022-08-02 17:45:00 |             1 |          1787 |       24.6571 | 87 days 12:30:00  |
| California    | Los Angeles  | 2022-01-01 00:00:00 | 2022-03-25 11:00:00 |             1 |         35499 |       1775.54 | 83 days 11:00:00  |
| Texas         | Harris       | 2019-07-27 19:00:00 | 2019-10-19 05:45:00 |             1 |         36534 |       1621.72 | 83 days 10:45:00  |
| California    | Los Angeles  | 2022-10-19 00:45:00 | 2023-01-08 15:00:00 |             1 |         25236 |        1914.1 | 81 days 14:15:00  |
| Louisiana     | St. Mary     | 2019-07-27 19:00:00 | 2019-10-08 20:15:00 |             4 |           387 |       9.63202 | 73 days 01:15:00  |
| Pennsylvania  | Philadelphia | 2022-04-20 00:00:00 | 2022-06-27 07:45:00 |             4 |          4988 |       105.379 | 68 days 07:45:00  |

2. Find the median duration of outages per county
3. Identify counties that frequently have outages lasting more than 2 hours
4. Calculate the average duration of outages across different states

### Geographic Hotspots:

1. Find the top 5 states with most outage events
2. Find the top 10 counties with most frequent outages
3. Identify states where multiple counties have simultaneous outages
4. Calculate the percentage of counties affected within each state

### Scale Impact:

1. Find incidents where over 1000 customers were affected
2. Rank counties by total customer-hours of outages
3. Identify the maximum number of customers affected in a single outage
4. Calculate average number of customers affected per state

### Time Patterns:

1. Find the hour of day with most outage starts
2. Identify which day of week has most outages
3. Calculate percentage of outages that start during night hours (10PM-6AM)
4. Find months with highest outage frequencies

### Pattern Analysis:

1. Identify counties that have regular patterns (same time each day)
2. Find counties with "flickering" patterns (multiple short outages)
3. Calculate the average time between repeated outages in same county
4. Identify if specific counties always have outages of similar size

# Evaluation Framework

### Metrics

Some options:
- Event classification (if there will be an outage)
- Lead time accuracy (how long will the outage last)
- Severity prediction (how many people are affected by the outage)
- Location precision (where exactly is the outage) < I expect that we would already make a per state prediction

### Baseline

Some options:
- Historical average for the same period: over all 10 years
- Seasonal Naive: from last year, month, or week? Or combined?
- Persistence model: most recent value

