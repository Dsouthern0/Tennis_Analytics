import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

grand_slam_df = pd.read_csv('data/tournaments_1877-2017_unindexed_csv.csv', parse_dates = ['tourney_dates'])
#grand_slam = ["wimbledon", "us-open", "australian-open", "roland-garros"]
grand_slam = ["wimbledon", "us-open", "australian-open", "roland-garros"]
#surface = ["Grass", "Hard", "Carpet", "Clay"]
surface = ["Grass", "Hard", "Carpet", "Clay"]

grand_slam_df = grand_slam_df[grand_slam_df["tourney_slug"].isin(grand_slam)]
grand_slam_df = grand_slam_df[grand_slam_df["tourney_surface"].isin(surface)]

count = grand_slam_df.groupby(['singles_winner_name']).cumcount().add(1)

grand_slam_df.insert(2, "count", count, True)
grand_slam_df = grand_slam_df.pivot(index = 'singles_winner_name', columns = 'tourney_dates', values = 'count')

grand_slam_df = grand_slam_df.T
grand_slam_df = grand_slam_df.fillna(method='bfill')

grand_slam_df.plot(legend = None)

plt.yticks([0, 4, 8, 12, 16, 20])
plt.xlabel("Year")
plt.ylabel("Grand Slam wins")
plt.title("Grand Slam wins per player")

mplcursors.cursor().connect(
    "add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

plt.show()
