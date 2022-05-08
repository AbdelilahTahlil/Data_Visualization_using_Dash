'''
Generate fake data
'''

# pylint: disable=invalid-name

import datetime
import uuid
import random as rd
from multiprocessing import Pool


from faker import Faker
import pandas as pd



num_pipelines = 40



data = pd.DataFrame(
    [[None]*13]*num_pipelines,
    columns= ['Pipeline_id', 'Lab', 'Level', 'Pipeline_status', 'Assessment',
        'Number_of_ODT_Win', 'Number_of_ODT_Linux', 'Num_build_impact_Win',
        'Num_build_impact_Linux', 'Num_server_impact', 'Server_impact','SSR_Eligible', 'Date']
)

def generate_id(x) :
    return uuid.uuid4()

test = Pool().map(generate_id, data.Pipeline_id)
data['Pipeline_id'] = test
'''data['Lab'] = Pool().map(lambda x: rd.choice(['Paris', 'Los Angeles', 'Marrakech', 'New Delhi', 'London']), data.Lab)
data['Level'] = Pool().map(lambda x: rd.choice(['v1', 'v2', 'v3', 'v4']), data.Level)
data['Pipeline_status'] = Pool().map(lambda x: rd.choice(['Success', 'Warning', 'Aborted']), data.Pipeline_status)
data['Assessment'] = Pool().map(lambda x: rd.choice(['GO', 'GOIF', 'NOGO']), data.Assessment)
data['Number_of_ODT_Win'] = Pool().map(lambda x: rd.randrange(3000), data.Number_of_ODT_Win)
data['Number_of_ODT_Linux'] = Pool().map(lambda x: rd.randrange(2100), data.Number_of_ODT_Linux)
data['Num_build_impact_Win'] = Pool().map(lambda x: rd.randrange(1,200), data.Num_build_impact_Win)
data['Num_build_impact_Linux'] = Pool().map(lambda x: rd.randrange(1,150), data.Num_build_impact_Linux)
data['Num_server_impact'] = Pool().map(lambda x: rd.randrange(20), data.Num_server_impact)
data['Server_impact'] = Pool().map(lambda x: False if x ==0 else True, data.Num_server_impact)
data['SSR_Eligible'] = Pool().map(lambda x: 'No server impact' if x ==0 else rd.choice(['SSR Eligible', 'Full reinstall']), data.Num_server_impact)
data['Date'] = Pool().map(lambda x: Faker().date_between(
    start_date=datetime.date(year=2021, month=1, day=1),
    end_date=datetime.date(year=2021, month=12, day=31)), data.Date)'''

print(data)

'''
data['Pipeline_id'] = Pool().map(lambda x: uuid.uuid4(), data.Pipeline_id)
data['Lab'] = Pool().map(lambda x: rd.choice(['Paris', 'Los Angeles', 'Marrakech', 'New Delhi', 'London']), data.Lab)
data['Level'] = Pool().map(lambda x: rd.choice(['v1', 'v2', 'v3', 'v4']), data.Level)
data['Pipeline_status'] = Pool().map(lambda x: rd.choice(['v1', 'v2', 'v3', 'v4']), data.Pipeline_status)
data['Assessment'] = Pool().map(lambda x: rd.choice(['GO', 'GOIF', 'NOGO']), data.Assessment)
data['Number_of_ODT_Win'] = Pool().map(lambda x: rd.randrange(3000), data.Number_of_ODT_Win)
data['Number_of_ODT_Linux'] = Pool().map(lambda x: rd.randrange(2100), data.Number_of_ODT_Linux)
data['Num_build_impact_Win'] = Pool().map(lambda x: rd.randrange(1,200), data.Num_build_impact_Win)
data['Num_build_impact_Linux'] = Pool().map(lambda x: rd.randrange(1,150), data.Num_build_impact_Linux)
data['Num_server_impact'] = Pool().map(lambda x: rd.randrange(20), data.Num_server_impact)
data['Server_impact'] = Pool().map(lambda x: False if x ==0 else True, data.Num_server_impact)
data['SSR_Eligible'] = Pool().map(lambda x: 'No server impact' if x ==0 else rd.choice(['SSR Eligible', 'Full reinstall']), data.Num_server_impact)
data['Date'] = Pool().map(lambda x: Faker().date_between(
    start_date=datetime.date(year=2021, month=1, day=1),
    end_date=datetime.date(year=2021, month=12, day=31)), data.Date)


data.to_csv('Data/data.csv', encoding='utf-8', sep=';', index=False)'''
