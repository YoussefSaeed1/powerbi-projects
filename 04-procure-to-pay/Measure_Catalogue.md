# Procure-to-Pay Performance · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Targets

### Target On-Time Delivery
Delivery target agreed with supply chain.
Format: `0%`

```dax
0.90
```

### Target Procure Cycle Days
Target days from requisition to goods receipt.
Format: `0`

```dax
25
```

### Target Spend Under Contract
Format: `0%`

```dax
0.80
```

### Target Maverick Spend
Format: `0%`

```dax
0.05
```

### Target Late Payments
Format: `0%`

```dax
0.05
```

### Late Payment Target Line
Format: `0%`

```dax
IF ( NOT ISBLANK ( [Late Payment % (Closed Months)] ), [Target Late Payments] )
```

### Procure Cycle Target Line
Format: `0`

```dax
IF ( NOT ISBLANK ( [Avg Procure Cycle (Closed Months)] ), [Target Procure Cycle Days] )
```

## Helpers

### Selected Year
Year in focus: the year picked in the slicer, or the latest year in the data.
Format: `0`

```dax
VAR _maxYear = YEAR ( CALCULATE ( MAX ( Fact_PO[PO_Date] ), REMOVEFILTERS () ) )
RETURN
    IF ( ISFILTERED ( Dim_Date[Year] ), MAX ( Dim_Date[Year] ), _maxYear )
```

### Data As Of
Format: `dd-mmm-yyyy`

```dax
CALCULATE ( MAX ( Fact_PO[PO_Date] ), REMOVEFILTERS () )
```

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

### Year Label

```dax
"FY" & [Selected Year] & " vs FY" & ( [Selected Year] - 1 )
```

## Spend

### Spend
Total value of purchase orders.
Format: `$#,0`

```dax
SUM ( Fact_PO[PO_Value_USD] )
```

### Spend CY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Spend], Dim_Date[Year] = _y )
```

### Spend LY
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [Spend], Dim_Date[Year] = _y - 1 )
```

### Spend YoY %
Format: `+0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [Spend CY] - [Spend LY], [Spend LY] )
```

### PO Count
Format: `#,0`

```dax
COUNTROWS ( Fact_PO )
```

### PO Count CY
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [PO Count], Dim_Date[Year] = _y )
```

### PO Count LY
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( [PO Count], Dim_Date[Year] = _y - 1 )
```

### PO Count YoY %
Format: `+0.0%;-0.0%;0.0%`

```dax
DIVIDE ( [PO Count CY] - [PO Count LY], [PO Count LY] )
```

### Spend CY $M
Format: `$#,0.0`

```dax
DIVIDE ( [Spend CY], 1000000 )
```

### Spend LY $M
Format: `$#,0.0`

```dax
DIVIDE ( [Spend LY], 1000000 )
```

## Cycle Time

### Avg Days PR to PO
Average days from requisition to purchase order.
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days PR to PO] ), Dim_Date[Year] = _y )
```

### Avg Days PO to Receipt
Average supplier lead time: PO to goods receipt.
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days PO to Receipt] ), Dim_Date[Year] = _y )
```

### Avg Days Receipt to Invoice
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days Receipt to Invoice] ), Dim_Date[Year] = _y )
```

### Avg Days Invoice to Payment
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days Invoice to Payment] ), Dim_Date[Year] = _y )
```

### Avg Procure Cycle
Average days from requisition to goods receipt (procure part of P2P).
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days PR to Receipt] ), Dim_Date[Year] = _y )
```

### Avg Procure Cycle LY
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days PR to Receipt] ), Dim_Date[Year] = _y - 1 )
```

### Receipt Completeness %
Share of POs already received. Months below 98% are still open.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( COUNT ( Fact_PO[GRN_Date] ), COUNTROWS ( Fact_PO ) ), Dim_Date[Year] = _y )
```

### Avg Procure Cycle (Closed Months)
Average procure cycle for months where almost every PO has been received; open months would show only the fast receipts.
Format: `0.0`

```dax
IF ( [Receipt Completeness %] < 0.98, BLANK (), [Avg Procure Cycle] )
```

### Avg Days PO to Receipt LY
Format: `0.0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( AVERAGE ( Fact_PO[Days PO to Receipt] ), Dim_Date[Year] = _y - 1 )
```

### Stage Days
Average days of the stage on the row (used with Dim_Stage).
Format: `0.0`

```dax
SWITCH (
    SELECTEDVALUE ( Dim_Stage[Stage Order] ),
    1, [Avg Days PR to PO],
    2, [Avg Days PO to Receipt],
    3, [Avg Days Receipt to Invoice],
    4, [Avg Days Invoice to Payment]
)
```

### Funnel Count
Documents reaching each step of the process in the year in focus.
Format: `#,0`

```dax
VAR _y = [Selected Year]
VAR _pr = CALCULATE ( COUNTROWS ( Fact_PR ), Dim_Date[Year] = _y, TREATAS ( VALUES ( Dim_Material[Category] ), Fact_PR[Category] ) )
VAR _prOk = CALCULATE ( COUNTROWS ( Fact_PR ), Dim_Date[Year] = _y, Fact_PR[Status] = "Converted to PO", TREATAS ( VALUES ( Dim_Material[Category] ), Fact_PR[Category] ) )
VAR _po = [PO Count CY]
VAR _grn = CALCULATE ( COUNTROWS ( Fact_PO ), Dim_Date[Year] = _y, NOT ISBLANK ( Fact_PO[GRN_Date] ) )
VAR _inv = [Invoices]
VAR _match = CALCULATE ( COUNTROWS ( Fact_PO ), Dim_Date[Year] = _y, Fact_PO[Match_Status] = "Matched first time" )
VAR _paid = CALCULATE ( COUNTROWS ( Fact_PO ), Dim_Date[Year] = _y, NOT ISBLANK ( Fact_PO[Payment_Date] ) )
RETURN
    SWITCH ( SELECTEDVALUE ( Dim_Funnel[Step Order] ), 1, _pr, 2, _prOk, 3, _po, 4, _grn, 5, _inv, 6, _match, 7, _paid )
```

### Buyer Status

```dax
VAR _d = [Avg Days PR to PO]
RETURN
    IF ( ISBLANK ( _d ), BLANK (), IF ( _d > 12, "Slow", IF ( _d > 9.5, "Watch", "OK" ) ) )
```

## Suppliers

### On-Time Delivery %
Share of received POs that arrived on or before the promised date.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( SUM ( Fact_PO[On Time] ), COUNT ( Fact_PO[On Time] ) ), Dim_Date[Year] = _y )
```

### On-Time Delivery % LY
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( SUM ( Fact_PO[On Time] ), COUNT ( Fact_PO[On Time] ) ), Dim_Date[Year] = _y - 1 )
```

### Quality Acceptance %
Accepted quantity as a share of ordered quantity.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( SUM ( Fact_PO[Qty_Accepted] ), SUM ( Fact_PO[Qty_Ordered] ) ), Dim_Date[Year] = _y )
```

### Active Suppliers
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DISTINCTCOUNT ( Fact_PO[SupplierID] ), Dim_Date[Year] = _y )
```

### Active Suppliers LY
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DISTINCTCOUNT ( Fact_PO[SupplierID] ), Dim_Date[Year] = _y - 1 )
```

### Supplier Spend Rank
Format: `0`

```dax
IF (
    HASONEVALUE ( Dim_Supplier[SupplierName] ),
    RANKX ( ALL ( Dim_Supplier[SupplierName] ), [Spend CY], , DESC, DENSE )
)
```

### Top 10 Supplier Share
Share of spend placed with the ten largest suppliers (concentration risk).
Format: `0.0%`

```dax
VAR _top = TOPN ( 10, ALL ( Dim_Supplier[SupplierName] ), [Spend CY], DESC )
RETURN
    DIVIDE ( CALCULATE ( [Spend CY], _top ), CALCULATE ( [Spend CY], ALL ( Dim_Supplier ) ) )
```

### Spend CY (Top 25 Suppliers)
Format: `$#,0`

```dax
IF ( [Supplier Spend Rank] <= 25, [Spend CY] )
```

### Supplier Score
0–100 score: 50% on-time delivery, 30% quality acceptance, 20% contract coverage.
Format: `0`

```dax
VAR _otd = [On-Time Delivery %]
VAR _qa = [Quality Acceptance %]
VAR _contract = IF ( SELECTEDVALUE ( Dim_Supplier[Has_Contract] ), 1, 0 )
RETURN
    IF ( NOT ISBLANK ( _otd ), ROUND ( 100 * ( 0.5 * _otd + 0.3 * _qa + 0.2 * _contract ), 0 ) )
```

### Supplier Status

```dax
VAR _s = [Supplier Score] RETURN IF ( ISBLANK ( _s ), BLANK (), IF ( _s >= 85, "Strong", IF ( _s >= 75, "Watch", "At risk" ) ) )
```

### Contract Label

```dax
IF ( SELECTEDVALUE ( Dim_Supplier[Has_Contract] ), "Yes", "No" )
```

## Compliance

### Spend Under Contract %
Share of spend placed under an active contract.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( CALCULATE ( [Spend], Fact_PO[Under_Contract] = TRUE () ), [Spend] ), Dim_Date[Year] = _y )
```

### Spend Under Contract % LY
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( CALCULATE ( [Spend], Fact_PO[Under_Contract] = TRUE () ), [Spend] ), Dim_Date[Year] = _y - 1 )
```

### Maverick Spend
Spend with no approved requisition, or with a PO raised after the invoice.
Format: `$#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( CALCULATE ( [Spend], Fact_PO[Maverick] = 1 ), Dim_Date[Year] = _y )
```

### Maverick Spend %
Format: `0.0%`

```dax
DIVIDE ( [Maverick Spend], [Spend CY] )
```

### Maverick Spend % LY
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( CALCULATE ( [Spend], Fact_PO[Maverick] = 1 ), [Spend] ), Dim_Date[Year] = _y - 1 )
```

### Maverick Spend $K
Format: `$#,0`

```dax
DIVIDE ( [Maverick Spend], 1000 )
```

### POs After Invoice
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( CALCULATE ( COUNTROWS ( Fact_PO ), Fact_PO[PO_After_Invoice] = TRUE () ), Dim_Date[Year] = _y )
```

### POs After Invoice LY
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( CALCULATE ( COUNTROWS ( Fact_PO ), Fact_PO[PO_After_Invoice] = TRUE () ), Dim_Date[Year] = _y - 1 )
```

## Payments

### Invoices
Format: `#,0`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( CALCULATE ( COUNTROWS ( Fact_PO ), NOT ISBLANK ( Fact_PO[Invoice_Date] ) ), Dim_Date[Year] = _y )
```

### First-Pass Match %
Invoices that matched PO and receipt on price and quantity without manual fixing.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( CALCULATE ( COUNTROWS ( Fact_PO ), Fact_PO[Match_Status] = "Matched first time" ), CALCULATE ( COUNTROWS ( Fact_PO ), NOT ISBLANK ( Fact_PO[Invoice_Date] ) ) ), Dim_Date[Year] = _y )
```

### First-Pass Match % LY
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( CALCULATE ( COUNTROWS ( Fact_PO ), Fact_PO[Match_Status] = "Matched first time" ), CALCULATE ( COUNTROWS ( Fact_PO ), NOT ISBLANK ( Fact_PO[Invoice_Date] ) ) ), Dim_Date[Year] = _y - 1 )
```

### Invoices (Match View)
Format: `#,0`

```dax
IF ( SELECTEDVALUE ( Fact_PO[Match_Status] ) = "Not invoiced yet", BLANK (), [Invoices] )
```

### Late Payment %
Invoices paid after the supplier's payment terms, plus unpaid invoices already past their due date.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( SUM ( Fact_PO[Paid Late] ), COUNT ( Fact_PO[Paid Late] ) ), Dim_Date[Year] = _y )
```

### Late Payment % LY
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( SUM ( Fact_PO[Paid Late] ), COUNT ( Fact_PO[Paid Late] ) ), Dim_Date[Year] = _y - 1 )
```

### Payment Maturity %
Share of POs whose invoice due date has passed by the data cut-off. Months below 95% are still open.
Format: `0.0%`

```dax
VAR _y = [Selected Year] RETURN CALCULATE ( DIVIDE ( SUM ( Fact_PO[Due Reached] ), COUNTROWS ( Fact_PO ) ), Dim_Date[Year] = _y )
```

### Late Payment % (Closed Months)
Late Payment % for months where almost every invoice has reached its due date; recent months are hidden so they don't look better than they are.
Format: `0.0%`

```dax
IF ( [Payment Maturity %] < 0.95, BLANK (), [Late Payment %] )
```

### Open Invoice Value
Unpaid invoice value at the data cut-off, split by invoice age.
Format: `$#,0`

```dax
VAR _asof = [Data As Of]
VAR _lo = SELECTEDVALUE ( Dim_AgeBucket[From Days], 0 )
VAR _hi = SELECTEDVALUE ( Dim_AgeBucket[To Days], 9999 )
RETURN
    CALCULATE (
        SUM ( Fact_PO[PO_Value_USD] ),
        REMOVEFILTERS ( Dim_Date ),
        FILTER (
            ALL ( Fact_PO[Invoice_Date], Fact_PO[Payment_Date] ),
            NOT ISBLANK ( Fact_PO[Invoice_Date] ) && ISBLANK ( Fact_PO[Payment_Date] )
                && DATEDIFF ( Fact_PO[Invoice_Date], _asof, DAY ) >= _lo
                && DATEDIFF ( Fact_PO[Invoice_Date], _asof, DAY ) <= _hi
        )
    )
```

## Data Quality

### DQ Value
Result of each data quality rule.

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_PO ) ), "#,0" ),
        2, FORMAT ( 0 + COUNTROWS ( ALL ( Fact_PO ) ) - DISTINCTCOUNT ( Fact_PO[PO_ID] ), "#,0" ),
        3, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PO ), ISBLANK ( RELATED ( Dim_Supplier[SupplierName] ) ) ) ), "#,0" ),
        4, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PO ), ISBLANK ( RELATED ( Dim_Plant[PlantName] ) ) ) ), "#,0" ),
        5, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PO ), Fact_PO[PO_Value_USD] <= 0 ) ), "#,0" ),
        6, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PO ), NOT ISBLANK ( Fact_PO[GRN_Date] ) && Fact_PO[GRN_Date] < Fact_PO[PO_Date] ) ), "#,0" ),
        7, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PO ), NOT ISBLANK ( Fact_PO[Payment_Date] ) && Fact_PO[Payment_Date] < Fact_PO[Invoice_Date] ) ), "#,0" ),
        8, FORMAT ( 0 + COUNTROWS ( FILTER ( ALL ( Fact_PO ), ISBLANK ( Fact_PO[GRN_Date] ) ) ), "#,0" ),
        9, FORMAT ( [Data As Of], "dd mmm yyyy" )
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
        _o IN { 1, 8, 9 }, "Info",
        _v = "0", "Pass",
        "Fail"
    )
```

### DQ Failed Checks
Format: `0`

```dax
COUNTROWS ( FILTER ( ALL ( Dim_DQ ), [DQ Status] = "Fail" ) )
```

## Insights

### Insight Overview
Narrative insights computed from the data in the current filter context.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Slowest Stage Days
Format: `0.0`

```dax
MAXX ( FILTER ( ALL ( Dim_Stage ), Dim_Stage[Stage Order] <= 2 ), [Stage Days] )
```

### Slowest Stage Name

```dax
VAR _max = [Slowest Stage Days]
RETURN
    MAXX ( FILTER ( ALL ( Dim_Stage ), Dim_Stage[Stage Order] <= 2 && [Stage Days] = _max ), Dim_Stage[Stage] )
```

### Top Maverick Dept

```dax
VAR _t = TOPN ( 1, ADDCOLUMNS ( VALUES ( Dim_Department[DepartmentName] ), "@m", [Maverick Spend] ), [@m], DESC )
RETURN
    MAXX ( _t, Dim_Department[DepartmentName] )
```

### Top Maverick Dept Share
Format: `0%`

```dax
VAR _t = TOPN ( 1, ADDCOLUMNS ( VALUES ( Dim_Department[DepartmentName] ), "@m", [Maverick Spend] ), [@m], DESC )
RETURN
    DIVIDE ( MAXX ( _t, [@m] ), [Maverick Spend] )
```

### Top Off-Contract Supplier

```dax
VAR _t = TOPN ( 1, ADDCOLUMNS ( VALUES ( Dim_Supplier[SupplierName] ), "@s", CALCULATE ( [Spend CY], Fact_PO[Under_Contract] = FALSE () ) ), [@s], DESC )
RETURN
    MAXX ( _t, Dim_Supplier[SupplierName] )
```

### Top Off-Contract Supplier Spend
Format: `$#,0`

```dax
VAR _t = TOPN ( 1, ADDCOLUMNS ( VALUES ( Dim_Supplier[SupplierName] ), "@s", CALCULATE ( [Spend CY], Fact_PO[Under_Contract] = FALSE () ) ), [@s], DESC )
RETURN
    MAXX ( _t, [@s] )
```

### Insight Compliance

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### KPI Overview
HTML for the KPI cards on the Overview page (HTML Content visual).

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Cycle

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Suppliers

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Compliance

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Text

### Spend YoY Note

```dax
VAR _c = [Spend CY] VAR _l = [Spend LY] VAR _d = DIVIDE ( _c - _l, _l ) RETURN IF ( ISBLANK ( _l ), "no prior year", IF ( _d >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( _d ), "0.0%" ) & " vs LY" )
```

### PO YoY Note

```dax
VAR _c = [PO Count CY] VAR _l = [PO Count LY] VAR _d = DIVIDE ( _c - _l, _l ) RETURN IF ( ISBLANK ( _l ), "no prior year", IF ( _d >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( _d ), "0.0%" ) & " vs LY" )
```

### Cycle Note

```dax
VAR _d = [Avg Procure Cycle] - [Avg Procure Cycle LY] RETURN IF ( ISBLANK ( [Avg Procure Cycle LY] ), "no prior year", IF ( _d <= 0, "▼ ", "▲ " ) & FORMAT ( ABS ( _d ), "0.0" ) & " days vs LY" )
```

### Contract Note

```dax
VAR _d = ( [Spend Under Contract %] - [Spend Under Contract % LY] ) * 100 RETURN IF ( ISBLANK ( [Spend Under Contract % LY] ), "no prior year", IF ( _d >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( _d ), "0.0" ) & " pts vs LY" )
```

### Lead Time Note

```dax
VAR _d = [Avg Days PO to Receipt] - [Avg Days PO to Receipt LY] RETURN IF ( ISBLANK ( [Avg Days PO to Receipt LY] ), "no prior year", IF ( _d <= 0, "▼ ", "▲ " ) & FORMAT ( ABS ( _d ), "0.0" ) & " days vs LY" )
```

### OTD Note

```dax
VAR _d = ( [On-Time Delivery %] - [On-Time Delivery % LY] ) * 100 RETURN IF ( ISBLANK ( [On-Time Delivery % LY] ), "no prior year", IF ( _d >= 0, "▲ ", "▼ " ) & FORMAT ( ABS ( _d ), "0.0" ) & " pts vs LY" )
```

## Formatting

### Stage Color
Highlights the slowest procure stage; the payment stage follows supplier terms so it is not flagged.

```dax
VAR _procure = MAXX ( FILTER ( ALL ( Dim_Stage ), Dim_Stage[Stage Order] <= 2 ), [Stage Days] )
RETURN
    IF ( SELECTEDVALUE ( Dim_Stage[Stage Order] ) <= 2 && [Stage Days] = _procure, "#E8A33D", "#2E7D8C" )
```

### Procure Cycle Color

```dax
IF ( [Avg Procure Cycle] > [Target Procure Cycle Days] * 1.15, "#D2584E", IF ( [Avg Procure Cycle] > [Target Procure Cycle Days], "#E8A33D", "#2E7D8C" ) )
```

### Supplier Status Pill

```dax
VAR _t = [Supplier Status]
VAR _bg = SWITCH ( _t, "Strong", "#3C8D5A", "Watch", "#E8A33D", "#D2584E" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='74' height='20' viewBox='0 0 74 20'>"
        & "<rect x='1' y='2' width='72' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='37' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### Funnel Color

```dax
IF ( SELECTEDVALUE ( Dim_Funnel[Step Order] ) = 6, "#E8A33D", "#2E7D8C" )
```

### Buyer Status Pill

```dax
VAR _t = [Buyer Status]
VAR _bg = SWITCH ( _t, "OK", "#3C8D5A", "Watch", "#E8A33D", "#D2584E" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='60' height='20' viewBox='0 0 60 20'>"
        & "<rect x='1' y='2' width='58' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='30' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### Dept Maverick Color

```dax
IF ( [Maverick Spend] >= 0.25 * CALCULATE ( [Maverick Spend], ALL ( Dim_Department ) ), "#D2584E", "#2E7D8C" )
```

### Age Color

```dax
IF ( SELECTEDVALUE ( Dim_AgeBucket[Age Order] ) >= 3, "#D2584E", IF ( SELECTEDVALUE ( Dim_AgeBucket[Age Order] ) = 2, "#E8A33D", "#2E7D8C" ) )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#3C8D5A", "Info", "#9CC4CC", "#D2584E" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='56' height='20' viewBox='0 0 56 20'>"
        & "<rect x='1' y='2' width='54' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='28' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

### Cycle Note Color

```dax
IF ( [Avg Procure Cycle] <= [Avg Procure Cycle LY], "#3C8D5A", "#D2584E" )
```
