# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:01:21 2023

@author: Usuario
"""

import sqlalchemy
import datetime
from sqlalchemy import create_engine, or_, and_
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Float, String

from datetime import datetime, timedelta, timezone

import ephem
from pysolar.solar import get_altitude

import Tablas as Tb

Base = declarative_base()

# datos de conexion a la base de datos
caelis_db_config = {
    'host'      :   'daza.opt.cie.uva.es',
    'username'  :   'curso2223',
    'password'  :   'Curso2223',
    'database'  :   'caelis',
    'drivername':   'mysql+pymysql',
}


# Conecta con la BD # ejecutamos directamente una consulta SQL

engine = create_engine(URL.create(**caelis_db_config), echo=False)
meta = MetaData()
meta.reflect(bind=engine)
con = engine.connect()

def create_gines_gonzalez_table(engine):

    table_name = "gines_gonzalez"

    if table_name not in meta.tables:
        table = Table(
            table_name,
            meta,
            Column("ph", Integer, primary_key=True),
            Column("site", String(50)),
            Column("date", DateTime, primary_key=True),
            Column("elevacion_solar", Float),
            Column("distancia_TS", Float),
            Column("presion", Float),
            Column("temperatura", Float)
        )
        table.create(engine)
        print(f"Created the '{table_name}' table.")
    else:
        print(f"The table '{table_name}' already exists.")

# Llamamos a la funcion
if __name__ == '__main__':
    create_gines_gonzalez_table(engine)

Session = sessionmaker(engine)
session = Session()


def calc_elevacion_solar(longitud, latitud, fecha):
    fecha_utc=datetime(fecha.year, fecha.month, fecha.day, fecha.hour, fecha.minute, fecha.second, tzinfo=timezone.utc)
    return round(get_altitude(latitud, longitud, fecha_utc), 4)

def calc_dist_tierra_sol(fecha):
    sun = ephem.Sun()
    sun.compute(fecha)    # posicion del Sol en la fecha proporcionada
    d_ephem = sun.earth_distance  # Obtiene la distancia entre la Tierra y el Sol en unidades astronomicas (AU)
    return round(d_ephem,5)

def calc_presion(altitud):
    t=288.15-((6.5*altitud)/1000)
    presion = 1013.25*pow((288.15/t),(-5.256))
    return round(presion, 3)


initial_time = '2022-08-15 14:00:00'  # 15 de octubre de 2023 a las 14:00
final_time = '2022-08-15 16:00:00'    # 15 de octubre de 2023 a las 16:00

scenes = session.query(
    Tb.CmlInstallation.photometer, Tb.CaeStation.name, Tb.CmlDataScene.date,
    Tb.CaeStation.longitude, Tb.CaeStation.latitude, Tb.CaeStation.altitude,
    Tb.CmlDataSceneParameter.value
).join(
    Tb.CmlInstallation,
    Tb.CmlInstallation.site == Tb.CaeStation.name,
    isouter=True
).join(
    Tb.CmlDataScene,
    Tb.CmlInstallation.photometer == Tb.CmlDataScene.ph,
    isouter=True
).join(
    Tb.CmlDataSceneParameter,
    Tb.CmlDataSceneParameter.date == Tb.CmlDataScene.date,
    isouter=True
).filter(
    Tb.CmlInstallation.photometer == 1219,
    Tb.CmlDataScene.date.between(initial_time, final_time),
    Tb.CmlInstallation.first <= initial_time,
    Tb.CmlInstallation.last >= final_time,
    Tb.CmlDataSceneParameter.key == "EL_TEMP"
).all()



for scene in scenes:
    print(scene.photometer, scene.name, scene.date, calc_elevacion_solar(scene.longitude, scene.latitude, scene.date), calc_dist_tierra_sol(scene.date),calc_presion(scene.altitude), scene.value)
    
for scene in scenes:
    data = Tb.GinesGonzalez(
            ph = scene.photometer, 
            date = scene.date, 
            site = scene.name,  
            elevacion_solar = calc_elevacion_solar(scene.longitude, scene.latitude, scene.date), 
            distancia_TS = calc_dist_tierra_sol(scene.date), 
            presion = calc_presion(scene.altitude), 
            temperatura = scene.value
            )
    session.add(data)  # Actualiza tabla
    session.commit()



