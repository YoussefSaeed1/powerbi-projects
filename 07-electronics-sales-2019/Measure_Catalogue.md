# Electronics Sales 2019 · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

## Sales

### Revenue
Quantity × price each.
Format: `$#,0`

```dax
SUMX ( Fact_Sales, Fact_Sales[Quantity] * Fact_Sales[PriceEach] )
```

### Revenue $M
Format: `$#,0.00`

```dax
DIVIDE ( [Revenue], 1000000 )
```

### Units
Format: `#,0`

```dax
SUM ( Fact_Sales[Quantity] )
```

### Orders
Distinct order IDs; one order can hold several lines.
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[OrderID] )
```

### Order Lines
Format: `#,0`

```dax
COUNTROWS ( Fact_Sales )
```

### Average Order Value
Format: `$#,0.0`

```dax
DIVIDE ( [Revenue], [Orders] )
```

### Revenue Share %
Format: `0.0%`

```dax
DIVIDE ( [Revenue], CALCULATE ( [Revenue], ALL ( Dim_City ), ALL ( Dim_Product ) ) )
```

### Units Share %
Format: `0.0%`

```dax
DIVIDE ( [Units], CALCULATE ( [Units], ALL ( Dim_City ), ALL ( Dim_Product ) ) )
```

### Group Role

```dax
VAR _r = [Revenue Share %]
VAR _u = [Units Share %]
RETURN
    IF ( ISBLANK ( _r ), BLANK (), IF ( _r >= 0.2, "Revenue driver", IF ( _u >= 0.3, "Traffic driver", IF ( _r >= 0.1, "Steady", "Add-on" ) ) ) )
```

### Orders by Hour
Format: `#,0`

```dax
[Orders]
```

### iPhone + Lightning Orders
Orders that contain both an iPhone and a Lightning cable.
Format: `#,0`

```dax
VAR _a = CALCULATETABLE ( VALUES ( Fact_Sales[OrderID] ), Dim_Product[Product] = "iPhone" )
VAR _b = CALCULATETABLE ( VALUES ( Fact_Sales[OrderID] ), Dim_Product[Product] = "Lightning Charging Cable" )
RETURN
    COUNTROWS ( INTERSECT ( _a, _b ) )
```

### Multi-Product Orders %
Format: `0.0%`

```dax
VAR _o = ADDCOLUMNS ( VALUES ( Fact_Sales[OrderID] ), "@n", CALCULATE ( COUNTROWS ( Fact_Sales ) ) )
RETURN
    DIVIDE ( COUNTROWS ( FILTER ( _o, [@n] > 1 ) ), COUNTROWS ( _o ) )
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Sales ) ), "#,0" ),
        2, FORMAT ( CALCULATE ( DISTINCTCOUNT ( Fact_Sales[OrderID] ), REMOVEFILTERS () ), "#,0" ),
        3, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), ISBLANK ( RELATED ( Dim_Product[Product Group] ) ) ) ), "#,0" ),
        4, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[Quantity] <= 0 ) ), "#,0" ),
        5, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[PriceEach] <> RELATED ( Dim_Product[List Price] ) ) ), "#,0" ),
        6, FORMAT ( 0 + COUNTROWS ( FILTER ( ADDCOLUMNS ( ALL ( Fact_Sales[OrderID] ), "@c", CALCULATE ( DISTINCTCOUNT ( Fact_Sales[City] ), REMOVEFILTERS ( Dim_City ) ) ), [@c] > 1 ) ), "#,0" ),
        7, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), YEAR ( Fact_Sales[OrderDate] ) <> 2019 ) ), "#,0" ),
        8, FORMAT ( CALCULATE ( MAX ( Fact_Sales[OrderDate] ), REMOVEFILTERS () ), "dd mmm yyyy" )
    )
```

### DQ Status

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
VAR _v = [DQ Value]
RETURN
    SWITCH ( TRUE (), ISBLANK ( _o ), BLANK (), _o IN { 1, 2, 8 }, "Info", _v = "0", "Pass", "Fail" )
```

### DQ Failed Checks
Format: `0`

```dax
COUNTROWS ( FILTER ( ALL ( Dim_DQ ), [DQ Status] = "Fail" ) )
```

## Insights

### Peak Month

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Date[Month], Dim_Date[MonthNo] ), [Revenue], DESC )
RETURN
    MAXX ( _t, Dim_Date[Month] )
```

### Peak Month Revenue
Format: `$#,0`

```dax
MAXX ( ALL ( Dim_Date[Month], Dim_Date[MonthNo] ), [Revenue] )
```

### Peak Month Share
Format: `0%`

```dax
DIVIDE ( [Peak Month Revenue], CALCULATE ( [Revenue], ALL ( Dim_Date ) ) )
```

### Q4 Share
Format: `0%`

```dax
DIVIDE ( CALCULATE ( [Revenue], Dim_Date[Quarter] = "Q4" ), CALCULATE ( [Revenue], ALL ( Dim_Date[Quarter] ) ) )
```

### Top City

```dax
VAR _t = TOPN ( 1, ALL ( Dim_City[City] ), [Revenue], DESC )
RETURN
    MAXX ( _t, Dim_City[City] )
```

### Top City Share
Format: `0%`

```dax
DIVIDE ( MAXX ( ALL ( Dim_City[City] ), [Revenue] ), CALCULATE ( [Revenue], ALL ( Dim_City ) ) )
```

### Peak Hours

```dax
VAR _t = TOPN ( 2, ALL ( Dim_Hour[Hour], Dim_Hour[Hour Label] ), [Orders], DESC )
RETURN
    CONCATENATEX ( _t, Dim_Hour[Hour Label], " and ", Dim_Hour[Hour], ASC )
```

### Laptop Revenue Share
Format: `0%`

```dax
CALCULATE ( [Revenue Share %], Dim_Product[Product Group] = "Laptops" )
```

### Laptop Units Share
Format: `0%`

```dax
CALCULATE ( [Units Share %], Dim_Product[Product Group] = "Laptops" )
```

### Cable Revenue Share
Format: `0%`

```dax
CALCULATE ( [Revenue Share %], Dim_Product[Product Group] = "Cables & batteries" )
```

### Cable Units Share
Format: `0%`

```dax
CALCULATE ( [Units Share %], Dim_Product[Product Group] = "Cables & batteries" )
```

### Top Product

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Product[Product] ), [Revenue], DESC )
RETURN
    MAXX ( _t, Dim_Product[Product] )
```

### Top Product Revenue
Format: `$#,0`

```dax
MAXX ( ALL ( Dim_Product[Product] ), [Revenue] )
```

### Most Units Product

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Product[Product] ), [Units], DESC )
RETURN
    MAXX ( _t, Dim_Product[Product] )
```

### Most Units
Format: `#,0`

```dax
MAXX ( ALL ( Dim_Product[Product] ), [Units] )
```

### Quietest Hour

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Hour[Hour], Dim_Hour[Hour Label] ), [Orders], ASC )
RETURN
    MAXX ( _t, Dim_Hour[Hour Label] )
```

### Insight When

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Products

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### Ticker When
KPI ticker for the When & Where page (HTML Content visual).

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Ticker Products
KPI ticker for the Products page (HTML Content visual).

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Q4 Label
Q4 call-out on the monthly chart.

```dax
"<div style='text-align:right;font-family:Segoe UI,sans-serif;font-size:11.5px;font-weight:700;color:#FF5A1F'>Q4 = " & FORMAT ( [Q4 Share], "0%" ) & " of revenue</div>"
```

### Hour Strip
Orders by hour as a 24-cell heat strip; the two busiest hours in orange.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Units vs Revenue
Share of units vs share of revenue by product group, drawn as a butterfly chart.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### Month Color
Peak month in orange, the rest of Q4 in light orange.

```dax
VAR _m = SELECTEDVALUE ( Dim_Date[MonthNo] )
RETURN
    IF ( [Revenue] = [Peak Month Revenue], "#FF5A1F", IF ( _m >= 10, "#FFB08F", "#2B2F38" ) )
```

### City Color

```dax
IF ( SELECTEDVALUE ( Dim_City[City] ) = [Top City], "#FF5A1F", "#2B2F38" )
```

### Group Color

```dax
IF ( [Revenue Share %] >= 0.2, "#FF5A1F", "#2B2F38" )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2F9E6E", "Info", "#8A8A96", "#E0303F" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='56' height='20' viewBox='0 0 56 20'>"
        & "<rect x='1' y='2' width='54' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='28' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```
