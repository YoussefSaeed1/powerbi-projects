# Sales Tracker · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Latest Order Date
Format: `dd-mmm-yyyy`

```dax
CALCULATE ( MAX ( Fact_Sales[OrderDate] ), REMOVEFILTERS () )
```

### Selected Year
Format: `0`

```dax
VAR _maxYear = YEAR ( [Latest Order Date] )
RETURN
    IF ( ISFILTERED ( Dim_Date[Year] ), MAX ( Dim_Date[Year] ), _maxYear )
```

### Selected Year Last Month
Format: `0`

```dax
VAR _y = [Selected Year]
VAR _end = [Latest Order Date]
RETURN
    CALCULATE ( MAX ( Dim_Date[MonthNo] ), REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _y, Dim_Date[Date] <= _end )
```

### Period Label

```dax
IF (
    ISFILTERED ( Dim_Date[Year] ),
    VAR _y = [Selected Year] VAR _m = [Selected Year Last Month] RETURN IF ( _m = 12, "FY" & _y, "Jan–" & FORMAT ( DATE ( _y, _m, 1 ), "mmm" ) & " " & _y ),
    "Jan 2015 – " & FORMAT ( [Latest Order Date], "mmm yyyy" )
)
```

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

## Sales

### Total Revenue
Units × list price.
Format: `#,0.00`

```dax
SUMX ( Fact_Sales, Fact_Sales[OrderQuantity] * RELATED ( Dim_Product[ProductPrice] ) )
```

### COGS
Units × product cost.
Format: `#,0.00`

```dax
SUMX ( Fact_Sales, Fact_Sales[OrderQuantity] * RELATED ( Dim_Product[ProductCost] ) )
```

### Total Profit
Format: `#,0.00`

```dax
[Total Revenue] - [COGS]
```

### Profit Margin %
Format: `0.00%`

```dax
DIVIDE ( [Total Profit], [Total Revenue] )
```

### Total Revenue $M
Format: `$#,0.00`

```dax
DIVIDE ( [Total Revenue], 1000000 )
```

### COGS $M
Format: `$#,0.00`

```dax
DIVIDE ( [COGS], 1000000 )
```

### Total Profit $M
Format: `$#,0.00`

```dax
DIVIDE ( [Total Profit], 1000000 )
```

### Total Orders
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[OrderNumber] )
```

### Total Quantity
Format: `#,0`

```dax
SUM ( Fact_Sales[OrderQuantity] )
```

### Total Customers
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[CustomerKey] )
```

### Products Sold
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[ProductKey] )
```

### Average Order Value
Format: `#,0.0`

```dax
DIVIDE ( [Total Revenue], [Total Orders] )
```

### Revenue Same Months LY
Revenue for the same months of the prior year (2017 has data to June only).
Format: `$#,0`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE ( [Total Revenue], REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _y - 1, Dim_Date[MonthNo] <= _m )
```

### Revenue YTD
Format: `$#,0`

```dax
VAR _y = [Selected Year]
VAR _m = [Selected Year Last Month]
RETURN
    CALCULATE ( [Total Revenue], REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _y, Dim_Date[MonthNo] <= _m )
```

### Revenue YoY %
Format: `+0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Revenue YTD] - [Revenue Same Months LY], [Revenue Same Months LY] )
```

### Category Share %
Format: `0.0%`

```dax
DIVIDE ( [Total Revenue], CALCULATE ( [Total Revenue], ALL ( Dim_Product[Category] ) ) )
```

### Bikes Share %
Share of revenue from bikes: the dependence on one category.
Format: `0.0%`

```dax
DIVIDE ( CALCULATE ( [Total Revenue], Dim_Product[Category] = "Bikes" ), CALCULATE ( [Total Revenue], ALL ( Dim_Product[Category] ) ) )
```

### Repeat Customer %
Customers with more than one order.
Format: `0.0%`

```dax
VAR _c = ADDCOLUMNS ( VALUES ( Fact_Sales[CustomerKey] ), "@o", CALCULATE ( DISTINCTCOUNT ( Fact_Sales[OrderNumber] ) ) )
RETURN
    DIVIDE ( COUNTROWS ( FILTER ( _c, [@o] > 1 ) ), COUNTROWS ( _c ) )
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Sales ) ), "#,0" ),
        2, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Returns ) ), "#,0" ),
        3, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Sales ) ) - COUNTROWS ( SUMMARIZE ( ALL ( Fact_Sales ), Fact_Sales[OrderNumber], Fact_Sales[OrderLineItem] ) ), "#,0" ),
        4, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), ISBLANK ( RELATED ( Dim_Product[ProductName] ) ) ) ), "#,0" ),
        5, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), ISBLANK ( RELATED ( Dim_Territory[Region] ) ) ) ), "#,0" ),
        6, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[OrderQuantity] <= 0 ) ), "#,0" ),
        7, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Dim_Product ), Dim_Product[ProductPrice] < Dim_Product[ProductCost] ) ), "#,0" ),
        8, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Dim_Product[ProductKey] ), CALCULATE ( SUM ( Fact_Returns[ReturnQuantity] ) ) > CALCULATE ( SUM ( Fact_Sales[OrderQuantity] ) ) ) ), "#,0" ),
        9, FORMAT ( [Latest Order Date], "dd mmm yyyy" )
    )
```

### DQ Status

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
VAR _v = [DQ Value]
RETURN
    SWITCH ( TRUE (), ISBLANK ( _o ), BLANK (), _o IN { 1, 2, 9 }, "Info", _v = "0", "Pass", "Fail" )
```

### DQ Failed Checks
Format: `0`

```dax
COUNTROWS ( FILTER ( ALL ( Dim_DQ ), [DQ Status] = "Fail" ) )
```

## Insights

### Top Territory

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Territory[Region] ), [Total Orders], DESC )
RETURN
    MAXX ( _t, Dim_Territory[Region] )
```

### Top Territory Orders
Format: `#,0`

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Territory[Region] ), [Total Orders], DESC )
RETURN
    MAXX ( _t, [Total Orders] )
```

### Top Subcategory

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Product[Subcategory] ), [Total Revenue], DESC )
RETURN
    MAXX ( _t, Dim_Product[Subcategory] )
```

### Top Subcategory Share
Format: `0%`

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Product[Subcategory] ), [Total Revenue], DESC )
RETURN
    DIVIDE ( MAXX ( _t, [Total Revenue] ), CALCULATE ( [Total Revenue], ALL ( Dim_Product ) ) )
```

### Accessory Margin %
Format: `0.0%`

```dax
CALCULATE ( [Profit Margin %], Dim_Product[Category] = "Accessories" )
```

### Bike Margin %
Format: `0.0%`

```dax
CALCULATE ( [Profit Margin %], Dim_Product[Category] = "Bikes" )
```

### Highest Return Category

```dax
VAR _t = TOPN ( 1, ALL ( Dim_Product[Category] ), [Return Rate %], DESC )
RETURN
    MAXX ( _t, Dim_Product[Category] )
```

### Highest Return Rate
Format: `0.00%`

```dax
MAXX ( ALL ( Dim_Product[Category] ), [Return Rate %] )
```

## KPI Cards

### KPI Executive

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Product

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Business

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2E9E6B", "Info", "#A9BCD0", "#C0504D" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='56' height='20' viewBox='0 0 56 20'>"
        & "<rect x='1' y='2' width='54' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='28' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

## Returns

### Total Returns
Returned units.
Format: `#,0`

```dax
SUM ( Fact_Returns[ReturnQuantity] )
```

### Return Rate %
Returned units ÷ units sold.
Format: `0.00%`

```dax
DIVIDE ( [Total Returns], [Total Quantity] )
```

### Return Value
Format: `$#,0`

```dax
SUMX ( Fact_Returns, Fact_Returns[ReturnQuantity] * RELATED ( Dim_Product[ProductPrice] ) )
```

### Net Revenue After Returns
Format: `$#,0`

```dax
[Total Revenue] - [Return Value]
```

## Visuals

### Units Sold vs Returned
Units sold vs units returned and the return rate, for the HTML Content visual. Replaces the old funnel that mixed counts with dollars.

```dax
VAR _sold = [Total Quantity]
VAR _ret = [Total Returns]
VAR _rate = DIVIDE ( _ret, _sold )
VAR _w = IF ( _sold > 0, ROUND ( 100 * DIVIDE ( _ret, _sold ), 1 ), 0 )
VAR _row = "display:flex;align-items:center;gap:10px;margin:0 0 14px"
VAR _lab = "width:118px;font-size:13px;font-weight:700;color:#1F2D3D"
RETURN
    "<div style='font-family:Segoe UI,sans-serif;padding:6px 18px 0 14px;box-sizing:border-box'>"
    & "<div style='" & _row & "'><div style='" & _lab & "'>Units sold</div><div style='flex:1;height:40px;background:#4D6F95;color:#fff;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:flex-end;padding-right:10px'>" & FORMAT ( _sold, "#,0" ) & "</div></div>"
    & "<div style='" & _row & "'><div style='" & _lab & "'>Units returned</div><div style='flex:1;display:flex;align-items:center;gap:8px'><div style='width:" & FORMAT ( MAX ( _w, 1.5 ), "0.0" ) & "%;height:40px;background:#C0504D'></div><div style='font-size:14px;font-weight:700;color:#1F2D3D'>" & FORMAT ( _ret, "#,0" ) & "</div></div></div>"
    & "<div style='font-size:12.5px;color:#1F2D3D;margin-top:4px'><b style='font-size:20px;color:#C0504D'>" & FORMAT ( _rate, "0.00%" ) & "</b>&nbsp; of units sold came back</div>"
    & "</div>"
```
