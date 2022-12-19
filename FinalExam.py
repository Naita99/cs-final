#Library
import os
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
import bs4
from bs4 import BeautifulSoup
import requests


#QUESTION 1

# from sqlalchemy import MetaData
# from sqlalchemy_schemadisplay import create_schema_graph

# graph = create_schema_graph(metadata=MetaData('sqlite:///hr.db'),
#                             show_datatypes=False,  
#                             show_indexes=False,  
#                             rankdir='LR',
#                             concentrate=False  
#                             )

# graph.write_png('Question_1.png')  



#QUESTION 2

connection = sqlite3.connect('hr.db')
df = pd.read_sql_query('select * from employees;', connection)

data_connected = pd.read_sql("SELECT employees.first_name, jobs.job_title " +
                                "FROM employees " + 
                                "INNER JOIN jobs ON employees.job_id " + 
                                "= jobs.job_id",connection)


app = Dash(__name__)
server =  app.server


jobs=pd.read_sql_query("select * from jobs;", connection)
jobs = jobs.iloc[1: , :]
jobs["difference"]=jobs['max_salary']-jobs['min_salary']
job=jobs[['job_title','difference']]
max_salary=job['difference'].max()



image2 = go.Figure()
image2 = px.bar(data_connected, x='job_title',color="job_title")



#QUESTION 3

@app.callback(
Output('image3', 'figure'),
Input('input3', 'value')
)

def update_output(value):
    minimum=value[0]
    maximum=value[-1]
    image3 = go.Figure()
    image3["layout"]["xaxis"]["title"] = "The difference between maximum and minimum of each job salarie"
    image3["layout"]["yaxis"]["title"] = "Types of job"
    t = job[job["difference"]>=minimum][job["difference"]<=maximum]
    image3.add_trace(go.Bar(x=t['difference'], y=t['job_title'],
    name='Job differences',  orientation="h"))
    return image3

#QUESTION 4

def scrape_data():
    URL = "https://www.itjobswatch.co.uk/jobs/uk/sqlite.do"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib') 
    table = soup.find('table', attrs = {'class':'summary'}) 
    table.find('form').decompose()
    table_data = table.tbody.find_all("tr")
    table = []
    for i in table_data:
        row = []
        rrr = i.find_all("td")
        if len(rrr) == 0:
            rrr = i.find_all("th")
        for j in rrr:
            row.append(j.text)
        table.append(row)

    hd = table[1]
    hd[0] = "index"
    employee_sal = pd.read_sql("SELECT employees.salary " +
                                "FROM employees",connection)
    avg_salary = employee_sal['salary'].mean()
    df = pd.DataFrame(table)
    df.drop(index=[0,1,2,3,4,5,6,7,10,11,14,15],axis=0,inplace=True)
    df.columns = hd
    df.set_index("index",inplace=True)
    df.reset_index(inplace=True)
    df['Same period 2021'] = df['Same period 2021'].str.replace('£','')
    df['Same period 2021'] = df['Same period 2021'].str.replace(',','')
    df['Same period 2021'] = df['Same period 2021'].str.replace('-','0').astype(float)
    df['6 months to19 Dec 2022'] = df['6 months to19 Dec 2022'].str.replace('£','')
    df['6 months to19 Dec 2022'] = df['6 months to19 Dec 2022'].str.replace(',','').astype(float)
    df['Same period 2020'] = df['Same period 2020'].str.replace('£','')
    df['Same period 2020'] = df['Same period 2020'].str.replace(',','').astype(float)

    df.loc[4] = ['Average', avg_salary, avg_salary,avg_salary] 

    return df

forth = scrape_data()

axis = forth["index"]
forth.drop("index",inplace=True,axis=1)
years = forth.columns


def update_dataframe3(year):
    return forth[year]


app.layout = html.Div(
    children=[
        html.Div(className="main",
            children=[
                    html.H1(children='Computer Science Final Exam', className="header"),
                    html.P(children = "Exercise 1 - Use the HR sqlite database available on https://www.w3resource.com/sqlite-exercises/, search for a solution to produce the diagram of the database using python. Do not invent solutions, search for existing solutions and try to present a fairly readable database diagram", className="question",),
                        html.Img(id='picture', src=app.get_asset_url('Question_1.png'), className="picture"),

                    html.P(children = "Exercise 2 - Present a bar chart with the number of employees with the same job. Use Plotly-Dash to make your bar chart dynamic and allow the user to choose the job titles to be seen in the char", className="question",),
                        dcc.Graph(id='image2', figure=image2, className="dashboard"),
                    
                     html.P(children = "Exercise 3 - Present a horizontal bar chart with the difference between the maximum and minimum of each job salaries. Make it dynamic by using a scale over salary. The scale can be visual or can be as 2 input boxes as min and max", className="question",),
                        dcc.RangeSlider(0, max_salary, 1000, value=[0, max_salary], id="input3"),
                        dcc.Graph(id="image3",className="dashboard"),

                    html.P(children = "Exercise 4 - Find the average salary. Then automatically go to https://www.itjobswatch.co.uk/jobs/uk/sqlite.do site and read 3 camps of 10 th Percentile, 20th Percentile, 75th Percentile, 90th Percentile. This should be done by using scrapping methods (beatifulsoup, selenium, etc) Plot a scatter chart where the average salary of your database is shown in black, and the 12numbers read from the 3 columns are shown in green. Make it dynamic in function of year.", className="question",),
   
                    html.P(children = "Exercise 4 - Find the average salary. Then automatically go to https://www.itjobswatch.co.uk/jobs/uk/sqlite.do site and read 3 camps of 10 th Percentile, 20th Percentile, 75th Percentile, 90th Percentile. This should be done by using scrapping methods (beatifulsoup, selenium, etc) Plot a scatter chart where the average salary of your database is shown in black, and the 12numbers read from the 3 columns are shown in green. Make it dynamic in function of year.", className="question1",),
                        dcc.Dropdown(years,
                             
                             value='all',
                             placeholder="Select Period",
                             id="years", className="dropdown"
                             ),
                        dcc.Graph(id='image4',className="dashboard")]
    )
            ],
            style={
                'backgroundColor':'#F5F5F5',
                'text-align':'center',
                'margin':'0',
            }
            )

app.css.append_css({
    "external_url":"http://"
})


@app.callback(
        Output('image4', 'figure'),
        Input('years', 'value')
        )
def update_output(value1):
    if value1 == "all" or value1 == None:
        y = forth["6 months to19 Dec 2022"]
    else:
        y =update_dataframe3(value1)
    image4 = go.Figure()
    image4.add_trace(go.Scatter(x=axis.values,y=y.values))
    
    return image4


if __name__ == '__main__':
    app.run_server("0.0.0.0", debug=False, port=int(os.environ.get('PORT', 8000)))
server = app.server
