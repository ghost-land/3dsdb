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
│   └── [tid].json              # Extra content data files
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




**JSON Structure :**

- base/[tid].json
```
{
  "id": "",  # The unique identifier for the game or content, often a hexadecimal string.
             # Example: "000400000017C200"

  "name": "",  # The official name of the game or content.
               # Example: "YO-KAI WATCH™"

  "product_code": "",  # The product code assigned by Nintendo, usually starts with "CTR" for 3DS.
                       # Example: "CTR-P-AYWZ"

  "platform": {
    "device": "",  # The device identifier, typically "CTR" for Nintendo 3DS.
                   # Example: "CTR"

    "name": ""     # The full name of the platform or distribution method.
                   # Example: "Nintendo 3DS (Card/Download)"
  },

  "publisher": "",  # The name of the company that published the game or content.
                    # Example: "Nintendo"

  "genre": "",  # The primary genre(s) of the game or content.
                # Example: "Adventure/RPG"

  "rating": {
    "name": "",  # The rating given by a regional rating board.
                 # Example: "PG"

    "age": 0     # The minimum age recommended by the rating.
                 # Example: 8
  },

  "descriptors": [],  # A list of content descriptors provided by the rating board.
                      # Example: ["Mild violence", "Online interactivity"]

  "release_dates": {
    "eshop": "",  # The release date of the game or content on the eShop in YYYY-MM-DD format.
                  # Example: "2015-12-05"

    "retail": ""  # The release date of the game or content for retail (physical copy) in YYYY-MM-DD format.
                  # Example: "TBD" (To Be Determined)
  },

  "formal_name": "",  # The formal or extended name of the game or content.
                      # Example: "YO-KAI WATCH™"

  "description": "",  # A brief description or synopsis of the game or content.
                      # Example: "Experience the international sensation of YO-KAI WATCH! YO-KAI WATCH is about hundreds of sometimes cute, sometimes spooky, and usually mischievous Yo-kai that inhabit our world..."

  "genres": [],  # A list of genres that best describe the game or content.
                 # Example: ["Adventure", "RPG"]

  "features": [],  # A list of key features or functionalities supported by the game or content.
                   # Example: ["Displays 3D Visuals", "Supports Local Play", "Supports StreetPass", "Supports SpotPass", "Nintendo Network"]

  "languages": [
    {
      "iso_code": "",  # The ISO code for the language supported by the game or content.
                       # Example: "en"

      "name": ""       # The name of the language.
                       # Example: "English"
    }
  ],

  "number_of_players": "",  # The number of players supported by the game or content, with optional descriptions.
                            # Example: "1 – 2 players (Supports 2 Players via Local Play)"

  "copyright": ""  # The copyright notice for the game or content.
                   # Example: "© LEVEL-5 Inc."
}

```