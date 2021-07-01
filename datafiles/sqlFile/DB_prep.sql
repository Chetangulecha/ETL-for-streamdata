CREATE DATABASE WeatherDB;
USE WeatherDB;

CREATE TABLE basic_weather(
    Id varchar(10),
    MinTemperature numeric(6,3),
    MaxTemperature numeric(6,3),
    AvgTemp numeric(6,3),
    Rainfall numeric(6,3),
    Evaporation numeric(6,3),
    Sunshine numeric(6,3),
    WindGustDir varchar(5),
    WindGustSpeed numeric(6,3),
    RainToday numeric(1,0) check(RainToday in (0,1)),
    RainTomorrow numeric(1,0) check(RainTomorrow in (0,1)),
    RiskMM numeric(6,3)
);


CREATE TABLE morning_weather(
    Id varchar(10),
    WindDirection varchar(10),
    WindSpeed numeric(6,3),
    Humidity numeric(6,3),
    Pressure numeric(10,3),
    Cloud numeric(6,3),
    Temperature numeric(6,3)  
);


CREATE TABLE afternoon_weather(
    Id varchar(10),
    WindDirection varchar(10),
    WindSpeed numeric(6,3),
    Humidity numeric(6,3),
    Pressure numeric(10,3),
    Cloud numeric(6,3),
    Temperature numeric(6,3)
);
