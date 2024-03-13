'''layout.py'''
import dash
from dash import html, dcc, dash_table

class Layout:
    def __init__(self, nutrition_db, dd1_options): #, dd2_options
        self.nutrition_db = nutrition_db
        self.dd1_options = dd1_options
        # self.dd2_options = dd2_options

    def create_layout(self):
        layout = html.Div([
            dcc.Dropdown(
                id          = 'dd1',
                options     = self.dd1_options,
                value       = None,  # Default value is None
                multi       = False,  # Single selection
                clearable   = False
            ),
            html.Div(id='output-container'),
            
            dcc.Dropdown(
                id          = 'dd2',
                options     = [],               #default
                value       = None,             # Default value is None
                multi       = False,            # Single selection
                clearable   = False
            ),
            dcc.Input(id            = 'portion-input', 
                      type          = 'number', 
                      placeholder   = 'Enter portion', 
                      value         = 1),

            html.Button("Add to Menu", id="add-to-menu-btn"),
            
            html.Div(id="menu-container", children=[
                dash_table.DataTable(
                    id='menu-table',
                    columns=[{"name": i, "id": i, "editable": True} if i == "portion" else {"name": i, "id": i, "editable": False} for i in self.nutrition_db.columns],
                    data=[]
                )
            ])
        ])
        
        return layout
