# 3DS-dB
An open Source database for Nintendo 3DS


________

Structure :
```
db/3ds/
├── base/                           # Retail / eShop games (regional releases)
│     └── [tid]/
├── digital-demos/                  # Downloadable demos (hShop digital-demos)
│     └── [tid]/
├── kiosk-demos/                    # Kiosk / demo-station builds (hShop kiosk-demos)
│     └── [tid]/
├── region-free/                    # Region-free titles (hShop world)
│     └── [tid]/
├── unknown-other/                  # Unsorted / unknown region (hShop unknown-other)
│     └── [tid]/
├── dlc/                            # Downloadable content
│     └── [tid]/
├── dsiware/                        # DSiWare games and applications
│     └── [tid]/
├── extras/                         # Additional content
│   ├── Custom DSiWare/             # Custom DSiWare creations
│   │     └── [tid]/
│   ├── DSi System Apps/            # System applications for DSi
│   │     └── [tid]/
│   ├── Dev Apps/                   # Developer tools and apps
│   │     └── [tid]/
│   ├── Miscellaneous/              # Miscellaneous content
│   │     └── [tid]/
│   ├── Homebrew/                   # Homebrew applications and games
│   │     └── [tid]/
│   ├── ROM Hacks/                  # Modified ROMs
│   │     └── [tid]/
│   └── Translated Games/           # Games with fan-made translations
│         └── [tid]/
├── themes/                         # 3DS themes
│     └── [tid]/
├── updates/                        # System or game updates
│     └── [tid]/
├── videos/                         # eShop video content (E3 clips, trailers, Nintendo Video)
│     └── [tid]/
└── virtual-console/                # Virtual Console games
      └── [tid]/
```

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
