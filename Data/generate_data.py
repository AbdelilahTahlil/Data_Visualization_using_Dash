'''
Generate fake data
'''

# pylint: disable=invalid-name

import datetime
import uuid
import random as rd

from faker import Faker
import pandas as pd


num_pipelines = 4000

data = pd.DataFrame(
    [],
    columns= ['Pipeline_id', 'Lab', 'Level', 'Pipeline_status', 'Assessment',
        'Number_of_ODT_Win', 'Number_of_ODT_Linux', 'Num_build_impact_Win',
        'Num_build_impact_Linux', 'Num_server_impact', 'Server_impact','SSR_Eligible', 'Date']
)
for i in range(num_pipelines) :
    pipeline_id = uuid.uuid4()
    lab = rd.choice(['Paris', 'Los Angeles', 'Marrakech', 'New Delhi', 'London'])
    level = rd.choice(['v1', 'v2', 'v3', 'v4'])
    pipeline_status = rd.choice(['Success', 'Warning', 'Aborted'])
    assessment = rd.choice(['GO', 'GOIF', 'NOGO'])
    number_of_odt_win = rd.randrange(3000)
    number_of_odt_linux = rd.randrange(2100)
    num_build_impact_win = rd.randrange(1,200)
    num_build_impact_linux = rd.randrange(1,150)
    num_server_impact = rd.randrange(20)
    if num_server_impact == 0:
        server_impact = False
        ssr_eligible = 'No server impact'
    else :
        server_impact = True
        ssr_eligible = rd.choice(['SSR Eligible', 'Full reinstall'])
    date = Faker().date_between(
        start_date=datetime.date(year=2021, month=1, day=1),
        end_date=datetime.date(year=2021, month=12, day=31)
    )

    data.loc[i] = [
        pipeline_id, lab, level, pipeline_status, assessment, number_of_odt_win,
        number_of_odt_linux, num_build_impact_win, num_build_impact_linux,
        num_server_impact, server_impact, ssr_eligible, date
    ]

data.to_csv('Data/data.csv', encoding='utf-8', sep=';', index=False)
