# import pandas as pd
# import bs4
# import requests
# import sqlite3
# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
# from bs4 import BeautifulSoup

# con = sqlite3.connect("hr.db")

# def scrape_data():
#     URL = "https://www.itjobswatch.co.uk/jobs/uk/sqlite.do"
#     r = requests.get(URL)
#     soup = BeautifulSoup(r.content, 'html5lib') 
#     table = soup.find('table', attrs = {'class':'summary'}) 
#     table.find('form').decompose()
#     table_data = table.tbody.find_all("tr")
#     table = []
#     for i in table_data:
#         row = []
#         rrr = i.find_all("td")
#         if len(rrr) == 0:
#             rrr = i.find_all("th")
#         for j in rrr:
#             row.append(j.text)
#         table.append(row)

#     hd = table[1]
#     hd[0] = "index"
#     employee_sal = pd.read_sql("SELECT employees.salary " +
#                                 "FROM employees",con)
#     avg_salary = employee_sal['salary'].mean()
#     df = pd.DataFrame(table)
#     df.drop(index=[0,1,2,3,4,5,6,7,10,11,14,15],axis=0,inplace=True)
#     df.columns = hd
#     df.set_index("index",inplace=True)
#     df.reset_index(inplace=True)
#     df['Same period 2021'] = df['Same period 2021'].str.replace('£','')
#     df['Same period 2021'] = df['Same period 2021'].str.replace(',','')
#     df['Same period 2021'] = df['Same period 2021'].str.replace('-','0').astype(float)
#     df['6 months to19 Dec 2022'] = df['6 months to19 Dec 2022'].str.replace('£','')
#     df['6 months to19 Dec 2022'] = df['6 months to19 Dec 2022'].str.replace(',','').astype(float)
#     df['Same period 2020'] = df['Same period 2020'].str.replace('£','')
#     df['Same period 2020'] = df['Same period 2020'].str.replace(',','').astype(float)

#     df.loc[4] = ['Average', avg_salary, avg_salary,avg_salary] 

#     return df

# forth = scrape_data()

# axis = forth["index"]
# forth.drop("index",inplace=True,axis=1)
# years = forth.columns





# def update_dataframe3(year):
#     return forth[year]


# app = Dash(__name__)
# app.layout = html.Div([
#     dcc.Dropdown(years,
                             
#                              value='all',
#                              placeholder="6 months to19 Dec 2022",
#                              id="years"
#                              ),
#         dcc.Graph(id="output3"),
# ])











# @app.callback(
#         Output('output3', 'figure'),
#         Input('years', 'value')
#         )
# def update_output(value1):
#     if value1 == "all" or value1 == None:
#         y = forth["6 months to19 Dec 2022"]
#     else:
#         y =update_dataframe3(value1)
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=axis.values,y=y.values))
    
#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)