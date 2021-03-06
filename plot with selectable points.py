import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import datetime

print("Enter start date:")
start_date = (input())
print("Enter end date:")
end_date = (input())

grand_slam_df = pd.read_csv('data/tournaments_1877-2017_unindexed_csv.csv', parse_dates = ['tourney_dates'])

match_scores_df_1877_1967 = pd.read_csv('data/match_scores_1877-1967_unindexed_csv.csv')
match_scores_df_1968_1990 = pd.read_csv('data/match_scores_1968-1990_unindexed_csv.csv')
match_scores_df_1991_2016 = pd.read_csv('data/match_scores_1991-2016_unindexed_csv.csv')
match_scores_df_2017 = pd.read_csv('data/match_scores_2017_unindexed_csv.csv')

match_scores_df = pd.concat([match_scores_df_1877_1967, match_scores_df_1968_1990, match_scores_df_1991_2016, match_scores_df_2017])

#Choose specific tourneys or surface types here

#grand_slam = ["wimbledon", "us-open", "australian-open", "roland-garros"]
grand_slam = ["wimbledon", "us-open", "australian-open", "roland-garros"]
#surface = ["Grass", "Hard", "Carpet", "Clay"]
surface = ["Grass", "Hard", "Carpet", "Clay"]

grand_slam_df = grand_slam_df[grand_slam_df["tourney_slug"].isin(grand_slam)]
grand_slam_df = grand_slam_df[grand_slam_df["tourney_surface"].isin(surface)]

match_scores_df = match_scores_df[match_scores_df["tourney_slug"].isin(grand_slam)]
match_scores_df['tourney_year'] = match_scores_df.tourney_year_id.astype(str).str[:4]

#counts player wins over time
count = grand_slam_df.groupby(['singles_winner_name']).cumcount().add(1)

#Manipulating dataframe here
grand_slam_df.insert(2, "count", count, True)
player_win_count_df = grand_slam_df.pivot(index = 'singles_winner_name', columns = 'tourney_dates', values = 'count')
player_win_count_df = player_win_count_df.T
player_win_count_df_temp = player_win_count_df.fillna(method='bfill')
player_win_count_df = player_win_count_df.fillna(player_win_count_df_temp - 1)
player_win_count_df  = player_win_count_df.loc[start_date:end_date]
player_win_count_df = player_win_count_df.plot(marker = '.', legend = None)

def serial_date_to_string(n):
    #converts days since unix epoch to year
    new_date = datetime.datetime(1970,1,1,0,0) + datetime.timedelta(n - 1)
    return new_date.strftime("%Y")


def function(date, count, player):
    '''
    date: days since unix epoch of the selected point
    count: y coord of plot - needs to be rounded
    player: player name of the selected line
    checks these againts grand_slam_df and returns select information about the matching row
    '''
      
    selected_df1 = grand_slam_df[(grand_slam_df.tourney_year == int(serial_date_to_string(date))) & (grand_slam_df["count"] == round(count)) & (grand_slam_df.singles_winner_name == str(player))]
  
    if selected_df1.empty:
        return "Please pick valid data point \n typically the final dot in a row will be correct"
    
    selected_df2 = match_scores_df[(match_scores_df.tourney_year == str(serial_date_to_string(date))) & (match_scores_df["tourney_slug"] == str(selected_df1.iat[0, 5])) & (match_scores_df["round_order"] == 1)]

    selected_df1 = selected_df1[['tourney_year', 'tourney_name', 'tourney_surface', 'singles_winner_name']]
    selected_df2 = selected_df2[['match_score_tiebreaks', 'loser_name']]
    return "Year: " + str(selected_df1.iat[0, 0]) + ", Tourney: " + str(selected_df1.iat[0, 1]) + "\nSurface: " + str(selected_df1.iat[0, 2]) + ", Winner: " + str(selected_df1.iat[0, 3] + "\nLoser: " + str(selected_df2.iat[0, 1]) + ", Score: " + str(selected_df2.iat[0, 0]))

#plot formatting
plt.yticks([0, 4, 8, 12, 16, 20])
plt.xlabel("Year")
plt.ylabel("Grand Slam wins")
plt.title("Grand Slam wins per player")

#create the tooltip for tourney info
mplcursors.cursor(player_win_count_df).connect(
   "add", lambda sel: sel.annotation.set_text(function(sel.target_[0], sel.target_[1],sel.artist.get_label())))

plt.show()
