# Sales vs Forecast · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Latest Month
Format: `mmm yyyy`

```dax
CALCULATE ( MAX ( Fact_Sales[MonthStart] ), REMOVEFILTERS () )
```

### Selected Year
Format: `0`

```dax
IF ( ISFILTERED ( Dim_Date[Year] ), MAX ( Dim_Date[Year] ), YEAR ( [Latest Month] ) )
```

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

## Sales

### Actual Sales
Actual sales amount.
Format: `$#,0`

```dax
SUM ( Fact_Sales[SalesAmount] )
```

### Actual CY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Actual Sales], Dim_Date[Year] = _y )
```

### Actual LY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Actual Sales], Dim_Date[Year] = _y - 1 )
```

### Actual CY $M
Format: `$#,0.00`

```dax
DIVIDE ( [Actual CY], 1000000 )
```

### Actual LY $M
Format: `$#,0.00`

```dax
DIVIDE ( [Actual LY], 1000000 )
```

### Change vs LY
Format: `$#,0`

```dax
[Actual CY] - [Actual LY]
```

### Change vs LY %
Format: `+0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Change vs LY], [Actual LY] )
```

### Change vs LY $M
Format: `+$#,0.00;-$#,0.00`

```dax
DIVIDE ( [Change vs LY], 1000000 )
```

### Bridge Value $M
Values for the year-on-year bridge: last year, then each country's change. The waterfall total is this year.
Format: `$#,0.00`

```dax
VAR _o = SELECTEDVALUE ( 'Bridge Step'[Step Order] )
VAR _c = SELECTEDVALUE ( 'Bridge Step'[Country] )
RETURN
    IF (
        _o = 1,
        CALCULATE ( [Actual LY $M], REMOVEFILTERS ( Dim_Geography ) ),
        CALCULATE ( [Change vs LY $M], Dim_Geography[Country] = _c )
    )
```

## Forecast

### Forecast Sales
Planned (forecast) sales amount.
Format: `$#,0`

```dax
SUM ( Fact_Forecast[ForecastAmount] )
```

### Forecast CY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Forecast Sales], Dim_Date[Year] = _y )
```

### Forecast CY $M
Format: `$#,0.00`

```dax
DIVIDE ( [Forecast CY], 1000000 )
```

### Gap vs Forecast
Actual minus forecast; positive means the plan was beaten.
Format: `+$#,0;-$#,0`

```dax
[Actual CY] - [Forecast CY]
```

### Gap vs Forecast %
Format: `+0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Gap vs Forecast], [Forecast CY] )
```

### Bias %
Actual vs forecast for the cell in context. Positive means the forecast was too low.
Format: `0.0%`

```dax
DIVIDE ( [Actual CY] - [Forecast CY], [Forecast CY] )
```

### Forecast Accuracy %
100% minus the mean absolute percentage error across the months of the year in focus, at the grain in context.
Format: `0.0%`

```dax
VAR _y = [Selected Year]
VAR _months =
    FILTER (
        CALCULATETABLE ( VALUES ( Dim_Date[YearMonthKey] ), Dim_Date[Year] = _y ),
        NOT ISBLANK ( CALCULATE ( [Forecast Sales] ) )
    )
VAR _mape =
    AVERAGEX ( _months, ABS ( DIVIDE ( CALCULATE ( [Actual Sales] ) - CALCULATE ( [Forecast Sales] ), CALCULATE ( [Forecast Sales] ) ) ) )
RETURN
    IF ( NOT ISBLANK ( _mape ), 1 - _mape )
```

### MAPE %
Format: `0.0%`

```dax
1 - [Forecast Accuracy %]
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
VAR _y = [Selected Year]
RETURN
    SWITCH (
        _o,
        1, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Sales ) ), "#,0" ),
        2, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Forecast ) ), "#,0" ),
        3, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), ISBLANK ( RELATED ( Dim_Product[ProductName] ) ) ) ), "#,0" ),
        4, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), ISBLANK ( RELATED ( Dim_Geography[Region] ) ) ) ), "#,0" ),
        5, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Forecast ), ISBLANK ( RELATED ( Dim_Category[Category] ) ) ) ), "#,0" ),
        6, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[SalesAmount] < 0 ) ) + COUNTROWS ( FILTER ( ALL ( Fact_Forecast ), Fact_Forecast[ForecastAmount] < 0 ) ), "#,0" ),
        7, FORMAT ( 0 + COUNTROWS ( FILTER ( CALCULATETABLE ( VALUES ( Dim_Date[YearMonthKey] ), REMOVEFILTERS (), Dim_Date[Year] = _y ),
                NOT ISBLANK ( CALCULATE ( [Actual Sales], REMOVEFILTERS ( Dim_Geography ), REMOVEFILTERS ( Dim_Category ) ) )
                    && ISBLANK ( CALCULATE ( [Forecast Sales], REMOVEFILTERS ( Dim_Geography ), REMOVEFILTERS ( Dim_Category ) ) ) ) ), "#,0" ),
        8, FORMAT ( [Latest Month], "mmm yyyy" )
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

### Lowest Accuracy Category

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Category[Category] ), [Forecast Accuracy %], ASC )
RETURN
    MAXX ( _t, Dim_Category[Category] )
```

### Lowest Accuracy
Format: `0.0%`

```dax
MINX ( ALL ( Dim_Category[Category] ), [Forecast Accuracy %] )
```

### Months Under Forecast
Months in the year in focus where actuals beat the forecast.
Format: `0`

```dax
VAR _y = [Selected Year]
RETURN
    COUNTROWS ( FILTER ( CALCULATETABLE ( VALUES ( Dim_Date[YearMonthKey] ), Dim_Date[Year] = _y ), CALCULATE ( [Actual Sales] ) > CALCULATE ( [Forecast Sales] ) ) )
```

### Months With Forecast
Format: `0`

```dax
VAR _y = [Selected Year]
RETURN
    COUNTROWS ( FILTER ( CALCULATETABLE ( VALUES ( Dim_Date[YearMonthKey] ), Dim_Date[Year] = _y ), NOT ISBLANK ( CALCULATE ( [Forecast Sales] ) ) ) )
```

### Biggest Decline Country

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Geography[Country] ), [Change vs LY], ASC )
RETURN
    MAXX ( _t, Dim_Geography[Country] )
```

### Biggest Decline Share
Format: `0%`

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Geography[Country] ), [Change vs LY], ASC )
RETURN
    DIVIDE ( MAXX ( _t, [Change vs LY] ), CALCULATE ( [Change vs LY], ALL ( Dim_Geography ) ) )
```

### Growing Categories

```dax
VAR _t = FILTER ( ALL ( Dim_Category[Category] ), [Change vs LY] > 0 )
RETURN
    CONCATENATEX ( _t, Dim_Category[Category], ", " )
```

### Insight Plan

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Accuracy

```dax
"<div style='font-family:Segoe UI,sans-serif;background:#2A2160;color:#DCD6FF;border-radius:10px;padding:12px 16px;box-sizing:border-box;height:100%;'><div style='font-size:12.5px;font-weight:700;margin:0 0 8px;color:#FFFFFF'>What the data says</div>"
    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "Actuals beat the forecast in " & "<b style='color:#F4B860'>" & FORMAT ( [Months Under Forecast], "0" ) & "</b>" & " of " & [Months With Forecast] & " months: a steady downward bias to correct in the next plan." ) & "</p>"
    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "<b style='color:#F4B860'>" & [Lowest Accuracy Category] & "</b>" & " is the hardest category to plan, at " & FORMAT ( [Lowest Accuracy], "0.0%" ) & " accuracy." ) & "</p>"
    & "</div>"
```

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### Accuracy Heatmap
HTML heatmap of forecast accuracy by category (rows) and country (columns).

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Plan

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### Change Color

```dax
IF ( [Change vs LY] < 0, "#FF7E7E", "#5FD0C0" )
```

### Bias Color

```dax
IF ( ABS ( [Bias %] ) > 0.05, "#F4B860", "#7B86F0" )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2E9E6B", "Info", "#5B6690", "#D1495B" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='56' height='20' viewBox='0 0 56 20'>"
        & "<rect x='1' y='2' width='54' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='28' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```
