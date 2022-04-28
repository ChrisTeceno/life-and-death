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
    """make a list of relevant files in the directory"""
    files = os.listdir(path)
    # choose only the files of concern
    files = [file for file in files if file.startswith("Provisional")]
    return files


def make_df():
    """make a dataframe from the files in the directory"""
    # get the list of files
    files = list_files(".")
    # create a dataframe for all the files
    df = pd.DataFrame()
    # run through all the files adding them to the dataframe
    for file in files:
        df = df.append(pd.read_csv(file, sep="\t"))
    return df


def prep_data(df):
    """prepare the dataframe for plotting"""
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
    """get the population data"""
    population = pd.read_csv("population_by_age_and_year.txt", sep="\t")
    return population


def prep_pop_data(df):
    """prepare the population data"""
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
    """merge the dataframes"""
    # merge the dataframes
    df = df.merge(population, on=["year", "age_group", "gender"])
    return df


def wrangle_data():
    """wrangle the data into the first major df"""
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
    """prepare the covid data"""
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
    df.month = pd.to_datetime(df.month)
    df["deaths_times_age"] = df["deaths"] * df["age"]
    return df


def prep_age_deaths():
    """prepare the age deaths data"""
    # remove redundant columns
    # *** population data is in a different file **
    df = pd.read_csv("deaths_by_age_and_month.txt", sep="\t")
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
    # convert month to datetime
    df.month = pd.to_datetime(df.month)
    # add a column to use later for avg age of death
    df["deaths_times_age"] = df["deaths"] * df["age"]
    return df


def get_covid_all_ages():
    covid_all_ages = prep_covid()
    covid_all_ages.month = pd.to_datetime(covid_all_ages.month)
    covid_all_ages["deaths_times_age"] = (
        covid_all_ages["deaths"] * covid_all_ages["age"]
    )
    return covid_all_ages


def get_monthly_deaths():
    """get the monthly deaths"""
    df = wrangle_data()
    covid_all_ages = get_covid_all_ages()
    monthly_deaths = pd.DataFrame()
    monthly_deaths["average_covid_death_age"] = (
        covid_all_ages.groupby("month").sum()["deaths_times_age"]
        / covid_all_ages.groupby("month").sum()["deaths"]
    )
    monthly_deaths["covid_deaths"] = covid_all_ages.groupby("month").sum()["deaths"]
    monthly_deaths["scaled_covid"] = (
        monthly_deaths["covid_deaths"] * 100 / monthly_deaths["covid_deaths"].max()
    )
    monthly_deaths["all_cause_deaths"] = df.groupby("month").sum()["deaths"]
    monthly_deaths["scaled_all_cause"] = (
        monthly_deaths["all_cause_deaths"]
        * 100
        / monthly_deaths["all_cause_deaths"].max()
    )
    return monthly_deaths


def make_df2():
    """make the second major df"""
    deaths_by_age = prep_age_deaths()
    df = wrangle_data()
    monthly_deaths = get_monthly_deaths()
    df2 = pd.DataFrame()
    df2["all_cause_deaths"] = df.groupby("month").sum()["deaths"]
    df2["covid_deaths"] = (
        df[df.cause.str.contains("COVID-19")].groupby("month").sum()["deaths"]
    )
    df2["scaled_covid"] = df2["covid_deaths"] * 100 / df2["covid_deaths"].max()
    df2["scaled_all_cause"] = (
        df2["all_cause_deaths"] * 100 / df2["all_cause_deaths"].max()
    )
    df2["difference"] = df2["scaled_covid"] - df2["scaled_all_cause"]
    df2["average_death_age"] = (
        deaths_by_age.groupby("month").sum()["deaths_times_age"]
        / deaths_by_age.groupby("month").sum()["deaths"]
    )
    df2["average_covid_death_age"] = monthly_deaths["average_covid_death_age"]
    df2.fillna(0, inplace=True)  # fills all the prepandemic covid data with zeros
    df2["heart_related_deaths"] = (
        df[df.cause.str.contains("heart")].groupby("month").sum()["deaths"]
    )
    df2["scaled_heart_deaths"] = (
        df2["heart_related_deaths"] * 100 / df2["heart_related_deaths"].max()
    )
    df2["homicide_deaths"] = (
        df[df.cause.str.contains("homicide")].groupby("month").sum()["deaths"]
    )
    df2["scaled_homicide_deaths"] = (
        df2["homicide_deaths"] * 100 / df2["homicide_deaths"].max()
    )
    df2["suicide_deaths"] = (
        df[df.cause.str.contains("suicide")].groupby("month").sum()["deaths"]
    )
    df2["scaled_suicide_deaths"] = (
        df2["suicide_deaths"] * 100 / df2["suicide_deaths"].max()
    )
    df2["diabetes_deaths"] = (
        df[df.cause.str.contains("Diabetes")].groupby("month").sum()["deaths"]
    )
    df2["scaled_diabetes_deaths"] = (
        df2["diabetes_deaths"] * 100 / df2["diabetes_deaths"].max()
    )
    df2["accident_deaths"] = (
        df[df.cause.str.contains("Accident")].groupby("month").sum()["deaths"]
    )
    df2["scaled_accident_deaths"] = (
        df2["accident_deaths"] * 100 / df2["accident_deaths"].max()
    )
    # make a male death df
    df_male = df[df.gender == "Male"].copy()
    # assign month to datetime
    df_male.month = pd.to_datetime(df_male.month)
    # repeat for female
    df_female = df[df.gender == "Female"].copy()
    df_female.month = pd.to_datetime(df_female.month)
    # add male deaths
    df2["male_covid_deaths"] = (
        df_male[df_male.cause.str.contains("COVID-19")].groupby("month").sum()["deaths"]
    )
    df2["male_scaled_covid"] = df2["covid_deaths"] * 100 / df2["covid_deaths"].max()
    df2["male_covid_deaths"].fillna(
        0, inplace=True
    )  # fills all the prepandemic covid data with zeros
    df2["male_heart_related_deaths"] = (
        df_male[df_male.cause.str.contains("heart")].groupby("month").sum()["deaths"]
    )
    df2["male_scaled_heart_deaths"] = (
        df2["male_heart_related_deaths"] * 100 / df2["male_heart_related_deaths"].max()
    )
    df2["male_homicide_deaths"] = (
        df_male[df_male.cause.str.contains("homicide")].groupby("month").sum()["deaths"]
    )
    df2["male_scaled_homicide_deaths"] = (
        df2["male_homicide_deaths"] * 100 / df2["male_homicide_deaths"].max()
    )
    df2["male_suicide_deaths"] = (
        df_male[df_male.cause.str.contains("suicide")].groupby("month").sum()["deaths"]
    )
    df2["male_scaled_suicide_deaths"] = (
        df2["male_suicide_deaths"] * 100 / df2["male_suicide_deaths"].max()
    )
    df2["male_diabetes_deaths"] = (
        df_male[df_male.cause.str.contains("Diabetes")].groupby("month").sum()["deaths"]
    )
    df2["male_scaled_diabetes_deaths"] = (
        df2["male_diabetes_deaths"] * 100 / df2["male_diabetes_deaths"].max()
    )
    df2["male_accident_deaths"] = (
        df_male[df_male.cause.str.contains("Accident")].groupby("month").sum()["deaths"]
    )
    df2["male_scaled_accident_deaths"] = (
        df2["male_accident_deaths"] * 100 / df2["male_accident_deaths"].max()
    )
    # list of columns where name contains 'scaled'
    male_scaled_cols = [
        col for col in df2.columns if ("male" in col) and ("scaled" in col)
    ]
    # list cols where deaths in name bad scaled is not
    male_deaths_cols = [
        col
        for col in df2.columns
        if ("male" in col) and ("deaths" in col) and ("scaled" not in col)
    ]

    # add female deaths
    df2["female_covid_deaths"] = (
        df_female[df_female.cause.str.contains("COVID-19")]
        .groupby("month")
        .sum()["deaths"]
    )
    df2["female_scaled_covid"] = df2["covid_deaths"] * 100 / df2["covid_deaths"].max()
    df2["female_covid_deaths"].fillna(
        0, inplace=True
    )  # fills all the prepandemic covid data with zeros
    df2["female_heart_related_deaths"] = (
        df_female[df_female.cause.str.contains("heart")]
        .groupby("month")
        .sum()["deaths"]
    )
    df2["female_scaled_heart_deaths"] = (
        df2["female_heart_related_deaths"]
        * 100
        / df2["female_heart_related_deaths"].max()
    )
    df2["female_homicide_deaths"] = (
        df_female[df_female.cause.str.contains("homicide")]
        .groupby("month")
        .sum()["deaths"]
    )
    df2["female_scaled_homicide_deaths"] = (
        df2["female_homicide_deaths"] * 100 / df2["female_homicide_deaths"].max()
    )
    df2["female_suicide_deaths"] = (
        df_female[df_female.cause.str.contains("suicide")]
        .groupby("month")
        .sum()["deaths"]
    )
    df2["female_scaled_suicide_deaths"] = (
        df2["female_suicide_deaths"] * 100 / df2["female_suicide_deaths"].max()
    )
    df2["female_diabetes_deaths"] = (
        df_female[df_female.cause.str.contains("Diabetes")]
        .groupby("month")
        .sum()["deaths"]
    )
    df2["female_scaled_diabetes_deaths"] = (
        df2["female_diabetes_deaths"] * 100 / df2["female_diabetes_deaths"].max()
    )
    df2["female_accident_deaths"] = (
        df_female[df_female.cause.str.contains("Accident")]
        .groupby("month")
        .sum()["deaths"]
    )
    df2["female_scaled_accident_deaths"] = (
        df2["female_accident_deaths"] * 100 / df2["female_accident_deaths"].max()
    )
    # list of columns where name contains 'scaled'
    female_scaled_cols = [
        col for col in df2.columns if ("female" in col) and ("scaled" in col)
    ]
    # list cols where deaths in name bad scaled is not
    female_deaths_cols = [
        col
        for col in df2.columns
        if ("female" in col) and ("deaths" in col) and ("scaled" not in col)
    ]
    return (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    )

