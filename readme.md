# COVID-19 Dashboard - India (2020)

This is a COVID-19 dashboard for India built using Dash, a Python framework for building analytical web applications. It provides visualizations and statistics related to COVID-19 cases in India, including total cases, active cases, recoveries, and deaths, along with age distribution and state-wise analysis.

## Features

- **Total Cases:** Displays the total number of COVID-19 cases in India.
- **Active Cases:** Shows the current number of active cases.
- **Recovered Cases:** Displays the total number of recovered cases.
- **Deaths:** Shows the total number of deaths due to COVID-19.
- **Pie Charts:** Visualizes COVID-19 status in India through pie charts.
- **Age Distribution:** Provides an age distribution of COVID-19 patients in India.
- **State-wise Analysis:** Allows users to view COVID-19 cases on a state-wise basis.
- **Interactive Graphs:** Displays interactive graphs for better data exploration.

## Usage

1. Install the required dependencies by running:
    pip install pandas numpy plotly dash

2. Run the application by executing the `app.py` file:
python app.py

3. Access the dashboard in your web browser at `http://localhost:5000`.

## External Dependencies

- [Bootstrap](https://getbootstrap.com/): External CSS stylesheet for styling.
- [Plotly](https://plotly.com/python/): Library for creating interactive plots.
- [Dash](https://dash.plotly.com/): Framework for building analytical web applications.

## Data Sources

- `data/AgeGroupDetails.csv`: Age group details of COVID-19 patients in India.
- `data/covid_19_india.csv`: COVID-19 dataset for India.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
