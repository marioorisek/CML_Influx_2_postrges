from influxdb import InfluxDBClient

db = InfluxDBClient(host="192.168.10.124", database="doom")

db_list = db.get_list_database()

sklenik_ch = db.get_list_series(database="sklenik")
doom_ch = db.get_list_series(database="doom")

result = db.query("SELECT SPREAD(*) FROM prepad_vrtu_absolut WHERE time > now() - 24h")

result  = result.raw["series"][0]["values"][0][1]

print(f"Prepad za poslednich 24 hodin: {result:,.0f} l.")