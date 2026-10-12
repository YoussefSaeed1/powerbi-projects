# Aftersales Performance · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Targets

### Target Sales
Format: `#,0`

```dax
SUM ( Fact_BranchTarget[TargetSales] )
```

### Target Gross Profit
Format: `#,0`

```dax
SUM ( Fact_BranchTarget[TargetGP] )
```

### Sales vs Target
Format: `0%`

```dax
DIVIDE ( [Net Sales], [Target Sales] )
```

### Gross Profit vs Target
Format: `0%`

```dax
DIVIDE ( [Gross Profit], [Target Gross Profit] )
```

### Rep Target
Format: `#,0`

```dax
SUM ( Fact_RepTarget[TargetSales] )
```

### Rep Achievement
Rep net sales ÷ rep target.
Format: `0%`

```dax
DIVIDE ( [Net Sales], [Rep Target] )
```

## Helpers

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

### Selected Year
Format: `0`

```dax
MAX ( Dim_Date[Year] )
```

## Sales

### Gross Sales
List price before discounts.
Format: `#,0`

```dax
SUM ( Fact_Sales[Gross] )
```

### Discounts
Format: `#,0`

```dax
SUM ( Fact_Sales[Discount] )
```

### Net Sales
Gross sales minus discounts.
Format: `#,0`

```dax
SUM ( Fact_Sales[NetSales] )
```

### Cost of Sales
Parts cost and technician cost of the work sold.
Format: `#,0`

```dax
SUM ( Fact_Sales[COGS] )
```

### Gross Profit
Format: `#,0`

```dax
[Net Sales] - [Cost of Sales]
```

### Gross Margin
Format: `0.0%`

```dax
DIVIDE ( [Gross Profit], [Net Sales] )
```

### Discount Rate
Discounts as a share of gross sales.
Format: `0.0%`

```dax
DIVIDE ( [Discounts], [Gross Sales] )
```

### Invoices
Format: `#,0`

```dax
DISTINCTCOUNT ( Fact_Sales[InvoiceID] )
```

### Average Invoice
Format: `#,0`

```dax
DIVIDE ( [Net Sales], [Invoices] )
```

### Workshop Visits
Retail job cards: one workshop invoice is one visit.
Format: `#,0`

```dax
CALCULATE ( DISTINCTCOUNT ( Fact_Sales[InvoiceID] ), Fact_Sales[Channel] = "Workshop" )
```

### Average Workshop Invoice
Format: `#,0`

```dax
DIVIDE ( CALCULATE ( [Net Sales], Fact_Sales[Channel] = "Workshop" ), [Workshop Visits] )
```

### Online Sales Share
Format: `0.0%`

```dax
DIVIDE ( CALCULATE ( [Net Sales], Fact_Sales[Channel] = "Online" ), [Net Sales] )
```

### Online Growth
Format: `+0%;-0%`

```dax
DIVIDE ( CALCULATE ( [Net Sales], Fact_Sales[Channel] = "Online" ), CALCULATE ( [Net Sales LY], Fact_Sales[Channel] = "Online" ) ) - 1
```

### Sales Index
Monthly net sales as an index, first-year monthly average = 100. Ignores the year slicer.
Format: `0`

```dax
VAR _m = SELECTEDVALUE ( Dim_Month[Month Start] )
VAR _first = CALCULATE ( MIN ( Dim_Date[Year] ), REMOVEFILTERS ( Dim_Date ) )
VAR _base = CALCULATE ( [Net Sales], REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _first ) / 12
RETURN
    DIVIDE ( CALCULATE ( [Net Sales], REMOVEFILTERS ( Dim_Date ), Dim_Date[Month Start] = _m ), _base ) * 100
```

### Visits Index
Monthly workshop visits as an index, first-year monthly average = 100. Ignores the year slicer.
Format: `0`

```dax
VAR _m = SELECTEDVALUE ( Dim_Month[Month Start] )
VAR _first = CALCULATE ( MIN ( Dim_Date[Year] ), REMOVEFILTERS ( Dim_Date ) )
VAR _base = CALCULATE ( [Workshop Visits], REMOVEFILTERS ( Dim_Date ), Dim_Date[Year] = _first ) / 12
RETURN
    DIVIDE ( CALCULATE ( [Workshop Visits], REMOVEFILTERS ( Dim_Date ), Dim_Date[Month Start] = _m ), _base ) * 100
```

## Insights

### Best Margin Line

```dax
MAXX ( TOPN ( 1, VALUES ( Dim_BusinessLine[Business Line] ), [Gross Margin], DESC ), Dim_BusinessLine[Business Line] )
```

### Story Overview

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Story Geography

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Story Locations

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Story Rep

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Story Customers

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Story Finance

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### KPI Overview

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Geography

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Locations

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Rep

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Customers

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Finance

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Line Mix
Each business line's share of net sales next to its share of gross profit; orange for the line that earns most above its weight.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Gross Profit Bridge
Last year's gross profit, plus the change in gross sales, minus extra discounts and extra cost of sales, gives this year's.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Map Bubbles
Map of Egypt: one circle per governorate sized by our cars on the road, coloured by penetration (orange = low); squares are service branches.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Region Table
Cars on the road, penetration, sales, growth and service branches by region of the customer.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Governorate Bars
Penetration by governorate, lowest first; orange where there is no service branch.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Branch Scatter
Service branches: utilisation (x) against operating margin after overheads (y), circle size = net sales. Orange: full, or idle and losing money.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Channel Table
Net sales, growth and gross margin by channel; the fastest-growing channel in orange.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Branch Scorecard
Every branch: sales, target, margin, workshop utilisation and operating profit after overheads.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Rep Card
Name, role, home branch and start year of the selected rep.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Rep Scatter
Every rep: target achievement against average discount. Dark = same role as the selected rep, orange = the selected rep.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Rep Strips
The selected rep (orange) against every rep in the same role (grey dots) and the role median (black line), on four measures.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Retention Bars
Share of last year's retail customers who came back this year, by age of their car; orange after the 3-year warranty.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Customer Types
Net sales, growth and margin by customer type; margins under 20% in orange.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Profit Bridge
Gross sales, minus discounts and cost of sales, gives gross profit; minus each overhead category gives operating profit. EGP.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Overhead Bullets
Overheads by category: bar = actual, black line = budget; orange more than 5% over budget.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Receivables Aging
Open receivables at the end of the period by customer type and days past due.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Customers

### Retail Customers
Format: `#,0`

```dax
CALCULATE ( DISTINCTCOUNT ( Fact_Sales[CustomerID] ), Dim_Customer[CustomerType] = "Retail" )
```

### Retail Customers LY
Format: `#,0`

```dax
CALCULATE ( [Retail Customers], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Retained Customers
Retail customers who bought last year and again this year.
Format: `#,0`

```dax
VAR _ly = CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), SAMEPERIODLASTYEAR ( Dim_Date[Date] ), Dim_Customer[CustomerType] = "Retail" )
VAR _cy = CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), Dim_Customer[CustomerType] = "Retail" )
RETURN
    COUNTROWS ( INTERSECT ( _ly, _cy ) )
```

### Retention Rate
Format: `0.0%`

```dax
DIVIDE ( [Retained Customers], [Retail Customers LY] )
```

### Lost Customers
Bought last year, not this year.
Format: `#,0`

```dax
[Retail Customers LY] - [Retained Customers]
```

### New Customers
Retail customers whose first purchase falls in the period.
Format: `#,0`

```dax
VAR _start = MIN ( Dim_Date[Date] )
RETURN
    COUNTROWS (
        FILTER (
            CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), Dim_Customer[CustomerType] = "Retail" ),
            CALCULATE ( MIN ( Fact_Sales[InvoiceDate] ), REMOVEFILTERS ( Dim_Date ) ) >= _start
        )
    )
```

### Sales per Retail Customer
Format: `#,0`

```dax
DIVIDE ( CALCULATE ( [Net Sales], Dim_Customer[CustomerType] = "Retail" ), [Retail Customers] )
```

### Retention by Car Age
Retention of owners whose car is this many years old in the selected year.
Format: `0%`

```dax
VAR _y = MAX ( Dim_Date[Year] )
VAR _a = SELECTEDVALUE ( Dim_CarAge[Car Age] )
RETURN
    CALCULATE ( [Retention Rate], FILTER ( ALL ( Dim_Customer[ModelYear] ), IF ( _a >= 8, Dim_Customer[ModelYear] <= _y - 8, Dim_Customer[ModelYear] = _y - _a ) ) )
```

### Retention In Warranty
Retention of owners whose car is 1 or 2 years old.
Format: `0%`

```dax
VAR _y = MAX ( Dim_Date[Year] ) RETURN CALCULATE ( [Retention Rate], FILTER ( ALL ( Dim_Customer[ModelYear] ), Dim_Customer[ModelYear] >= _y - 2 && Dim_Customer[ModelYear] <= _y - 1 ) )
```

### Retention After Warranty
Retention of owners whose car is 4 years or older (warranty ended).
Format: `0%`

```dax
VAR _y = MAX ( Dim_Date[Year] ) RETURN CALCULATE ( [Retention Rate], FILTER ( ALL ( Dim_Customer[ModelYear] ), Dim_Customer[ModelYear] <= _y - 4 ) )
```

### Lapsed Owners 3-5
Owners of 3 to 5-year-old cars who bought last year and not this year.
Format: `#,0`

```dax
VAR _y = MAX ( Dim_Date[Year] )
VAR _ly = CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), SAMEPERIODLASTYEAR ( Dim_Date[Date] ), Dim_Customer[CustomerType] = "Retail", Dim_Customer[ModelYear] >= _y - 5, Dim_Customer[ModelYear] <= _y - 3 )
VAR _cy = CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), Dim_Customer[CustomerType] = "Retail" )
VAR _lost = EXCEPT ( _ly, _cy )
RETURN
    COUNTROWS ( _lost )
```

### Lapsed Owners 3-5 Spend
What those owners spent with us last year.
Format: `#,0`

```dax
VAR _y = MAX ( Dim_Date[Year] )
VAR _ly = CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), SAMEPERIODLASTYEAR ( Dim_Date[Date] ), Dim_Customer[CustomerType] = "Retail", Dim_Customer[ModelYear] >= _y - 5, Dim_Customer[ModelYear] <= _y - 3 )
VAR _cy = CALCULATETABLE ( VALUES ( Fact_Sales[CustomerID] ), Dim_Customer[CustomerType] = "Retail" )
VAR _lost = EXCEPT ( _ly, _cy )
RETURN
    SUMX ( _lost, CALCULATE ( [Net Sales], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) ) )
```

### Call List Spend
Last year's spend of a lapsed owner with a 3 to 5-year-old car; blank for everyone else.
Format: `#,0`

```dax
VAR _y = MAX ( Dim_Date[Year] )
VAR _my = SELECTEDVALUE ( Dim_Customer[ModelYear] )
RETURN
    IF (
        HASONEVALUE ( Dim_Customer[CustomerID] )
            && SELECTEDVALUE ( Dim_Customer[CustomerType] ) = "Retail"
            && _y - _my >= 3 && _y - _my <= 5
            && ISBLANK ( [Net Sales] ),
        [Net Sales LY]
    )
```

### Call List Last Visit
Format: `dd mmm yyyy`

```dax
IF ( NOT ISBLANK ( [Call List Spend] ), CALCULATE ( MAX ( Fact_Sales[InvoiceDate] ), REMOVEFILTERS ( Dim_Date ) ) )
```

## Finance

### Overheads
Format: `#,0`

```dax
SUM ( Fact_Overhead[Actual] )
```

### Overhead Budget
Format: `#,0`

```dax
SUM ( Fact_Overhead[Budget] )
```

### Overheads vs Budget
Format: `+0.0%;-0.0%`

```dax
DIVIDE ( [Overheads], [Overhead Budget] ) - 1
```

### Operating Profit
Gross profit minus branch overheads.
Format: `#,0`

```dax
[Gross Profit] - [Overheads]
```

### Operating Margin
Format: `0.0%`

```dax
DIVIDE ( [Operating Profit], [Net Sales] )
```

### Branches Losing Money
Format: `0`

```dax
COUNTROWS ( FILTER ( VALUES ( Dim_Branch[Branch] ), [Operating Profit] < 0 ) )
```

## Last Year

### Gross Sales LY
Format: `#,0`

```dax
CALCULATE ( [Gross Sales], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Discounts LY
Format: `#,0`

```dax
CALCULATE ( [Discounts], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Net Sales LY
Format: `#,0`

```dax
CALCULATE ( [Net Sales], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Cost of Sales LY
Format: `#,0`

```dax
CALCULATE ( [Cost of Sales], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Gross Profit LY
Format: `#,0`

```dax
CALCULATE ( [Gross Profit], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Gross Margin LY
Format: `0.0%`

```dax
CALCULATE ( [Gross Margin], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Discount Rate LY
Format: `0.0%`

```dax
CALCULATE ( [Discount Rate], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Workshop Visits LY
Format: `#,0`

```dax
CALCULATE ( [Workshop Visits], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Average Workshop Invoice LY
Format: `#,0`

```dax
CALCULATE ( [Average Workshop Invoice], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Hours Sold LY
Format: `#,0`

```dax
CALCULATE ( [Hours Sold], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Operating Profit LY
Format: `#,0`

```dax
CALCULATE ( [Operating Profit], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Operating Margin LY
Format: `0.0%`

```dax
CALCULATE ( [Operating Margin], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

## Network

### Cars on Road
Cars the group sold that are still on the road.
Format: `#,0`

```dax
SUM ( Fact_CarsOnRoad[CarsOnRoad] )
```

### Owners Visited
Retail owners with at least one workshop visit in the period.
Format: `#,0`

```dax
CALCULATE ( DISTINCTCOUNT ( Fact_Sales[CustomerID] ), Fact_Sales[Channel] = "Workshop", Dim_Customer[CustomerType] = "Retail" )
```

### Penetration
Owners who visited ÷ our cars on the road.
Format: `0.0%`

```dax
DIVIDE ( [Owners Visited], [Cars on Road] )
```

### Lowest Region

```dax
MAXX ( TOPN ( 1, FILTER ( VALUES ( Dim_Governorate[Region] ), [Cars on Road] > 0 ), [Penetration], ASC ), Dim_Governorate[Region] )
```

### Lowest Region Penetration
Format: `0.0%`

```dax
VAR _r = [Lowest Region] RETURN CALCULATE ( [Penetration], Dim_Governorate[Region] = _r )
```

### Other Regions Penetration
Format: `0.0%`

```dax
VAR _r = [Lowest Region] RETURN CALCULATE ( [Penetration], KEEPFILTERS ( Dim_Governorate[Region] <> _r ) )
```

### Cars Without Branch
Our cars in governorates with no service branch.
Format: `#,0`

```dax
CALCULATE ( [Cars on Road], Dim_Governorate[Has Branch] = 0 )
```

### Governorates Without Branch

```dax
CONCATENATEX ( FILTER ( VALUES ( Dim_Governorate[Governorate] ), CALCULATE ( MAX ( Dim_Governorate[Has Branch] ) ) = 0 ), Dim_Governorate[Governorate], ", ", Dim_Governorate[Governorate], ASC )
```

## Receivables

### Receivables
Credit invoices issued and not yet paid at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d )
    )
```

### Receivables Not Due
Receivables by days past the due date at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d ),
        FILTER ( ALL ( Fact_Invoice[DueDate] ), _d - Fact_Invoice[DueDate] <= 0 )
    )
```

### Receivables 1-30 Days
Receivables by days past the due date at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d ),
        FILTER ( ALL ( Fact_Invoice[DueDate] ), _d - Fact_Invoice[DueDate] > 0 && _d - Fact_Invoice[DueDate] <= 30 )
    )
```

### Receivables 31-60 Days
Receivables by days past the due date at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d ),
        FILTER ( ALL ( Fact_Invoice[DueDate] ), _d - Fact_Invoice[DueDate] > 30 && _d - Fact_Invoice[DueDate] <= 60 )
    )
```

### Receivables 61-90 Days
Receivables by days past the due date at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d ),
        FILTER ( ALL ( Fact_Invoice[DueDate] ), _d - Fact_Invoice[DueDate] > 60 && _d - Fact_Invoice[DueDate] <= 90 )
    )
```

### Receivables Over 90 Days
Receivables by days past the due date at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d ),
        FILTER ( ALL ( Fact_Invoice[DueDate] ), _d - Fact_Invoice[DueDate] > 90 )
    )
```

### Receivables Overdue
Receivables by days past the due date at the end of the period.
Format: `#,0`

```dax
VAR _d = MAX ( Dim_Date[Date] )
RETURN
    CALCULATE (
        SUM ( Fact_Invoice[NetSales] ),
        REMOVEFILTERS ( Dim_Date ),
        Fact_Invoice[CreditTerms] > 0,
        Fact_Invoice[InvoiceDate] <= _d,
        FILTER ( ALL ( Fact_Invoice[PaidDate] ), ISBLANK ( Fact_Invoice[PaidDate] ) || Fact_Invoice[PaidDate] > _d ),
        FILTER ( ALL ( Fact_Invoice[DueDate] ), _d - Fact_Invoice[DueDate] > 0 )
    )
```

### Credit Sales
Format: `#,0`

```dax
CALCULATE ( SUM ( Fact_Invoice[NetSales] ), Fact_Invoice[CreditTerms] > 0 )
```

### Days Sales Outstanding
Receivables ÷ credit sales × days in the period.
Format: `0`

```dax
DIVIDE ( [Receivables], [Credit Sales] ) * COUNTROWS ( Dim_Date )
```

## Reps

### Role Median Discount
Format: `0.0%`

```dax
VAR _r = SELECTEDVALUE ( Dim_Rep[Role] ) RETURN MEDIANX ( FILTER ( ALL ( Dim_Rep ), Dim_Rep[Role] = _r && NOT ISBLANK ( [Net Sales] ) ), [Discount Rate] )
```

### Role Median Margin
Format: `0.0%`

```dax
VAR _r = SELECTEDVALUE ( Dim_Rep[Role] ) RETURN MEDIANX ( FILTER ( ALL ( Dim_Rep ), Dim_Rep[Role] = _r && NOT ISBLANK ( [Net Sales] ) ), [Gross Margin] )
```

### Role Median Achievement
Format: `0%`

```dax
VAR _r = SELECTEDVALUE ( Dim_Rep[Role] ) RETURN MEDIANX ( FILTER ( ALL ( Dim_Rep ), Dim_Rep[Role] = _r && NOT ISBLANK ( [Net Sales] ) ), [Rep Achievement] )
```

### Rep Growth
Format: `+0%;-0%`

```dax
DIVIDE ( [Net Sales], [Net Sales LY] ) - 1
```

## Workshop

### Hours Sold
Technician hours billed on labour and body & paint lines.
Format: `#,0`

```dax
SUM ( Fact_Sales[Hours] )
```

### Labour Sales per Hour
Labour net sales per hour sold, after discounts.
Format: `#,0`

```dax
DIVIDE ( CALCULATE ( [Net Sales], Dim_BusinessLine[Business Line] = "Labour" ), CALCULATE ( [Hours Sold], Dim_BusinessLine[Business Line] = "Labour" ) )
```

### Available Hours
Technicians × working days × 8 hours × 85%.
Format: `#,0`

```dax
SUM ( Fact_Capacity[AvailableHours] )
```

### Utilisation
Hours sold ÷ hours available. Above 95% the workshop turns work away.
Format: `0%`

```dax
DIVIDE ( [Hours Sold], [Available Hours] )
```
