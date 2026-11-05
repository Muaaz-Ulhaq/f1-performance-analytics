import fastf1
import pandas as pd
fastf1.Cache.enable_cache('cache')  # Enable caching for faster data retrieval

session = fastf1.get_session(2025, 'Monza', 'Q')

session.load()  # Load the session data

#print(session.laps.columns)
pd = session.laps.pick_fastest()
#print(pd.array[1]) # it will print second index that has driver name abbrevation
#print(pd) #prints all data

#print(session.laps.pick_fastest().get_telemetry())

#print(session.laps.pick_not_deleted())
#print(session.laps.pick_not_deleted())
#print(deletedDrivers)
#print(session.results.iloc[0:10].loc[:,['Abbrevation', 'Q3']]) #prints the first row of the results dataframe
#print(session.results.iloc[0:10].loc[:, ['Abbreviation', 'Q3']])
#print(session.laps.pick_fastest().Driver)

not_deleted_laps = session.laps.pick_not_deleted()
#print(f"Number of not deleted laps: {not_deleted_laps}") 
#print(session.laps.pick_fastest().Driver)
#print(session.laps.pick_fastest().LapTime)
#rint(session.laps.pick_fastest().get_telemetry().columns)
'''so the idea to find how many deleted laps and reason for them is:
loop till the session.laps
check on [Deleted] column for each iteration
if [Deleted] found, increment deletedCount and append [DeletedReason] column into an array
'''

from collections import Counter

laps = session.laps

deleted_count = 0
reasons = []
for _, lap in laps.iterrows():
    if lap["Deleted"] == True:
        deleted_count += 1
        reasons.append(lap["DeletedReason"])

print(deleted_count)
print(Counter(reasons))

deleted = laps[laps["Deleted"] == True]

print(len(deleted))
print(deleted["DeletedReason"].value_counts())
print(deleted[["Driver", "LapNumber", "LapTime", "DeletedReason"]])