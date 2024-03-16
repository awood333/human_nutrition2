'''app.py'''
import pandas as pd
import json
import dash
from dash import html, Input, Output, State, callback_context, dcc
from dash.exceptions import PreventUpdate
from layout import Layout

nutrition_db1 = pd.read_csv('E:\\old_F_drive\\human_nutrition\\nutrition_table.csv', index_col=None, header=0)
nutrition_db = nutrition_db1.iloc[:,:-1].copy()
numeric_columns = ['calories', 'carb', 'fat', 'protein', 'fiber', 'GI']

# unique names in description_1 column
dd1_options = [{'label': desc, 'value': desc} for desc in nutrition_db['description_1'].unique()]

app = dash.Dash(__name__)

layout = Layout(nutrition_db, dd1_options) 
app.layout = layout.create_layout()

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
    Output('output-container-dd1', 'children'),
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

# Consolidate the functionality of both callbacks into a single callback
@app.callback(
    [Output('menu-table', 'data'),
     Output('output-container-dd2', 'children')],
    [Input('add-to-menu-btn', 'n_clicks'),
     Input('calculate-totals-btn', 'n_clicks')],
    [State('portion-input', 'value'),
     State('dd2', 'value'),
     State('menu-table', 'data'),
     State('json-type', 'value')]
)
def handle_menu_operations(add_to_menu_clicks, calculate_totals_clicks,
                            portion_input, selected_row, current_data, json_type):
    ctx = callback_context

    # If neither button is clicked, prevent update
    if not ctx.triggered:
        raise PreventUpdate

    # Determine which button triggered the callback
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # add to menu
    if triggered_id == 'add-to-menu-btn' and add_to_menu_clicks:
        if selected_row is None:
            raise PreventUpdate
        
        selected_row_data = nutrition_db[(nutrition_db['description_2'] == selected_row)]
        if len(selected_row_data) == 0: 
            raise PreventUpdate
        
        selected_row_data_copy = selected_row_data.copy()

        selected_row_data_copy['portion'] = portion_input
        selected_row_data_copy.iloc[:, 3:8] *= portion_input  # Elementwise multiply col by scalar

        idx = len(current_data) + 1
        selected_row_data_copy['Index'] = idx

        updated_columns = selected_row_data_copy.iloc[:,3:8] * portion_input
        selected_row_data_copy.iloc[:,3:8] = updated_columns

        totals_row = {'Description 1': 'Total', 'Description 2': '', 
                      'Portion': '', 'calories': 0, 'carb': 0, 
                      'fat': 0, 'protein': 0, 'fiber': 0, 'GI': 0}

        current_data.append(selected_row_data_copy.iloc[0].to_dict())  # DataTable expects a JSON serializable dtype
        return current_data, None  # Return the updated menu data and no message for output container

    # Handle calculating totals and appending
    elif triggered_id == 'calculate-totals-btn' and calculate_totals_clicks:
        totals_row = calculate_totals_and_append(calculate_totals_clicks, current_data, json_type)
        return totals_row[0], html.Div(totals_row[1])

    # If no button is clicked, prevent update
    else:
        raise PreventUpdate

def calculate_totals_and_append(n_clicks, current_data, json_type):
    totals_row = {'Description 1': 'Total', 'Description 2': '', 
                  'Portion': '', 'calories': 0, 'carb': 0, 
                  'fat': 0, 'protein': 0, 'fiber': 0, 'GI': 0}

    for row in current_data:
        for col in numeric_columns:
            if col != 'Portion' and row[col] is not None:
                totals_row[col] += float(row[col])

    filename = f'{json_type}.json'
    with open(filename, 'a') as json_file:
        json.dump(current_data, json_file)

    return current_data + [totals_row], f'Appended to {json_type}.json'

if __name__ == '__main__':
    app.run_server(debug=True, port=8081)