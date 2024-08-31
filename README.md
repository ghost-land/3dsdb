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
"id": ""
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