# 3DS-dB
An open Source database for Nintendo 3DS


________

Structure :
```
data/
├── base/
│   └── [tid].json              # Base game data files
├── dlc/
│   └── [tid].json              # DLC data files
├── dsiware/
│   └── [tid].json              # DSiWare data files
├── extras/
│   ├── Custom DSiWare/
│   │   └── [tid].json          # Custom DSiWare content files
│   ├── DSi System Apps/
│   │   └── [tid].json          # DSi System applications data files
│   ├── Dev Apps/
│   │   └── [tid].json          # Development applications data files
│   ├── Miscellaneous/
│   │   └── [tid].json          # Miscellaneous extra content data files
│   ├── Homebrew/
│   │   └── [tid].json          # Homebrew software data files
│   ├── ROM Hacks/
│   │   └── [tid].json          # ROM hacks data files
│   └── Translated Games/
│       └── [tid].json          # Translated games data files
├── themes/
│   └── [tid].json              # Theme data files
├── updates/
│   └── [tid].json              # Update data files
├── videos/
│   └── [tid].json              # Video data files
└── virtual-console/
    └── [tid].json              # Virtual Console game data files
```

```
media/
├── [tid]/
│   ├── banner.jpg                                   # Banner image for the content
│   ├── icon.jpg                                     # Icon image for the content
│   ├── top_image.jpg                                # Top image for the content
│   ├── screenshots/                                 # Directory for screenshots
│   │   └── screenshot_[n].jpg                       # Screenshot files
│   ├── thumbnails/                                  # Directory for thumbnails
│   │   └── thumbnail_[n].jpg                        # Thumbnail files
│   └── screenshots_uncompiled/                      # Uncompiled screenshots
│       ├── screenshot_[n]_lower.jpg                 # Lower screen
│       └── screenshot_[n]_upper.jpg                 # Upper screen
```


Json Structure :
```
"tid": ""
"nid": ""
"name": ""
"product_code": ""
"region": ""
"platform": {"device": "", "name": ""}
"publisher": ""
"genre": ""
"rating": {"system": "", "rating": "", "age": ""}
"keywords": [""]
"descriptors": [""]
"releases_dates": {"eshop": "", "retail": ""}
"formal_name": ""
"description": ""
"movies_id": [""]
"disclaimer": ""
"genres": [""]
"features": [""]
"languages": [{"iso_code": "", "name": ""}]
"number_of_players": ""
"copyright": ""
"catch_copy": ""
"websites": [{"name": "", "url": "", "official" false}]
```



Iso code and more :
```
AE': Arabic (ar)
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
'JP': Japanese (jp)
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
'TR': Turkish (tr)```

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
language_priority = ['en', 'jp', 'fr', 'es', 'de', 'it', 'nl', 'pt', 'zh', 'ru', 'ko', 'ar', 'tr', 'sv', 'fi', 'da', 'no', 'pl', 'cs', 'sk', 'sl', 'sr', 'hr', 'hu', 'lt', 'lv', 'el', 'bg', 'ro', 'ms', 'mt', 'et']
```