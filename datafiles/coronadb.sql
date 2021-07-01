
CREATE DATABASE CORONA_DB;
USE CORONA_DB;

CREATE TABLE INFO(
    iso_code varchar(10),
    continent varchar(10),
    loc varchar(10),
    death_newcases_percent numeric(6,3),
    total_cases numeric(6),
    new_cases numeric(6),
    total_deaths numeric(6),
    new_deaths numeric(6),
    tests_per_case numeric(6,3),
    tests_units numeric(1,0) check(tests_units in (0,1))
);