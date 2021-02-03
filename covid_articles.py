from urllib.request import urlopen
from bs4 import BeautifulSoup
from sys import exit
from pandas import DataFrame
from collections import Counter
import matplotlib.pyplot as plt


def replacer(text, dictionary):
    """Replaces multiple things based on a dictionary: {"original": "new"}.
    Inspired by J. Hansen's answer on stackoverflow."""
    for i, j in dictionary.items():
        text = text.replace(i, j)
    return text


final_list = []
replace_dict = {
    # "aktualizováno" = updated
    "aktualizováno\xa0\r\n": "",
    "          ": "",
    "ledna": "Jan",
    "leden": "Jan",
    "února": "Feb",
    "únor": "Feb",
    "března": "Mar",
    "březen": "Mar",
    "dubna": "Apr",
    "duben": "Apr",
    "května": "May",
    "květen": "May",
    "června": "Jun",
    "červen": "Jun",
    "července": "Jul",
    "červenec": "Jul",
    "srpna": "Aug",
    "srpen": "Aug",
    "září": "Sep",
    "října": "Oct",
    "říjen": "Oct",
    "listopadu": "Nov",
    "listopad": "Nov",
    "prosince": "Dec",
    "prosinec": "Dec"
}

# The end number, 290 (289), changes each day as new articles are published
for pgnum in range(2, 290):
    link = "https://www.idnes.cz/zpravy/zahranicni/koronavirus.K466979/" + str(pgnum)

    try:
        pg = urlopen(link)
    except (NameError, ValueError) as err:
        print("Incorrect link -", err)
        exit()

    soup = BeautifulSoup(pg, "html.parser")
    content = soup.find("div", {"id": "list-art-count"})

    date = ""

    # Find dates, strip-off whitespaces and other unwanted content
    for dt in content.findAll("span", {"class": "time"}):
        date = date + " " + dt.text
        date = date.strip()
        date = replacer(date, replace_dict)

    final_list = final_list + date.splitlines()
    print("Page", pgnum, "completed")

# Remove the trailing whitespace where applicable
for item in range(len(final_list)):
    final_list[item] = final_list[item].rstrip()

# Remove outliers
try:
    final_list.remove("14. Jun 2015")
    final_list.remove("11. Jun 2015")
# Ignore the "x not in list" error
except ValueError:
    pass

# Count the occurrences of each date which is also the number of articles/day
date_counter = Counter(final_list)
df = DataFrame.from_dict(
    date_counter,
    orient="index",
    columns=["Number of articles"]
)

# Reverse the order of the dataframe
df = df.reindex(index=df.index[::-1])
df.plot(
    kind="line",
    figsize=(14, 6),
    title="Coronavirus-related articles on idnes.cz",
    grid=True,
    xlabel="Date",
    ylabel="Frequency"
)
plt.show()
