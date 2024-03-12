import pandas as pd
import dash
from dash import Input, Output, State, html, dcc, callback_context, dash_table
from dash.exceptions import PreventUpdate

nutrition_db1 = pd.read_csv('E:\\old_F_drive\\human_nutrition\\nutrition_table.csv', index_col=None, header=0)
nutrition_db = nutrition_db1.iloc[:,:-1].copy()

app = dash.Dash(__name__)

# Dropdown options for dd1
dd1_options = [{'label': desc, 'value': desc} for desc in nutrition_db['description_1'].unique()]

# Initial empty options for dd2
dd2_options = []

# Layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='dd1',
        options=dd1_options,
        value=None,  # Default value is None
        multi=False,  # Single selection
        clearable=False
    ),
    html.Div(id='output-container'),
    
    dcc.Dropdown(
        id='dd2',
        options=dd2_options,
        value=None,  # Default value is None
        multi=False,  # Single selection
        clearable=False
    ),
    dcc.Input(id='portion-input', type='number', placeholder='Enter portion', value=1),
    html.Button("Add to Menu", id="add-to-menu-btn"),
    
    html.Div(id="menu-container", children=[
        dash_table.DataTable(
            id='menu-table',
            columns=[{"name": i, "id": i, "editable": True} if i == "portion" else {"name": i, "id": i, "editable": False} for i in nutrition_db.columns],
            data=[]
        )
    ])
])

# Update options for dd2 based on selected value from dd1
@app.callback(
    Output('dd2', 'options'),
    [Input('dd1', 'value')]
)
def update_dd2_options(selected_value):
    if selected_value is None:
        raise PreventUpdate
    
    filtered_df = nutrition_db[nutrition_db['description_1'] == selected_value]
    dd2_options = [{'label': desc, 'value': desc} for desc in filtered_df['description_2']]
    return dd2_options

# Display the selected rows in a container
@app.callback(
    Output('output-container', 'children'),
    [Input('dd1', 'value')]
)
def display_selected_rows(selected_value):
    if selected_value is None:
        raise PreventUpdate
    
    filtered_df = nutrition_db[nutrition_db['description_1'] == selected_value]
    return html.Div([
        html.H4(f"Selected rows for '{selected_value}':"),
        html.Table([
            html.Tr([html.Th(col) for col in filtered_df.columns]),
            *[
                html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns])
                for i in range(len(filtered_df))
            ]
        ])
    ])

# Add selected row from dd2 to the menu
@app.callback(
    Output('menu-table', 'data'),
    [Input('add-to-menu-btn', 'n_clicks')],
    [State('portion-input', 'value'), 
     State('dd2', 'value'),
     State('menu-table', 'data')]
)
def add_to_menu(n_clicks, portion_input, selected_row, current_data):
    if not n_clicks or selected_row is None:
        raise PreventUpdate
    
    selected_row_data = nutrition_db[(nutrition_db['description_2'] == selected_row)]
    if len(selected_row_data) == 0: 
        raise PreventUpdate
    
    selected_row_data_copy = selected_row_data.copy()

    selected_row_data_copy['portion'] = portion_input
    selected_row_data_copy.iloc[:, 3:8] *= portion_input
        
    current_data.append(selected_row_data_copy.iloc[0].to_dict())

    # print('current_data = ', current_data)



    return current_data

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
