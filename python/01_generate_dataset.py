import numpy as np
import pandas as pd
from config import CFG, RAW_DIR, RANDOM_SEED
from utils import logger

def generate_datasets() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    gen_cfg = CFG["data_generation"]
    n_cust, n_prod, n_camp, n_ord = gen_cfg["num_customers"], gen_cfg["num_products"], gen_cfg["num_campaigns"], gen_cfg["num_orders"]

    logger.info("Generating synthetic customers...")
    first_names = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "Sophia", "Lucas", "Mia", "Ethan", "Priya", "Arjun"]
    last_names = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Moore", "Patel", "Kim", "Garcia", "Davis"]
    countries = ["USA", "UK", "Canada", "Germany", "Australia"]
    channels = ["Organic Search", "Paid Social", "Email", "Referral", "Direct"]

    signup_dates = pd.to_datetime("2023-06-01") + pd.to_timedelta(rng.integers(0, 700, size=n_cust), unit="D")
    customers = pd.DataFrame({
        "customer_id": [f"CUST-{i:05d}" for i in range(1, n_cust + 1)],
        "first_name": rng.choice(first_names, size=n_cust),
        "last_name": rng.choice(last_names, size=n_cust),
        "email": [f"user{i}@example-shop.com" for i in range(1, n_cust + 1)],
        "gender": rng.choice(["Female", "Male", "Non-Binary"], size=n_cust, p=[0.50, 0.46, 0.04]),
        "age": rng.integers(18, 74, size=n_cust),
        "city": rng.choice(["New York", "London", "Toronto", "Berlin", "Sydney", "Chicago", "Austin"], size=n_cust),
        "state": rng.choice(["NY", "ON", "CA", "TX", "NSW", "BE", "LDN"], size=n_cust),
        "country": rng.choice(countries, size=n_cust, p=[0.52, 0.16, 0.14, 0.10, 0.08]),
        "acquisition_channel": rng.choice(channels, size=n_cust, p=[0.34, 0.26, 0.16, 0.12, 0.12]),
        "signup_date": signup_dates.strftime("%Y-%m-%d"),
        "is_active": rng.choice([True, False], size=n_cust, p=[0.91, 0.09]),
    })

    customers.loc[rng.choice(n_cust, 35, replace=False), "gender"] = None
    customers.loc[rng.choice(n_cust, 20, replace=False), "acquisition_channel"] = "  Organic Search "
    customers_raw = pd.concat([customers, customers.sample(15, random_state=RANDOM_SEED)], ignore_index=True)
    customers_raw.to_csv(RAW_DIR / "customers_raw.csv", index=False)

    logger.info("Generating synthetic products...")
    catalog = {
        "Electronics": [("Wireless Headphones", 38, 119), ("4K Monitor", 145, 349), ("Smartwatch", 65, 199), ("Bluetooth Speaker", 22, 69)],
        "Apparel": [("Merino Wool Sweater", 24, 79), ("Running Jacket", 28, 95), ("Denim Jeans", 19, 68), ("Performance Tee", 9, 34)],
        "Home & Kitchen": [("Espresso Machine", 85, 249), ("Cast Iron Skillet", 16, 54), ("Air Purifier", 52, 159), ("Chef Knife", 21, 74)],
        "Beauty": [("Vitamin C Serum", 7, 38), ("Hydrating Cleanser", 5, 26), ("Retinol Night Cream", 9, 48)],
        "Sports": [("Yoga Mat Pro", 14, 58), ("Adjustable Dumbbells", 78, 219), ("Resistance Bands", 6, 28)],
    }
    prod_rows = []
    for i in range(1, n_prod + 1):
        cat = rng.choice(list(catalog.keys()), p=[0.28, 0.25, 0.20, 0.15, 0.12])
        subcat, base_cost, base_price = catalog[cat][rng.integers(0, len(catalog[cat]))]
        cost = round(base_cost * rng.uniform(0.9, 1.15), 2)
        price = round(base_price * rng.uniform(0.95, 1.2), 2)
        prod_rows.append({
            "product_id": f"PROD-{i:03d}",
            "product_name": f"{subcat} Series {rng.integers(100, 999)}",
            "category": cat,
            "subcategory": subcat,
            "brand": rng.choice(["NovaTech", "AuraLiving", "PeakGear", "Veloce", "Lumina"]),
            "unit_cost": cost,
            "unit_price": max(price, round(cost * 1.25, 2)),
            "stock_quantity": int(rng.integers(15, 600)),
            "rating": round(rng.uniform(3.4, 4.95), 2),
        })
    products_raw = pd.DataFrame(prod_rows)
    products_raw.to_csv(RAW_DIR / "products_raw.csv", index=False)

    logger.info("Generating synthetic marketing campaigns...")
    camp_channels = ["Google Ads", "Meta Ads", "Email", "Influencer", "Affiliate"]
    camp_rows = []
    for i in range(1, n_camp + 1):
        ch = camp_channels[(i - 1) % len(camp_channels)]
        budget = round(rng.uniform(4500, 38000), 2)
        impressions = int(budget * rng.uniform(45, 120))
        clicks = int(impressions * rng.uniform(0.015, 0.045))
        conversions = int(clicks * rng.uniform(0.03, 0.09))
        camp_rows.append({
            "campaign_id": f"CAMP-{i:02d}",
            "campaign_name": f"{ch} Q{((i - 1) % 4) + 1} Growth Push {2024 + (i // 7)}",
            "channel": ch,
            "budget": budget,
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "start_date": "2024-01-01",
            "end_date": "2025-12-31",
        })
    pd.DataFrame(camp_rows).to_csv(RAW_DIR / "campaigns_raw.csv", index=False)

    logger.info("Generating synthetic orders & order_items...")
    cust_weights = rng.pareto(a=2.2, size=n_cust)
    cust_weights /= cust_weights.sum()
    chosen_custs = rng.choice(customers["customer_id"], size=n_ord, p=cust_weights)

    start_ts = pd.Timestamp(gen_cfg["start_date"]).value // 10**9
    end_ts = pd.Timestamp(gen_cfg["end_date"]).value // 10**9
    order_dates = pd.to_datetime(rng.integers(start_ts, end_ts, size=n_ord), unit="s").sort_values()

    camp_choices = [None] + [f"CAMP-{i:02d}" for i in range(1, n_camp + 1)]
    camp_probs = [0.40] + [0.60 / n_camp] * n_camp

    orders_list, items_list = [], []
    item_counter = 1
    prod_lookup = products_raw.set_index("product_id").to_dict("index")
    prod_ids = list(prod_lookup.keys())

    for idx in range(1, n_ord + 1):
        oid = f"ORD-{idx:06d}"
        cid = chosen_custs[idx - 1]
        odate = order_dates[idx - 1]
        status = rng.choice(["Completed", "Returned", "Cancelled", "Processing"], p=[0.84, 0.08, 0.05, 0.03])
        device = rng.choice(["Mobile", "Desktop", "Tablet"], p=[0.58, 0.35, 0.07])
        n_items = rng.choice([1, 2, 3, 4], p=[0.52, 0.30, 0.13, 0.05])
        selected_prods = rng.choice(prod_ids, size=n_items, replace=False)

        order_gross, order_discount = 0.0, 0.0
        for pid in selected_prods:
            pinfo = prod_lookup[pid]
            qty = int(rng.choice([1, 2, 3], p=[0.78, 0.17, 0.05]))
            disc_pct = float(rng.choice([0.0, 5.0, 10.0, 15.0, 20.0, 25.0], p=[0.55, 0.12, 0.15, 0.08, 0.06, 0.04]))
            if device == "Desktop" and rng.random() < 0.25:
                qty += 1
            u_price, u_cost = pinfo["unit_price"], pinfo["unit_cost"]
            gross = qty * u_price
            disc_val = round(gross * (disc_pct / 100.0), 2)
            line_total = round(gross - disc_val, 2)
            line_margin = round(line_total - (qty * u_cost), 2)
            order_gross += gross
            order_discount += disc_val
            items_list.append({
                "order_item_id": f"ITEM-{item_counter:06d}", "order_id": oid, "product_id": pid,
                "quantity": qty, "unit_price": u_price, "unit_cost": u_cost,
                "discount_pct": disc_pct, "line_total": line_total, "line_margin": line_margin,
            })
            item_counter += 1

        shipping = 0.0 if (order_gross - order_discount) >= 100 else round(float(rng.choice([5.99, 8.99, 12.50])), 2)
        total_amt = round(order_gross - order_discount + shipping, 2)
        orders_list.append({
            "order_id": oid, "customer_id": cid, "campaign_id": rng.choice(camp_choices, p=camp_probs),
            "order_date": odate.strftime("%Y-%m-%d %H:%M:%S"), "order_status": status,
            "payment_method": rng.choice(["Credit Card", "PayPal", "Apple Pay", "Debit Card", "BNPL"], p=[0.44, 0.24, 0.16, 0.10, 0.06]),
            "device_type": device, "shipping_cost": shipping, "discount_amount": round(order_discount, 2), "total_amount": total_amt,
        })

    orders_raw = pd.DataFrame(orders_list)
    orders_raw.loc[rng.choice(len(orders_raw), 25, replace=False), "payment_method"] = None
    orders_raw.to_csv(RAW_DIR / "orders_raw.csv", index=False)
    pd.DataFrame(items_list).to_csv(RAW_DIR / "order_items_raw.csv", index=False)
    logger.info("Synthetic datasets generated successfully.")

if __name__ == "__main__":
    generate_datasets()
