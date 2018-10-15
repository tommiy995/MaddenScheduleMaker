# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:29:05 2018

@author: Thamas
"""

import pandas as pd
import os

'input path to madden folder'
path = input("What is the path to the madden export folder (add '\\' to end)? ")

'replace \ from file location to /'
path = path.replace("\\","/")

'read in teams file'
teams = pd.read_csv(path + 'teams.csv', header = 0)

'create dictionaries of team anmes and user names, and team id and name'
cols = ['abbrName','teamId','userName']
users = teams[cols].dropna(subset = ['userName'])
users_dict = dict(zip(users.abbrName, users.userName))
cols = ['teamId', 'abbrName']
teamID = teams[cols]
teamID_dict = dict(zip(teamID.teamId, teamID.abbrName))

'user list for later'
userlist = users.userName.T.tolist()

'create all schedules into one dataframe'
path_reg = path + "schedules/reg/"
path_pre = path + "schedules/pre/"
files_reg = os.listdir(path_reg)
files_pre = os.listdir(path_pre)
files_reg.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
sched = {}
schedpre = {}
sched_reg = list(map(lambda each:each.replace(".csv",''), files_reg))
sched_reg = list(map(lambda each:each.replace("-",''), sched_reg))
sched_pre = list(map(lambda each:each.replace(".csv",''), files_pre))
sched_pre = list(map(lambda each:each.replace("(",''), sched_pre))
sched_pre = list(map(lambda each:each.replace(")",''), sched_pre))
sched_pre = list(map(lambda each:each.replace(" ",''), sched_pre))

for a,f in zip(sched_reg, files_reg):
    sched[a]= pd.read_csv(path_reg + f)
    
for a,f in zip(sched_pre, files_pre):
    schedpre[a]= pd.read_csv(path_pre + f)

'format these dataframes'
df_reg = pd.concat(sched, keys = sched_reg)
df_reg.weekIndex = df_reg.weekIndex + 1
df_pre = pd.concat(schedpre, keys = sched_pre)
dict_week = {0 :'pre 1', 1 :'pre 2', 2 : 'pre 3', 3 :'pre 4'}
df_pre.weekIndex = df_pre.weekIndex.map(lambda s: dict_week.get(s) if s in dict_week else s)

'combine the dataframes'
df = pd.concat([df_pre, df_reg])


team_schedule = df.applymap(lambda s: teamID_dict.get(s) if s in teamID_dict else s)
user_schedule = team_schedule.applymap(lambda s: users_dict.get(s) if s in users_dict else s)
cols = ['awayScore','awayTeamId','homeScore','homeTeamId','weekIndex']
team_schedule = team_schedule[cols]
user_schedule = user_schedule[cols]

pvp = pd.DataFrame()
pvp = user_schedule[cols]
pvp['Visiting Outcome']= ''
pvp['Home Outcome']= ''
pvp['Discord Message']= ''
pvp[''] = ''
pvp['Start Date'] = ''
pvp['Last Day to Play Game'] = ''
cols = ['weekIndex','Start Date', 'Last Day to Play Game', 'awayTeamId', 'awayScore','', 'homeScore', 'homeTeamId', 'Visiting Outcome', 'Home Outcome', 'Discord Message']
pvp = pvp[cols]
pvp = pvp[pvp['awayTeamId'].isin(userlist) & pvp['homeTeamId'].isin(userlist)]


writer = pd.ExcelWriter(path + 'Madden Schedule.xlsx', engine='xlsxwriter')
user_schedule.to_excel(writer, sheet_name = 'Full Schedule', index = False)
pvp.to_excel(writer, sheet_name = 'Player vs Player Schedule', index = False)

workbook = writer.book
worksheet1 = writer.sheets['Full Schedule']
worksheet2 = writer.sheets['Player vs Player Schedule']
worksheet2.data_validation('I1:J1000', {'validate':'list', 'source': ['W','L','T']})

writer.save()
         







