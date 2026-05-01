# Business Rule Patterns — Predicting Irrigation Need

## Numeric Range Rules

| Column | Min | Max | Domain Rationale |
|--------|----:|----:|-----------------|
| Soil_pH | 0.0 | 14.0 | pH scale hard limit |
| Soil_pH | 4.0 | 9.0 | Agronomic tolerance for crops |
| Soil_Moisture | 0.0 | 100.0 | Percentage — cannot exceed 100 |
| Organic_Carbon | 0.0 | 10.0 | % weight; >10% is peat, not typical cropland |
| Electrical_Conductivity | 0.0 | 10.0 | dS/m; >10 is hyper-saline, crop-toxic |
| Temperature_C | -10.0 | 60.0 | Field agricultural range |
| Humidity | 0.0 | 100.0 | Relative humidity percentage |
| Rainfall_mm | 0.0 | 5000.0 | Annual; >5000 mm is extreme (Amazon-level) |
| Sunlight_Hours | 0.0 | 24.0 | Hours per day hard limit |
| Wind_Speed_kmh | 0.0 | 250.0 | Sustained farm-level wind |
| Field_Area_hectare | 0.0 | 1000.0 | Practical farm size |
| Previous_Irrigation_mm | 0.0 | 1000.0 | Per-event irrigation depth |

## Categorical Allowed Value Sets

| Column | Allowed Values |
|--------|---------------|
| Soil_Type | Sandy, Clay, Loamy, Silt |
| Crop_Type | Sugarcane, Rice, Cotton, Maize, Wheat, Potato |
| Crop_Growth_Stage | Sowing, Vegetative, Flowering, Harvest |
| Season | Kharif, Rabi, Zaid |
| Irrigation_Type | Canal, Sprinkler, Rainfed, Drip |
| Water_Source | Reservoir, River, Groundwater, Rainwater |
| Mulching_Used | Yes, No |
| Region | North, South, East, West, Central |
| Irrigation_Need | Low, Medium, High |

## Logical / Cross-Column Rules (for future validation)

| Rule | Description |
|------|-------------|
| Rainfed + high Previous_Irrigation_mm | Rainfed irrigation type should have low or zero Previous_Irrigation_mm |
| High Rainfall_mm + High irrigation | High annual rainfall should correlate with less irrigation need |
