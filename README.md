# 3DS-dB
An open-source metadata & media database for Nintendo 3DS.

Per Title ID: eShop-style `meta.json` (name, region, product code, genres, …) plus media assets (`icon`, `banner`, `top_image`, screenshots / thumbnails). Not a ROM archive — metadata and artwork only.

Also ships `data/title_catalog.json`: games grouped across regions, with linked updates / DLC / demos.

________

Structure :
```
db/3ds/
├── base/                           # Retail / eShop games (regional releases)
│     └── [tid]/
├── digital-demos/                  # Downloadable demos
│     └── [tid]/
├── kiosk-demos/                    # Kiosk / demo-station builds
│     └── [tid]/
├── region-free/                    # Region-free titles
│     └── [tid]/
├── unknown-other/                  # Unsorted / unknown region
│     └── [tid]/
├── dlc/                            # Downloadable content
│     └── [tid]/
├── dsiware/                        # DSiWare games and applications
│     └── [tid]/
├── extras/                         # Extra / non-retail content
│   ├── custom-dsiware/             # Custom DSiWare (not on 3DS eShop)
│   │     └── [tid]/
│   ├── devapps-misc/               # Dev Apps / Miscellaneous (prototypes, tools…)
│   │     └── [tid]/
│   ├── hb/                         # Homebrew
│   │     └── [tid]/
│   ├── rom-hacks/                  # ROM hacks / undubs / modified games
│   │     └── [tid]/
│   └── translated-games/           # Fan translations
│         └── [tid]/
├── updates/                        # System or game updates
│     └── [tid]/
├── videos/                         # eShop video content (E3 clips, trailers, Nintendo Video)
│     └── [tid]/
└── virtual-console/                # Virtual Console games
      └── [tid]/
```

Themes are omitted for now: theme installer packs often share one TID / product code, so they do not map 1:1 to eShop title folders.

eShop media sizes (Nintendo originals only):
- `icon.jpg` = 48×48
- `banner.jpg` = 400×168
- `top_image.jpg` ≈ 400×240 (sometimes larger trailer stills)


```
[tid]/
├── banner.jpg                # Banner image for the content
├── icon.jpg                  # Icon image for the content
├── top_image.jpg             # Main display image
├── meta.json                 # Metadata file (e.g., title, description, etc.)
├── screenshots/              # Folder for compiled screenshots
│   └── screenshot_[n].jpg      # Screenshot file (variable number)
├── thumbnails/               # Folder for thumbnails of screenshots
│   └── thumbnail_[n].jpg       # Thumbnail file (variable number)
└── screenshots_uncompiled/   # Folder for uncompiled screenshots
    ├── screenshot_[n]_lower.jpg # Lower screen of screenshot (variable number)
    ├── screenshot_[n]_upper.jpg # Upper screen of screenshot (variable number)
```

___

Metadata:   
db/3ds/:category/:tid/meta.json
```json
{
    "tid": "",
    "uid": "",
    "name": "",
    "formal_name": "",
    "description": "",
    "release_date_on_eshop": "",
    "product_code": "",
    "platform_name": "",
    "region": "",
    "genres": [],
    "features": [],
    "languages": [],
    "rating_system": {
        "name": "",
        "age": ""
    },
    "version": "",
    "disclaimer": null,
    "descriptors": []
}
```

`release_date_on_eshop` is the release date the region's Nintendo eShop lists for the title (Nintendo's own store data for that region).

`region` in `meta.json` = SKU / locale code (`JP`, `US`, `EU`, `FR`, `DE`, `GB`, …) or `FREE` (region-free / homebrew). `EU` is the generic PAL market; country-specific SKUs use `FR` / `DE` / … when applicable. Languages stay ISO-639 (`ja`, `en`).

Title catalog (`data/title_catalog.json`, via `utils/build_title_catalog.py`):
- groups the same game by product-code serial (`CTR:AMK`)
- keys releases by **`meta.region`** (pick the SKU for the user: FR vs US vs JP)
- adds **`market`** from the product-code letter (console market: `JP`/`US`/`EU`/`KR`/`TW`/`CN`)
- sets **`region_conflict: true`** when those two disagree
- a TitleID does not encode region by itself

___

Iso code and more :
```
'AE': Arabic (ar)
'AG', 'AI', 'BM', 'BS', 'BZ', 'CA', 'DM', 'GD', 'GY', 'IE', 'JM', 'KN', 'KY', 'LC', 'MS', 'MT', 'NZ', 'SG', 'TC', 'TT', 'VC', 'VG', 'VI', 'ZA': English (en)
'AN', 'AW', 'NL', 'BE': Dutch (nl)
'AR', 'BO', 'CL', 'CO', 'CR', 'DO', 'EC', 'ES', 'GT', 'HN', 'MX', 'NI', 'PA', 'PE', 'PY', 'SV', 'UY', 'VE': Spanish (es)
'AT', 'CH', 'DE': German (de)
'AU', 'GB', 'US': English (en)
'BG': Bulgarian (bg)
'BR', 'PT': Portuguese (pt)
'CY': Greek (el)
'CZ': Czech (cs)
'DK': Danish (da)
'EE': Estonian (et)
'FI': Finnish (fi)
'FR', 'GF', 'GP', 'HT', 'LU', 'MQ': French (fr)
'GR': Greek (el)
'HK', 'TW': Chinese (zh)
'HR': Croatian (hr)
'HU': Hungarian (hu)
'IT': Italian (it)
'JP': Japanese (ja)
'KR': Korean (ko)
'LT': Lithuanian (lt)
'LV': Latvian (lv)
'MY': Malay (ms)
'NO': Norwegian (no)
'PL': Polish (pl)
'RO': Romanian (ro)
'RU': Russian (ru)
'SA': Arabic (ar)
'SE': Swedish (sv)
'SI': Slovenian (sl)
'SK': Slovak (sk)
'SR': Serbian (sr)
'TR': Turkish (tr)

```
```
'Australia': 'au'
'Canada': 'ca'
'China': 'cn'
'Digital Demos': 'dd'
'Europe': 'eu'
'France': 'fr'
'Germany': 'de'
'Italy': 'it'
'Japan': 'jp'
'Kiosk Demos': 'kd'
'Korea': 'kr'
'North America': 'na'
'Region Free': 'rf'
'Russia': 'ru'
'Spain': 'es'
'Taiwan': 'tw'
'The Netherlands': 'nl'
'The United Kingdom': 'uk'
'UnknownOther': 'unknown'
```
```
language_priority = ['en', 'ja', 'fr', 'es', 'de', 'it', 'nl', 'pt', 'zh', 'ru', 'ko', 'ar', 'tr', 'sv', 'fi', 'da', 'no', 'pl', 'cs', 'sk', 'sl', 'sr', 'hr', 'hu', 'lt', 'lv', 'el', 'bg', 'ro', 'ms', 'mt', 'et']
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [License](./LICENSE) file for details.

## Related Projects

- [3DSDBAPI](https://github.com/ghost-land/3DSDBAPI)
- [3dserver](https://github.com/ghost-land/3dserver)
