import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load cleaned data
df = pd.read_csv("data/StudentsPerformance_clean.csv")

# Prepare dropdown options
gender_options = [{"label": "All", "value": "ALL"}] + [{"label": g, "value": g} for g in df["gender"].unique()]

# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout with multi-page via Tabs
app.layout = html.Div([
    dcc.Tabs(id="tabs", value="overview", children=[
        dcc.Tab(label="Overview", value="overview"),
        dcc.Tab(label="Analysis", value="analysis"),
    ]),
    html.Div(id="tabs-content")
])

# Overview content
overview_layout = html.Div([
    html.H1("Students Performance Dashboard"),
    html.P(
        "This dashboard explores how demographics (gender, parental education, race/ethnicity) "
        "and test preparation affect student exam outcomes. Navigate to the Analysis tab for interactive charts."
    ),
])

# Analysis content
analysis_layout = html.Div([
    html.H1("Analysis: Demographics & Performance"),
    html.P(
        "Use the controls below to explore how gender, parental education, "
        "and test preparation relate to students’ average exam scores."
    ),

    # Gender filter + chart
    html.Div([
        html.Label("Filter by Gender:"),
        dcc.Dropdown(
            id="gender-filter",
            options=gender_options,
            value="ALL",
        ),
        dcc.Graph(id="bar-gender"),
    ], className="graph-container"),

    # Parental edu filter + box plot (DO HERE !!!!!!!)

    # Heatmap subject selector + heatmap

])

# Callback to switch tabs
@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "analysis":
        return analysis_layout
    else:
        return overview_layout

# Callback: update bar chart (removed avg-score-slider input and filtering)
@app.callback(
    Output("bar-gender", "figure"),
    Input("gender-filter", "value")
)
def update_bar_chart(selected_gender):
    if selected_gender != "ALL":
        df_gender = df[df["gender"] == selected_gender]
    else:
        df_gender = df.copy()

    avg_by_gender = (
        df_gender.groupby("gender")[['math score','reading score','writing score']].mean().reset_index()
    )

    # Promt: "Can you suggest how to reshape the aggregated DataFrame 'avg_by_gender'
    #  to plot grouped bar charts of math, reading, and writing average scores
    #  by gender using Plotly Express?"
    #
    # Response: "You can use pandas ‘melt’ to unpivot the DataFrame into long form:
    # 
    #    avg_by_gender.melt(
    #        id_vars='gender',
    #        value_vars=['math score','reading score','writing score'],
    #        var_name='subject',
    #        value_name='average score'
    #    )
    # 
    # Then feed that to Plotly Express:
    # 
    #    fig = px.bar(
    #        avg_by_gender.melt(id_vars="gender", value_vars=['math score','reading score','writing score'],
    #                           var_name="subject", value_name="average score"),
    #        x="gender", y="average score", color="subject",
    #        barmode="group", title="Average Exam Scores by Gender"
    #    )"

    fig = px.bar(
        avg_by_gender.melt(id_vars="gender", value_vars=['math score','reading score','writing score'],
                            var_name="subject", value_name="average score"),
        x="gender", y="average score", color="subject",
        barmode="group", title="Average Exam Scores by Gender"
    )
    return fig

# Callback: update box plot (DO HERE !!!!!!!)

#  Callback: update heatmap

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
