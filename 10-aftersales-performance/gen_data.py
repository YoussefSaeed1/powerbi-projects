"""Sample aftersales data for a fictional multi-brand car distributor in Egypt (Nilestar Auto Group), 2023-2024,
valued at 31 Dec 2024. Seeded and reproducible. Built-in patterns: 2024 prices rise after the currency move
while workshop visits fall; owners leave the network when the 3-year warranty ends; Upper Egypt has many
cars on the road but one branch; some reps reach target through discounts; government and insurance pay late."""
import os, numpy as np, pandas as pd
rng = np.random.default_rng(2024)
ASOF = pd.Timestamp("2024-12-31")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aftersales_Sample.xlsx")

# ---------------- branches ----------------
B = pd.DataFrame([
 # id, branch, city, governorate, region, lat, lon, type, bays, techs
 (1, "Nasr City", "Cairo", "Cairo", "Greater Cairo", 30.06, 31.34, "3S centre", 16, 11),
 (2, "Maadi", "Cairo", "Cairo", "Greater Cairo", 29.96, 31.26, "Service centre", 10, 7),
 (3, "New Cairo", "Cairo", "Cairo", "Greater Cairo", 30.03, 31.47, "3S centre", 12, 8),
 (4, "6th of October", "Giza", "Giza", "Greater Cairo", 29.97, 30.93, "3S centre", 14, 10),
 (5, "Mohandessin", "Giza", "Giza", "Greater Cairo", 30.05, 31.20, "Parts outlet", 2, 0),
 (6, "Smouha", "Alexandria", "Alexandria", "Alexandria", 31.21, 29.95, "3S centre", 13, 9),
 (7, "Borg El Arab", "Alexandria", "Alexandria", "Alexandria", 30.92, 29.54, "Service centre", 8, 6),
 (8, "Tanta", "Tanta", "Gharbia", "Delta", 30.79, 31.00, "Service centre", 7, 5),
 (9, "Mansoura", "Mansoura", "Dakahlia", "Delta", 31.04, 31.38, "Service centre", 7, 5),
 (10, "Zagazig", "Zagazig", "Sharqia", "Delta", 30.59, 31.50, "Service centre", 6, 4),
 (11, "Ismailia", "Ismailia", "Ismailia", "Canal", 30.60, 32.27, "Service centre", 6, 4),
 (12, "Port Said", "Port Said", "Port Said", "Canal", 31.26, 32.30, "Parts outlet", 2, 0),
 (13, "Assiut", "Assiut", "Assiut", "Upper Egypt", 27.18, 31.18, "Service centre", 5, 3),
], columns=["BranchID","Branch","City","Governorate","Region","Lat","Lon","BranchType","Bays","Technicians"])
B["BranchManagerEmail"] = ["%s.manager@nilestar.example" % b.lower().replace(" ", "").replace("6thof", "") for b in B.Branch]

BRANDS = {"Kia": .22, "Nissan": .19, "MG": .17, "Peugeot": .13, "Suzuki": .12, "Renault": .10, "Jetour": .07}
# cars on the road sold by the group, by governorate and brand (end of 2024)
GOV_PARC = {"Cairo": 11600, "Giza": 6200, "Alexandria": 5400, "Gharbia": 1900, "Dakahlia": 2100, "Sharqia": 1560,
            "Ismailia": 960, "Port Said": 840, "Assiut": 1840, "Sohag": 1220, "Minya": 1380, "Qena": 780}
# where owners from each governorate go for service (branch weights); Upper Egypt owners mostly go elsewhere
GOV_BRANCH = {"Cairo": {1: .42, 2: .24, 3: .34}, "Giza": {4: .78, 5: .22}, "Alexandria": {6: .72, 7: .28},
              "Gharbia": {8: 1}, "Dakahlia": {9: 1}, "Sharqia": {10: .85, 1: .15}, "Ismailia": {11: 1}, "Port Said": {11: .55, 12: .45},
              "Assiut": {13: 1}, "Sohag": {13: 1}, "Minya": {13: .6, 4: .4}, "Qena": {13: 1}}
GOV_REACH = {"Cairo": 1, "Giza": 1, "Alexandria": 1, "Gharbia": 1, "Dakahlia": 1, "Sharqia": .9, "Ismailia": .95, "Port Said": .8,
             "Assiut": .62, "Sohag": .30, "Minya": .34, "Qena": .22}   # distance to the nearest branch lowers visits
GOV_REGION = {"Cairo": "Greater Cairo", "Giza": "Greater Cairo", "Alexandria": "Alexandria", "Gharbia": "Delta", "Dakahlia": "Delta",
              "Sharqia": "Delta", "Ismailia": "Canal", "Port Said": "Canal", "Assiut": "Upper Egypt", "Sohag": "Upper Egypt",
              "Minya": "Upper Egypt", "Qena": "Upper Egypt"}

def pick(d, n): k = list(d); p = np.array(list(d.values()), float); return rng.choice(k, size=n, p=p / p.sum())

# ---------------- reps ----------------
reps, rid = [], 1
first = ["Ahmed","Mohamed","Mahmoud","Omar","Youssef","Karim","Mostafa","Hassan","Tarek","Amr","Sherif","Hany","Nour","Mariam",
         "Salma","Ali","Islam","Khaled","Walid","Ramy","Ehab","Sameh","Basma","Hossam","Ayman","Reem","Adel","Nada","Ziad","Fady",
         "Yasmin","Mina","Bassem","Dina","Hesham","Sara"]
last = ["Fathy","Saber","Nabil","Gamal","Ragab","Zaki","Shawky","Lotfy","Fouad","Hamdy","Mansour","Hegazy","Ashour","Farouk",
        "Kamel","Sobhy","Morsy","Tawfik","Hafez","Ibrahim","Galal","Rashad","Salem","Eid","Helmy","Badr","Wahba","Osman","Taha",
        "Fahmy","Selim","Naguib","Amer","Shaker","Rizk","Darwish"]
for _, b in B.iterrows():
    roles = ["Service Advisor"] * (0 if b.BranchType == "Parts outlet" else (3 if b.Bays >= 20 else 2)) + ["Parts Sales"] * (2 if b.BranchType == "Parts outlet" else 1)
    for r in roles:
        reps.append(dict(RepID=rid, Rep=f"{first[(rid*5) % 36]} {last[(rid*13 + rid // 36) % 36]}", Role=r, BranchID=b.BranchID)); rid += 1
for b in (1, 6, 4, 9):   # key-account reps for fleet and trade customers
    reps.append(dict(RepID=rid, Rep=f"{first[(rid*5) % 36]} {last[(rid*13 + rid // 36) % 36]}", Role="Key Account", BranchID=b)); rid += 1
R = pd.DataFrame(reps)
R["HireDate"] = [pd.Timestamp(2016 + int(rng.integers(0, 8)), int(rng.integers(1, 13)), 1) for _ in range(len(R))]
# behaviour: a discount appetite and a skill factor per rep
R_DISC = dict(zip(R.RepID, np.clip(rng.normal(1, .25, len(R)), .55, 1.6)))
R_SKILL = dict(zip(R.RepID, np.clip(rng.normal(1, .12, len(R)), .78, 1.25)))
heavy = R[R.Role != "Key Account"].sample(4, random_state=7).RepID.tolist()   # reps who buy volume with discounts
for h in heavy: R_DISC[h] = 2.6; R_SKILL[h] = 1.06

# ---------------- customers ----------------
cust = []
cid = 100001
n_retail = 23000
govs = pick({g: GOV_PARC[g] for g in GOV_PARC}, n_retail)
for g in govs:
    my = int(rng.choice(np.arange(2014, 2025), p=np.array([3,4,5,6,7,8,9,10,11,12,13], float) / 88))
    cust.append(dict(CustomerID=cid, CustomerType="Retail", Governorate=g, VehicleBrand=pick(BRANDS, 1)[0],
                     ModelYear=my, PurchaseDate=pd.Timestamp(my, int(rng.integers(1, 13)), int(rng.integers(1, 28)))))
    cid += 1
B2B = [("Fleet", 140), ("Trade", 230), ("Insurance", 8), ("Government", 14)]
ins_names = ["Nile Assurance", "Pyramid General", "Delta Insurance", "Cairo Mutual", "Horus Takaful", "Sinai General", "Lotus Insurance", "Red Sea Re"]
for t, n in B2B:
    for i in range(n):
        g = pick({k: v for k, v in GOV_PARC.items() if GOV_REACH[k] > .5 or t == "Trade"}, 1)[0]
        cust.append(dict(CustomerID=cid, CustomerType=t, Governorate=g, VehicleBrand=None, ModelYear=None, PurchaseDate=pd.NaT,
                         CustomerName=(ins_names[i] if t == "Insurance" else None)))
        cid += 1
C = pd.DataFrame(cust)
C["Region"] = C.Governorate.map(GOV_REGION)
C["CustomerName"] = C.CustomerName.fillna(C.CustomerType + " customer " + C.CustomerID.astype(str))
C.loc[C.CustomerType == "Retail", "CustomerName"] = "Retail " + C.CustomerID.astype(str)
TERMS = {"Retail": 0, "Fleet": 60, "Trade": 30, "Insurance": 60, "Government": 90}
C["CreditTerms"] = C.CustomerType.map(TERMS)

# ---------------- price & volume drivers ----------------
months = pd.date_range("2023-01-01", "2024-12-01", freq="MS")
def price_idx(d):   # parts follow the exchange rate from March 2024
    if d.year == 2023: return 1.0 + 0.012 * (d.month - 1)
    return 1.14 + (0.30 if d.month >= 3 else 0.02) + 0.006 * (d.month - 3 if d.month >= 3 else 0)
def lab_rate(d): return 650 if d.year == 2023 else (700 if d.month < 4 else 880)
SEAS = {1: .92, 2: .90, 3: .97, 4: 1.0, 5: 1.02, 6: 1.06, 7: 1.12, 8: 1.10, 9: 1.0, 10: .99, 11: .97, 12: .95}
LINE_GP = {"Labour": .66, "Parts": .24, "Oil & Lubricants": .31, "Accessories": .37, "Body & Paint": .41}

rep_by_branch = {b: R[(R.BranchID == b)] for b in B.BranchID}
def rep_for(branch, kind):
    df = rep_by_branch[branch]
    if kind == "workshop":
        d = df[df.Role == "Service Advisor"]
        if len(d) == 0: d = df
    else:
        d = df[df.Role == "Parts Sales"]
        if len(d) == 0: d = df
    return int(rng.choice(d.RepID.values))
KA = R[R.Role == "Key Account"].RepID.values

hdr, lines = [], []
inv = 1
def add_inv(date, branch, cust_id, ctype, channel, rep, brand, items):
    global inv
    iid = "INV-%d-%06d" % (date.year, inv); inv += 1
    terms = TERMS[ctype] if channel not in ("Workshop", "Parts Counter", "Online") or ctype != "Retail" else 0
    if ctype == "Retail": terms = 0
    hdr.append(dict(InvoiceID=iid, InvoiceDate=date, BranchID=branch, CustomerID=cust_id, RepID=rep, Channel=channel,
                    VehicleBrand=brand, CreditTerms=terms))
    for line, gross, hours in items:
        lines.append((iid, line, gross, hours, rep, ctype, channel))

retail = C[C.CustomerType == "Retail"].reset_index(drop=True)
for _, c in retail.iterrows():
    reach = GOV_REACH[c.Governorate]
    for yr in (2023, 2024):
        age = yr - c.ModelYear
        if age < 0: continue
        start = max(pd.Timestamp(yr, 1, 1), c.PurchaseDate)
        if start > pd.Timestamp(yr, 12, 31): continue
        frac = (pd.Timestamp(yr, 12, 31) - start).days / 365
        rate = (2.2 if age <= 2 else (1.05 if age == 3 else .45 if age <= 6 else .28)) * reach * frac
        rate *= .80 if yr == 2024 else 1.0     # fewer visits once prices jump
        n = rng.poisson(rate)
        for _ in range(n):
            d = start + pd.Timedelta(days=int(rng.integers(0, max(1, (pd.Timestamp(yr, 12, 31) - start).days))))
            if rng.random() > SEAS[d.month] / 1.12: d = d + pd.Timedelta(days=int(rng.integers(-40, 40)))
            d = min(max(d, pd.Timestamp(yr, 1, 1)), pd.Timestamp(yr, 12, 31))
            br = int(pick(GOV_BRANCH[c.Governorate], 1)[0])
            if B.loc[B.BranchID == br, "BranchType"].iloc[0] == "Parts outlet":
                br = {5: 4, 12: 11}[br]
            pi, lr = price_idx(d), lab_rate(d)
            hrs = round(float(rng.gamma(2.4, 1.15) * (1 + .12 * min(age, 8))), 1)
            parts = float(rng.gamma(1.8, 2300) * (1 + .18 * min(age, 8)) * pi)
            items = [("Labour", hrs * lr, hrs), ("Parts", parts, 0.0)]
            if rng.random() < .62: items.append(("Oil & Lubricants", float(rng.gamma(4, 330) * pi), 0.0))
            if rng.random() < .09: items.append(("Accessories", float(rng.gamma(2, 1400) * pi), 0.0))
            if rng.random() < .07:
                bh = round(float(rng.gamma(2, 3.5)), 1); items.append(("Body & Paint", bh * lr * 1.1 + float(rng.gamma(2, 2600) * pi), bh))
            add_inv(d, br, c.CustomerID, "Retail", "Workshop", rep_for(br, "workshop"), c.VehicleBrand, items)
        # parts counter purchases by owners out of warranty
        if age >= 3 and rng.random() < .22 * reach:
            d = pd.Timestamp(yr, 1, 1) + pd.Timedelta(days=int(rng.integers(0, 365)))
            br = int(pick(GOV_BRANCH[c.Governorate], 1)[0])
            add_inv(d, br, c.CustomerID, "Retail", "Parts Counter" if rng.random() > (.06 if yr == 2023 else .16) else "Online",
                    rep_for(br, "parts"), c.VehicleBrand, [("Parts", float(rng.gamma(1.6, 1900) * price_idx(d)), 0.0)])

b2b = C[C.CustomerType != "Retail"]
for _, c in b2b.iterrows():
    home = [k for k, v in GOV_BRANCH.get(c.Governorate, {13: 1}).items()]
    br0 = int(home[0])
    size = rng.lognormal(0, .7)
    for m in months:
        if c.CustomerType == "Fleet":
            n = rng.poisson(1.6 * size * (1.08 if m.year == 2024 else 1))
            for _ in range(n):
                d = m + pd.Timedelta(days=int(rng.integers(0, 28))); pi, lr = price_idx(d), lab_rate(d) * .92
                hrs = round(float(rng.gamma(2.5, 1.1)), 1)
                items = [("Labour", hrs * lr, hrs), ("Parts", float(rng.gamma(2, 2600) * pi), 0.0), ("Oil & Lubricants", float(rng.gamma(4, 360) * pi), 0.0)]
                add_inv(d, br0, c.CustomerID, "Fleet", "Fleet", int(rng.choice(KA)) if rng.random() < .55 else rep_for(br0, "workshop"), pick(BRANDS, 1)[0], items)
        elif c.CustomerType == "Trade":
            n = rng.poisson(1.3 * size * (1.12 if m.year == 2024 else 1))
            for _ in range(n):
                d = m + pd.Timedelta(days=int(rng.integers(0, 28)))
                items = [("Parts", float(rng.gamma(2, 7500) * price_idx(d)), 0.0)]
                if rng.random() < .45: items.append(("Oil & Lubricants", float(rng.gamma(3, 3800) * price_idx(d)), 0.0))
                if rng.random() < .15: items.append(("Accessories", float(rng.gamma(2, 3500) * price_idx(d)), 0.0))
                brr = br0 if rng.random() < .6 else int(rng.choice([5, 12, 1, 6]))
                add_inv(d, brr, c.CustomerID, "Trade", "Wholesale", int(rng.choice(KA)) if rng.random() < .5 else rep_for(brr, "parts"), pick(BRANDS, 1)[0], items)
        elif c.CustomerType == "Insurance":
            n = rng.poisson(26 * (1 if c.CustomerName != "Nile Assurance" else 1.8))
            for _ in range(n):
                d = m + pd.Timedelta(days=int(rng.integers(0, 28))); pi, lr = price_idx(d), lab_rate(d)
                brr = int(rng.choice(B[B.BranchType != "Parts outlet"].BranchID, p=None))
                bh = round(float(rng.gamma(2.4, 4)), 1)
                items = [("Body & Paint", bh * lr * 1.1 + float(rng.gamma(2, 3800) * pi), bh), ("Parts", float(rng.gamma(2, 3600) * pi), 0.0)]
                add_inv(d, brr, c.CustomerID, "Insurance", "Insurance", rep_for(brr, "workshop"), pick(BRANDS, 1)[0], items)
        else:  # government fleets
            n = rng.poisson(2.2 * size)
            for _ in range(n):
                d = m + pd.Timedelta(days=int(rng.integers(0, 28))); pi, lr = price_idx(d), lab_rate(d) * .9
                hrs = round(float(rng.gamma(3, 1.2)), 1)
                items = [("Labour", hrs * lr, hrs), ("Parts", float(rng.gamma(2.2, 3200) * pi), 0.0)]
                add_inv(d, br0, c.CustomerID, "Government", "Fleet", int(rng.choice(KA)), pick(BRANDS, 1)[0], items)

H = pd.DataFrame(hdr)
L = pd.DataFrame(lines, columns=["InvoiceID", "BusinessLine", "Gross", "Hours", "RepID", "CType", "Channel"])
# discounts: by channel, rep appetite, and heavier in 2024 H2 to hold volume
Hd = H.set_index("InvoiceID")
yr = Hd.loc[L.InvoiceID, "InvoiceDate"].dt.year.values
mo = Hd.loc[L.InvoiceID, "InvoiceDate"].dt.month.values
base = L.Channel.map({"Workshop": .045, "Parts Counter": .03, "Online": .02, "Wholesale": .085, "Fleet": .07, "Insurance": .05}).values
base = base * np.where((yr == 2024) & (mo >= 6), 1.35, 1.0) * L.RepID.map(R_DISC).values
disc_rate = np.clip(rng.normal(base, base * .35), 0, .32)
L["Discount"] = (L.Gross * disc_rate).round(2)
L["Gross"] = L.Gross.round(2)
L["NetSales"] = (L.Gross - L.Discount).round(2)
gp = L.BusinessLine.map(LINE_GP).values
L["COGS"] = (L.Gross * (1 - gp) * rng.normal(1, .04, len(L))).round(2)
L.loc[L.BusinessLine == "Labour", "COGS"] = (L.loc[L.BusinessLine == "Labour", "Hours"] * np.where(yr[L.BusinessLine == "Labour"] == 2024, 235, 175)).round(2)
L["LineID"] = np.arange(1, len(L) + 1)
L = L[["LineID", "InvoiceID", "BusinessLine", "Hours", "Gross", "Discount", "NetSales", "COGS"]]

# ---------------- receivables: payment dates for credit invoices ----------------
tot = L.groupby("InvoiceID").NetSales.sum()
H["NetSales"] = H.InvoiceID.map(tot).round(2)
H["DueDate"] = H.InvoiceDate + pd.to_timedelta(H.CreditTerms, unit="D")
ct = H.CustomerID.map(C.set_index("CustomerID").CustomerType)
late = ct.map({"Retail": 0, "Fleet": 14, "Trade": 9, "Insurance": 58, "Government": 120}).values
late = late * np.where(H.InvoiceDate.dt.year == 2024, 1.35, 1.0)
delay = np.where(H.CreditTerms > 0, rng.gamma(1.6, np.maximum(late, 1) / 1.6), 0)
pdays = H.CreditTerms.values * rng.uniform(.6, 1.0, len(H)) + delay
H["PaidDate"] = H.InvoiceDate + pd.to_timedelta(np.round(pdays), unit="D")
H.loc[H.PaidDate > ASOF, "PaidDate"] = pd.NaT
H = H.drop(columns=["NetSales"])

# ---------------- targets (set in Dec 2023 for 2024: 2023 x expected inflation) ----------------
HL = L.merge(H[["InvoiceID", "InvoiceDate", "BranchID", "RepID"]], on="InvoiceID")
HL["Month"] = HL.InvoiceDate.values.astype("datetime64[M]")
a23 = HL[HL.InvoiceDate.dt.year == 2023].groupby(["BranchID", "BusinessLine", HL.InvoiceDate.dt.month]).agg(NS=("NetSales", "sum"), C=("COGS", "sum")).reset_index()
a23.columns = ["BranchID", "BusinessLine", "M", "NS", "C"]
tg = []
for y in (2023, 2024):
    f = 1.0 if y == 2023 else 1.42
    for r in a23.itertuples():
        noise = rng.normal(1, .04) if y == 2024 else rng.normal(1.03, .05)
        ts = r.NS * f * noise
        tg.append(dict(Month=pd.Timestamp(y, r.M, 1), BranchID=r.BranchID, BusinessLine=r.BusinessLine,
                       TargetSales=round(ts, 0), TargetGP=round(ts * (1 - r.C / max(r.NS, 1)) * (1.02 if y == 2024 else 1), 0)))
T = pd.DataFrame(tg)
# rep targets: share of branch target by 2023 share
rs = HL[HL.InvoiceDate.dt.year == 2023].groupby(["BranchID", "RepID"]).NetSales.sum()
rs = (rs / rs.groupby(level=0).transform("sum")).reset_index().rename(columns={"NetSales": "Share"})
bt = T.groupby(["Month", "BranchID"]).TargetSales.sum().reset_index()
RT = bt.merge(rs, on="BranchID")
RT["TargetSales"] = (RT.TargetSales * RT.Share * rng.normal(1, .03, len(RT))).round(0)
RT = RT[["Month", "RepID", "TargetSales"]]
# key-account reps sell across branches: give them a target from their own 2023 sales
ka23 = HL[(HL.InvoiceDate.dt.year == 2023) & HL.RepID.isin(KA)].groupby(["RepID", HL.InvoiceDate.dt.month]).NetSales.sum().reset_index()
ka23.columns = ["RepID", "M", "NS"]
kat = [dict(Month=pd.Timestamp(y, r.M, 1), RepID=r.RepID, TargetSales=round(r.NS * (1.0 if y == 2023 else 1.40) * rng.normal(1.02, .03), 0)) for y in (2023, 2024) for r in ka23.itertuples()]
RT = pd.concat([RT[~RT.RepID.isin(KA)], pd.DataFrame(kat)]).groupby(["Month", "RepID"], as_index=False).TargetSales.sum()

# ---------------- overhead: actual and budget ----------------
oh = []
for _, b in B.iterrows():
    size = (b.Technicians + 2) / 9
    for m in months:
        y24 = m.year == 2024
        for cat, base_amt, infl, over in [("Salaries", .32e6, 1.32, 1.07), ("Rent", .11e6, 1.18, 1.0), ("Utilities", .04e6, 1.45, 1.12),
                                          ("Marketing", .025e6, 1.2, .9), ("Admin & IT", .055e6, 1.25, 1.03)]:
            bud = base_amt * size * (infl if y24 else 1) * (1 + .01 * (m.month - 1) * (1 if y24 else .5))
            act = bud * (over if y24 else 1.0) * rng.normal(1, .05)
            if cat == "Rent" and b.BranchType == "Parts outlet": bud, act = bud * .5, act * .5
            oh.append(dict(Month=m, BranchID=b.BranchID, Category=cat, Budget=round(bud, 0), Actual=round(act, 0)))
O = pd.DataFrame(oh)

# ---------------- workshop capacity ----------------
cap = []
for _, b in B.iterrows():
    if b.Technicians == 0: continue
    for m in months:
        days = 26
        cap.append(dict(Month=m, BranchID=b.BranchID, AvailableHours=round(b.Technicians * days * 8 * .85, 0)))
CAP = pd.DataFrame(cap)

# ---------------- cars on the road ----------------
P = []
for g, n in GOV_PARC.items():
    for br, s in BRANDS.items():
        P.append(dict(Governorate=g, Region=GOV_REGION[g], VehicleBrand=br, CarsOnRoad=int(n * s * rng.normal(1, .06))))
P = pd.DataFrame(P)

# ---------------- write ----------------
C_out = C[["CustomerID", "CustomerName", "CustomerType", "Governorate", "Region", "VehicleBrand", "ModelYear", "PurchaseDate", "CreditTerms"]]
if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with pd.ExcelWriter(OUT, engine="openpyxl") as xw:
        H.to_excel(xw, sheet_name="Invoices", index=False)
        L.to_excel(xw, sheet_name="InvoiceLines", index=False)
        C_out.to_excel(xw, sheet_name="Customers", index=False)
        B.to_excel(xw, sheet_name="Branches", index=False)
        R.to_excel(xw, sheet_name="Reps", index=False)
        T.to_excel(xw, sheet_name="BranchTargets", index=False)
        RT.to_excel(xw, sheet_name="RepTargets", index=False)
        O.to_excel(xw, sheet_name="Overhead", index=False)
        CAP.to_excel(xw, sheet_name="Capacity", index=False)
        P.to_excel(xw, sheet_name="CarsOnRoad", index=False)
    print(OUT, len(H), len(L), len(C_out))
