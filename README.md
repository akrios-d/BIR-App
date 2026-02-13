
# GCDF–BRI Local Map App

A lightweight **local** Streamlit app to explore **AidData's Geospatial Global Chinese Development Finance (GeoGCDF v3)** dataset on your PC. It reads a **GeoPackage (.gpkg)** or a **folder of GeoJSONs** and renders:

- An **interactive global map** (Folium/Leaflet) with filters (country, sector, year, precision, financing bucket)
- **Analytical overlays**: density heatmap (by points), optional custom overlays (e.g., BRI corridors, IMEC, Global Gateway)
- Export of **filtered subset** to GeoJSON

> The dataset contains geospatial features for 9,405 projects across 148 countries, including 6,266 precisely mapped roads, rail, energy lines, and buildings (>$830B) — see AidData docs. 

## 1) Install (recommended: Conda/Mamba)
```bash
# Create environment
mamba env create -f environment.yml  # or: conda env create -f environment.yml
conda activate gcdf-bri

# Run
streamlit run app.py
```

### Alternative: pip (may require system GDAL/PROJ)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scriptsctivate
pip install -r requirements.txt
streamlit run app.py
```

## 2) Prepare Data
- Place the **GeoPackage** in `./data/` (e.g., `geogcdf_v3.gpkg`), **or** keep a folder of per-project **GeoJSONs** under `./data/geojsons/`.
- Optionally drop overlay files (e.g., **BRI corridors**, **IMEC**, **Global Gateway**) as GeoJSON into `./overlays/`.

## 3) Usage Notes
- Use the sidebar to select the data source, filters, and overlays.
- Large datasets: enable *geometry simplification* and *tiling by type* in the sidebar.
- Export the filtered data via the **Download** button.

## 4) Folder Structure
```
gcdf_bri_app/
  app.py                # Streamlit app
  utils.py              # Helper functions
  environment.yml       # Conda environment
  requirements.txt      # pip fallback
  data/                 # Put your .gpkg or geojson folder here
  overlays/             # Optional overlay layers (corridors, etc.)
  assets/               # Icons, logos (optional)
  README.md
```

## 5) Data Sources & Context
- GeoGCDF v3 GitHub repository and documentation.
- AidData blog on the GeoGCDF v3 release (context and scope).
- Scientific Data open-access article describing methods and coverage.

## 6) Troubleshooting
- If GeoPandas fails to install via pip, use **Conda/Mamba**. The `environment.yml` pins compatible `gdal`, `geopandas`, and `pyogrio`.
- If the map is slow, enable *simplify geometries* and filter by region/years.

---
Made for local, offline exploration.
