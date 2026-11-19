# Meta Product Catalog Feed — Field Reference

> Scope: all 33 columns currently present in `meta-product-feed.csv`.
>
> This document distinguishes fields documented by Meta from fields whose requirements depend on catalog type, category, or ingestion path. A field being recognized by a Product Item API does not automatically prove that the same spelling and behavior are accepted by every CSV feed workflow. Validate the final feed in Commerce Manager.

## 1. Current feed schema

The repository's current CSV has 33 columns:

```csv
id,title,description,rich_text_description,availability,condition,price,link,image_link,additional_image_link,brand,gtin,mpn,google_product_category,fb_product_category,product_type,sale_price,sale_price_effective_date,item_group_id,color,size,material,pattern,gender,age_group,inventory,quantity_to_sell_on_facebook,status,custom_label_0,custom_label_1,custom_label_2,custom_label_3,custom_label_4
```

## 2. Requirement levels

| Level | Meaning |
|---|---|
| Required | Required for the standard ecommerce product catalog use cases described by Meta. |
| Conditional | Required only for particular checkout, catalog, or product-category scenarios. |
| Optional | Documented field that can enrich the product record but is not universally required. |
| Verify | Present in this repository's schema or a related Meta API model, but confirm CSV-feed acceptance and behavior for the specific catalog before relying on it. |

For standard ecommerce products, Meta's published feed guidance lists `id`, `title`, `description`, `availability`, `condition`, `price`, `link`, `image_link`, and at least one of `brand`, `mpn`, or `gtin` as required. Requirements can vary by channel and checkout setup.

## 3. Field-by-field reference

### 3.1 Product identity and content

| Field | Level | Purpose and guidance |
|---|---|---|
| `id` | Required | Unique, case-sensitive item/content ID. Prefer a stable SKU. Do not reuse the same ID for multiple variants. For catalog ads, align it with the corresponding Pixel/Conversions API content ID. |
| `title` | Required | Product name. Use a specific, readable title; Meta's reference gives a 200-character maximum and recommends keeping it shorter to avoid truncation. |
| `description` | Required | Plain-text product description. Keep it distinct from the title; do not put HTML in this field. Retain it as the fallback even when `rich_text_description` is populated. |
| `rich_text_description` | Optional | HTML/rich-text product description, maximum 9,999 characters in the catalog feed reference. It is not supported in ads; the plain-text `description` remains required. See [HTML guidance](#4-rich_text_description-html-guidance). |

### 3.2 Availability, price, and destination

| Field | Level | Purpose and guidance |
|---|---|---|
| `availability` | Required | Current stock state. Common feed values include `in stock` and `out of stock`; use only values accepted for the catalog workflow. Keep synchronized with real inventory. |
| `condition` | Required | Product condition. Common values are `new`, `refurbished`, and `used`. |
| `price` | Required | Regular item price. Feed format: numeric amount, space, ISO 4217 currency code, e.g. `24999000 IDR`. Do not use currency symbols or localized thousands separators. |
| `link` | Required | Direct product page URL on the merchant's website, beginning with `https://` or `http://`. It should lead to the exact item/variant represented by the row. |
| `image_link` | Required | Main product image URL. Use an accessible product image that meets Meta's image specifications; the feed reference specifies JPEG/PNG and minimum image dimensions. |
| `additional_image_link` | Optional | Additional product image URLs. Up to 20 URLs and 2,000 characters in the feed reference. Supported separators include comma, semicolon, space, and vertical bar (`|`). Quote the complete CSV cell when it contains a list. All image URLs should meet the same image requirements as the main image. |
| `sale_price` | Optional | Promotional price, formatted like `price`. It should be lower than the regular price. |
| `sale_price_effective_date` | Optional | Start/end period for the sale, with start and end separated by `/`. Use date-time values with timezone, for example `2026-11-27T00:00+07:00/2026-11-30T23:59+07:00`. |
| `status` | Optional | Catalog item state: `active` or `archived`. Active items can appear in connected channels; archived items are not shown. |

### 3.3 Brand and product identifiers

| Field | Level | Purpose and guidance |
|---|---|---|
| `brand` | Required alternative | Brand/manufacturer name. At least one of `brand`, `mpn`, or `gtin` must be provided for standard ecommerce product feeds. |
| `gtin` | Required alternative | Valid Global Trade Item Number, such as UPC, EAN, JAN, or ISBN where applicable. Do not invent or reuse a GTIN. |
| `mpn` | Required alternative | Manufacturer Part Number. Use the actual manufacturer-assigned identifier; do not substitute an internal SKU unless it is genuinely the MPN. |

### 3.4 Categorization and variants

| Field | Level | Purpose and guidance |
|---|---|---|
| `google_product_category` | Conditional / optional | Google product taxonomy category. Meta feed guidance identifies it as additionally required for certain checkout/channel configurations. Use a valid taxonomy value when applicable. |
| `fb_product_category` | Optional | Meta/Facebook product taxonomy category. Choose the most specific applicable category from Meta's taxonomy. |
| `product_type` | Optional | Merchant-defined category path, useful for internal product categorization. It is not a substitute for a required platform taxonomy field when one is required. |
| `item_group_id` | Optional | Shared identifier connecting variants of one parent product. Use the same value for all variants in a group, and keep it distinct from each variant's `id`. |
| `color` | Optional / category-dependent | Variant color. Use a concise, consistent value for each variant. |
| `size` | Conditional | Product size. Required for certain product categories in Shops, notably clothing and shoes; not generally required for a phone storage variant. |
| `material` | Optional / category-dependent | Material composition or finish, when relevant and accurate. |
| `pattern` | Optional / category-dependent | Product pattern, when applicable. |
| `gender` | Optional / category-dependent | Intended gender audience. Common values include `female`, `male`, and `unisex`; only populate when relevant to the product. |
| `age_group` | Optional / category-dependent | Intended age group. Common taxonomy values include `adult`, `all ages`, `infant`, `kids`, `newborn`, `teen`, and `toddler`; choose only when meaningful for the product. |

### 3.5 Inventory, checkout, and custom labels

| Field | Level | Purpose and guidance |
|---|---|---|
| `inventory` | Conditional | Inventory information required for some Facebook/Instagram checkout and Page Shop configurations. The exact expected representation depends on the catalog/checkout workflow. Do not leave it blank when the selected workflow requires it. |
| `quantity_to_sell_on_facebook` | Verify / workflow-dependent | Quantity offered for sale on Facebook in the Product Item model. Confirm that the chosen CSV feed ingestion path accepts this attribute and check its checkout-specific behavior before relying on it. |
| `custom_label_0` | Optional | Custom text label for organizing/filtering products or use in ad creative. Maximum 100 characters in the product field reference. |
| `custom_label_1` | Optional | Second custom text label; same purpose and constraints as `custom_label_0`. |
| `custom_label_2` | Optional | Third custom text label; same purpose and constraints as `custom_label_0`. |
| `custom_label_3` | Optional | Fourth custom text label; same purpose and constraints as `custom_label_0`. |
| `custom_label_4` | Optional | Fifth custom text label; same purpose and constraints as `custom_label_0`. |

Custom labels are five separate scalar fields, not a semicolon- or pipe-separated list. Example values such as `flash_sale`, `discount`, or `black_friday` are merchant-defined classifications; they do not independently create or activate a Meta promotion.

## 4. `rich_text_description` HTML guidance

Meta's feed reference lists these supported HTML tags:

- Structure/content: `<form>`, `<fieldset>`, `<div>`, `<span>`, `<section>`, `<header>`
- Headings: `<h1>` through `<h6>`
- Tables: `<table>`, `<tbody>`, `<tfoot>`, `<thead>`, `<td>`, `<th>`, `<tr>`
- Lists: `<ul>`, `<li>`, `<ol>`, `<dl>`, `<dd>`, `<dt>`
- Formatting: `<b>`, `<u>`, `<i>`, `<em>`, `<strong>`, `<title>`, `<small>`, `<br>`, `<p>`, `<sub>`, `<sup>`, `<pre>`, `<q>`, `<s>`

Meta may strip HTML attributes such as inline styling. Do not assume that arbitrary HTML, CSS, JavaScript, embeds, or interactive elements are supported. Keep markup semantic and simple, and validate the rendered result in the target Shop.

Recommended product-description subset:

```html
<html>
  <h2>Product Name</h2>
  <p>Short product description.</p>

  <h3>Product Details</h3>
  <ul>
    <li><strong>Brand:</strong> Example Brand</li>
    <li><strong>Model:</strong> Example Model</li>
    <li><strong>Color:</strong> Black</li>
  </ul>

  <h3>Features</h3>
  <ul>
    <li>Feature one</li>
    <li>Feature two</li>
  </ul>

  <h3>Specifications</h3>
  <table>
    <tbody>
      <tr><th>Storage</th><td>256GB</td></tr>
      <tr><th>Condition</th><td>New</td></tr>
    </tbody>
  </table>
</html>
```

The tag list above is a documented allow-list reference, not a guarantee that every combination renders identically in every placement. Rich text is not used for catalog ads.

## 5. CSV formatting rules

1. The first row contains exact field names in US English.
2. Each following row represents one catalog item/variant.
3. Use commas as the CSV column delimiter.
4. Quote a field with double quotes when it contains commas, line breaks, or quote characters.
5. Escape a quote inside a quoted CSV value by doubling it: `""`.
6. For `additional_image_link`, separators inside the value may be comma, semicolon, space, or pipe. The complete value must remain one quoted CSV cell when necessary.
7. For `sale_price_effective_date`, separate the start and end timestamps with `/`; this is not a list separator.
8. Keep currency values in the format `amount ISO_CURRENCY`, for example `24999000 IDR`.
9. Keep identifiers stable and unique. Each variant gets its own `id`; variants share `item_group_id`.
10. Do not insert HTML into `description`; reserve HTML for `rich_text_description`.

## 6. Validation checklist

- [ ] All required fields are populated for the intended catalog channel.
- [ ] At least one of `brand`, `gtin`, or `mpn` is present and genuine.
- [ ] Every `id` is unique and stable.
- [ ] Variant rows share the correct `item_group_id`.
- [ ] `price` and `sale_price` use valid currency formatting.
- [ ] `sale_price` is lower than `price` and its effective dates are valid.
- [ ] Product and image URLs are publicly accessible and point to the correct variant.
- [ ] Additional image URLs are correctly quoted and within documented limits.
- [ ] `availability` and inventory data reflect actual stock.
- [ ] Category fields match the product and intended catalog.
- [ ] Custom labels contain one value each and are not treated as promotions.
- [ ] CSV parses to the same number of columns on every row.
- [ ] The feed is uploaded/tested in Commerce Manager and item diagnostics are reviewed.

## 7. Important status of this repository's sample data

The current `meta-product-feed.csv` is a demonstration file. It contains placeholder `example.com` links, sample prices/quantities, and fictional iPhone 18 Pro Max variant examples. Do not use it as a production feed until real product specifications, GTIN/MPN values, product URLs, image URLs, prices, stock, and sale dates have been supplied and validated.

## 8. References

- Meta Business Help Center — [Data Feed Specifications for Catalogs](https://www.facebook.com/business/help/120325381656392)
- Meta Developers — [Product Item reference](https://developers.facebook.com/docs/marketing-api/reference/product-item/)
- Meta Developers — [Marketplace Partner Item API](https://developers.facebook.com/docs/marketplace/partnerships/itemAPI/)
- Meta Developers — [Feed API Reference](https://developers.facebook.com/documentation/ads-commerce/catalog/guides/feed-api)

**Documentation note:** Meta changes catalog fields and requirements over time. Re-check the current official specification and the requirements shown for the target catalog/channel before treating this document as a production contract.
