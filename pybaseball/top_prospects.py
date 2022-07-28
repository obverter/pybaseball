import pandas as pd
import requests

from . import cache


@cache.df_cache()
def top_prospects(teamName=None, playerType=None):
    teamUrl = "" if teamName is None else teamName.lower() + '/'
    url = f"https://www.mlb.com/{teamUrl}prospects/stats/top-prospects"
    res = requests.get(url, timeout=None).content
    prospectList = pd.read_html(res)
    if playerType == "batters":
        return postprocess(prospectList[0])
    elif playerType == "pitchers":
        return postprocess(prospectList[1])
    elif playerType is None:
        topProspects = pd.concat(prospectList)
        topProspects.sort_values(by=['Rk'], inplace = True)
        topProspects = postprocess(topProspects)
        return topProspects


def postprocess(prospectList):
    prospectList = prospectList.drop(list(prospectList.filter(regex = 'Tm|Unnamed:*')), axis = 1)
    return prospectList
