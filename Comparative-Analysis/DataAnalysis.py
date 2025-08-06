import pandas as pd
import time,os,psutil

# Start performance tracking
start_time = time.time()
process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / (1024 * 1024)
# Load and process data
df = pd.read_csv("INDIAVIX.csv", parse_dates=["Date"])
df.sort_values("Date", inplace=True)
df["Year"] = df["Date"].dt.year
# Filter for years 2009 to 2021
df_filtered = df[(df["Year"] >= 2009) & (df["Year"] <= 2021)]

# Group by year and calculate summary stats on 'Close'
yearly_summary = df_filtered.groupby("Year")["Close"].agg(
    Average_VIX="mean",
    Max_VIX="max",
    Min_VIX="min",
    Std_Dev_VIX="std"
).reset_index()

# Add trend based on change in average VIX
yearly_summary["Trend"] = yearly_summary["Average_VIX"].diff().apply(
    lambda x: "↑ Up" if x > 0 else ("↓ Down" if x < 0 else "→ Flat")
)
# First year has no prior year to compare
yearly_summary.loc[0, "Trend"] = "N/A"

# End performance tracking
mem_after = process.memory_info().rss / (1024 * 1024)
print(f"Execution Time: {time.time() - start_time:.3f}s")
print(f"Memory Used: {mem_after - mem_before:.2f} MB")
# Print results
print("\nYearly India VIX Summary with Trends (2009–2021):")
print(yearly_summary.to_string(index=False, float_format="%.2f"))


