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
    html.Div([
        html.Label("Choose Parental Level of Education:"),
        dcc.Dropdown(
            id="parent-edu-dropdown",
            options=[{"label": "All", "value": "ALL"}] + [
                {"label": level, "value": level} for level in df["parental level of education"].unique()
            ],
            value="ALL"
        ),
        dcc.Graph(id="boxplot-parent-edu")
    ], className="graph-container"),

    # Heatmap subject selector + heatmap

    html.Div([
        html.Label("Select Subject for Correlation Heatmap:"),
        dcc.Dropdown(
            id="heatmap-subject-dropdown",
            options=[
                {"label": "Math Score", "value": "math score"},
                {"label": "Reading Score", "value": "reading score"},
                {"label": "Writing Score", "value": "writing score"}
            ],
            value="math score"
        ),
        dcc.Graph(id="correlation-heatmap")
    ], className="graph-container")
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

@app.callback(
    Output("boxplot-parent-edu", "figure"),
    Input("parent-edu-dropdown", "value")
)
def update_parent_edu_boxplot(selected_edu):
    if selected_edu == "ALL":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["parental level of education"] == selected_edu]

    melted_df = pd.melt(
        filtered_df,
        id_vars=["parental level of education"],
        value_vars=["math score", "reading score", "writing score"],
        var_name="subject",
        value_name="score"
    )

    fig = px.box(
        melted_df,
        x="subject",
        y="score",
        title="Score Distribution by Subject (Based on Parental Education)",
        points="all"
    )
    return fig

#  Callback: update heatmap
@app.callback(
    Output("correlation-heatmap", "figure"),
    Input("heatmap-subject-dropdown", "value")
)
def update_heatmap(selected_subject):
    df_corr = df.copy()

    df_corr["gender"] = df_corr["gender"].astype("category").cat.codes
    df_corr["race/ethnicity"] = df_corr["race/ethnicity"].astype("category").cat.codes
    df_corr["parental level of education"] = df_corr["parental level of education"].astype("category").cat.codes
    df_corr["lunch"] = df_corr["lunch"].astype("category").cat.codes
    df_corr["test preparation course"] = df_corr["test preparation course"].astype("category").cat.codes

    correlations = df_corr.corr()[[selected_subject]].sort_values(by=selected_subject, ascending=False)

    fig = px.imshow(
        correlations,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title=f"Correlation with {selected_subject.title()}"
    )
    return fig

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
