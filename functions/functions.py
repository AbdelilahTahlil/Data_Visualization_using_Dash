"""
Functions used to process the database according to inputs
"""
from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

def update_df(csv_path):
    """
    Update the database of pipelines
    """
    # pylint: disable=unsubscriptable-object
    # pylint: disable=unsupported-assignment-operation
    # pylint: disable=invalid-name
    db = pd.read_csv(csv_path, encoding='utf-8', sep=';')
    db.set_index('Pipeline_id', inplace = True)
    db['Date'] = pd.to_datetime(db['Date']).dt.tz_localize(None)

    return db


def convert_num_to_range(list_, slices_dict) :
    """
    list_ : a list of numbers
    slices_dict: a dictionary containig as keys ranges of numbers, and as values the interval
        (as a string) corresponding. Example: {range(0,10): '[0,9]' , range(10,20): '[10,19]'}

    Returns a list of same length, where the numbers of list_ are replaced with
        the interval they belong to in slices_dict
    """
    return list(map(lambda x: get_membership_range(x, slices_dict), list_))

# Determine to wich slice a number belongs
def get_membership_range(number, slices_dict) :
    """
    Returns to which interval of the slices_dict the number belongs to
    """
    if number != number :
        return 'Null'
    if number > list(slices_dict.keys())[-1] :
        return slices_dict[list(slices_dict.keys())[-1]]
    try :
        for slice_range in slices_dict:
            if number in slice_range:
                return slices_dict[slice_range]
    except :
        print('slices_dict', slices_dict)
        print('slice_range', slice_range)
        print('number', number)
        raise


# Returns filtered DataFrame
def filter_df(df, filter_dict) :
    """
    df: dataframe
    filter_dict: dictionary containing as keys the name of columns in df to filter on,
        and as values the values to keep
    Returns a dataframe filtered according to the values of filter_dict
    """
    df_filtre_total = df.copy()
    there_is_a_filter = False
    for (col, value) in filter_dict.items() :
        if value is None or value == [] or value == 'None' or col == 'osds':
            continue

        there_is_a_filter = True
        df_filtre_selon_val = pd.DataFrame(columns=df.columns)
        if col == 'Date' :
            start_date = filter_dict['Date'][0]
            end_date = filter_dict['Date'][1]
            df_filtre_selon_val = pd.concat([df_filtre_selon_val,df[(df.Date >= start_date) &
                (df.Date <= end_date)]], axis = 0)
        elif col in ['Range_of_ODTs', 'Range_of_Build_impact'] :
            for val in value :
                df_filtre_selon_val = pd.concat([df_filtre_selon_val,
                    df[eval(f"df['{col}_({filter_dict['osds']})']") == val ]], # pylint: disable= eval-used
                    axis = 0)
        else :
            for val in value :
                df_filtre_selon_val = pd.concat([df_filtre_selon_val,
                    df[eval(f"df['{col}']") == val ]], # pylint: disable= eval-used
                    axis = 0)
        df_filtre_total = df_filtre_total.loc[
            df_filtre_total.index.intersection(df_filtre_selon_val.index)]
    if there_is_a_filter :
        return df_filtre_total.drop_duplicates()
    return df


# Display all graphs + Total Pipelines number after applying a filter
def display_interactive_chart(df, filter_dict=None, chart_type='Pie', ts_period='M', ts_subcat='None', color_blind=False):
    """
    Return all the interactive charts
    """
    if color_blind:
        # naming a layout theme for future reference
        pio.templates['color_blind'] = go.layout.Template(
            layout_colorway=['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00',
                  '#704214', '#e8000d', '#f2f0e6', '#4e82b4']
        )

        # setting color blind color palette as default
        pio.templates.default = 'color_blind'
    else :
        pio.templates.default = 'plotly'




    # Dictionaries to define slices' range for ODTs, Build Impact and server impact
    slices_dict_odts = {
        range(0,1): '0',
        range(1,51): '[1 - 50]',
        range(51,251): '[51 - 250]',
        range(251,501): '[251 - 500]',
        range(501,1001): '[501 - 1000]',
        range(1001,2001): '[1001 - 2000]',
        2000: '2001+',
    }

    slices_dict_build_impact = {
        range(1,2): '1',
        range(2,6): '[2 - 5]',
        range(6,16): '[6 - 15]',
        range(16,51): '[16 - 50]',
        range(51,101): '[51 - 100]',
        100: '101+'
    }

    slices_dict_server_impact = {
        range(0,1): '0',
        range(1,2): '1',
        range(2,6): '[2 - 5]',
        range(6,11): '[6 - 10]',
        10: '11+'
    }


    df['Range_of_Server_impact'] = convert_num_to_range(df.Num_server_impact,
        slices_dict_server_impact)
    df['Range_of_ODTs_(Win)'] = convert_num_to_range(df.Number_of_ODT_Win, slices_dict_odts)
    df['Range_of_ODTs_(Linux)'] = convert_num_to_range(df.Number_of_ODT_Linux, slices_dict_odts)
    df['Range_of_Build_impact_(Win)'] = convert_num_to_range(df.Num_build_impact_Win,
        slices_dict_build_impact)
    df['Range_of_Build_impact_(Linux)'] = convert_num_to_range(df.Num_build_impact_Linux,
        slices_dict_build_impact)

    df = filter_df(df, filter_dict)
    if ts_subcat == 'None':
        df_for_ts_figure = df.copy().loc[:,'Date'].reset_index(drop=False)

    elif ts_subcat in ['Range_of_ODTs', 'Range_of_Build_impact']:
        ts_subcat = ts_subcat + f"_({filter_dict['osds']})"
        df_for_ts_figure = df.copy().loc[:,[ts_subcat,'Date']].reset_index(drop=False)
    else :
        df_for_ts_figure = df.copy().loc[:,[ts_subcat,'Date']].reset_index(drop=False)

    # Drop unwanted columns depending on chosen osds
    if filter_dict['osds'] == 'Win' :
        df.drop(columns=[ 'Date',
                'Number_of_ODT_Win', 'Num_build_impact_Win','Number_of_ODT_Linux',
                'Num_build_impact_Linux','Num_server_impact',
                'Range_of_ODTs_(Linux)','Range_of_Build_impact_(Linux)', ],
            inplace=True)
    else :
        df.drop(columns=[ 'Date',
                'Number_of_ODT_Win', 'Num_build_impact_Win','Number_of_ODT_Linux',
                'Num_build_impact_Linux','Num_server_impact',
                'Range_of_ODTs_(Win)', 'Range_of_Build_impact_(Win)',],
            inplace=True)


    list_fig = []
    legend_order = {
        'Range_of_ODTs_(Win)': dict(
            zip(list(slices_dict_odts.values()),
                list(range(len(slices_dict_odts.values()))))
        ),
        'Range_of_ODTs_(Linux)': dict(
            zip(list(slices_dict_odts.values()),
                list(range(len(slices_dict_odts.values()))))
            ),
        'Range_of_Build_impact_(Win)': dict(
            zip(list(slices_dict_build_impact.values()),
                list(range(len(slices_dict_build_impact.values()))))
            ),
        'Range_of_Build_impact_(Linux)': dict(
            zip(list(slices_dict_build_impact.values()),
                list(range(len(slices_dict_build_impact.values()))))
            ),
        'Range_of_Server_impact': dict(
            zip(list(slices_dict_server_impact.values()),
                list(range(len(slices_dict_server_impact.values()))))
        ),
        'Pipeline_status': {
            'SUCCESS':0,
            'UNSTABLE':1,
            'ABORTED':2,
            'FAILURE':3,
            'Null':4
        }
    }



    # Create Pie charts
    for col in df.columns :
        count = Counter(df.loc[:,col])
        labels = list(count.keys())
        values = list(count.values())
        df_rep = pd.DataFrame(columns = ['labels', 'values'])
        df_rep['labels'] = labels
        df_rep['values'] = values
        #if col == 'SSR_Eligible' :
        #    df_rep = df_rep[df_rep.labels != 'Null']
        if col in legend_order:
            df_rep = df_rep.iloc[df_rep['labels'].map(legend_order[col]).sort_values().index]
        else :
            df_rep.sort_values(by = 'labels', inplace=True)

        if col in ['Range_of_ODTs_(Win)','Range_of_ODTs_(Linux)', 'Range_of_Build_impact_(Win)',
            'Range_of_Build_impact_(Linux)', 'Range_of_Server_impact']:
            hovertemplate = 'Range: %{label} <br>Percentage: %{percent}<extra></extra>'
        else:
            hovertemplate = (f"{col.replace('_',' ')}:"
                '%{label} <br>Percentage: %{percent}<extra></extra>')

        if chart_type == 'Pie':
            list_fig.append(go.Figure(data=go.Pie(
                labels=df_rep['labels'],
                values= df_rep['values'],
                hovertemplate= hovertemplate,
                sort = False),
            ).
            update_layout(
                title={
                    'text': col.replace('_', ' '),
                    'y':0.04,
                    'x':0.48,
                    'xanchor': 'center',
                    'yanchor': 'bottom'},
                    title_font_size=25 ).
            update_traces(textinfo='value'))

        elif chart_type == 'Bar' :
            df_rep['color'] = list(map(str,range(df_rep.shape[0])))
            list_fig.append(go.Figure(data=px.bar(df_rep, x='labels', y='values', color='labels')).
            update_layout(
                title={
                    'text': col.replace('_', ' '),
                    'y':0.04,
                    'x':0.48,
                    'xanchor': 'center',
                    'yanchor': 'bottom'},
                    title_font_size=25,
                xaxis={'title' :  '' , 'visible': True, 'showticklabels': True},
                yaxis={'title' : '' , 'visible': True, 'showticklabels': True},
                showlegend=False,
                paper_bgcolor='white',
                plot_bgcolor = 'white'  ))



    list_fig.append(create_ts_figure(df_for_ts_figure, ts_period= ts_period, ts_subcat=ts_subcat,
    start_date=filter_dict['Date'][0], end_date=filter_dict['Date'][1]))
    list_fig.append(f'*Total Pipelines: {df.shape[0]}*')
    return list_fig




def create_ts_figure(data, ts_period, ts_subcat, start_date, end_date) :
    """
    Returns the evolution of the pipelines figure.
    """
    global_data = pd.DataFrame(data.Date.dt.to_period(ts_period).value_counts().sort_index())
    global_data.index = global_data.index.astype(str)
    global_data.index = pd.DatetimeIndex(global_data.index)
    global_data.rename(columns = {'Date': 'Count'}, inplace= True)

    # In case a subcategory is demanded we create data for bar representation
    if ts_subcat != 'None':
        data['Date'] = data.Date.dt.to_period(ts_period)
        data = data.groupby(['Date', ts_subcat]).count().reset_index(drop = False)
        data.rename(columns = {'index': 'Count'}, inplace= True)
        data = data.set_index('Date')
        data.index = data.index.astype(str)
        data.index = pd.DatetimeIndex(data.index)


    #For daily evolution graph, we add missing days with fill_value = 0
    if ts_period == 'D':
        idx = pd.date_range(start_date,  end_date)
        global_data= global_data.reindex(idx, fill_value = 0)


    # Customize layout parameters depending on ts_period
    if ts_period == 'M' :
        hoverformat = '%b'
        dtick = 'M1'
    elif ts_period == 'Y' :
        hoverformat = '%Y'
        dtick = 'M12'
    else :
        hoverformat = ''
        dtick = ''


    # Generate figures depending on input parameters
    if ts_period == 'D' or ts_subcat == 'None':
        fig = go.Figure([go.Scatter(x=global_data.index, y=global_data['Count'], name='Total')])
        fig.update_traces(
            mode="markers+lines",
            hovertemplate= 'Total count: %{y}<extra></extra>')
        fig.update_layout(hovermode = 'x')
    else:
        data.reset_index(drop=False, inplace=True)
        fig = go.Figure(data= px.bar(data, x='Date', y='Count',
        color = ts_subcat ,
        text='Count',
        ))
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        fig.update_layout(uniformtext_minsize=9, uniformtext_mode='hide')
        fig.add_trace(go.Scatter(x=global_data.index, y=global_data['Count'], name= 'Total',
        mode='markers+text', hovertemplate= 'Total count: %{y}<extra></extra>',
        text = list(map(lambda x: f'Total: {x}',global_data.Count)), textposition = 'top center'))

    fig.update_layout(
        title={
        'text': 'Evolution of the number of Pipelines',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'bottom'},
        title_font_size=25,
        plot_bgcolor = 'white',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            hoverformat= hoverformat,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            dtick = dtick,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
            ),
        )
    )
    fig.update_yaxes(rangemode="tozero")
    return fig
