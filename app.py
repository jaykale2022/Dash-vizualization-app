#app.py
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
#reading csv files
df1 = pd.read_csv("Category YoY.csv")
df2 = pd.read_csv("Maker YoY.csv")
df3 = pd.read_csv("Category QoQ.csv")
df4 = pd.read_csv("Maker QoQ.csv")

#removing ',' from the rows of every dataset and removing gap
for col in df1.columns[1:]:
    df1[col] = df1[col].astype(str).str.replace(",", "").astype(int)
for col in df2.columns[1:]:
    df2[col] = df2[col].astype(str).str.replace(",", "").astype(int)
for col in df3.columns[1:]:
    df3[col] = df3[col].astype(str).str.replace(",", "").astype(int)
for col in df4.columns[1:]:
    df4[col] = df4[col].astype(str).str.replace(",", "").astype(int)
# Reshape wide → long format
df_longCY = df1.melt(
    id_vars="Category YoY",
    value_vars=["2021", "2022", "2023", "2024", "2025"],
    var_name="Year",
    value_name="Total Vehicles Registered"
)
df_longMY = df2.melt(
    id_vars="Maker YoY",
    value_vars=["2021", "2022", "2023", "2024", "2025"],
    var_name="Year",
    value_name="Total Vehicles Registered"
)
df_longCQ = df3.melt(
    id_vars="Category QoQ",
    value_vars=["JAN", "FEB", "MAR", "APR", "MAY", "JUN","JUL","AUG","SEP","OCT","NOV","DEC"],
    var_name="Month",
    value_name="Total Vehicles Registered"
)
df_longMQ = df4.melt(
    id_vars="Maker QoQ",
    value_vars=["JAN", "FEB", "MAR", "APR", "MAY", "JUN","JUL","AUG","SEP","OCT","NOV","DEC"],
    var_name="Month",
    value_name="Total Vehicles Registered"
)
# df_longC["Year"] = df_longC["Year"].astype(int)
# Clean column names (remove spaces, lowercase for matching)
clean_Ccolumns = {col.strip().lower(): col for col in df1.columns}
df1.columns = [col.strip() for col in df1.columns]

clean_Mcolumns = {col.strip().lower(): col for col in df2.columns}
df2.columns = [col.strip() for col in df2.columns]

# Try to find Category column
category_col= []
for key, original in clean_Ccolumns.items():
    if "category" in key:
        category_col = original 
        break

# Try to find Maker column
maker_col= []
for key, original in clean_Mcolumns.items():
    if "maker" in key:
        maker_col = original
        break
# Get unique values safely
categories = sorted(df1[category_col].dropna().unique()) if category_col else []
makers = sorted(df2[maker_col].dropna().unique()) if maker_col else []
# --- Create App ---
app = Dash(__name__, external_stylesheets=["/assets/style.css"])

# --- Layout ---
app.layout = html.Div(className="page-wrapper", children=[

    # Top Bar
    html.Div(className="top-bar", children=[
        html.Div(["YoY Growth: ", html.Span("+12%", id="yoy-value")],id="pctY"),
        html.Div(["QoQ Growth: ", html.Span("+3%", id="qoq-value")],id="pctQ")
    ]),

    # Content Wrapper
    html.Div(className="content-wrapper", children=[



        # Sidebar
        html.Div(id="sidebar", children=[
            html.H3("Filters"),
       
            # Date Range
            # html.Div(className="filter-group", children=[
            #     html.Label("Date Range"),
            #     dcc.DatePickerRange(
            #         id='date-range',
            #         display_format='YYYY-MM-DD'
            #     )
            # ]),
html.Label("Select Filter Type for YoY graph:"),
dcc.Dropdown(
    id='filter_typeY',
    options=[
        {"label": "Category YoY", "value": "Category YoY"},
        {"label": "Maker YoY", "value": "Maker YoY"}
    ],
    value="Category",   # default selection
    clearable=False
),
html.Label("Select Value for YoY graph:"),
dcc.Dropdown(
    id='filter_valueY',
    options=[],   # will be filled dynamically in a callback
    value=None,
    clearable=False
),
html.Label(" Start Year:"),
    dcc.Dropdown(
        id="start_dateG",
        options=[{"label": int(y), "value": int(y)} for y in sorted(df_longCY["Year"].unique())],
        value=int(df_longCY["Year"].min()),
        clearable=False
    ),

             html.Label(" End Year:"),
               dcc.Dropdown(
        id="end_dateG",
        options=[{"label": int(y), "value": int(y)} for y in sorted(df_longCY["Year"].unique())],
        value=int(df_longCY["Year"].max()),
        clearable=False
    ),
html.Label("Select Filter Type for QoQ graph:"),
dcc.Dropdown(
    id='filter_typeQ',
    options=[
        {"label": "Category QoQ", "value": "Category QoQ"},
        {"label": "Maker QoQ", "value": "Maker QoQ"}
    ],
    value="Category",   # default selection
    clearable=False
),
html.Label("Select Value for QoQ graph:"),
dcc.Dropdown(
    id='filter_valueQ',
    options=[],   # will be filled dynamically in a callback
    value=None,
    clearable=False
),
#provided date filtering panel with yearly filters
 
#provided date filtering panel with monthly filters               
         html.Label(" Start Month:"),
    dcc.Dropdown(
        id="start_monthG",
        options=[{"label": y, "value":y} for y in df_longCQ["Month"].unique()],
        value="Jan",
        clearable=False
    ),

             html.Label(" End Month:"),
               dcc.Dropdown(
        id="end_monthG",
        options=[{"label": y, "value": y} for y in df_longCQ["Month"].unique()],
        value="Dec",
        clearable=False
    )        
          
        ]),
    
        # Graph Container
        html.Div(className="graph-container",children=[
             # Graph section (to replace old placeholder)
            
              
              
                
        
    
 
    # html.Div(id="graph-containerY"),
    # html.Div(id="graph-containerQ"),
    dcc.Graph(id="trend_graphY"),
    dcc.Graph(id="trend_graphQ"),
    # Percentage change text
    html.Div(id='percent_change1', children=[],style={'fontSize': 18, 'marginTop': 20}),
    html.Div(id='percent_change2', children=[],style={'fontSize': 18, 'marginTop': 20})

    ]),
    ]),
])
    
print(categories)
# --- Run App ---



@app.callback(
    [Output("trend_graphY", "figure"),
     Output("pctY","children"),
    Input("filter_typeY", "value"),
     Input("filter_valueY", "value"),
     Input("start_dateG", "value"),   # assuming numeric year (2021–2025)
     Input("end_dateG", "value")
    #  Input("end_dateG", "value"),
    #  Input("end_dateG", "value")
     ]  # same
)






def update_graph(filter_type, filter_value, start_year, end_year):
    # filter dataset depending on type
   
    print("start_year:", type(start_year), start_year)
    print("end_year:", type(end_year), end_year)
    print("Year dtype:", df_longCY["Year"].dtype)

    if filter_type == "Category YoY":
        df_longCY["Year"] = pd.to_numeric(df_longCY["Year"], errors="coerce").astype("Int64")
        dff = df_longCY[(df_longCY["Category YoY"] == filter_value)]
        dff["Year"] = pd.to_numeric(dff["Year"], errors="coerce").astype("Int64")
       
    elif filter_type == "Maker YoY":
        df_longMY["Year"] = pd.to_numeric(df_longMY["Year"], errors="coerce").astype("Int64")
        dff = df_longMY[(df_longMY["Maker YoY"] == filter_value)]
        dff["Year"] = pd.to_numeric(dff["Year"], errors="coerce").astype("Int64")
       
    else:
        dff = df_longCY.copy()
   
 
    print(dff)
    dff = dff[dff["Year"].astype(int).between(start_year,end_year)]
    
    
    # build figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dff["Year"], y=dff["Total Vehicles Registered"],
        mode='lines+markers',
        name=filter_value
    ))
    fig.update_layout(
        title=f"Total Vehicles Registered YoY basis ({filter_type}: {filter_value})",
        xaxis_title="Year",
        yaxis_title="Total Vehicles Registered"
    )

    # percentage change
    if not dff.empty:
        first_val = dff["Total Vehicles Registered"].iloc[0]
        last_val = dff["Total Vehicles Registered"].iloc[-1]
        pct_change = ((last_val - first_val) / first_val) * 100 if first_val != 0 else 0
        pct_text = f"YoY Growth ({start_year} → {end_year}): {pct_change:.2f}%"
    else:
        pct_text = "No data in this range."

    return fig, pct_text

@app.callback(
    [Output("trend_graphQ", "figure"),
     Output("pctQ","children"),
    Input("filter_typeQ", "value"),
     Input("filter_valueQ", "value"),
     Input("start_monthG", "value"),   # assuming numeric year (2021–2025)
     Input("end_monthG", "value")
     ]  # same
)



def update_graph(filter_type, filter_value, start_month, end_month):


    if  filter_type == "Category QoQ":
        
        dff = df_longCQ[(df_longCQ["Category QoQ"] == filter_value)]
        
    elif filter_type == "Maker QoQ":
      
        dff = df_longMQ[(df_longMQ["Maker QoQ"] == filter_value)]
        
    else:
        dff = df_longCQ.copy()
   
    # crop by year
    
    dff = dff[dff["Month"].between(start_month,end_month)]

    # build figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dff["Month"], y=dff["Total Vehicles Registered"],
        mode='lines+markers',
        name=filter_value
    ))
    fig.update_layout(
        title=f"Total Vehicles Registered QoQ basis({filter_type}: {filter_value})",
        xaxis_title="Month",
        yaxis_title="Total Vehicles Registered"
    )

    # percentage change
    if not dff.empty:
        first_val = dff["Total Vehicles Registered"].iloc[0]
        last_val = dff["Total Vehicles Registered"].iloc[-1]
        pct_change = ((last_val - first_val) / first_val) * 100 if first_val != 0 else 0
        pct_text = f"QoQ Growth ({start_month} → {end_month}): {pct_change:.2f}%"
    else:
        pct_text = "No data in this range."

    return fig, pct_text
# Populate filter_value options dynamically AND set a default value
@app.callback(
    [Output("filter_valueY", "options"),
     Output("filter_valueY", "value")],
    Input("filter_typeY", "value")
)
def set_filter_options(filter_typeY):
    if filter_typeY == "Category YoY":
        opts = [{"label": c, "value": c} for c in df_longCY["Category YoY"].unique()]
    elif filter_typeY == "Maker YoY" and "Maker YoY" in df_longMY.columns:
        opts = [{"label": m, "value": m} for m in df_longMY["Maker YoY"].unique()]
    else:
        opts = []
    # return options and set first option as default value
    return opts, (opts[0]["value"] if opts else None)

@app.callback(
    [Output("filter_valueQ", "options"),
     Output("filter_valueQ", "value")],
    Input("filter_typeQ", "value")
)
def set_filter_options(filter_typeQ):
    if filter_typeQ == "Category QoQ":
        opts = [{"label": c, "value": c} for c in df_longCQ["Category QoQ"].unique()]
    elif filter_typeQ == "Maker QoQ" and "Maker QoQ" in df_longMQ.columns:
        opts = [{"label": m, "value": m} for m in df_longMQ["Maker QoQ"].unique()]
    else:
        opts = []
    # return options and set first option as default value
    return opts, (opts[0]["value"] if opts else None)



if __name__ == '__main__':
    app.run(debug=True)






  