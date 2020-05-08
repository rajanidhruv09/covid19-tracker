import psycopg2
import os
import numpy as np

from psycopg2.extensions import AsIs

connection = psycopg2.connect(
        "postgres://odxvjcehadzztn:0637ed833c56eb0f260e3e7f90eaefceacc038fdbda29c535d340c522a38af5f@ec2-52-6-143-153.compute-1.amazonaws.com:5432/d36gmj4qglmqra",
        sslmode='require')
cursor = connection.cursor()


def get_dates_for_graph():
    try:
        cursor.execute("""SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'confirmed'
                    ORDER BY ORDINAL_POSITION""")
        response = cursor.fetchall()
        columns = []
        for row in response:
            columns.append(row[0])
        return columns[4:]
    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)
    finally:
        cursor.execute("ROLLBACK")
        connection.commit()


def query_database(table_name, country):
    try:
        cursor.execute("""SELECT * FROM %s WHERE Country = %s""", (AsIs(table_name), country))
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)
    finally:
        cursor.execute("ROLLBACK")
        connection.commit()


def get_daily_changes(values):
    changes = [values[0]]
    for i in range(1, len(values)):
        diff = values[i] - values[i - 1]
        changes.append(diff if diff > 0 else 0)
    print(changes)
    return combine_graph_values_and_labels(changes)


def combine_graph_values_and_labels(values):
    labels_and_values_list = []
    column_names = get_dates_for_graph()
    for i in range(len(values)):
        labels_and_values_list.append({"date": column_names[i], "count": values[i]})
    return labels_and_values_list


def parse_data_confirmed(data, parse_body, country):
    if len(data) == 1:  # There is no info available for the states/provinces of the country
        parse_body['total_confirmed'] = data[0][-1]
        parse_body['line_graph_data'] = combine_graph_values_and_labels(list(data[0][4:]))
        parse_body['daily_change_graph_data'] = get_daily_changes(list(data[0][4:]))
        parse_body['confirmed_change_today'] = parse_body['daily_change_graph_data'][-1]['count']
        parse_body['table_data'] = [{"location": country, "confirmed": data[0][-1]}]
    else:
        total = 0
        graphing_data = np.zeros((len(data[0][4:]),), dtype=int)
        parse_body['table_data'] = []
        for state_data in data:
            parse_body['table_data'].append({"location": state_data[0], "confirmed": state_data[-1]})
            total += state_data[-1]
            graphing_data += np.array(state_data[4:])
        parse_body['total_confirmed'] = total
        parse_body['line_graph_data'] = combine_graph_values_and_labels(graphing_data.tolist())
        parse_body['daily_change_graph_data'] = get_daily_changes(graphing_data.tolist())
        parse_body['confirmed_change_today'] = parse_body['daily_change_graph_data'][-1]['count']


def parse_data_recovered(data, parse_body):
    parse_body['total_recovered'] = data[0][-1]
    parse_body['recovered_change_today'] = data[0][-1] - data[0][-2]


def parse_data_deaths(data, parse_body):
    if len(data) == 1:  # There is no info available for the states/provinces of the country
        parse_body['total_deaths'] = data[0][-1]
        parse_body['table_data'][0]["deaths"] = data[0][-1]
        parse_body['deaths_change_today'] = data[0][-1] - data[0][-2]
    else:
        total = 0
        total_change = 0
        for index, state_data in enumerate(data):
            parse_body['table_data'][index]['deaths'] = state_data[-1]
            total += state_data[-1]
            total_change += state_data[-1] - state_data[-2]
        parse_body['total_deaths'] = total
        parse_body['deaths_change_today'] = total_change


def get_country_data(country):
    confirmed = query_database("confirmed" if not country == "US" else "confirmed_us", country)
    recovered = query_database("recovered", country)
    deaths = query_database("deaths" if not country == "US" else "deaths_us", country)

    response = {}
    parse_data_confirmed(confirmed, response, country)
    parse_data_recovered(recovered, response)
    parse_data_deaths(deaths, response)

    return response
