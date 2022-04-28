import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import style

style.use("ggplot")
import os


# list all files in this directory with .txt
def list_files(path):
    files = os.listdir(path)
    # choose only the files of concern
    files = [file for file in files if file.startswith("Provisional")]
    return files


def make_df():
    # get the list of files
    files = list_files(".")
    # create a dataframe for all the files
    df = pd.DataFrame()
    # run through all the files adding them to the dataframe
    for file in files:
        df = df.append(pd.read_csv(file, sep="\t"))
    return df


def prep_data(df):
    # remove notes column
    df = df.drop(columns=["Notes"])
    # remove all rows with "Data not shown due to 6 month lag to account"
    df = df[
        df["UCD - ICD-10 113 Cause List"].str.startswith(
            "Data not shown due to 6 month lag to account"
        )
        == False
    ]
    # remove redundant columns
    # *** population data is in a different file **
    df = df.drop(
        columns=[
            "Month",
            "Ten-Year Age Groups",
            "Crude Rate",
            "Gender Code",
            "Population",
        ]
    )
    # change the column names to be more readable
    df.rename(
        columns={
            "UCD - ICD-10 113 Cause List": "Cause",
            "UCD - ICD-10 113 Cause List Code": "Cause Code",
            "Month Code": "month",
            "Ten-Year Age Groups Code": "age_group",
        },
        inplace=True,
    )
    # make all columns lowercase
    df.columns = df.columns.str.lower()
    # replace all spaces with underscores
    df.columns = df.columns.str.replace(" ", "_")
    # deaths to int
    df["deaths"] = df["deaths"].astype(int)
    # change age_group age group '1' to '01'
    df.loc[df["age_group"] == "1", "age_group"] = "01"
    # change age_group age group '1-4' to '01-04'
    df.loc[df["age_group"] == "1-4", "age_group"] = "01-04"
    # change age_group age group '5-14' to '05-14'
    df.loc[df["age_group"] == "5-14", "age_group"] = "05-14"
    # add a column for the year from month
    df["year"] = df["month"].str[:4]
    # keep data only where cause starts with #
    df = df[df["cause"].str.startswith("#")]  # this keeps only the main groups of death
    df.month = pd.to_datetime(df.month)
    # drop 2022/03 due to missing data
    df = df[df.month != "2022/03"]
    return df


def get_population():
    population = pd.read_csv("population_by_age_and_year.txt", sep="\t")
    return population


def prep_pop_data(df):
    # remove notes column
    df = df.drop(columns=["Notes"])
    # remove redundant columns
    df = df.drop(
        columns=[
            "Year Code",
            "Ten-Year Age Groups",
            "Crude Rate",
            "Deaths",
            "Gender Code",
        ]
    )
    # change the column names to be more readable
    df.rename(
        columns={
            "UCD - ICD-10 113 Cause List": "Cause",
            "UCD - ICD-10 113 Cause List Code": "Cause Code",
            "Month Code": "month",
            "Ten-Year Age Groups Code": "age_group",
        },
        inplace=True,
    )
    # drop nulls caused by deleting the notes column
    df.dropna(inplace=True)
    # make all columns lowercase
    df.columns = df.columns.str.lower()
    # replace all spaces with underscores
    df.columns = df.columns.str.replace(" ", "_")
    # change age_group age group '1' to '01'
    df.loc[df["age_group"] == "1", "age_group"] = "01"
    # change age_group age group '1-4' to '01-04'
    df.loc[df["age_group"] == "1-4", "age_group"] = "01-04"
    # change age_group age group '5-14' to '05-14'
    df.loc[df["age_group"] == "5-14", "age_group"] = "05-14"
    df.year = df.year.str[:4]
    return df


def merge_data(df, population):
    # merge the dataframes
    df = df.merge(population, on=["year", "age_group", "gender"])
    return df


def wrangle_data():
    df = make_df()
    df = prep_data(df)
    pop = get_population()
    pop = prep_pop_data(pop)
    df = merge_data(df, pop)
    # make population and int
    df["population"] = df["population"].astype(int)
    # make a crude rate column
    df["crude_rate"] = df["deaths"] / df["population"]
    return df


def prep_covid():
    df = pd.read_csv("covid_deaths_by_age_and_month.txt", sep="\t")
    # remove redundant columns
    # *** population data is in a different file **
    df = df.drop(
        columns=[
            "Notes",
            "UCD - ICD-10 113 Cause List",
            "UCD - ICD-10 113 Cause List Code",
            "Crude Rate",
            "Population",
            "Month",
            "Single-Year Ages Code",
        ]
    )
    # drop nulls caused by deleting the notes column
    df.dropna(inplace=True)
    # change the column names to be more readable
    df.rename(
        columns={"Single-Year Ages": "age", "Month Code": "month"}, inplace=True,
    )
    # make all columns lowercase
    df.columns = df.columns.str.lower()
    # replace all spaces with underscores
    df.columns = df.columns.str.replace(" ", "_")
    # replace all - with _
    df.columns = df.columns.str.replace("-", "_")
    # deaths to int
    df["deaths"] = df["deaths"].astype(int)
    # change age < 1 to age 0
    df.loc[df["age"] == "< 1 year", "age"] = "0"
    # change age 100+ to age 100
    df.loc[df["age"] == "100+ years", "age"] = "100"
    # split age string and take the first number
    df.age = df.age.str.split().str[0]
    # make age an int
    df.age = df.age.astype(int)
    # make a year column
    df["year"] = df.month.str[:4]

    return df


def prep_age_deaths():
    df = pd.read_csv("deaths_by_age_and_month.txt", sep="\t")
    # remove redundant columns
    # *** population data is in a different file **
    df = df.drop(
        columns=[
            "Notes",
            "Crude Rate",
            "Population",
            "Month",
            "Gender",
            "Single-Year Ages",
        ]
    )
    # drop nulls caused by deleting the notes column
    df.dropna(inplace=True)
    # change the column names to be more readable
    df.rename(
        columns={"Single-Year Ages Code": "age", "Month Code": "month"}, inplace=True,
    )
    # make all columns lowercase
    df.columns = df.columns.str.lower()
    # replace all spaces with underscores
    df.columns = df.columns.str.replace(" ", "_")
    # replace all - with _
    df.columns = df.columns.str.replace("-", "_")
    # deaths to int
    df["deaths"] = df["deaths"].astype(int)
    # remove columns where age == 'NS'
    df = df[df.age != "NS"]
    # make age an int
    df.age = df.age.astype(int)
    # make a year column
    df["year"] = df.month.str[:4]

    return df


def get_covid_all_ages():
    covid_all_ages = prep_covid()
    covid_all_ages.month = pd.to_datetime(covid_all_ages.month)
    covid_all_ages["deaths_times_age"] = (
        covid_all_ages["deaths"] * covid_all_ages["age"]
    )
    return covid_all_ages

