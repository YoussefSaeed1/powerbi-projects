# Egypt Property Market · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

## Market

### Listings
Format: `#,0`

```dax
COUNTROWS ( Fact_Listings )
```

### Average Price
Format: `#,0`

```dax
AVERAGE ( Fact_Listings[Price_EGP] )
```

### Average Price M
Format: `#,0.00`

```dax
DIVIDE ( [Average Price], 1000000 )
```

### Median Price
Format: `#,0`

```dax
MEDIAN ( Fact_Listings[Price_EGP] )
```

### Average Area
Format: `#,0`

```dax
AVERAGE ( Fact_Listings[Area_m2] )
```

### Price per m2
Total asking price ÷ total area (EGP per m²).
Format: `#,0`

```dax
DIVIDE ( SUM ( Fact_Listings[Price_EGP] ), SUM ( Fact_Listings[Area_m2] ) )
```

### Price per m2 K
Format: `#,0.0`

```dax
DIVIDE ( [Price per m2], 1000 )
```

### Listings Share %
Format: `0%`

```dax
DIVIDE ( [Listings], CALCULATE ( [Listings], ALL ( Dim_Bedrooms ), ALL ( Dim_Budget ) ) )
```

### Listing Area
Area of the listing (used per listing in the scatter).
Format: `#,0`

```dax
SUM ( Fact_Listings[Area_m2] )
```

### Listing Price M
Format: `#,0.00`

```dax
DIVIDE ( SUM ( Fact_Listings[Price_EGP] ), 1000000 )
```

## Value

### Area for EGP 2M
Square metres EGP 2 million buys at the average price per m².
Format: `#,0`

```dax
DIVIDE ( 2000000, [Price per m2] )
```

### Budget Listings
Format: `#,0`

```dax
VAR _lo = SELECTEDVALUE ( Dim_Budget[From EGP] )
VAR _hi = SELECTEDVALUE ( Dim_Budget[To EGP] )
RETURN
    CALCULATE ( [Listings], Fact_Listings[Price_EGP] >= _lo, Fact_Listings[Price_EGP] < _hi )
```

### Budget Share %
Format: `0%`

```dax
DIVIDE ( [Budget Listings], CALCULATE ( [Listings], ALL ( Dim_Budget ) ) )
```

### Budget Typical Area
Median area of the listings in the budget band.
Format: `#,0`

```dax
VAR _lo = SELECTEDVALUE ( Dim_Budget[From EGP] )
VAR _hi = SELECTEDVALUE ( Dim_Budget[To EGP] )
RETURN
    CALCULATE ( MEDIAN ( Fact_Listings[Area_m2] ), Fact_Listings[Price_EGP] >= _lo, Fact_Listings[Price_EGP] < _hi )
```

### Budget Typical Type

```dax
VAR _lo = SELECTEDVALUE ( Dim_Budget[From EGP] )
VAR _hi = SELECTEDVALUE ( Dim_Budget[To EGP] )
VAR _t = TOPN ( 1, ADDCOLUMNS ( CROSSJOIN ( ALL ( Dim_Bedrooms[Bedrooms] ), ALL ( Dim_Type[PropertyType] ) ),
        "@n", CALCULATE ( [Listings], Fact_Listings[Price_EGP] >= _lo, Fact_Listings[Price_EGP] < _hi ) ), [@n], DESC )
RETURN
    MAXX ( _t, Dim_Bedrooms[Bedrooms] & "-bed " & LOWER ( Dim_Type[PropertyType] ) )
```

### Mid Band Share
Format: `0%`

```dax
CALCULATE ( [Budget Share %], Dim_Budget[Budget Order] = 2 )
```

### Mid Band Typical Area
Format: `#,0`

```dax
CALCULATE ( [Budget Typical Area], Dim_Budget[Budget Order] = 2 )
```

### Mid Band Typical Type

```dax
CALCULATE ( [Budget Typical Type], Dim_Budget[Budget Order] = 2 )
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( MAX ( DQ_Source[RawRows] ), "#,0" ),
        2, FORMAT ( MAX ( DQ_Source[DuplicateIDs] ), "#,0" ),
        3, FORMAT ( MAX ( DQ_Source[InvalidAreaOrPrice] ), "#,0" ),
        4, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Listings ) ), "#,0" ),
        5, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Listings ), ISBLANK ( RELATED ( Dim_Location[City] ) ) ) ), "#,0" ),
        6, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Listings ), Fact_Listings[Bathrooms] > Fact_Listings[Bedrooms] + 1 ) ), "#,0" ),
        7, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Listings ), DIVIDE ( Fact_Listings[Price_EGP], Fact_Listings[Area_m2] ) < 3000 || DIVIDE ( Fact_Listings[Price_EGP], Fact_Listings[Area_m2] ) > 40000 ) ), "#,0" ),
        8, FORMAT ( CALCULATE ( MAX ( Fact_Listings[ListedOn] ), REMOVEFILTERS () ), "dd mmm yyyy" )
    )
```

### DQ Status

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
VAR _v = [DQ Value]
RETURN
    SWITCH ( TRUE (), ISBLANK ( _o ), BLANK (), _o IN { 1, 4, 8 }, "Info", _o IN { 2, 3 }, IF ( _v = "0", "Pass", "Cleaned" ), _v = "0", "Pass", "Fail" )
```

### DQ Failed Checks
Format: `0`

```dax
COUNTROWS ( FILTER ( ALL ( Dim_DQ ), [DQ Status] = "Fail" ) )
```

## Insights

### Most Expensive Segment

```dax
VAR _t = TOPN ( 1, CROSSJOIN ( ALL ( Dim_Location[City] ), ALL ( Dim_Type[PropertyType] ) ), [Average Price], DESC )
RETURN
    MAXX ( _t, Dim_Location[City] & " " & LOWER ( Dim_Type[PropertyType] ) & "s" )
```

### Most Expensive Segment Price
Format: `#,0`

```dax
MAXX ( CROSSJOIN ( ALL ( Dim_Location[City] ), ALL ( Dim_Type[PropertyType] ) ), [Average Price] )
```

### Cheapest Apartment City

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Location[City] ), CALCULATE ( [Price per m2], Dim_Type[PropertyType] = "Apartment" ), ASC )
RETURN
    MAXX ( _t, Dim_Location[City] )
```

### Cheapest Apartment PPM
Format: `#,0`

```dax
MINX ( ALL ( Dim_Location[City] ), CALCULATE ( [Price per m2], Dim_Type[PropertyType] = "Apartment" ) )
```

### Priciest Villa City

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Location[City] ), CALCULATE ( [Price per m2], Dim_Type[PropertyType] = "Villa" ), DESC )
RETURN
    MAXX ( _t, Dim_Location[City] )
```

### Priciest Villa PPM
Format: `#,0`

```dax
MAXX ( ALL ( Dim_Location[City] ), CALCULATE ( [Price per m2], Dim_Type[PropertyType] = "Villa" ) )
```

### Most Common Bedrooms

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Bedrooms[Bedrooms], Dim_Bedrooms[Bedroom Label] ), [Listings], DESC )
RETURN
    MAXX ( _t, Dim_Bedrooms[Bedroom Label] )
```

### Most Common Bedrooms Share
Format: `0%`

```dax
DIVIDE ( MAXX ( ALL ( Dim_Bedrooms[Bedrooms] ), [Listings] ), CALCULATE ( [Listings], ALL ( Dim_Bedrooms ) ) )
```

### Space Gain vs Cairo
How much more apartment space the cheapest city buys than Cairo for the same budget.
Format: `0%`

```dax
VAR _cairo = CALCULATE ( [Price per m2], Dim_Type[PropertyType] = "Apartment", Dim_Location[City] = "Cairo" )
VAR _best = [Cheapest Apartment PPM]
RETURN
    DIVIDE ( _cairo, _best ) - 1
```

### Cheapest Bedrooms

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Bedrooms[Bedrooms], Dim_Bedrooms[Bedroom Label] ), [Price per m2], ASC )
RETURN
    MAXX ( _t, Dim_Bedrooms[Bedroom Label] )
```

### Cairo Premium
Checks whether the cheapest Cairo district is still above every other district.

```dax
VAR _cmin = MINX ( CALCULATETABLE ( VALUES ( Dim_Location[District] ), Dim_Location[City] = "Cairo" ), [Price per m2] )
VAR _omax = MAXX ( CALCULATETABLE ( VALUES ( Dim_Location[District] ), Dim_Location[City] <> "Cairo" ), [Price per m2] )
RETURN
    IF ( _cmin > _omax, "Every Cairo district costs more per m² than any district in Giza or Alexandria.", "Cairo districts are the most expensive per m² on average." )
```

### Insight Market

```dax
"<div style='font-family:Segoe UI,sans-serif;background:#183A2F;color:#E6EDE8;border-radius:10px;padding:12px 16px;box-sizing:border-box;height:100%;'><div style='font-size:12.5px;font-weight:700;margin:0 0 8px;color:#FFFFFF'>What the data says</div>"
    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "<b style='color:#E3C98F'>" & [Cheapest Apartment City] & "</b>" & " has the cheapest apartments per m² (EGP " & FORMAT ( [Cheapest Apartment PPM] / 1000, "#,0.0" ) & "K) and " & "<b style='color:#E3C98F'>" & [Priciest Villa City] & "</b>" & " the priciest villas (EGP " & FORMAT ( [Priciest Villa PPM] / 1000, "#,0.0" ) & "K)." ) & "</p>"
    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( [Cairo Premium] ) & "</p>"
    & "</div>"
```

### Insight Value

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### PPM Heatmap
HTML heatmap of price per m² by city and property type.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Side KPIs
Headline numbers in the side panel (HTML Content visual).

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### City Cards
One card per city: average price and price per m² for apartments and villas. The cheapest apartment city is highlighted.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Budget Waffle
What EGP 2 million buys in each city and property type; each square is 10 m².

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### Bedroom Color

```dax
IF ( [Price per m2] = MINX ( ALL ( Dim_Bedrooms ), [Price per m2] ), "#C2603F", "#5E8574" )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2E8B57", "Info", "#C9D3CC", "Cleaned", "#C2603F", "#B23A3A" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='62' height='20' viewBox='0 0 62 20'>"
        & "<rect x='1' y='2' width='60' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='31' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### District Color

```dax
SWITCH ( SELECTEDVALUE ( Dim_Location[City] ), "Cairo", "#183A2F", "Giza", "#5E8574", "#C2603F" )
```
