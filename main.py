from influxdb import InfluxDBClient

db = InfluxDBClient(host="192.168.10.124")

db_list = db.get_list_database()

def read_metric(database, channel_name, metric, time_frame="24h"):
    result = db.query(f"SELECT {metric}(*) FROM {database}..{channel_name} WHERE time > now() - {time_frame}")
    result = result.raw["series"][0]["values"][0][1]
    return result

def read_24h_spread(database, channel_name):
    return(read_metric(database, channel_name, "SPREAD"))

def read_24h_min(database, channel_name):
    return(read_metric(database, channel_name, "MIN"))

def read_24h_max(database, channel_name):
    return(read_metric(database, channel_name, "MAX"))

sklenik_ch = db.get_list_series(database="sklenik")
doom_ch = db.get_list_series(database="doom")

result = read_24h_spread(channel_name="prepad_vrtu_absolut", database="doom")
print(f"Prepad za poslednich 24 hodin: {result:,.0f} l.")