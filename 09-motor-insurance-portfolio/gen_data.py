"""Sample motor insurance portfolio (fictional insurer), 2023-2025, valued at 31 Dec 2025.
Seeded and reproducible. Built-in patterns: young drivers and SUVs are priced below their risk,
repair costs rise in 2025, online policies renew less. A few deliberate data issues for the DQ page."""
import numpy as np, pandas as pd
rng = np.random.default_rng(2025)
ASOF = pd.Timestamp("2025-12-31")

REGIONS = {"Cairo": .38, "Giza": .18, "Alexandria": .15, "Delta": .14, "Canal": .07, "Upper Egypt": .08}
REG_RISK = {"Cairo": 1.18, "Giza": 1.10, "Alexandria": .95, "Delta": .88, "Canal": .85, "Upper Egypt": .82}
VEH = {"Sedan": .46, "Hatchback": .22, "SUV": .20, "Pickup": .07, "Van": .05}
VEH_SI = {"Sedan": 850e3, "Hatchback": 600e3, "SUV": 1.6e6, "Pickup": 900e3, "Van": 1.0e6}
VEH_RATE = {"Sedan": .030, "Hatchback": .031, "SUV": .027, "Pickup": .034, "Van": .033}     # premium % of sum insured
VEH_RISK = {"Sedan": 1.0, "Hatchback": 1.0, "SUV": 1.30, "Pickup": 1.12, "Van": 1.10}     # true claim cost relativity
AGES = {"18-25": .09, "26-35": .27, "36-50": .38, "51-65": .20, "65+": .06}
AGE_PRICE = {"18-25": 1.25, "26-35": 1.05, "36-50": 1.0, "51-65": .97, "65+": 1.08}
AGE_RISK = {"18-25": 1.95, "26-35": 1.12, "36-50": .92, "51-65": .85, "65+": 1.15}
CH = {2023: {"Agent": .47, "Broker": .26, "Bank": .18, "Online": .09},
      2024: {"Agent": .45, "Broker": .25, "Bank": .18, "Online": .12},
      2025: {"Agent": .41, "Broker": .24, "Bank": .17, "Online": .18}}
COMM = {"Agent": .12, "Broker": .15, "Bank": .18, "Online": .03}
PROD = {"Comprehensive": .78, "Third-party": .22}

def pick(d, n): return rng.choice(list(d), size=n, p=np.array(list(d.values())) / sum(d.values()))

pols, cust_next = [], 100001
def new_policies(year, n):
    global cust_next
    rows = []
    for i in range(n):
        start = pd.Timestamp(year, 1, 1) + pd.Timedelta(days=int(rng.integers(0, 365)))
        rows.append(dict(CustomerID=cust_next, Start=start, Region=pick(REGIONS, 1)[0], Vehicle=pick(VEH, 1)[0],
                         AgeBand=pick(AGES, 1)[0], Product=pick(PROD, 1)[0], Channel=pick(CH[year], 1)[0],
                         VehicleYear=int(year - rng.integers(0, 12)), PrevPolicy=None))
        cust_next += 1
    return rows

N_NEW = {2023: 11500, 2024: 5600, 2025: 6400}
book = {2023: new_policies(2023, N_NEW[2023])}
pid = 1
def finalize(rows, year):
    global pid
    out = []
    for r in rows:
        r = dict(r); r["PolicyID"] = "MP-%d-%06d" % (year, pid); pid += 1
        r["End"] = r["Start"] + pd.DateOffset(years=1) - pd.Timedelta(days=1)
        si = VEH_SI[r["Vehicle"]] * rng.lognormal(0, .28) * (0.93 ** max(0, year - r["VehicleYear"]) if r["Product"] == "Comprehensive" else 1)
        r["SumInsured"] = round(si, -3)
        base = r["SumInsured"] * VEH_RATE[r["Vehicle"]] if r["Product"] == "Comprehensive" else 1900 + 0.002 * r["SumInsured"]
        infl = {2023: 1.0, 2024: 1.06, 2025: 1.12}[year]
        r["GWP"] = round(base * AGE_PRICE[r["AgeBand"]] * infl * rng.lognormal(0, .06), 2)
        r["Commission"] = round(r["GWP"] * COMM[r["Channel"]], 2)
        out.append(r)
    return out

all_pols = finalize(book[2023], 2023)
claims = []
cid = 1
def sim_claims(p, year):
    global cid
    freq = (0.165 if p["Product"] == "Comprehensive" else 0.055) * AGE_RISK[p["AgeBand"]] * VEH_RISK[p["Vehicle"]] * REG_RISK[p["Region"]]
    n = rng.poisson(freq)
    out = []
    for _ in range(n):
        loss = p["Start"] + pd.Timedelta(days=int(rng.integers(0, 365)))
        if loss > ASOF: continue
        ctype = rng.choice(["Own damage", "Theft", "Third-party injury", "Third-party property", "Glass"],
                           p=[.62, .05 * (1.6 if p["Region"] in ("Cairo", "Giza") else .7) / 1.05, .07, .17, .09 - (.05 * (1.6 if p["Region"] in ("Cairo", "Giza") else .7) / 1.05 - .05)]) \
            if p["Product"] == "Comprehensive" else rng.choice(["Third-party injury", "Third-party property"], p=[.35, .65])
        sev_base = {"Own damage": 24000, "Theft": .30 * p["SumInsured"], "Third-party injury": 60000, "Third-party property": 18000, "Glass": 6500}[ctype]
        sev_infl = {2023: 1.0, 2024: 1.07, 2025: 1.25}[loss.year]
        cost = 1.75 * sev_base * sev_infl * rng.lognormal(-0.18, .6) * (VEH_RISK[p["Vehicle"]] ** .5 if ctype == "Own damage" else 1)
        report = loss + pd.Timedelta(days=int(rng.gamma(2, 6)))
        if report > ASOF: continue
        age_days = (ASOF - report).days
        if rng.random() < .06:
            status, paid, os_ = "Rejected", 0.0, 0.0
        elif age_days < 120 and rng.random() < .75 or age_days < 365 and rng.random() < .18:
            status = "Open"; paid = round(cost * rng.uniform(0, .5), 2); os_ = round(cost - paid, 2)
        else:
            status, paid, os_ = "Closed", round(cost, 2), 0.0
        out.append(dict(ClaimID="CL-%07d" % cid, PolicyID=p["PolicyID"], LossDate=loss, ReportDate=report, ClaimType=ctype,
                        Status=status, Paid=paid, Outstanding=os_))
        cid += 1
    return out

for year in (2023, 2024, 2025):
    yr_pols = [p for p in all_pols if p["Start"].year == year]
    for p in yr_pols:
        claims += sim_claims(p, year)
    if year == 2025: break
    had_claim = {c["PolicyID"] for c in claims}
    renew = []
    for p in yr_pols:
        pr = .74 * {"Agent": 1.04, "Broker": 1.0, "Bank": .98, "Online": .80}[p["Channel"]] * (.78 if p["PolicyID"] in had_claim else 1) * (.86 if p["AgeBand"] == "18-25" else 1)
        if rng.random() < pr:
            r = {k: p[k] for k in ("CustomerID", "Region", "Vehicle", "AgeBand", "Product", "Channel", "VehicleYear")}
            r["Start"] = p["End"] + pd.Timedelta(days=1); r["PrevPolicy"] = p["PolicyID"]
            if r["AgeBand"] == "18-25" and rng.random() < .25: r["AgeBand"] = "26-35"
            renew.append(r)
    nxt = finalize(renew + new_policies(year + 1, N_NEW[year + 1]), year + 1)
    all_pols += nxt

P = pd.DataFrame(all_pols)
C = pd.DataFrame(claims)
# driver birth year instead of band (band is derived in Power Query)
band_lo = {"18-25": 18, "26-35": 26, "36-50": 36, "51-65": 51, "65+": 66}
band_hi = {"18-25": 25, "26-35": 35, "36-50": 50, "51-65": 65, "65+": 78}
P["DriverBirthYear"] = [s.year - int(rng.integers(band_lo[b], band_hi[b] + 1)) for s, b in zip(P.Start, P.AgeBand)]
# ---- deliberate data issues (handled in the model, shown on the DQ page)
miss = rng.choice(len(P), 45, replace=False); P.loc[miss, "DriverBirthYear"] = np.nan
P["Region"] = P["Region"].astype(object)
messy = rng.choice(len(P), 120, replace=False); P.loc[messy, "Region"] = P.loc[messy, "Region"].str.upper() + " "
dup = C.sample(18, random_state=7); C = pd.concat([C, dup]).sort_values("ClaimID").reset_index(drop=True)
idx = C.sample(9, random_state=11).index
pmap = P.set_index("PolicyID")
for i in idx:
    C.at[i, "LossDate"] = pmap.loc[C.at[i, "PolicyID"], "End"] + pd.Timedelta(days=int(rng.integers(5, 40)))
    if C.at[i, "LossDate"] > ASOF: C.at[i, "LossDate"] = ASOF - pd.Timedelta(days=3)
    C.at[i, "ReportDate"] = max(C.at[i, "ReportDate"], C.at[i, "LossDate"])

pol_out = P[["PolicyID", "CustomerID", "PrevPolicy", "Start", "End", "Product", "Channel", "Region", "Vehicle", "VehicleYear",
             "DriverBirthYear", "SumInsured", "GWP", "Commission"]].rename(columns={"Start": "StartDate", "End": "EndDate", "PrevPolicy": "RenewalOf",
                                                                                  "Vehicle": "VehicleType", "GWP": "GrossPremium"})
clm_out = C[["ClaimID", "PolicyID", "LossDate", "ReportDate", "ClaimType", "Status", "Paid", "Outstanding"]].rename(columns={"Outstanding": "Reserve"})
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Motor_Insurance_Sample.xlsx")
with pd.ExcelWriter(out, engine="openpyxl") as w:
    pol_out.to_excel(w, sheet_name="Policies", index=False)
    clm_out.to_excel(w, sheet_name="Claims", index=False)
print(len(pol_out), "policies,", len(clm_out), "claim rows ->", out)
