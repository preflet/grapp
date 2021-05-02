import mysql.connector
import pandas as pd
import settings

from db import cache

query = '''select
a.created_date,
YEARWEEK(a.created_date) as year_week,
DATE_FORMAT(a.created_date, '%Y-%m-%d') as date_m,
DATE_FORMAT(a.created_date, "%H:%i") as time_m,
a.instant_day_of_week,
a.clock_type,
a.created_by,
a.id,
a.device_id, a.employee_id , a.geoip_id, a.weather_id, a.department_id,
b.operating_system_name,
b.operating_system_version,
b.device_brand,
c.city_name,
c.country_name,
c.subdivision_name,
d.humidity,
d.latitude,
d.longitude,
d.pressure,
d.symbol_name,
d.symbol_number,
d.temperature,
d.wind_direction,
d.wind_direction_angle,
d.wind_speed,
ROW_NUMBER() OVER (PARTITION BY clock_type, created_by, instant_day ORDER BY created_date) AS int_rank,
ROW_NUMBER() OVER (PARTITION BY symbol_name, created_by, instant_day ORDER BY created_date) AS wt_rank
from clock a
left join clock_device_info b on a.device_id = b.id
left join ipaddress_info c on a.geoip_id = c.id
left join weather_info d on a.weather_id = d.id
where a.created_date between '2020-10-01' and '2020-11-01'
order by a.created_by, a.created_date'''


class SQL:
    host = settings.HOST_MYSQL
    user = settings.USER
    password = settings.PASSWORD

    def __init__(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database="ristorail"
        )

    def get_result_and_cache(self):
        cursor = self.db.cursor()
        cursor.execute(query)
        output = cursor.fetchall()
        self.cache_result(output)
        return output

    @cache
    def cache_result(self, cache_result):
        return cache_result


if __name__ == '__main__':
    sql = SQL()
    result = sql.get_result_and_cache()
    df = pd.DataFrame(result)
    # df.columns = ["created_date","year_week","date_m","time_m"]
    print(df.head())
