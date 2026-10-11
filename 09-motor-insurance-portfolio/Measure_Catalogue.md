# Motor Insurance Portfolio · measure catalogue

Every measure in the model, grouped by display folder. Generated from the model definition.

## Helpers

### Last Refresh

```dax
"Data refreshed " & FORMAT ( MAX ( _Refresh[RefreshedAt] ), "dd mmm yyyy" )
```

### Valuation Date
Figures are valued at this date: the last day of the calendar.
Format: `dd mmm yyyy`

```dax
CALCULATE ( MAX ( Dim_Date[Date] ), REMOVEFILTERS () )
```

## Data Quality

### DQ Value

```dax
VAR _o = SELECTEDVALUE ( Dim_DQ[Check Order] )
RETURN
    SWITCH (
        _o,
        1, FORMAT ( MAX ( DQ_Source[PolicyRows] ), "#,0" ),
        2, FORMAT ( MAX ( DQ_Source[ClaimRows] ), "#,0" ),
        3, FORMAT ( MAX ( DQ_Source[DuplicateClaims] ), "#,0" ),
        4, FORMAT ( MAX ( DQ_Source[OutsideCover] ), "#,0" ),
        5, FORMAT ( MAX ( DQ_Source[MessyRegion] ), "#,0" ),
        6, FORMAT ( MAX ( DQ_Source[MissingBirthYear] ), "#,0" ),
        7, FORMAT ( MAX ( DQ_Source[UnknownPolicy] ), "#,0" ),
        8, FORMAT ( MAX ( DQ_Source[NegativePaid] ), "#,0" ),
        9, FORMAT ( MAX ( DQ_Source[UnknownRenewal] ), "#,0" ),
        10, FORMAT ( CALCULATE ( MAX ( Fact_Claims[LossDate] ), REMOVEFILTERS () ), "dd mmm yyyy" )
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
        _o IN { 1, 2, 10 }, "Info",
        _v = "0", "Pass",
        _o IN { 3, 4, 5, 6 }, "Handled",
        "Fail"
    )
```

## Insights

### Best Channel

```dax
MAXX ( TOPN ( 1, ALL ( Fact_Policy[Channel] ), [Loss Ratio], ASC ), Fact_Policy[Channel] )
```

### Worst Channel

```dax
MAXX ( TOPN ( 1, ALL ( Fact_Policy[Channel] ), [Loss Ratio], DESC ), Fact_Policy[Channel] )
```

### Best Channel LR
Format: `0.0%`

```dax
VAR _c = [Best Channel] RETURN CALCULATE ( [Loss Ratio], Fact_Policy[Channel] = _c )
```

### Worst Channel LR
Format: `0.0%`

```dax
VAR _c = [Worst Channel] RETURN CALCULATE ( [Loss Ratio], Fact_Policy[Channel] = _c )
```

### Best Channel Renewal
Format: `0.0%`

```dax
VAR _c = [Best Channel] RETURN CALCULATE ( [Renewal Rate], Fact_Policy[Channel] = _c )
```

### Theft Claim Share
Format: `0%`

```dax
DIVIDE ( CALCULATE ( [Claims Reported], Fact_Claims[ClaimType] = "Theft" ), [Claims Reported] )
```

### Theft Cost Share
Format: `0%`

```dax
DIVIDE ( CALCULATE ( [Claims Incurred], Fact_Claims[ClaimType] = "Theft" ), [Claims Incurred] )
```

### Insight Overview

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Claims

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Pricing

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Insight Retention

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### DQ Summary

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## KPI Cards

### KPI Overview

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Claims

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Pricing

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### KPI Retention

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Channel Bars
Written premium by channel, coloured by whether the channel's loss ratio is above target.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Claim Type Bars
Incurred cost by claim type; coral when a type's share of cost is at least three times its share of claims.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Region Table
Claim frequency, average cost and loss ratio by region.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

### Pricing Heatmap
Loss ratio by driver age band and vehicle type; coral above the target loss ratio, teal below.

_Returns HTML for the HTML Content visual. Full DAX is in the model._

## Formatting

### Loss Ratio Color

```dax
IF ( [Loss Ratio] > [Target Loss Ratio], "#E76F51", "#2A9D8F" )
```

### Rate Change Color

```dax
IF ( [Rate Change Needed] > 0, "#E76F51", "#2A9D8F" )
```

### Renewal Color

```dax
VAR _all = CALCULATE ( [Renewal Rate], REMOVEFILTERS ( Fact_Policy[Age Band] ), REMOVEFILTERS ( Fact_Policy[Claim History] ) )
RETURN
    IF ( [Renewal Rate] < _all - 0.05, "#E76F51", "#14213D" )
```

### DQ Status Pill

```dax
VAR _t = [DQ Status]
VAR _bg = SWITCH ( _t, "Pass", "#2A9D8F", "Info", "#A8B0BD", "Handled", "#F4A261", "#E76F51" )
VAR _svg =
    "<svg xmlns='http://www.w3.org/2000/svg' width='66' height='20' viewBox='0 0 66 20'>"
        & "<rect x='1' y='2' width='64' height='16' rx='8' fill='" & _bg & "'/>"
        & "<text x='33' y='14' text-anchor='middle' font-family='Segoe UI,sans-serif' font-size='10' font-weight='600' fill='#FFFFFF'>" & _t & "</text></svg>"
RETURN
    IF ( NOT ISBLANK ( _t ),
        "data:image/svg+xml;utf8," & SUBSTITUTE ( SUBSTITUTE ( _svg, "%", "%25" ), "#", "%23" ) )
```

## Assumptions

### Admin Expense Ratio
Assumed admin cost as a share of premium. The sample data has no expense ledger.
Format: `0%`

```dax
0.14
```

### Profit Margin Target
Profit margin the price should leave after claims and expenses.
Format: `0%`

```dax
0.05
```

## Claims

### Claims Reported
Claims by loss date, inside the policy period.
Format: `#,0`

```dax
0 + COUNTROWS ( Fact_Claims )
```

### Claims Paid
Format: `#,0`

```dax
SUM ( Fact_Claims[Paid] )
```

### Reserves
Amount still expected to be paid on open claims.
Format: `#,0`

```dax
SUM ( Fact_Claims[Reserve] )
```

### Claims Incurred
Paid plus reserves.
Format: `#,0`

```dax
SUM ( Fact_Claims[Incurred] )
```

### Open Claims
Format: `#,0`

```dax
CALCULATE ( 0 + COUNTROWS ( Fact_Claims ), Fact_Claims[Status] = "Open" )
```

### Average Claim Cost
Format: `#,0`

```dax
DIVIDE ( [Claims Incurred], [Claims Reported] )
```

### Claim Frequency
Claims per vehicle-year.
Format: `0.0%`

```dax
DIVIDE ( [Claims Reported], [Exposure] )
```

## Last Year

### Gross Written Premium LY
Format: `#,0`

```dax
CALCULATE ( [Gross Written Premium], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Earned Premium LY
Format: `#,0`

```dax
CALCULATE ( [Earned Premium], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Claims Incurred LY
Format: `#,0`

```dax
CALCULATE ( [Claims Incurred], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Loss Ratio LY
Format: `0.0%`

```dax
CALCULATE ( [Loss Ratio], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Combined Ratio LY
Format: `0.0%`

```dax
CALCULATE ( [Combined Ratio], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Policies Written LY
Format: `#,0`

```dax
CALCULATE ( [Policies Written], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Claims Reported LY
Format: `#,0`

```dax
CALCULATE ( [Claims Reported], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Claim Frequency LY
Format: `0.0%`

```dax
CALCULATE ( [Claim Frequency], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Average Claim Cost LY
Format: `#,0`

```dax
CALCULATE ( [Average Claim Cost], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Average Premium LY
Format: `#,0`

```dax
CALCULATE ( [Average Premium], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

### Renewal Rate LY
Format: `0.0%`

```dax
CALCULATE ( [Renewal Rate], SAMEPERIODLASTYEAR ( Dim_Date[Date] ) )
```

## Premium

### Gross Written Premium
Premium of policies that start in the period.
Format: `#,0`

```dax
CALCULATE ( SUM ( Fact_Policy[GrossPremium] ), USERELATIONSHIP ( Fact_Policy[StartDate], Dim_Date[Date] ) )
```

### Policies Written
Format: `#,0`

```dax
CALCULATE ( COUNTROWS ( Fact_Policy ), USERELATIONSHIP ( Fact_Policy[StartDate], Dim_Date[Date] ) )
```

### Average Premium
Format: `#,0`

```dax
DIVIDE ( [Gross Written Premium], [Policies Written] )
```

### Commission
Format: `#,0`

```dax
CALCULATE ( SUM ( Fact_Policy[Commission] ), USERELATIONSHIP ( Fact_Policy[StartDate], Dim_Date[Date] ) )
```

### Commission Ratio
Format: `0.0%`

```dax
DIVIDE ( [Commission], [Gross Written Premium] )
```

### Expense Ratio
Commission ratio plus the admin cost assumption.
Format: `0.0%`

```dax
[Commission Ratio] + [Admin Expense Ratio]
```

### Earned Premium
Each policy's premium spread over the days it covers inside the period.
Format: `#,0`

```dax
VAR _s = MIN ( Dim_Date[Date] )
VAR _e = MAX ( Dim_Date[Date] )
RETURN
    SUMX (
        Fact_Policy,
        VAR _days = INT ( MIN ( Fact_Policy[EndDate], _e ) - MAX ( Fact_Policy[StartDate], _s ) ) + 1
        RETURN IF ( _days > 0, Fact_Policy[GrossPremium] * _days / Fact_Policy[TermDays] )
    )
```

### Exposure
Vehicle-years insured in the period.
Format: `#,0`

```dax
VAR _s = MIN ( Dim_Date[Date] )
VAR _e = MAX ( Dim_Date[Date] )
RETURN
    SUMX (
        Fact_Policy,
        VAR _days = INT ( MIN ( Fact_Policy[EndDate], _e ) - MAX ( Fact_Policy[StartDate], _s ) ) + 1
        RETURN IF ( _days > 0, _days / 365.25 )
    )
```

## Pricing

### Segments Above Target

```dax
VAR _cells =
    FILTER (
        CROSSJOIN ( VALUES ( Fact_Policy[Age Band] ), VALUES ( Fact_Policy[Vehicle Type] ) ),
        Fact_Policy[Age Band] <> "Unknown" && NOT ISBLANK ( [Loss Ratio] )
    )
RETURN
    COUNTROWS ( FILTER ( _cells, [Loss Ratio] > [Target Loss Ratio] ) ) & " of " & COUNTROWS ( _cells )
```

### Worst Age Band

```dax
VAR _t = TOPN ( 1, FILTER ( ALL ( Fact_Policy[Age Band] ), Fact_Policy[Age Band] <> "Unknown" ), [Loss Ratio], DESC )
RETURN
    MAXX ( _t, Fact_Policy[Age Band] )
```

### Worst Age Band LR
Format: `0.0%`

```dax
VAR _b = [Worst Age Band] RETURN CALCULATE ( [Loss Ratio], Fact_Policy[Age Band] = _b )
```

### Worst Age Band Change
Format: `+0%;-0%`

```dax
VAR _b = [Worst Age Band] RETURN CALCULATE ( [Rate Change Needed], Fact_Policy[Age Band] = _b )
```

### Worst Vehicle

```dax
VAR _t = TOPN ( 1, ALL ( Fact_Policy[Vehicle Type] ), [Loss Ratio], DESC )
RETURN
    MAXX ( _t, Fact_Policy[Vehicle Type] )
```

### Worst Vehicle LR
Format: `0.0%`

```dax
VAR _v = [Worst Vehicle] RETURN CALCULATE ( [Loss Ratio], Fact_Policy[Vehicle Type] = _v )
```

## Ratios

### Loss Ratio
Claims incurred ÷ earned premium.
Format: `0.0%`

```dax
DIVIDE ( [Claims Incurred], [Earned Premium] )
```

### Combined Ratio
Below 100% the book makes an underwriting profit.
Format: `0.0%`

```dax
[Loss Ratio] + [Expense Ratio]
```

### Target Loss Ratio
The highest loss ratio that still leaves the target margin after expenses.
Format: `0.0%`

```dax
1 - [Expense Ratio] - [Profit Margin Target]
```

### Target Loss Ratio (Year)
Target loss ratio for the whole year, used as a flat line on monthly charts.
Format: `0.0%`

```dax
CALCULATE ( [Target Loss Ratio], REMOVEFILTERS ( Dim_Date[Month], Dim_Date[MonthNo], Dim_Date[Year-Month], Dim_Date[YearMonthKey] ) )
```

### Rate Change Needed
Price change that would bring the loss ratio to the target.
Format: `+0%;-0%;0%`

```dax
IF ( NOT ISBLANK ( [Loss Ratio] ), DIVIDE ( [Loss Ratio], [Target Loss Ratio] ) - 1 )
```

### Underwriting Result
Format: `#,0`

```dax
[Earned Premium] - [Claims Incurred] - [Earned Premium] * [Expense Ratio]
```

### Waterfall Value
EGP millions for the premium-to-result waterfall.
Format: `#,0.0`

```dax
VAR _o = SELECTEDVALUE ( Dim_Step[Step Order] )
VAR _ep = [Earned Premium]
RETURN
    DIVIDE (
        SWITCH ( _o, 1, _ep, 2, - [Claims Incurred], 3, - _ep * [Commission Ratio], 4, - _ep * [Admin Expense Ratio] ),
        1000000
    )
```

## Retention

### Policies Due
Policies that expired in the period.
Format: `#,0`

```dax
CALCULATE ( COUNTROWS ( Fact_Policy ), USERELATIONSHIP ( Fact_Policy[EndDate], Dim_Date[Date] ) )
```

### Policies Renewed
Format: `#,0`

```dax
CALCULATE ( 0 + SUM ( Fact_Policy[Renewed] ), USERELATIONSHIP ( Fact_Policy[EndDate], Dim_Date[Date] ) )
```

### Policies Lost
Format: `#,0`

```dax
[Policies Due] - [Policies Renewed]
```

### Renewal Rate
Expired policies replaced by a new policy for the same customer.
Format: `0.0%`

```dax
DIVIDE ( [Policies Renewed], [Policies Due] )
```

### Premium Lost
Last premium of the customers who did not renew.
Format: `#,0`

```dax
CALCULATE ( SUM ( Fact_Policy[GrossPremium] ), USERELATIONSHIP ( Fact_Policy[EndDate], Dim_Date[Date] ), Fact_Policy[Renewed] = 0 )
```

### Renewal Rate After Claim
Format: `0.0%`

```dax
CALCULATE ( [Renewal Rate], Fact_Policy[Claim History] = "Had a claim" )
```

### Renewal Rate No Claim
Format: `0.0%`

```dax
CALCULATE ( [Renewal Rate], Fact_Policy[Claim History] = "No claim" )
```
