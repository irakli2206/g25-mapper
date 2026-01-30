import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import contextily as cx
import io

# 1. DATA PARSING
# 1. DATA LOADING
csv_data = """Target,Distance,China_AmurRiver_N,Georgia_Kotias.SG,Iran_GanjDareh_N,Israel_Natufian,Russia_Karelia_HG,Turkey_Barcin_LN.SG
Georgian_Megr,0.02342345,0.0,62.0,0.6,3.0,0.0,34.4
Georgian_Svaneti,0.02402861,1.6,61.8,0.4,1.4,2.2,32.6
Abkhasian,0.02332650,1.8,59.2,0.0,3.4,2.6,33.0
Georgian_Guria,0.02661309,0.0,59.2,1.2,5.0,0.0,34.6
Abkhasian_Gudauta,0.03075723,0.4,59.0,0.8,5.4,3.8,30.6
Georgian_West,0.02504950,0.0,59.0,2.4,2.8,0.0,35.8
Georgian_Ratcha,0.03144960,0.0,58.6,3.0,5.6,0.0,32.8
Georgian_Imer,0.02591823,0.0,57.6,3.8,2.4,0.0,36.2
Ossetian,0.02273099,4.0,55.4,1.0,2.0,7.4,30.2
North_Ossetian,0.02513942,5.2,53.4,0.6,4.0,9.4,27.4
Georgian_Ajar,0.02874763,0.0,53.0,6.0,3.4,0.0,37.6
Georgian_Lechkhumi,0.02780471,1.2,53.0,6.2,5.0,0.0,34.6
Adygei,0.02192540,3.0,52.0,0.0,2.6,10.8,31.6
Georgian_Mtiuleti,0.03496813,0.0,51.6,7.4,0.0,4.0,37.0
Balkar,0.02382585,5.6,50.0,0.4,1.4,11.8,30.8
Georgian_NorthEast,0.03285699,0.0,49.4,7.0,2.8,6.4,34.4
Ingushian,0.03014065,3.0,48.6,4.0,2.4,12.4,29.6
Chechen,0.03406884,1.4,48.4,5.0,1.4,14.8,29.0
Georgian_Khevs,0.03246008,0.0,47.0,9.2,1.6,8.6,33.6
Hunzib,0.03773200,0.0,47.0,10.2,0.0,16.4,26.4
Circassian,0.02309369,6.0,46.4,2.4,1.6,12.2,31.4
Karachay,0.02049055,6.4,46.4,3.2,1.4,11.4,31.2
Georgian_Tush,0.03048405,0.0,46.2,9.0,0.0,9.0,35.8
Georgian_Laz,0.02857044,0.0,46.0,8.6,3.4,0.0,42.0
Georgian_Javakheti,0.03053718,0.0,45.6,12.2,2.6,0.0,39.6
Georgian_Kart,0.02994189,0.0,45.4,10.8,3.2,2.6,38.0
Darginian,0.04324269,0.0,44.2,9.2,0.0,23.0,23.6
Georgian_Kakh,0.02733996,0.0,44.0,12.6,4.4,1.4,37.6
Kabardin,0.02207105,6.4,43.6,3.2,1.2,12.6,33.0
Avar,0.04074581,0.0,43.0,10.6,0.0,22.0,24.4
Kaitag,0.04147812,0.0,41.4,9.8,0.0,22.2,26.6
Lak,0.03994312,0.4,41.4,12.0,0.0,21.0,25.2
Georgian_Samtckhe,0.02836476,0.0,41.2,14.0,3.6,0.0,41.2
Andian_A,0.03171108,0.0,40.4,13.4,3.4,5.4,37.4
Andian_B,0.03713386,0.0,40.0,11.8,0.0,22.4,25.8
Tabasaran,0.03962453,0.2,38.8,13.0,0.0,20.2,27.8
Kumyk,0.02996329,4.2,37.0,11.0,1.4,14.6,31.8
Lezgin,0.04239569,1.0,33.8,17.4,0.0,19.4,28.4
Azerbaijani_Republic_Shaki,0.02942448,2.4,29.0,19.6,5.6,7.0,36.4
Armenian_Syunik,0.03469479,0.0,27.8,21.2,5.6,2.4,43.0
Azerbaijani_Dagestan,0.03057347,3.2,27.6,21.8,2.6,11.6,33.2
Armenian_Ararat,0.03427140,0.0,26.0,21.8,7.0,0.0,45.2
Azerbaijani_Republic_Gabala,0.02947373,3.6,25.4,23.2,4.2,7.8,35.8
Azerbaijani_Republic_Agjabedi,0.03022576,5.2,20.6,26.6,6.8,5.8,35.0"""
df = pd.read_csv(io.StringIO(csv_data))

# 2. COORDINATES
coords = {
    # Existing Georgian & Abkhasian Groups
    "Georgian_Tush": (42.45, 45.6), 
    "Georgian_Khevs": (42.53, 44.95),
    "Georgian_Mtiuleti": (42.4, 44.6), 
    "Georgian_NorthEast": (42.61, 44.57),
    "Georgian_Kart": (41.99, 44.11), 
    "Georgian_Svaneti": (43.0, 42.5),
    "Georgian_Imer": (42.2, 42.9), 
    "Georgian_Megr": (42.5, 42.1),
    "Georgian_Kakh": (41.92, 45.48), 
    "Georgian_Lechkhumi": (42.6, 42.7),
    "Georgian_Ajar": (41.6, 42.0), 
    "Georgian_Guria": (41.9, 42.1),
    "Georgian_Javakheti": (41.4, 43.5), 
    "Georgian_Samtckhe": (41.6, 43.1),
    "Georgian_Ratcha": (42.6, 43.4), 
    "Georgian_Laz": (41.3, 41.5),
    "Georgian_West": (42.2, 42.3),
    "Abkhasian": (43.00, 41.01), 
    "Abkhasian_Gudauta": (43.10, 40.61),

    # North Caucasus Groups (Russia)
    "Chechen": (43.2, 45.6),
    "Ingushian": (43.1, 44.8),
    "Kabardin": (43.5, 43.4),
    "Adygei": (44.6, 40.1),
    "Circassian": (44.2, 42.0),
    "Karachay": (43.7, 42.1),
    "Balkar": (43.3, 43.2),
    "North_Ossetian": (43.0, 44.2),
    "Ossetian": (42.2, 44.0), # South Ossetia region
    "Kumyk": (43.1, 47.3),

    # Dagestan Highlands (North East Caucasus)
    "Avar": (42.4, 46.5),
    "Darginian": (42.3, 47.4),
    "Lak": (42.2, 47.1),
    "Lezgin": (41.6, 47.8),
    "Andian_A": (42.7, 46.2),
    "Andian_B": (42.7, 46.3),
    "Tabasaran": (41.9, 48.0),
    "Kaitag": (42.1, 47.8),
    "Hunzib": (42.2, 46.2),

    # South Caucasus (Armenia & Azerbaijan)
    "Armenian_Ararat": (39.8, 44.7),
    "Armenian_Syunik": (39.3, 46.2),
    "Azerbaijani_Dagestan": (42.0, 48.2),
    "Azerbaijani_Republic_Agjabedi": (40.0, 47.4),
    "Azerbaijani_Republic_Gabala": (40.9, 47.8),
    "Azerbaijani_Republic_Shaki": (41.2, 47.1)
}

df["Lat"] = df["Target"].map(lambda x: coords.get(x, (None, None))[0])
df["Lon"] = df["Target"].map(lambda x: coords.get(x, (None, None))[1])
df = df.dropna(subset=["Lat", "Lon"])

# 3. CONVERT & REPROJECT
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Lon, df.Lat), crs="EPSG:4326").to_crs(epsg=3857)

# 4. PLOTTING
fig, ax = plt.subplots(figsize=(15, 10))
ax.set_aspect('equal')

# Using Georgia_Kotias.SG (CHG) for color
# Cmap 'YlGn' (Yellow to Green) works well for ancestry %
scatter = ax.scatter(gdf.geometry.x, gdf.geometry.y, c=gdf['Georgia_Kotias.SG'], 
                     cmap='YlGn', s=500, edgecolor='black', linewidth=1.2, alpha=0.9, zorder=3)

# Add Legend
cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, pad=0.02)
cbar.set_label('CHG Ancestry % (Georgia_Kotias.SG)', fontsize=12, fontweight='bold')

# Basemap (Clean gray style)
cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)

# Add Labels
for i, row in gdf.iterrows():
    name = row["Target"].replace("Georgian_", "").replace("_", " ")
    ax.text(row.geometry.x, row.geometry.y, f" {name}\n ({row['Georgia_Kotias.SG']}%)", 
            fontsize=8, fontweight='bold', ha='left', va='center', zorder=4,
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.5))

# Expand extent slightly to avoid cramming
minx, miny, maxx, maxy = gdf.total_bounds
padding = 100000 
ax.set_xlim(minx - padding, maxx + padding)
ax.set_ylim(miny - padding, maxy + padding)

ax.set_axis_off()
plt.title("Distribution of CHG (Caucasus Hunter-Gatherer) Ancestry", fontsize=18, pad=25, fontweight='bold')
plt.tight_layout()
plt.show()