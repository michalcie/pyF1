from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import matplotlib.pyplot as plt


### Data extraction for the whole season
source = urllib.request.urlopen('https://www.formula1.com/en/results.html/2021/drivers.html').read()
soup = BeautifulSoup(source,'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
df.drop(["Unnamed: 0","Unnamed: 6"],axis=1, inplace=True)
# df.plot.bar(x="Driver", y="PTS");
# plt.show()

### Data extraction for one race
source = urllib.request.urlopen(f"https://www.formula1.com/en/results.html/1990/races/64/united-states/race-result.html").read()
soup = BeautifulSoup(source,'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table), flavor='bs4', header=[0])[0]

### Extraction of race urls
def get_race_urls(year):
    race_urls = []
    source = urllib.request.urlopen(f"https://www.formula1.com/en/results.html/{year}/"
                                    f"races.html").read()
    soup = BeautifulSoup(source,'html.parser')

    for url in soup.find_all('a'):
        if (str(year) in str(url.get('href'))) and ('race-result.html' in str(url.get('href'))) and (url.get('href') not in race_urls):
            race_urls.append(url.get('href'))
    return race_urls

### Extraction of multiple races in season

### I have issue do season 2020, 2021
def seasons_results(race_urls):

    for n, race in enumerate(race_urls):
        HOMEPAGE = f"https://www.formula1.com"
        placeholder = [0 for i in range(n)]
        race_name = race.split('/')[6]
        x = 2
        race_name_temp = race_name
        while n != 0 and (race_name_temp in season_results_df.columns):
            race_name_temp += str(' ')
            race_name_temp += str(x)
            x += 1
            if race_name_temp in season_results_df.columns:
                race_name_temp = race_name
            else:
                race_name = race_name_temp

        print(race_name)
        results_page = urllib.request.urlopen(f"{HOMEPAGE}{race}").read()
        race_results = BeautifulSoup(results_page,'html.parser')
        if len(race_results.find_all('table')) > 0:
            table = race_results.find_all('table')[0]
        df = pd.read_html(str(table), flavor='bs4', header=[0])[0]
        df.drop(["Unnamed: 0","Unnamed: 8"], axis=1, inplace=True)
        df.set_index('No', inplace=True)

        #establish season results df on first race information
        if n == 0:
            season_results_df = pd.DataFrame(df[['Driver','Car']], columns=['Driver','Car'], index=df.index)


        #add drivers if they are not in season_results_df
        for ind in df.index.difference(season_results_df.index):
            season_results_df.loc[ind] = [df['Driver'].loc[ind],df['Car'].loc[ind],*placeholder]
            # season_results_df.append([df['Driver'].loc[ind],df['Car'].loc[ind],*placeholder])

        for ind in df.index:
            if 'PTS' in df.columns:
                pts = df['PTS'].where(df.index == ind).dropna()
                season_results_df.loc[ind, race_name] = int(pts)


    #####Format the dataframe with a few lines#####
    season_results_df.sort_index(inplace=True)
    season_results_df.fillna(0, inplace=True)
    # season_results_df['Car'] = season_results_df['Car'].apply(lambda s : s[:3]).map(str.upper) #retain last 3 digits and caps
    return season_results_df

race_urls = get_race_urls(2021)
print(race_urls)
season_results_df = None
results = seasons_results(race_urls)
print(results)
cum_results = results.drop(['Driver', 'Car'], axis=1).cumsum(axis=1)
####configure dataframe for plotting####
cum_results['Driver'] = results['Driver'].apply(lambda s : s[-3:]).map(str.upper)
cum_results.set_index('Driver', inplace=True)
cum_results.sort_values(by='austria',ascending=False, inplace=True)
print(cum_results)


cum_results.transpose().plot.line(figsize=(14,8),use_index=False,
                                  xlim=(0,15)).legend(loc='center left',
                                                      bbox_to_anchor=(1.0, 0.5))

plt.show()
