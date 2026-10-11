# Pharmaceutical Trade Intelligence - Egypt · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Latest Data Date
Format: `mmm yyyy`

```dax
CALCULATE ( MAX ( Fact_Trade[Date] ), REMOVEFILTERS () )
```

### Selected Year
Year in focus: the year picked in the slicer, or the latest year in the data.
Format: `0`

```dax
VAR _maxYear = YEAR ( [Latest Data Date] )
RETURN
    IF ( ISFILTERED ( Dim_Date[Year] ), MAX ( Dim_Date[Year] ), _maxYear )
```

### Selected Year Last Month
Last month with data in the year in focus (September for 2025).
Format: `0`

```dax
VAR _y = [Selected Year]
VAR _end = [Latest Data Date]
RETURN
    CALCULATE ( MAX ( Dim_Date[MonthNo] ), REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _y, Dim_Date[Date] <= _end )
```

### Period Label

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    IF ( _m = 12, "FY" & _y, "Jan–" & FORMAT ( DATE ( _y, _m, 1 ), "mmm" ) & " " & _y )
```

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

## Trade

### Import Value
Value of antibiotic medicaments (HS 300420) exported to Egypt, as reported by the exporting countries (USD).
Format: `$#,0`

```dax
SUM ( Fact_Trade[Value_USD] )
```

### Value YTD CY
Value for the year in focus, up to the last month with data.
Format: `$#,0`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE ( [Import Value], Dim_Date[Year] = _y, Dim_Date[MonthNo] <= _m )
```

### Value YTD LY
Same months of the prior year, so partial years compare fairly.
Format: `$#,0`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE ( [Import Value], Dim_Date[Year] = _y - 1, Dim_Date[MonthNo] <= _m )
```

### Value YoY %
Format: `+0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Value YTD CY] - [Value YTD LY], [Value YTD LY] )
```

### Value CY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Import Value], Dim_Date[Year] = _y )
```

### Value LY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Import Value], Dim_Date[Year] = _y - 1 )
```

### Value CY $M
Format: `$#,0.0`

```dax
DIVIDE ( [Value CY], 1000000 )
```

### Value LY $M
Format: `$#,0.0`

```dax
DIVIDE ( [Value LY], 1000000 )
```

### Value R12
Rolling 12 months ending at the last month in context.
Format: `$#,0`

```dax
VAR _end = MIN ( [Latest Data Date], MAX ( Dim_Date[Date] ) )
RETURN
    CALCULATE ( [Import Value], REMOVEFILTERS ( Dim_Date ), DATESINPERIOD ( Dim_Date[Date], _end, -12, MONTH ) )
```

### Value by Trend Year $M
Annual value for the long-term chart (not filtered by the year slicer).
Format: `$#,0.0`

```dax
VAR _yr = SELECTEDVALUE ( 'Trend Year'[Year] )
RETURN
    DIVIDE ( CALCULATE ( [Import Value], REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _yr ), 1000000 )
```

### Net Weight Kg
Format: `#,0`

```dax
SUM ( Fact_Trade[NetWeight_Kg] )
```

### Price per Kg
Value per kg, using only rows that report a net weight.
Format: `$#,0.00`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE (
        DIVIDE ( SUM ( Fact_Trade[Value_USD] ), SUM ( Fact_Trade[NetWeight_Kg] ) ),
        Dim_Date[Year] = _y, Dim_Date[MonthNo] <= _m,
        Fact_Trade[NetWeight_Kg] > 0
    )
```

### Price per Kg LY
Format: `$#,0.00`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE (
        DIVIDE ( SUM ( Fact_Trade[Value_USD] ), SUM ( Fact_Trade[NetWeight_Kg] ) ),
        Dim_Date[Year] = _y - 1, Dim_Date[MonthNo] <= _m,
        Fact_Trade[NetWeight_Kg] > 0
    )
```

### Supplier Countries
Format: `0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DISTINCTCOUNT ( Fact_Trade[ReporterCode] ), Fact_Trade[Value_USD] > 0, Dim_Date[Year] = _y )
```

### Supplier Countries LY
Format: `0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DISTINCTCOUNT ( Fact_Trade[ReporterCode] ), Fact_Trade[Value_USD] > 0, Dim_Date[Year] = _y - 1 )
```

## Suppliers

### Supplier Share %
Share of the import value in the period, by exporting country.
Format: `0.0%`

```dax
DIVIDE ( [Value YTD CY], CALCULATE ( [Value YTD CY], ALL ( Dim_Supplier ) ) )
```

### Top Supplier Share %
Format: `0.0%`

```dax
MAXX ( ALL ( Dim_Supplier[Country] ), [Supplier Share %] )
```

### Top Supplier

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Supplier[Country] ), [Value YTD CY], DESC )
RETURN
    MAXX ( _t, Dim_Supplier[Country] )
```

### Second Supplier

```dax
VAR _t2 = TOPN ( 2, ALL ( Dim_Supplier[Country] ), [Value YTD CY], DESC )
VAR _t1 = TOPN ( 1, ALL ( Dim_Supplier[Country] ), [Value YTD CY], DESC )
RETURN
    MAXX ( EXCEPT ( _t2, _t1 ), Dim_Supplier[Country] )
```

### Top 2 Share %
Format: `0.0%`

```dax
VAR _t = TOPN ( 2, ALL ( Dim_Supplier[Country] ), [Value YTD CY], DESC )
RETURN
    DIVIDE ( CALCULATE ( [Value YTD CY], _t ), CALCULATE ( [Value YTD CY], ALL ( Dim_Supplier ) ) )
```

### Top 3 Share %
Format: `0.0%`

```dax
VAR _t = TOPN ( 3, ALL ( Dim_Supplier[Country] ), [Value YTD CY], DESC )
RETURN
    DIVIDE ( CALCULATE ( [Value YTD CY], _t ), CALCULATE ( [Value YTD CY], ALL ( Dim_Supplier ) ) )
```

### HHI
Herfindahl-Hirschman index of supplier concentration (0–10,000). Above 2,500 is highly concentrated.
Format: `#,0`

```dax
ROUND ( SUMX ( ALL ( Dim_Supplier[Country] ), [Supplier Share %] ^ 2 ) * 10000, 0 )
```

### HHI Label

```dax
VAR _h = [HHI] RETURN IF ( _h > 2500, "highly concentrated", IF ( _h > 1500, "moderately concentrated", "competitive" ) )
```

### Volatility %
Month-to-month variation over the year in focus and the year before (coefficient of variation). Months with no shipments count as zero.
Format: `0%`

```dax
VAR _y = [Selected Year]
VAR _end = [Latest Data Date]
VAR _months =
    CALCULATETABLE ( VALUES ( Dim_Date[YearMonthKey] ), REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] >= _y - 1, Dim_Date[Year] <= _y, Dim_Date[Date] <= _end )
VAR _vals =
    ADDCOLUMNS ( _months, "@v", COALESCE ( CALCULATE ( [Import Value], REMOVEFILTERS ( Dim_Date[Year] ) ), 0 ) )
RETURN
    IF ( NOT ISBLANK ( [Value YTD CY] ), DIVIDE ( STDEVX.P ( _vals, [@v] ), AVERAGEX ( _vals, [@v] ) ) )
```

### Share Rank
Format: `0`

```dax
VAR _set = FILTER ( ALLSELECTED ( Dim_Supplier[Country] ), NOT ISBLANK ( [Value YTD CY] ) )
RETURN
    IF ( NOT ISBLANK ( [Value YTD CY] ), RANKX ( _set, [Value YTD CY], , DESC, DENSE ) )
```

### Supplier Score
0–100 strategic score: 30% share, 30% growth, 20% stability, 20% price (lower price scores higher). Ranks are within the countries in view.
Format: `0`

```dax
VAR _set = FILTER ( ALLSELECTED ( Dim_Supplier[Country] ), NOT ISBLANK ( [Value YTD CY] ) )
VAR _n = COUNTROWS ( _set )
VAR _rShare = RANKX ( _set, [Value YTD CY], , DESC, DENSE )
VAR _rGrowth = RANKX ( _set, [Value YoY %], , DESC, DENSE )
VAR _rStable = RANKX ( _set, [Volatility %], , ASC, DENSE )
VAR _rPrice = RANKX ( _set, [Price per Kg], , ASC, DENSE )
VAR _norm = MAX ( _n - 1, 1 )
RETURN
    IF (
        NOT ISBLANK ( [Value YTD CY] ),
        ROUND ( 100 * ( 0.3 * ( 1 - ( _rShare - 1 ) / _norm ) + 0.3 * ( 1 - ( _rGrowth - 1 ) / _norm )
            + 0.2 * ( 1 - ( _rStable - 1 ) / _norm ) + 0.2 * ( 1 - ( _rPrice - 1 ) / _norm ) ), 0 )
    )
```

### Supplier Tier

```dax
VAR _s = [Supplier Score] RETURN IF ( ISBLANK ( _s ), BLANK (), IF ( _s >= 65, "Strategic", IF ( _s >= 40, "Develop", "Monitor" ) ) )
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
VAR _raw = MAX ( DQ_Source[RawValue] )
VAR _tot = MAX ( DQ_Source[TotalValue] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( MAX ( DQ_Source[RawRows] ), "#,0" ),
        2, FORMAT ( MAX ( DQ_Source[TotalRows] ), "#,0" ),
        3, FORMAT ( _raw / 1000000, "$#,0.0" ) & "M",
        4, FORMAT ( _tot / 1000000, "$#,0.0" ) & "M",
        5, FORMAT ( DIVIDE ( _raw, _tot ), "0.00" ) & "×",
        6, FORMAT ( MAX ( DQ_Source[DuplicateTotals] ), "#,0" ),
        7, FORMAT ( MAX ( DQ_Source[NotEgyptPartner] ), "#,0" ),
        8, FORMAT ( MAX ( DQ_Source[NotExportFlow] ), "#,0" ),
        9, FORMAT ( MAX ( DQ_Source[OtherCommodity] ), "#,0" ),
        10, FORMAT ( MAX ( DQ_Source[TotalRowsNoWeight] ), "#,0" ),
        11, FORMAT ( MAX ( DQ_Source[MonthsCovered] ), "#,0" ),
        12, FORMAT ( MAX ( DQ_Source[LastPeriod] ), "mmm yyyy" )
    )
```

### DQ Status

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( _o ), BLANK (),
        _o IN { 1, 2, 4, 11, 12 }, "Info",
        _o IN { 3, 5 }, "Handled",
        _o = 10, IF ( MAX ( DQ_Source[TotalRowsNoWeight] ) = 0, "Pass", "Handled" ),
        [DQ Value] = "0", "Pass",
        "Fail"
    )
```

### Overstatement Factor
Format: `0.00`

```dax
DIVIDE ( MAX ( DQ_Source[RawValue] ), MAX ( DQ_Source[TotalValue] ) )
```

## Insights

### Insight Market

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Suppliers

```dax
"<div style='font-family:Segoe UI,sans-serif;background:#1F3E8C;color:#E3E9F8;border-radius:10px;padding:12px 16px;box-sizing:border-box;height:100%;'><div style='font-size:12.5px;font-weight:700;margin:0 0 8px;color:#FFFFFF'>Concentration risk</div>"
    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "If " & [Top Supplier] & " stopped shipping, " & FORMAT ( [Top Supplier Share %], "0%" ) & " of supply would need a new source. Tiers: <b>Strategic</b> 65+, <b>Develop</b> 40–64, <b>Monitor</b> below 40." ) & "</p>"
    & "</div>"
```

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### KPI Market

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Suppliers

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### Trend Year Color

```dax
IF ( SELECTEDVALUE ( 'Trend Year'[Year] ) = [Selected Year], "#E7A923", "#1F3E8C" )
```

### Supplier Tier Pill

```dax
VAR _t = [Supplier Tier]
VAR _bg = SWITCH ( _t, "Strategic", "#2E9E6B", "Develop", "#E7A923", "#667089" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='70' height='20' viewBox='0 0 70 20'>"
        & "<rect x='1' y='2' width='68' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='35' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### Share Color

```dax
IF ( [Share Rank] <= 2, "#1F3E8C", "#A9C1EC" )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2E9E6B", "Info", "#A9C1EC", "Handled", "#E7A923", "#D1495B" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='66' height='20' viewBox='0 0 66 20'>"
        & "<rect x='1' y='2' width='64' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='33' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

## Transport

### Mode Value
Format: `$#,0`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE ( SUM ( Fact_Transport[Value_USD] ), Dim_Date[Year] = _y, Dim_Date[MonthNo] <= _m )
```

### Mode Coverage %
Share of the import value whose transport mode is reported.
Format: `0%`

```dax
DIVIDE ( CALCULATE ( [Mode Value], ALL ( Fact_Transport[Mode] ) ), [Value YTD CY] )
```

### Air Share %
Format: `0%`

```dax
DIVIDE ( CALCULATE ( [Mode Value], Fact_Transport[Mode] = "Air" ), CALCULATE ( [Mode Value], ALL ( Fact_Transport[Mode] ) ) )
```
