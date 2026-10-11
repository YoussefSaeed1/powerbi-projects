# E-Commerce Sales and Profit · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

## Sales

### Sales
Invoice sales after removing duplicate rows.
Format: `$#,0`

```dax
SUM ( Fact_Sales[Sales] )
```

### Profit
Format: `$#,0`

```dax
SUM ( Fact_Sales[Profit] )
```

### Sales $K
Format: `#,0.0`

```dax
DIVIDE ( [Sales], 1000 )
```

### Profit $K
Format: `#,0.0`

```dax
DIVIDE ( [Profit], 1000 )
```

### Margin %
Profit ÷ sales.
Format: `0.0%`

```dax
DIVIDE ( [Profit], [Sales] )
```

### Orders
Distinct orders. Replaces the old 'Number of Orders', which returned the returned-order IDs.
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[Order ID] )
```

### Customers
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[Customer ID] )
```

### Units
Format: `#,0`

```dax
SUM ( Fact_Sales[Quantity] )
```

### Average Discount
Average discount rate per line. Replaces 'Total Discount', which added rates together and showed them as dollars.
Format: `0.0%`

```dax
AVERAGE ( Fact_Sales[Discount] )
```

### Shipping Cost
Format: `$#,0`

```dax
SUM ( Fact_Sales[Shipping Cost] )
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( MAX ( DQ_Source[RawRows] ), "#,0" ),
        2, FORMAT ( MAX ( DQ_Source[DuplicateRows] ), "#,0" ),
        3, FORMAT ( MAX ( DQ_Source[RowIdConflicts] ), "#,0" ),
        4, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[Profit] > Fact_Sales[Sales] ) ), "#,0" ),
        5, FORMAT ( MAX ( DQ_Source[MissingPriority] ), "#,0" ),
        6, FORMAT ( MAX ( DQ_Source[PaddedPriority] ), "#,0" ),
        7, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[Ship Date] < Fact_Sales[Order Date] ) ), "#,0" ),
        8, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[Sales] <= 0 ) ), "#,0" ),
        9, FORMAT ( MAX ( DQ_Source[ReturnsMatched] ), "#,0" ) & " of " & FORMAT ( MAX ( DQ_Source[ReturnRows] ), "#,0" ),
        10, FORMAT ( CALCULATE ( MAX ( Fact_Sales[Order Date] ), REMOVEFILTERS () ), "dd mmm yyyy" )
    )
```

### DQ Status

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
VAR _v = [DQ Value]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( _o ), BLANK (),
        _o IN { 1, 10 }, "Info",
        _o IN { 2, 6 }, IF ( _v = "0", "Pass", "Cleaned" ),
        _o = 9, "Watch",
        _v = "0", "Pass",
        _o IN { 3, 4, 5 }, "Watch",
        "Fail"
    )
```

### DQ Watch Checks
Format: `0`

```dax
COUNTROWS ( FILTER ( ALL ( Dim_DQ ), [DQ Status] IN { "Watch", "Fail" } ) )
```

## Insights

### Worst Region

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Region[Region] ), [Profit], ASC )
RETURN
    MAXX ( _t, Dim_Region[Region] )
```

### Worst Region Profit
Format: `$#,0`

```dax
MINX ( ALL ( Dim_Region[Region] ), [Profit] )
```

### Worst Region Sales
Format: `$#,0`

```dax
VAR _r = [Worst Region] RETURN CALCULATE ( [Sales], Dim_Region[Region] = _r )
```

### Worst Region Discount
Format: `0.0%`

```dax
VAR _r = [Worst Region] RETURN CALCULATE ( [Average Discount], Dim_Region[Region] = _r )
```

### Worst Region Category

```dax
VAR _r = [Worst Region]
VAR _t = TOPN ( 1, ALL ( Dim_Product[Product Category] ), CALCULATE ( [Profit], Dim_Region[Region] = _r ), ASC )
RETURN
    MAXX ( _t, Dim_Product[Product Category] )
```

### Worst Region Category Profit
Format: `$#,0`

```dax
VAR _r = [Worst Region]
RETURN
    MINX ( ALL ( Dim_Product[Product Category] ), CALCULATE ( [Profit], Dim_Region[Region] = _r ) )
```

### Worst Region Sub-Category

```dax
VAR _r = [Worst Region]
VAR _t = TOPN ( 1, ALL ( Dim_Product[Product Sub-Category] ), CALCULATE ( [Profit], Dim_Region[Region] = _r ), ASC )
RETURN
    LOWER ( MAXX ( _t, Dim_Product[Product Sub-Category] ) )
```

### Best Month

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Date[Month], Dim_Date[MonthNo] ), [Profit], DESC )
RETURN
    FORMAT ( DATE ( 2015, MAXX ( _t, Dim_Date[MonthNo] ), 1 ), "mmmm" )
```

### Best Month Profit
Format: `$#,0`

```dax
MAXX ( ALL ( Dim_Date[Month], Dim_Date[MonthNo] ), [Profit] )
```

### Best Month Sales
Format: `$#,0`

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Date[Month], Dim_Date[MonthNo] ), [Profit], DESC )
RETURN
    SUMX ( _t, [Sales] )
```

### Break-even Months
Months whose margin was below 1%.

```dax
VAR _t = FILTER ( ALL ( Dim_Date[Month], Dim_Date[MonthNo] ), NOT ISBLANK ( [Sales] ) && [Margin %] < 0.01 )
RETURN
    CONCATENATEX ( _t, FORMAT ( DATE ( 2015, Dim_Date[MonthNo], 1 ), "mmmm" ), " and ", Dim_Date[MonthNo], ASC )
```

### Worst Sub-Category

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Product[Product Sub-Category] ), [Profit], ASC )
RETURN
    MAXX ( _t, Dim_Product[Product Sub-Category] )
```

### Worst Sub-Category Profit
Format: `$#,0`

```dax
MINX ( ALL ( Dim_Product[Product Sub-Category] ), [Profit] )
```

### Worst Sub-Category Sales
Format: `$#,0`

```dax
VAR _s = [Worst Sub-Category] RETURN CALCULATE ( [Sales], Dim_Product[Product Sub-Category] = _s )
```

### Best Segment

```dax
VAR _t = TOPN ( 1, ALL ( Fact_Sales[Customer Segment] ), [Margin %], DESC )
RETURN
    MAXX ( _t, Fact_Sales[Customer Segment] )
```

### Best Segment Margin
Format: `0.0%`

```dax
MAXX ( ALL ( Fact_Sales[Customer Segment] ), [Margin %] )
```

### Largest Segment

```dax
VAR _t = TOPN ( 1, ALL ( Fact_Sales[Customer Segment] ), [Sales], DESC )
RETURN
    MAXX ( _t, Fact_Sales[Customer Segment] )
```

### Largest Segment Margin
Format: `0.0%`

```dax
VAR _s = [Largest Segment] RETURN CALCULATE ( [Margin %], Fact_Sales[Customer Segment] = _s )
```

### Loss Sub-Categories
Format: `0`

```dax
COUNTROWS ( FILTER ( ALL ( Dim_Product[Product Sub-Category] ), [Profit] < 0 ) )
```

### Insight Overview

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Drivers

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### Sub-Category Bars
Diverging bars: the six sub-categories that lose the most and the six that earn the most.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Region Category Heatmap
Profit by region and category ($K); coral is a loss, mint a profit, darker is larger.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Row

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### Profit Color

```dax
IF ( [Profit] < 0, "#F25F5C", "#2EC4B6" )
```

### Band Color

```dax
IF ( [Band Margin %] < 0, "#F25F5C", "#2EC4B6" )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2E9E6B", "Info", "#9FB3C8", "Cleaned", "#2EC4B6", "Watch", "#F2A541", "#F25F5C" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='62' height='20' viewBox='0 0 62 20'>"
        & "<rect x='1' y='2' width='60' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='31' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

## Profit Drivers

### Band Sales $K
Format: `#,0`

```dax
VAR _lo = SELECTEDVALUE ( Dim_DiscountBand[From] )
VAR _hi = SELECTEDVALUE ( Dim_DiscountBand[To] )
RETURN
    CALCULATE ( [Sales $K], Fact_Sales[Discount] >= _lo, Fact_Sales[Discount] < _hi )
```

### Band Margin %
Margin of the lines whose discount falls in the band.
Format: `0.0%`

```dax
VAR _lo = SELECTEDVALUE ( Dim_DiscountBand[From] )
VAR _hi = SELECTEDVALUE ( Dim_DiscountBand[To] )
RETURN
    CALCULATE ( [Margin %], Fact_Sales[Discount] >= _lo, Fact_Sales[Discount] < _hi )
```

### High Discount Margin
Format: `0.0%`

```dax
CALCULATE ( [Margin %], Fact_Sales[Discount] >= 0.085 )
```

### High Discount Sales
Format: `$#,0`

```dax
CALCULATE ( [Sales], Fact_Sales[Discount] >= 0.085 )
```

### Low Discount Margin
Format: `0.0%`

```dax
CALCULATE ( [Margin %], Fact_Sales[Discount] < 0.025 )
```
