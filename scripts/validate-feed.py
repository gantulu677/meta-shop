#!/usr/bin/env python3
"""Validate the Meta Product Catalog CSV using only Python's standard library."""
import argparse
import csv
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HEADERS = """id,title,description,rich_text_description,availability,condition,price,link,image_link,additional_image_link,brand,gtin,mpn,google_product_category,fb_product_category,product_type,sale_price,sale_price_effective_date,item_group_id,color,size,material,pattern,gender,age_group,inventory,quantity_to_sell_on_facebook,status,custom_label_0,custom_label_1,custom_label_2,custom_label_3,custom_label_4""".split(",")
REQUIRED = ("id", "title", "description", "availability", "condition", "price", "link", "image_link", "brand")
LIMITS = {"id":100,"title":200,"description":9999,"rich_text_description":9999,"item_group_id":100,"color":200,"size":200,"material":200,"pattern":100,"product_type":750, **{f"custom_label_{i}":100 for i in range(5)}}
TAGS = {"form","fieldset","div","span","section","header",*(f"h{i}" for i in range(1,7)),"table","tbody","tfoot","thead","td","th","tr","ul","li","ol","dl","dd","dt","b","u","i","em","strong","title","small","br","p","sub","sup","pre","q","s"}
PRICE = re.compile(r"^(\d+(?:\.\d{1,2})?) ([A-Z]{3})$")
SPLIT_IMAGES = re.compile(r"[|,;\s]+")

class TagCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() not in TAGS: self.bad.append(tag)
    def handle_endtag(self, tag):
        if tag.lower() not in TAGS: self.bad.append(tag)

class Validator:
    def __init__(self, production=False):
        self.production, self.errors, self.warnings = production, [], []
    def error(self, row, message): self.errors.append(f"row {row}: {message}")
    def warn(self, row, message): self.warnings.append(f"row {row}: {message}")
    @staticmethod
    def parse_price(value):
        match = PRICE.fullmatch(value.strip())
        return (float(match.group(1)), match.group(2)) if match else None
    @staticmethod
    def url_ok(value):
        parsed = urlparse(value.strip())
        return parsed.scheme in {"http","https"} and bool(parsed.netloc)
    def run(self, path):
        try:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                if reader.fieldnames != HEADERS:
                    self.error(1, "header tidak sama persis dengan schema 33 kolom (nama/urutan)")
                    return False
                rows = list(reader)
        except (OSError, UnicodeError, csv.Error) as exc:
            self.error("file", f"gagal membaca CSV: {exc}")
            return False
        if not rows:
            self.error("file", "tidak ada baris produk")
            return False
        ids = set()
        for n, row in enumerate(rows, 2):
            if None in row or any(v is None for v in row.values()):
                self.error(n, "jumlah kolom tidak sama dengan header")
                continue
            for field in REQUIRED:
                if not row[field].strip(): self.error(n, f"required field {field} kosong")
            if row["id"] in ids: self.error(n, f"duplicate id {row['id']}")
            ids.add(row["id"])
            for field, limit in LIMITS.items():
                if len(row[field]) > limit: self.error(n, f"{field} melebihi {limit} karakter")
            if row["availability"].lower() not in {"in stock","out of stock"}: self.error(n, "availability tidak valid")
            if row["condition"].lower() not in {"new","refurbished","used"}: self.error(n, "condition tidak valid")
            if row["status"].strip() and row["status"].lower() not in {"active","archived"}: self.error(n, "status tidak valid")
            price = self.parse_price(row["price"])
            sale = self.parse_price(row["sale_price"]) if row["sale_price"].strip() else None
            if price is None: self.error(n, "price harus 'amount ISO_CURRENCY'")
            if row["sale_price"].strip() and sale is None: self.error(n, "sale_price harus 'amount ISO_CURRENCY'")
            if price and sale:
                if price[1] != sale[1]: self.error(n, "currency sale_price dan price berbeda")
                if sale[0] >= price[0]: self.error(n, "sale_price harus lebih rendah dari price")
            effective = row["sale_price_effective_date"].strip()
            if effective:
                parts = effective.split("/")
                try:
                    if len(parts) != 2: raise ValueError()
                    start, end = [datetime.fromisoformat(x) for x in parts]
                    if start.tzinfo is None or end.tzinfo is None or start >= end: raise ValueError()
                except ValueError: self.error(n, "sale_price_effective_date harus ISO 8601 start/end dengan timezone")
            for field in ("link","image_link"):
                if row[field].strip() and not self.url_ok(row[field]): self.error(n, f"{field} bukan URL HTTP(S) valid")
            additional = row["additional_image_link"].strip()
            if additional:
                images = [x for x in SPLIT_IMAGES.split(additional) if x]
                if len(additional) > 2000: self.error(n, "additional_image_link > 2.000 karakter")
                if len(images) > 20: self.error(n, "additional_image_link > 20 URL")
                for image in images:
                    if not self.url_ok(image): self.error(n, f"additional image URL tidak valid: {image}")
            if row["inventory"].strip(): self.error(n, "inventory legacy wajib kosong; gunakan quantity_to_sell_on_facebook")
            qty = row["quantity_to_sell_on_facebook"].strip()
            if qty and not qty.isdigit(): self.error(n, "quantity_to_sell_on_facebook harus integer non-negatif")
            elif qty and int(qty) == 0 and row["availability"].lower() == "in stock": self.error(n, "quantity 0 tidak konsisten dengan in stock")
            elif qty and int(qty) > 0 and row["availability"].lower() == "out of stock": self.error(n, "quantity positif tidak konsisten dengan out of stock")
            rich = row["rich_text_description"]
            if rich:
                checker = TagCheck(); checker.feed(rich); checker.close()
                if checker.bad: self.error(n, "HTML tag tidak didukung: " + ", ".join(sorted(set(checker.bad))))
                if re.search(r"<\s*(html|body)\b", rich, re.I): self.error(n, "rich text harus fragmen tanpa html/body wrapper")
                if re.search(r"Condition:\s*in stock", rich, re.I): self.error(n, "condition tidak boleh bernilai in stock")
            if "<" in row["description"] or ">" in row["description"]: self.error(n, "description harus plain text")
            urls = row["link"] + row["image_link"] + row["additional_image_link"]
            placeholder = "example.com" in urls.lower()
            sample = "(sample)" in row["title"].lower() or "data dummy" in row["description"].lower()
            if placeholder:
                (self.error if self.production else self.warn)(n, "menggunakan URL placeholder example.com")
            if self.production and sample: self.error(n, "sample/demo marker tidak diizinkan pada production")
        return not self.errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=ROOT / "meta-product-feed.csv")
    parser.add_argument("--production", action="store_true", help="tolak placeholder dan penanda sample")
    args = parser.parse_args()
    check = Validator(args.production)
    valid = check.run(args.csv)
    for item in check.warnings: print("WARNING:", item)
    for item in check.errors: print("ERROR:", item)
    if valid:
        print(f"PASS: {args.csv} valid ({'production' if args.production else 'demo/schema'} mode)")
        if check.warnings: print(f"Warnings: {len(check.warnings)}")
        return 0
    print(f"FAIL: {len(check.errors)} error(s), {len(check.warnings)} warning(s)")
    return 1

if __name__ == "__main__":
    sys.exit(main())
