# Inventory Management · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Selected Year
Year in focus: the year picked in the slicer, or the latest year with sales.

```dax
VAR _maxYear = YEAR ( CALCULATE ( MAX ( Fact_Sales[OrderDate] ), ALL ( Fact_Sales ) ) )
			RETURN
			    IF ( ISFILTERED ( Dim_Date[Year] ), MAX ( Dim_Date[Year] ), _maxYear )
```

### Last Snapshot Date

```dax
CALCULATE (
			    MAX ( Fact_Inventory[SnapshotDate] ),
			    REMOVEFILTERS ( Products ),
			    REMOVEFILTERS ( Suppliers ),
			    REMOVEFILTERS ( Warehouses ),
			    REMOVEFILTERS ( Fact_Inventory[Inventory Health] ),
			    REMOVEFILTERS ( Fact_Inventory[Health Sort] ),
			    REMOVEFILTERS ( Fact_Inventory[Movement Class] ),
			    REMOVEFILTERS ( Fact_Inventory[Movement Sort] ),
			    REMOVEFILTERS ( Fact_Inventory[Stock Action] )
			)
```

### Filter Status

```dax
VAR f =
			    ISFILTERED ( Products[Category] ) || ISFILTERED ( Suppliers[SupplierName] )
			        || ISFILTERED ( Warehouses[WarehouseName] ) || ISFILTERED ( Fact_Inventory[Inventory Health] )
			        || ISFILTERED ( Dim_Date[Year] ) || ISFILTERED ( Products[ProductName] )
			RETURN
			    IF ( f, "Filters applied!", "No filter applied!" )
```

### Greeting

```dax
VAR h = HOUR ( NOW () )
			RETURN
			    SWITCH ( TRUE (), h < 12, "Good Morning!", h < 17, "Good Afternoon!", "Good Evening!" )
```

### Last Refresh

```dax
"Last Refresh: " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd-MMM-yyyy" )
```

## Sales

### Revenue
Sales revenue: quantity × unit price.

```dax
SUM ( Fact_Sales[Revenue] )
```

### COGS
Cost of goods sold: quantity × unit cost.

```dax
SUM ( Fact_Sales[COGS] )
```

### Gross Profit
Revenue minus COGS.

```dax
[Revenue] - [COGS]
```

### Margin %
Gross profit as a share of revenue.

```dax
DIVIDE ( [Gross Profit], [Revenue] )
```

### Revenue CY
Revenue in the year in focus.

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Revenue], Dim_Date[Year] = _y )
```

### Revenue LY
Revenue in the year before the year in focus.

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Revenue], Dim_Date[Year] = _y - 1 )
```

### Revenue YoY %
Revenue growth vs the prior year.

```dax
DIVIDE ( [Revenue CY] - [Revenue LY], [Revenue LY] )
```

### Revenue YoY Label

```dax
VAR v = [Revenue YoY %]
			RETURN
			    IF ( ISBLANK ( v ), "–", FORMAT ( v, "+0.0%;-0.0%;0.0%" ) & IF ( v >= 0, " ▲", " ▼" ) )
```

### Revenue YoY Color

```dax
IF ( [Revenue YoY %] >= 0, "#2E9E4F", "#D9363E" )
```

### COGS CY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [COGS], Dim_Date[Year] = _y )
```

### Gross Profit CY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Gross Profit], Dim_Date[Year] = _y )
```

### Gross Profit LY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Gross Profit], Dim_Date[Year] = _y - 1 )
```

### Gross Profit YoY %

```dax
DIVIDE ( [Gross Profit CY] - [Gross Profit LY], [Gross Profit LY] )
```

### Gross Profit YoY Label

```dax
VAR v = [Gross Profit YoY %]
			RETURN
			    IF ( ISBLANK ( v ), "–", FORMAT ( v, "+0.0%;-0.0%;0.0%" ) & IF ( v >= 0, " ▲", " ▼" ) )
```

### Gross Profit YoY Color

```dax
IF ( [Gross Profit YoY %] >= 0, "#2E9E4F", "#D9363E" )
```

### Margin % CY

```dax
DIVIDE ( [Gross Profit CY], [Revenue CY] )
```

### Units Sold CY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( SUM ( Fact_Sales[Quantity] ), Dim_Date[Year] = _y )
```

## Suppliers

### Avg Lead Time (Days)
Average days from purchase order to receipt.

```dax
AVERAGE ( Fact_PurchaseOrders[Lead Time Days] )
```

### Avg Lead Time CY
Average supplier lead time in the year in focus.

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Avg Lead Time (Days)], Dim_Date[Year] = _y )
```

### Lead Time Note

```dax
IF ( [Avg Lead Time CY] <= 15, "Within typical target range", "Above typical target range" )
```

### Lead Time Color

```dax
VAR v = [Avg Lead Time CY] RETURN SWITCH ( TRUE (), ISBLANK ( v ), BLANK (), v >= 15, "#D9363E", v >= 10, "#D98A1C", "#2E9E4F" )
```

### Active Suppliers
Suppliers of the SKUs that appear in the inventory snapshots.

```dax
CALCULATE ( DISTINCTCOUNT ( Products[SupplierID] ), Fact_Inventory )
```

### Active Suppliers Note

```dax
"Supplying " & CALCULATE ( DISTINCTCOUNT ( Products[SKU] ), Fact_Inventory ) & " active SKUs"
```

### SKUs Supplied

```dax
CALCULATE ( DISTINCTCOUNT ( Products[SKU] ), Fact_Inventory )
```

### Stockout Risk Color

```dax
VAR v = [Stockout Rate CY] RETURN SWITCH ( TRUE (), ISBLANK ( v ), BLANK (), v >= 0.3, "#D9363E", v >= 0.15, "#D98A1C", "#2E9E4F" )
```

### Stockout Risk Note

```dax
VAR v = [Stockout Rate CY] RETURN SWITCH ( TRUE (), v < 0.15, "Manageable supplier risk", v < 0.3, "Elevated supplier risk", "High supplier risk" )
```

### Stock Value Spread
Gap between the highest and the lowest warehouse stock value.

```dax
MAXX ( VALUES ( Warehouses[WarehouseName] ), [Inventory Value] ) - MINX ( VALUES ( Warehouses[WarehouseName] ), [Inventory Value] )
```

### Stock Value Spread Color

```dax
IF ( DIVIDE ( [Stock Value Spread], [Inventory Value] ) > 0.2, "#D9363E", "#222222" )
```

### Stock Value Spread Note

```dax
IF ( DIVIDE ( [Stock Value Spread], [Inventory Value] ) > 0.2, "Significant imbalance across locations", "Balanced across locations" )
```

## Data Quality

### DQ Value
Result of each data quality rule in Dim_DQ.

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
			RETURN
			    SWITCH (
			        _o,
			        1, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Sales ) ), "#,0" ),
			        2, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_Inventory ) ), "#,0" ),
			        3, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_PurchaseOrders ) ), "#,0" ),
			        4, FORMAT ( 0 + COUNTROWS ( ALL ( Products ) ) - CALCULATE ( DISTINCTCOUNT ( Products[SKU] ), ALL ( Products ) ), "#,0" ),
			        5, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), ISBLANK ( RELATED ( Products[ProductName] ) ) ) ), "#,0" ),
			        6, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Inventory ), ISBLANK ( RELATED ( Products[ProductName] ) ) ) ), "#,0" ),
			        7, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Inventory ), Fact_Inventory[OnHandQty] < 0 ) ), "#,0" ),
			        8, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PurchaseOrders ), NOT ISBLANK ( Fact_PurchaseOrders[ReceivedDate] ) && Fact_PurchaseOrders[ReceivedDate] < Fact_PurchaseOrders[OrderDate] ) ), "#,0" ),
			        9, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PurchaseOrders ), Fact_PurchaseOrders[ReceivedQty] > Fact_PurchaseOrders[OrderedQty] ) ), "#,0" ),
			        10, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_Sales ), Fact_Sales[UnitPrice] <= 0 ) ), "#,0" ),
			        11, FORMAT ( CALCULATE ( MAX ( Fact_Inventory[SnapshotDate] ), REMOVEFILTERS () ), "dd mmm yyyy" )
			    )
```

### DQ Status
Pass / Fail / Info for each data quality rule.

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
			VAR _v = [DQ Value]
			RETURN
			    SWITCH (
			        TRUE (),
			        ISBLANK ( _o ), BLANK (),
			        _o IN { 1, 2, 3, 11 }, "Info",
			        _v = "0", "Pass",
			        "Fail"
			    )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
			VAR _bg = SWITCH ( _t, "Pass", "#2E9E4F", "Info", "#A6A1D6", "#D9363E" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='56' height='20' viewBox='0 0 56 20'>"
			        & "<rect x='1' y='2' width='54' height='16' rx='8' fill='" & _bg & "'/>"
			        & "<text x='28' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _t ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### DQ Failed Checks

```dax
COUNTROWS ( FILTER ( ALL ( Dim_DQ ), [DQ Status] = "Fail" ) )
```

### DQ Summary
HTML summary for the Data Quality page.

```dax
"<div style='font-family:Segoe UI,sans-serif;background:#100E6F;color:#E6E5F5;border-radius:12px;padding:12px 16px;box-sizing:border-box;height:100%;'><div style='font-size:12.5px;font-weight:700;margin:0 0 8px;color:#FFFFFF'>How this report is governed</div>"
			    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "<b>Data quality:</b> " & IF ( [DQ Failed Checks] = 0, "all checks pass on the last refresh.", FORMAT ( [DQ Failed Checks], "0" ) & " check(s) failed on the last refresh." ) ) & "</p>"
			    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "<b>Security:</b> the Warehouse Manager role uses a mapping table (Security_WarehouseAccess), so access is changed by editing data, not the model. Leadership sees every warehouse." ) & "</p>"
			    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "<b>Definitions:</b> KPI measures carry descriptions and live in display folders; the full list is in Measure_Catalogue.md." ) & "</p>"
			    & "<p style='font-size:12px;line-height:1.45;margin:0 0 7px'>" & ( "<b>Freshness:</b> " & [Last Refresh] & "." ) & "</p>"
			    & "</div>"
```

## KPI Text

### KPI Revenue

```dax
VAR v = [Revenue CY]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Revenue LY

```dax
VAR v = [Revenue LY]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Gross Profit

```dax
VAR v = [Gross Profit CY]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Gross Profit LY

```dax
VAR v = [Gross Profit LY]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Inventory Value

```dax
VAR v = [Inventory Value CY]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Inventory Value LY

```dax
VAR v = [Inventory Value LY]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Stockout Rate

```dax
FORMAT ( [Stockout Rate CY], "0.0%" )
```

### KPI Stockout Rate LY

```dax
FORMAT ( [Stockout Rate LY], "0.0%" )
```

### KPI Turnover

```dax
FORMAT ( [Inventory Turnover CY], "0.00" )
```

### KPI Turnover LY

```dax
FORMAT ( [Inventory Turnover LY], "0.00" )
```

### KPI Restock Cost

```dax
VAR v = [Restock Cost]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Stock Value Spread

```dax
VAR v = [Stock Value Spread]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Stock Value

```dax
VAR v = [Inventory Value]
			RETURN
			    SWITCH ( TRUE (),
			        ISBLANK ( v ), "–",
			        ABS ( v ) >= 1000000, FORMAT ( v / 1000000, "$#,0.00" ) & "M",
			        ABS ( v ) >= 1000, FORMAT ( v / 1000, "$#,0.0" ) & "K",
			        FORMAT ( v, "$#,0" )
			    )
```

### KPI Avg Unit Cost

```dax
FORMAT ( [Avg Unit Cost], "$#,0.0" )
```

### KPI Stockout Risk

```dax
FORMAT ( [Stockout Rate CY], "0.0%" )
```

## Charts

### Trend CY

```dax
SWITCH ( SELECTEDVALUE ( 'Trend Metric'[Metric], "Revenue" ), "Inventory", [Inventory Value CY], [Revenue CY] )
```

### Trend LY

```dax
SWITCH ( SELECTEDVALUE ( 'Trend Metric'[Metric], "Revenue" ), "Inventory", [Inventory Value LY], [Revenue LY] )
```

### Contribution Value

```dax
SWITCH ( SELECTEDVALUE ( 'Contribution Metric'[Metric], "Revenue" ), "Gross Profit", [Gross Profit CY], [Revenue CY] )
```

### Category Revenue

```dax
CALCULATE ( [Revenue CY] )
```

### Category Share %
Category revenue as a share of the selected categories.

```dax
DIVIDE ( [Revenue CY], CALCULATE ( [Revenue CY], ALLSELECTED ( Products[Category] ) ) )
```

### Channel Share %
Channel revenue as a share of the selected channels.

```dax
DIVIDE ( [Revenue CY], CALCULATE ( [Revenue CY], ALLSELECTED ( Fact_Sales[Channel] ) ) )
```

### Top N Value

```dax
SELECTEDVALUE ( 'Top N'[Value], 5 )
```

### Product Rank
Rank of the product by revenue in the year in focus.

```dax
IF ( NOT ISBLANK ( [Revenue CY] ), RANKX ( ALLSELECTED ( Products[ProductName] ), [Revenue CY], , DESC, DENSE ) )
```

### In Top N

```dax
IF ( [Product Rank] <= [Top N Value], 1 )
```

### ABC Class

```dax
VAR rev = [Revenue CY]
			VAR total = CALCULATE ( [Revenue CY], ALLSELECTED ( Products[ProductName] ) )
			VAR cum = SUMX ( FILTER ( ALLSELECTED ( Products[ProductName] ), [Revenue CY] >= rev ), [Revenue CY] )
			VAR pct = DIVIDE ( cum, total )
			RETURN
			    IF ( NOT ISBLANK ( rev ), SWITCH ( TRUE (), pct <= 0.7, "A Class", pct <= 0.9, "B Class", "C Class" ) )
```

### Top Rank

```dax
IF ( [In Top N] = 1, [Product Rank] )
```

### Top Revenue

```dax
IF ( [In Top N] = 1, [Revenue CY] )
```

### Top COGS

```dax
IF ( [In Top N] = 1, [COGS CY] )
```

### Top Gross Profit

```dax
IF ( [In Top N] = 1, [Gross Profit CY] )
```

### Top Margin %

```dax
IF ( [In Top N] = 1, [Margin % CY] )
```

### Top ABC Class

```dax
IF ( [In Top N] = 1, [ABC Class] )
```

### ABC Color

```dax
SWITCH ( [Top ABC Class], "A Class", "#100E6F", "B Class", "#7E70B0", "C Class", "#9A9A9A" )
```

### Ops Trend Value

```dax
VAR _y = [Selected Year]
			VAR m = SELECTEDVALUE ( 'Ops Metric'[Metric], "Avg. Days of Supply" )
			RETURN
			    CALCULATE (
			        SWITCH ( m,
			            "Stockout Rate %", [Stockout Rate %] * 100,
			            "Units Received", [Units Received],
			            "Units Sold", [Units Sold (Stock)],
			            [Avg Days of Supply]
			        ),
			        Dim_Date[Year] = _y
			    )
```

### Ops Trend Color

```dax
VAR v = [Ops Trend Value]
			VAR mx = MAXX ( ALLSELECTED ( Dim_Date[Month], Dim_Date[MonthNo] ), [Ops Trend Value] )
			VAR mn = MINX ( ALLSELECTED ( Dim_Date[Month], Dim_Date[MonthNo] ), [Ops Trend Value] )
			RETURN
			    SWITCH ( TRUE (), ISBLANK ( v ), BLANK (), v = mx, "#100E6F", v = mn, "#CCD3EB", "#EBEBEE" )
```

### Health Count

```dax
VAR v = SELECTEDVALUE ( 'Health View'[View], "Health" )
			RETURN
			    SWITCH ( v,
			        "Movement", CALCULATE ( COUNTROWS ( Fact_Inventory ), TREATAS ( VALUES ( 'Health View'[Item] ), Fact_Inventory[Movement Class] ) ),
			        CALCULATE ( COUNTROWS ( Fact_Inventory ), TREATAS ( VALUES ( 'Health View'[Item] ), Fact_Inventory[Inventory Health] ) )
			    )
```

### Health Bar Color

```dax
SWITCH ( SELECTEDVALUE ( 'Health View'[Item] ),
			    "Stockout", "#D46A6A", "Critical Low", "#EBA14B", "Healthy", "#6A9E68",
			    "Overstocked", "#F2CE5B", "Dead Stock", "#8C8C8C",
			    "Fast Moving", "#100E6F", "Moderate", "#7E70B0", "Slow Moving", "#B8B3DA", "Non-Moving", "#8C8C8C"
			)
```

### Supplier Trend Value

```dax
VAR _y = [Selected Year]
			VAR m = SELECTEDVALUE ( 'Supplier Metric'[Metric], "Stockout Rate %" )
			RETURN
			    CALCULATE (
			        SWITCH ( m,
			            "Avg Lead Time (Days)", [Avg Lead Time (Days)],
			            "Inventory Value", [Inventory Value],
			            [Stockout Rate %] * 100
			        ),
			        Dim_Date[Year] = _y
			    )
```

### Supplier Trend Color

```dax
VAR v = [Supplier Trend Value]
			VAR mx = MAXX ( ALLSELECTED ( Dim_Date[Month], Dim_Date[MonthNo] ), [Supplier Trend Value] )
			VAR mn = MINX ( ALLSELECTED ( Dim_Date[Month], Dim_Date[MonthNo] ), [Supplier Trend Value] )
			RETURN
			    SWITCH ( TRUE (), ISBLANK ( v ), BLANK (), v = mx, "#100E6F", v = mn, "#CCD3EB", "#EBEBEE" )
```

### Warehouse Value
Value of the metric picked in the warehouse toggle (inventory, revenue or units sold).

```dax
SWITCH ( SELECTEDVALUE ( 'Warehouse Metric'[Metric], "Inventory" ),
			    "Revenue", [Revenue CY],
			    "Units Sold", [Units Sold CY],
			    [Inventory Value]
			)
```

### Warehouse Share %

```dax
DIVIDE ( [Warehouse Value], CALCULATE ( [Warehouse Value], ALLSELECTED ( Warehouses[WarehouseName] ) ) )
```

### Breakdown Value

```dax
VAR t = SELECTEDVALUE ( Breakdown[Type], "Category" )
			RETURN
			    SWITCH ( t,
			        "Channel", CALCULATE ( [Revenue CY], TREATAS ( VALUES ( Breakdown[Item] ), Fact_Sales[Channel] ) ),
			        CALCULATE ( [Revenue CY], TREATAS ( VALUES ( Breakdown[Item] ), Products[Category] ) )
			    )
```

### Breakdown Share %

```dax
DIVIDE ( [Breakdown Value], CALCULATE ( [Breakdown Value], ALLSELECTED ( Breakdown[Item] ) ) )
```

## Details

### Total SKUs Note

```dax
[Active SKUs] & " of " & CALCULATE ( DISTINCTCOUNT ( Products[SKU] ), ALL ( Products ) ) & " SKUs selected"
```

### Stock Value Note

```dax
"Current inventory on hand value"
```

### Avg Unit Cost

```dax
AVERAGEX ( FILTER ( VALUES ( Products[SKU] ), NOT ISBLANK ( [Current Stock] ) ), CALCULATE ( MAX ( Products[UnitCost] ) ) )
```

### Avg Unit Cost Note

```dax
"Blended cost across selected SKUs"
```

### SKU Lead Time

```dax
AVERAGEX ( FILTER ( VALUES ( Products[SKU] ), NOT ISBLANK ( [Current Stock] ) ), CALCULATE ( MAX ( Products[LeadTimeDays] ) ) )
```

### SKU Lead Time Note

```dax
"Avg days to replenish selected SKUs"
```

## Inventory

### Inventory Value
Stock value at cost on the last snapshot date in context.

```dax
VAR _last = [Last Snapshot Date]
			RETURN
			    CALCULATE ( SUM ( Fact_Inventory[Inventory Value] ), Dim_Date[Date] = _last )
```

### Current Stock
Units on hand on the last snapshot date in context.

```dax
VAR _last = [Last Snapshot Date]
			RETURN
			    CALCULATE ( SUM ( Fact_Inventory[OnHandQty] ), Dim_Date[Date] = _last )
```

### Current Stock Action

```dax
VAR _last = [Last Snapshot Date]
			RETURN
			    CALCULATE ( SELECTEDVALUE ( Fact_Inventory[Stock Action] ), Dim_Date[Date] = _last )
```

### Current Health

```dax
VAR _last = [Last Snapshot Date]
			RETURN
			    CALCULATE ( SELECTEDVALUE ( Fact_Inventory[Inventory Health] ), Dim_Date[Date] = _last )
```

### Current Days of Supply

```dax
VAR _last = [Last Snapshot Date]
			RETURN
			    CALCULATE ( MAX ( Fact_Inventory[Days of Supply] ), Dim_Date[Date] = _last )
```

### Inventory Value CY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Inventory Value], Dim_Date[Year] = _y )
```

### Inventory Value LY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Inventory Value], Dim_Date[Year] = _y - 1 )
```

### Inventory Value YoY %

```dax
DIVIDE ( [Inventory Value CY] - [Inventory Value LY], [Inventory Value LY] )
```

### Inventory Value YoY Label

```dax
VAR v = [Inventory Value YoY %]
			RETURN
			    IF ( ISBLANK ( v ), "–", FORMAT ( v, "+0.0%;-0.0%;0.0%" ) & IF ( v >= 0, " ▲", " ▼" ) )
```

### Inventory Value YoY Color

```dax
IF ( [Inventory Value YoY %] >= 0, "#2E9E4F", "#D9363E" )
```

### Avg Inventory Value

```dax
AVERAGEX ( VALUES ( Fact_Inventory[SnapshotDate] ), CALCULATE ( SUM ( Fact_Inventory[Inventory Value] ) ) )
```

### Inventory Turnover
Annualised COGS ÷ average inventory value.

```dax
DIVIDE ( [COGS], [Avg Inventory Value] ) * DIVIDE ( 12, DISTINCTCOUNT ( Fact_Inventory[SnapshotDate] ) )
```

### Inventory Turnover CY
Inventory turnover in the year in focus.

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Inventory Turnover], Dim_Date[Year] = _y )
```

### Inventory Turnover LY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Inventory Turnover], Dim_Date[Year] = _y - 1 )
```

### Inventory Turnover YoY %

```dax
DIVIDE ( [Inventory Turnover CY] - [Inventory Turnover LY], [Inventory Turnover LY] )
```

### Inventory Turnover YoY Label

```dax
VAR v = [Inventory Turnover YoY %]
			RETURN
			    IF ( ISBLANK ( v ), "–", FORMAT ( v, "+0.0%;-0.0%;0.0%" ) & IF ( v >= 0, " ▲", " ▼" ) )
```

### Inventory Turnover YoY Color

```dax
IF ( [Inventory Turnover YoY %] >= 0, "#2E9E4F", "#D9363E" )
```

### DIO
Days inventory outstanding: 365 ÷ turnover.

```dax
DIVIDE ( 365, [Inventory Turnover CY] )
```

### DIO Color

```dax
IF ( [DIO] > 30, "#D9363E", "#222222" )
```

### DIO Note

```dax
IF ( [DIO] > 30, "Slow turnover — excess stock risk", "Healthy turnover pace" )
```

## Other

### HTML KPI Overview

```dax
VAR _y = [Selected Year]
			VAR _rows = {
			    ( 1, "Revenue",            [KPI Revenue],         [Revenue YoY %],            [KPI Revenue LY],         1 ),
			    ( 2, "Gross Profit",       [KPI Gross Profit],    [Gross Profit YoY %],       [KPI Gross Profit LY],    1 ),
			    ( 3, "Inventory Value",    [KPI Inventory Value], [Inventory Value YoY %],    [KPI Inventory Value LY], 1 ),
			    ( 4, "Stockout Rate",      [KPI Stockout Rate],   [Stockout Rate YoY %],      [KPI Stockout Rate LY],   0 ),
			    ( 5, "Inventory Turnover", [KPI Turnover],        [Inventory Turnover YoY %], [KPI Turnover LY],        1 )
			}
			VAR _card = "flex:1;min-width:0;background:#FFFFFF;border-radius:12px;padding:10px 14px;box-shadow:0 1px 4px rgba(16,14,111,.10);display:flex;flex-direction:column;justify-content:space-between"
			VAR _cards =
			    CONCATENATEX (
			        _rows,
			        VAR _idx = [Value1]
			        VAR _p = [Value4]
			        VAR _up = _p >= 0
			        VAR _good = IF ( [Value6] = 1, _up, NOT _up )
			        VAR _fg = IF ( ISBLANK ( _p ), "#8A8A95", IF ( _good, "#1E8E4A", "#D9363E" ) )
			        VAR _bg = IF ( ISBLANK ( _p ), "#F1F1F5", IF ( _good, "#E6F5EC", "#FDECEC" ) )
			        VAR _arrow =
			            IF ( NOT ISBLANK ( _p ),
			                "<svg width='9' height='9' viewBox='0 0 10 10'><path d='"
			                    & IF ( _up, "M5 1.5 L9 8.5 H1 Z", "M5 8.5 L9 1.5 H1 Z" )
			                    & "' fill='" & _fg & "'/></svg>" )
			        -- sparkline: monthly values of the selected year
			        VAR _m =
			            FILTER (
			                ADDCOLUMNS (
			                    CALCULATETABLE ( VALUES ( Dim_Date[MonthNo] ), Dim_Date[Year] = _y ),
			                    "@v", CALCULATE (
			                        SWITCH ( _idx, 1, [Revenue], 2, [Gross Profit], 3, [Inventory Value],
			                                       4, [Stockout Rate %], [Inventory Turnover] ),
			                        Dim_Date[Year] = _y )
			                ),
			                NOT ISBLANK ( [@v] )
			            )
			        VAR _mn = MINX ( _m, [@v] )
			        VAR _mx = MAXX ( _m, [@v] )
			        VAR _pts =
			            CONCATENATEX ( _m,
			                FORMAT ( ( Dim_Date[MonthNo] - 1 ) / 11 * 84, "0.0" ) & ","
			                    & FORMAT ( 26 - DIVIDE ( [@v] - _mn, _mx - _mn, 0.5 ) * 22, "0.0" ),
			                " ", Dim_Date[MonthNo], ASC )
			        VAR _lm = MAXX ( _m, Dim_Date[MonthNo] )
			        VAR _lv = MAXX ( FILTER ( _m, Dim_Date[MonthNo] = _lm ), [@v] )
			        VAR _spark =
			            IF ( COUNTROWS ( _m ) > 1,
			                "<svg width='88' height='30' viewBox='-2 0 90 30'><polyline points='" & _pts
			                    & "' fill='none' stroke='#100E6F' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' opacity='.85'/>"
			                    & "<circle cx='" & FORMAT ( ( _lm - 1 ) / 11 * 84, "0.0" )
			                    & "' cy='" & FORMAT ( 26 - DIVIDE ( _lv - _mn, _mx - _mn, 0.5 ) * 22, "0.0" )
			                    & "' r='3' fill='#100E6F'/></svg>" )
			        RETURN
			            "<div style='" & _card & "'>"
			                & "<div style='font-size:12px;color:#6B6B76;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>" & [Value2] & "</div>"
			                & "<div style='display:flex;align-items:flex-end;justify-content:space-between;gap:6px'>"
			                    & "<div style='font-size:24px;font-weight:600;color:#1F1A4F;line-height:1.1;white-space:nowrap'>" & [Value3] & "</div>"
			                    & _spark
			                & "</div>"
			                & "<div style='display:flex;align-items:center;gap:6px;font-size:10px;color:#8A8A95;white-space:nowrap'>"
			                    & "<span style='display:inline-flex;align-items:center;gap:4px;padding:2px 7px;border-radius:10px;font-weight:600;background:" & _bg & ";color:" & _fg & "'>"
			                    & _arrow & IF ( ISBLANK ( _p ), "–", FORMAT ( ABS ( _p ), "0.0%" ) ) & "</span>"
			                    & "vs LY " & [Value5]
			                & "</div>"
			            & "</div>",
			        "", [Value1], ASC
			    )
			RETURN
			    "<div style='display:flex;gap:16px;height:118px;box-sizing:border-box;font-family:Segoe UI,sans-serif'>" & _cards & "</div>"
```

### HTML KPI Operations

```dax
VAR _rows = {
			    ( 1, "Low Stock SKUs",      FORMAT ( [Low Stock SKUs], "#,0" ),      [Low Stock Color],      [Low Stock Note] ),
			    ( 2, "Stockout Count",      FORMAT ( [Stockout Count], "#,0" ),      [Stockout Count Color], [Stockout Count Note] ),
			    ( 3, "Avg. Days of Supply", FORMAT ( [Avg Days of Supply], "#,0.0" ),
			         IF ( [Avg Days of Supply] > 40, "#D98A1C", "#1F1A4F" ),                                 [Avg Days of Supply Note] ),
			    ( 4, "Units Received",      FORMAT ( [Units Received], "#,0" ),      "#1F1A4F",              [Units Received Note] ),
			    ( 5, "Restock Cost",        [KPI Restock Cost],                      "#1F1A4F",              [Restock Cost Note] )
			}
			VAR _card = "flex:1;min-width:0;background:#FFFFFF;border-radius:12px;padding:10px 14px;box-shadow:0 1px 4px rgba(16,14,111,.10);display:flex;flex-direction:column;justify-content:space-between"
			VAR _cards =
			    CONCATENATEX (
			        _rows,
			        VAR _c = IF ( [Value4] = "#222222" || ISBLANK ( [Value4] ), "#1F1A4F", [Value4] )
			        RETURN
			            "<div style='" & _card & "'>"
			                & "<div style='display:flex;align-items:center;gap:6px;font-size:12px;color:#6B6B76;white-space:nowrap;overflow:hidden'>"
			                    & "<span style='width:8px;height:8px;border-radius:50%;background:" & _c & ";flex:none'></span>" & [Value2]
			                & "</div>"
			                & "<div style='font-size:24px;font-weight:600;color:" & _c & ";line-height:1.1;white-space:nowrap'>" & [Value3] & "</div>"
			                & "<div style='font-size:9.5px;color:#5A5A66;background:#F1F1F5;border-radius:10px;padding:3px 9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>" & [Value5] & "</div>"
			            & "</div>",
			        "", [Value1], ASC
			    )
			RETURN
			    "<div style='display:flex;gap:16px;height:118px;box-sizing:border-box;font-family:Segoe UI,sans-serif'>" & _cards & "</div>"
```

### HTML KPI Suppliers

```dax
VAR _card  = "flex:1;min-width:0;background:#FFFFFF;border-radius:12px;padding:10px 14px;box-shadow:0 1px 4px rgba(16,14,111,.10);display:flex;flex-direction:column;justify-content:space-between"
			VAR _tStyle = "display:flex;align-items:center;gap:6px;font-size:12px;color:#6B6B76;white-space:nowrap;overflow:hidden"
			VAR _nStyle = "font-size:9.5px;color:#5A5A66;background:#F1F1F5;border-radius:10px;padding:3px 9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
			VAR _vStyle = "font-size:24px;font-weight:600;line-height:1.1;white-space:nowrap;color:"
			
			-- colors (neutral = navy)
			VAR _c1 = COALESCE ( [Lead Time Color], "#1F1A4F" )
			VAR _c2 = IF ( [DIO Color] = "#222222", "#1F1A4F", [DIO Color] )
			VAR _c3 = "#1F1A4F"
			VAR _c4 = COALESCE ( [Stockout Risk Color], "#1F1A4F" )
			VAR _c5 = IF ( [Stock Value Spread Color] = "#222222", "#1F1A4F", [Stock Value Spread Color] )
			
			-- values
			VAR _v1 = FORMAT ( [Avg Lead Time CY], "#,0.0" )
			VAR _v2 = FORMAT ( [DIO], "#,0.0" )
			VAR _v3 = FORMAT ( [Active Suppliers], "#,0" )
			VAR _v4 = [KPI Stockout Risk]
			VAR _v5 = [KPI Stock Value Spread]
			
			VAR _k1 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c1 & "'></span>Avg Lead Time (Days)</div><div style='" & _vStyle & _c1 & "'>" & _v1 & "</div><div style='" & _nStyle & "'>" & [Lead Time Note] & "</div></div>"
			VAR _k2 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c2 & "'></span>DIO</div><div style='" & _vStyle & _c2 & "'>" & _v2 & "</div><div style='" & _nStyle & "'>" & [DIO Note] & "</div></div>"
			VAR _k3 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c3 & "'></span>Active Suppliers</div><div style='" & _vStyle & _c3 & "'>" & _v3 & "</div><div style='" & _nStyle & "'>" & [Active Suppliers Note] & "</div></div>"
			VAR _k4 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c4 & "'></span>Stockout Risk</div><div style='" & _vStyle & _c4 & "'>" & _v4 & "</div><div style='" & _nStyle & "'>" & [Stockout Risk Note] & "</div></div>"
			VAR _k5 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c5 & "'></span>Stock Value Spread</div><div style='" & _vStyle & _c5 & "'>" & _v5 & "</div><div style='" & _nStyle & "'>" & [Stock Value Spread Note] & "</div></div>"
			RETURN
			    "<div style='display:flex;gap:16px;height:118px;box-sizing:border-box;font-family:Segoe UI,sans-serif'>"
			        & _k1 & _k2 & _k3 & _k4 & _k5 & "</div>"
```

### HTML KPI Details

```dax
VAR _card   = "flex:1;min-width:0;background:#FFFFFF;border-radius:12px;padding:10px 14px;box-shadow:0 1px 4px rgba(16,14,111,.10);display:flex;flex-direction:column;justify-content:space-between"
			VAR _tStyle = "display:flex;align-items:center;gap:6px;font-size:12px;color:#6B6B76;white-space:nowrap;overflow:hidden"
			VAR _nStyle = "font-size:9.5px;color:#5A5A66;background:#F1F1F5;border-radius:10px;padding:3px 9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
			VAR _vStyle = "font-size:24px;font-weight:600;line-height:1.1;white-space:nowrap;color:"
			
			-- colors (navy = neutral, orange = attention)
			VAR _c1 = "#1F1A4F"
			VAR _c2 = "#1F1A4F"
			VAR _c3 = IF ( [Restock Cost] > 0, "#D98A1C", "#1F1A4F" )
			VAR _c4 = "#1F1A4F"
			VAR _c5 = "#1F1A4F"
			
			-- values
			VAR _v1 = FORMAT ( [Active SKUs], "#,0" )
			VAR _v2 = [KPI Stock Value]
			VAR _v3 = [KPI Restock Cost]
			VAR _v4 = [KPI Avg Unit Cost]
			VAR _v5 = FORMAT ( [SKU Lead Time], "#,0.0" ) & " days"
			
			VAR _k1 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c1 & "'></span>Total SKUs</div><div style='" & _vStyle & _c1 & "'>" & _v1 & "</div><div style='" & _nStyle & "'>" & [Total SKUs Note] & "</div></div>"
			VAR _k2 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c2 & "'></span>Stock Value</div><div style='" & _vStyle & _c2 & "'>" & _v2 & "</div><div style='" & _nStyle & "'>" & [Stock Value Note] & "</div></div>"
			VAR _k3 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c3 & "'></span>Restock Cost</div><div style='" & _vStyle & _c3 & "'>" & _v3 & "</div><div style='" & _nStyle & "'>" & [Restock Cost Note (Detail)] & "</div></div>"
			VAR _k4 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c4 & "'></span>Avg Unit Cost</div><div style='" & _vStyle & _c4 & "'>" & _v4 & "</div><div style='" & _nStyle & "'>" & [Avg Unit Cost Note] & "</div></div>"
			VAR _k5 = "<div style='" & _card & "'><div style='" & _tStyle & "'><span style='width:8px;height:8px;border-radius:50%;flex:none;background:" & _c5 & "'></span>SKU Lead Time</div><div style='" & _vStyle & _c5 & "'>" & _v5 & "</div><div style='" & _nStyle & "'>" & [SKU Lead Time Note] & "</div></div>"
			RETURN
			    "<div style='display:flex;gap:16px;height:118px;box-sizing:border-box;font-family:Segoe UI,sans-serif'>"
			        & _k1 & _k2 & _k3 & _k4 & _k5 & "</div>"
```

### SVG Stock Status

```dax
VAR _t = [Current Stock Action]
			VAR _bg = SWITCH ( _t, "Reorder Now", "#D9363E", "Healthy", "#2E9E4F" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<rect x='2' y='2' width='86' height='18' rx='9' fill='" & _bg & "'/>"
			        & "<text x='45' y='15' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _t ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### SVG Stock Health

```dax
VAR _t = [Current Health]
			VAR _bg = SWITCH ( _t, "Stockout", "#D9363E", "Critical Low", "#E07B10", "Healthy", "#2E9E4F",
			                       "Overstocked", "#D9A400", "Dead Stock", "#7A7A7A" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<rect x='2' y='2' width='86' height='18' rx='9' fill='" & _bg & "'/>"
			        & "<text x='45' y='15' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _t ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### SVG ABC Class

```dax
VAR _t = [Top ABC Class]
			VAR _bg = SWITCH ( _t, "A Class", "#100E6F", "B Class", "#7E70B0", "C Class", "#9A9A9A" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<rect x='12' y='2' width='66' height='18' rx='9' fill='" & _bg & "'/>"
			        & "<text x='45' y='15' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _t ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### SVG Revenue Bar

```dax
VAR _v = [Top Revenue]
			VAR _max = MAXX ( ALLSELECTED ( Products[ProductName] ), [Top Revenue] )
			VAR _w = DIVIDE ( _v, _max ) * 86
			VAR _txt = FORMAT ( _v, "$#,0" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<rect x='2' y='3' width='" & FORMAT ( _w, "0.0" ) & "' height='16' rx='3' fill='#CCD3EB'/>"
			        & "<text x='6' y='15' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#1F1A4F'>"
			        & _txt & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _v ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### SVG Margin

```dax
VAR _p = [Top Margin %]
			VAR _c = 2 * PI () * 7          -- circumference for r = 7
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<circle cx='12' cy='11' r='7' fill='none' stroke='#E4E2F3' stroke-width='4'/>"
			        & "<circle cx='12' cy='11' r='7' fill='none' stroke='#100E6F' stroke-width='4' transform='rotate(-90 12 11)'"
			        & " stroke-dasharray='" & FORMAT ( _p * _c, "0.0" ) & " " & FORMAT ( _c, "0.0" ) & "'/>"
			        & "<text x='26' y='15' font-family='Segoe UI,sans-serif' font-size='10' fill='#333333'>" & FORMAT ( _p, "0.0%" ) & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _p ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### SVG Lead Time

```dax
VAR _v = [Avg Lead Time CY]
			VAR _bg = SWITCH ( TRUE (), _v >= 15, "#D9363E", _v >= 10, "#D98A1C", "#2E9E4F" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<rect x='12' y='2' width='66' height='18' rx='9' fill='" & _bg & "'/>"
			        & "<text x='45' y='15' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>"
			        & FORMAT ( _v, "0" ) & " days</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _v ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### SVG Stockout Rate

```dax
VAR _v = [Stockout Rate CY]
			VAR _bg = SWITCH ( TRUE (), _v >= 0.3, "#D9363E", _v >= 0.15, "#D98A1C", "#2E9E4F" )
			VAR _svg =
			    "<svg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'>"
			        & "<rect x='12' y='2' width='66' height='18' rx='9' fill='" & _bg & "'/>"
			        & "<text x='45' y='15' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>"
			        & FORMAT ( _v, "0.0%" ) & "</text></svg>"
			RETURN
			    IF ( NOT ISBLANK ( _v ),
			        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

## Stock Health

### SKU Months

```dax
COUNTROWS ( Fact_Inventory )
```

### Stockout Count

```dax
CALCULATE ( COUNTROWS ( Fact_Inventory ), Fact_Inventory[OnHandQty] <= 0 ) + 0
```

### Stockout Rate %
Share of SKU-months with zero or negative stock.

```dax
DIVIDE ( CALCULATE ( COUNTROWS ( Fact_Inventory ), Fact_Inventory[OnHandQty] <= 0 ) + 0, COUNTROWS ( Fact_Inventory ) )
```

### Stockout Rate CY
Stockout rate in the year in focus.

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Stockout Rate %], Dim_Date[Year] = _y )
```

### Stockout Rate LY

```dax
VAR _y = [Selected Year]
			RETURN
			    CALCULATE ( [Stockout Rate %], Dim_Date[Year] = _y - 1 )
```

### Stockout Rate YoY %

```dax
DIVIDE ( [Stockout Rate CY] - [Stockout Rate LY], [Stockout Rate LY] )
```

### Stockout Rate YoY Label

```dax
VAR v = [Stockout Rate YoY %]
			RETURN
			    IF ( ISBLANK ( v ), "–", FORMAT ( v, "+0.0%;-0.0%;0.0%" ) & IF ( v >= 0, " ▲", " ▼" ) )
```

### Stockout Rate YoY Color

```dax
IF ( [Stockout Rate YoY %] >= 0, "#D9363E", "#2E9E4F" )
```

### Stockout Count Note

```dax
"Out of " & FORMAT ( [SKU Months], "#,0" ) & " SKU-months tracked"
```

### Active SKUs
SKUs with stock recorded on the last snapshot.

```dax
COUNTROWS ( FILTER ( VALUES ( Products[SKU] ), NOT ISBLANK ( [Current Stock] ) ) )
```

### Low Stock SKUs
SKUs at or below their reorder point on the last snapshot.

```dax
COUNTROWS ( FILTER ( VALUES ( Products[SKU] ), [Current Stock Action] = "Reorder Now" ) ) + 0
```

### Low Stock Note

```dax
FORMAT ( DIVIDE ( [Low Stock SKUs], [Active SKUs] ), "0%" ) & " of catalog needs reorder"
```

### Avg Days of Supply
Average days the current stock lasts at the current sales rate (capped at 365).

```dax
AVERAGE ( Fact_Inventory[Days of Supply] )
```

### Avg Days of Supply Note

```dax
VAR v = [Avg Days of Supply]
			RETURN
			    SWITCH ( TRUE (), v > 40, "Avg. above target (30–40 days)", v < 30, "Avg. below target (30–40 days)", "Within target (30–40 days)" )
```

### Units Received

```dax
SUM ( Fact_Inventory[UnitsReceived] )
```

### Units Sold (Stock)

```dax
SUM ( Fact_Inventory[UnitsSold] )
```

### Units Received Note

```dax
"Across " & DISTINCTCOUNT ( Fact_Inventory[SnapshotDate] ) & " months: " & CALCULATE ( DISTINCTCOUNT ( Fact_Inventory[SKU] ), Fact_Inventory[UnitsReceived] > 0 ) & " SKUs restocked"
```

### Restock Cost
Cost to reorder every low-stock SKU at its reorder quantity.

```dax
SUMX (
			    FILTER ( VALUES ( Products[SKU] ), [Current Stock Action] = "Reorder Now" ),
			    CALCULATE ( MAX ( Products[ReorderQty] ) * MAX ( Products[UnitCost] ) )
			)
```

### Restock Cost Note

```dax
"To restock " & [Low Stock SKUs] & " SKUs now"
```

### Restock Cost Note (Detail)

```dax
"To restock " & [Low Stock SKUs] & " low stock SKUs"
```

### Reorder Point (SKU)

```dax
IF ( NOT ISBLANK ( [Current Stock] ), SUM ( Products[ReorderPoint] ) )
```

### Reorder Quantity (SKU)

```dax
IF ( NOT ISBLANK ( [Current Stock] ), SUM ( Products[ReorderQty] ) )
```

### Restock Cost (SKU)

```dax
IF ( [Current Stock Action] = "Reorder Now", SUMX ( Products, Products[ReorderQty] * Products[UnitCost] ) )
```

### Unit Cost (SKU)

```dax
IF ( NOT ISBLANK ( [Current Stock] ), MAX ( Products[UnitCost] ) )
```

### Lead Time (SKU)

```dax
IF ( NOT ISBLANK ( [Current Stock] ), MAX ( Products[LeadTimeDays] ) )
```

### Action Color

```dax
SWITCH ( [Current Stock Action], "Reorder Now", "#D9363E", "Healthy", "#2E9E4F" )
```

### Health Color (SKU)

```dax
SWITCH ( [Current Health], "Stockout", "#D9363E", "Critical Low", "#E07B10", "Healthy", "#2E9E4F", "Overstocked", "#D9A400", "Dead Stock", "#7A7A7A" )
```

### Low Stock Color

```dax
IF ( [Low Stock SKUs] > 0, "#E2620F", "#222222" )
```

### Stockout Count Color

```dax
IF ( [Stockout Rate %] > 0.05, "#E2620F", "#222222" )
```
