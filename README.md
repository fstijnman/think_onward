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
