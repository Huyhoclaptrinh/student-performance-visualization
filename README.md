# Students Performance Dashboard

This interactive dashboard provides insights into how student demographics and test preparation activities relate to exam performance in math, reading, and writing. It’s built with Dash and Plotly for a rich, interactive experience.

## Features

- **Overview Tab**: Introduction and navigation.
- **Analysis Tab**:
  - **Average Score Range Slider**: Filter students by their average exam score.
  - **Bar Chart**: Compare average scores by gender.
  - **Box Plot**: Visualize score distributions by parental education level.
  - **Heatmap**: Show average scores by parental education **vs.** test preparation status, with selectable subjects.
- **Interactive Controls**: Dropdown filters for gender, parental education, and subject selection.
- **Custom Styling**: Applied via `assets/styles.css` for consistent look and feel.(Will update)

## Project Structure

```
student-performance-visualization/
├── app.py                           # Main Dash application
├── assets/
│   └── styles.css                   # Custom CSS
├── data/
│   ├── StudentsPerformance.csv      # Raw dataset
│   └── StudentsPerformance_clean.csv# Cleaned dataset
├── notebooks/
│   └── 01-explore-data.ipynb        # Data exploration notebook
├── pages/
│   ├── overview.py                  # Overview page layout
│   └── analysis.py                  # Analysis page layout and callbacks
├── utils/
│   └── data_processing.py           # Data cleaning script
├── environment.yml                  # Conda environment spec
└── README.md                        # This file
```

## Environment Setup

### Using Conda (Recommended)

1. Create the environment:

Active the base to use conda:

```bash
path\to\anaconda3\Scripts\activate 
```

For me is: C:\Users\admin\anaconda3\Scripts\activate on Window. Just insert the path include activate, enter and then you can use conda.

```bash
conda env create -f environment.yml
```

2. Activate it:

```bash
conda activate students_dash
```

## Running the Dashboard

1. Ensure the cleaned data is available:

   ```bash
   python utils/data_processing.py
   ```

2. Launch the app:

   ```bash
   python pages\analysis.py
   ```

3. Open your browser and navigate to:

   ```
   http://127.0.0.1:8050/
   ```

## Notes

- The dashboard automatically loads custom CSS from the `assets/` folder.
- Update `StudentsPerformance_clean.csv` whenever you change cleaning logic.

---
*Created with guidance from ChatGPT*
