'''layout.py'''
import dash
from dash import html, dcc, dash_table

class Layout:
    def __init__(self, nutrition_db, dd1_options):
        self.nutrition_db = nutrition_db
        self.dd1_options = dd1_options

    def create_layout(self):

        menu_data = self.nutrition_db.copy()
        menu_data['Select'] = False

        layout = html.Div([
            dcc.Dropdown(
                id='dd1',
                options=self.dd1_options,
                value=None,
                multi=False,
                clearable=False
            ),
            html.Div(id='output-container-dd1'),
            
            dcc.Dropdown(
                id='dd2',
                options=[],              
                value=None,             
                multi=False,            
                clearable=False
            ),
            html.Div(id='output-container-dd2'),

            dcc.Input(
                id='portion-input', 
                type='number', 
                placeholder='Enter portion', 
                value=1
            ),

            html.Button("Add to Menu", id="add-to-menu-btn"),
            html.Button("Calculate totals and append ", id="calculate-totals-btn"),
            
            html.Div(id="menu-container", children=[
                dash_table.DataTable(
                    id='menu-table',
                    columns=[
                        # {"name": "Select", "id": "Select", "presentation": "dropdown"},
                        # {"name": "Index", "id": "Index", "editable": False},
                        {"name": "Description 1", "id": "description_1", "editable": False},
                        {"name": "Description 2", "id": "description_2", "editable": False},
                        {"name": "Portion", "id": "portion", "editable": True},
                        {"name": "calories", "id": 'calories'},
                        {"name": "carb", "id": "carb"},
                        {"name": "fat", "id":"fat"},
                        {"name": "protein", "id": "protein"},
                        {"name": "fiber", "id": "fiber"},
                        {"name": "GI", "id": "GI"},
                    ],
                    data = [],  #this avoids displaying the nutrition_db on the screen
                    row_deletable = True),

            html.Div([
                dcc.RadioItems(
                    id='json-type',
                    options=[{'label': 'Meals', 'value': 'meals'},
                        {'label': 'Recipes', 'value': 'recipes'}
                    ],
                    value='meals', #default value
                    labelStyle={'display': 'inline-block'}
                )
            ])
            ]   )
    ])
         
        return layout
    
