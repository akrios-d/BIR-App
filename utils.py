import geopandas as gpd
import pandas as pd
from pathlib import Path
from typing import Optional

# --- Column detection sets ---

PRECISION_COL_CANDIDATES = [
    'geo_precision', 'geographic_precision', 'precision', 'location_precision'
]

COUNTRY_COL_CANDIDATES = [
    'country', 'recipient_country', 'iso3', 'country_name'
]

SECTOR_COL_CANDIDATES = [
    'sector', 'broad_sector_name', 'sector_name'
]

YEAR_COL_CANDIDATES = [
    'year', 'commitment_year', 'start_year'
]

VALUE_COL_CANDIDATES = [
    'project_value_usd', 'usd_commitment', 'commitment_amount_usd', 'value_usd_2021_const'
]


def detect_columns(gdf: gpd.GeoDataFrame):
    cols = gdf.columns.str.lower()
    def pick(cands):
        for c in cands:
            if c in cols:
                return gdf.columns[cols.get_loc(c)]
        return None
    return {
        'precision': pick(PRECISION_COL_CANDIDATES),
        'country': pick(COUNTRY_COL_CANDIDATES),
        'sector': pick(SECTOR_COL_CANDIDATES),
        'year': pick(YEAR_COL_CANDIDATES),
        'value': pick(VALUE_COL_CANDIDATES)
    }


# ------------------------------------------------------------------
# FIXED & FULLY WORKING GPKG READER
# ------------------------------------------------------------------
def read_geopackage(path: Path, layer: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    Robust GeoPackage reader using pyogrio if available, then Fiona, then generic read_file.
    Always returns a GeoDataFrame or raises a meaningful error.
    """
    if path is None:
        raise ValueError("No GeoPackage path provided.")

    # 1) Try pyogrio first (best and Fiona-independent)
    try:
        import pyogrio
        if layer is None:
            layers = [l[0] for l in pyogrio.list_layers(str(path))]
            if not layers:
                raise RuntimeError(f"No layers found inside {path}")

            # try returning the first non-empty layer
            for lyr in layers:
                g = gpd.read_file(path, layer=lyr, engine="pyogrio")
                if len(g):
                    return g
            # otherwise return first layer even if empty
            return gpd.read_file(path, layer=layers[0], engine="pyogrio")

        # explicit layer requested
        return gpd.read_file(path, layer=layer, engine="pyogrio")

    except Exception:
        pass

    # 2) Try Fiona
    try:
        import fiona
        if layer is None:
            layers = fiona.listlayers(str(path))
            if not layers:
                raise RuntimeError(f"No layers found in {path} via Fiona")

            for lyr in layers:
                g = gpd.read_file(path, layer=lyr)
                if len(g):
                    return g
            return gpd.read_file(path, layer=layers[0])

        return gpd.read_file(path, layer=layer)

    except Exception:
        pass

    # 3) Last resort — generic (may fail if no engine can read GPKG)
    try:
        return gpd.read_file(path)
    except Exception as exc:
        raise RuntimeError(f"Unable to read GeoPackage {path}. Cause: {exc}")


# ------------------------------------------------------------------
# GeoJSON folder reader
# ------------------------------------------------------------------
def read_geojson_folder(folder: Path) -> gpd.GeoDataFrame:
    files = list(folder.glob('*.geojson'))
    if not files:
        raise FileNotFoundError('No .geojson files found in folder')
    frames = []
    for f in files:
        try:
            frames.append(gpd.read_file(f))
        except Exception:
            continue
    if not frames:
        raise RuntimeError('Could not read any GeoJSON files')
    return pd.concat(frames, ignore_index=True)


# ------------------------------------------------------------------
# CRS tools
# ------------------------------------------------------------------
def to_wgs84(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        return gdf.set_crs(4326, allow_override=True)
    try:
        if gdf.crs.to_epsg() == 4326:
            return gdf
    except Exception:
        pass
    return gdf.to_crs(4326)


# ------------------------------------------------------------------
# Simplify
# ------------------------------------------------------------------
def simplify_geometries(gdf: gpd.GeoDataFrame, tolerance: float = 0.001) -> gpd.GeoDataFrame:
    try:
        gdf = gdf.copy()
        gdf['geometry'] = gdf.geometry.simplify(tolerance, preserve_topology=True)
        return gdf
    except Exception:
        return gdf