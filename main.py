from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# MANIFEST
# =========================================================

MANIFEST = {
    "id": "org.tomandjerry.classic",
    "version": "2.2.0",
    "name": "Tom & Jerry (Classic)",
    "description": "Tom & Jerry Classic Collection",
    "resources": ["catalog", "meta", "stream"],
    "types": ["series"],
    "idPrefixes": ["tj_classic"],
    "catalogs": [
        {
            "type": "series",
            "id": "tj_catalog",
            "name": "Tom & Jerry - Classic"
        }
    ]
}

# =========================================================
# SERIES IMAGES
# =========================================================

SERIES_POSTER = (
    "https://upload.wikimedia.org/wikipedia/en/5/5f/"
    "Tom_and_Jerry_title_card.png"
)

SERIES_BACKGROUND = (
    "https://images.wallpapersden.com/image/download/"
    "tom-and-jerry-art_bGdpZm2UmZqaraWkpJRmZmdlrWZnZWU.jpg"
)

SERIES_LOGO = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/"
    "Tom_and_Jerry_logo.svg/1200px-Tom_and_Jerry_logo.svg.png"
)

# =========================================================
# EPISODE TITLES
# =========================================================

EPISODE_TITLES = [
    "Puss Gets the Boot",
    "The Midnight Snack",
    "The Night Before Christmas",
    "Fraidy Cat",
    "Dog Trouble",
    "Puss n' Toots",
    "The Bowling Alley Cat",
    "Fine Feathered Friend",
    "Sufferin' Cats!",
    "The Lonesome Mouse",
    "The Yankee Doodle Mouse",
    "Baby Puss",
    "The Zoot Cat",
    "The Million Dollar Cat",
    "The Bodyguard",
    "Puttin' on the Dog",
    "Mouse Trouble",
    "The Mouse Comes to Dinner",
    "Mouse in Manhattan",
    "Tee for Two",
    "Flirty Birdy",
    "Quiet Please!",
    "Springtime for Thomas",
    "The Milky Waif",
    "Trap Happy",
    "Solid Serenade",
    "Cat Fishin'",
    "Part Time Pal",
    "The Cat Concert",
    "Dr. Jekyll and Mr. Mouse",
    "Salt Water Tabby",
    "A Mouse in the House",
    "The Invisible Mouse",
    "Kitty Foiled",
    "The Truce Hurts",
    "Old Rockin' Chair Tom",
    "Professor Tom",
    "Mouse Cleaning",
    "Polka-Dot Puss",
    "The Little Orphan",
    "Hatch Up Your Troubles",
    "Heavenly Puss",
    "The Cat and the Mermouse",
    "Love That Puppy",
    "Jerry's Diary",
    "Tennis Chumps",
    "Little Quacker",
    "Saturday Evening Puss",
    "Texas Tom",
    "Jerry and the Lion",
    "Safety Second",
    "Tom and Cherie",
    "Cue Ball Cat",
    "Casanova Cat",
    "Jerry and the Goldfish",
    "Jerry's Cousin",
    "Sleepy-Time Tom",
    "His Mouse Friday",
    "Slicked-up Pup",
    "Nit-witty Kitty",
    "Cat Napping",
    "The Flying Cat",
    "The Duck Doctor",
    "The Two Mouseketeers",
    "Smitten Kitten",
    "Triple Trouble",
    "Little Runaway",
    "Fit to Be Tied",
    "Push-Button Kitty",
    "Cruise Cat",
    "The Dog House",
    "Missing Mouse",
    "Jerry and Jumbo",
    "Johann Mouse",
    "That's My Pup!",
    "Just Ducky",
    "Two Little Indians",
    "Life with Tom",
    "Puppy Tale",
    "Posse Cat",
    "Hic-cup Pup",
    "Little School Mouse",
    "Baby Butch",
    "Mice Follies",
    "Neapolitan Mouse",
    "Downhearted Duckling",
    "Pet Snack",
    "Touché, Pussy Cat!",
    "Southbound Duckling",
    "Pup on a Leash",
    "Designing Mice",
    "Puppy's Birthday",
    "Smarty Cat",
    "Pecos Pest",
    "That's My Mommy",
    "The Flying Sorceress",
    "The Egg and Jerry",
    "Busy Buddies",
    "Muscle Beach Tom",
    "Down Beat Bear",
    "Blue Cat Blues",
    "Barbecue Brawl",
    "Tops with Pops",
    "Timid Tabby",
    "Feedin' the Kiddie",
    "Mucho Mouse",
    "Tom's Photo Finish",
    "Happy Go Ducky",
    "Royal Cat Nap",
    "The Vanishing Duck",
    "Robin Hoodwinked",
    "Tot Watchers",
    "Switchin' Kitten",
    "Down and Outing",
    "High Steaks",
    "Mouse Into Space",
    "Landing Stripling",
    "Calypso Cat",
    "Dicky Moe",
    "The Tom and Jerry Cartoon Kit",
    "Tall in the Trap",
    "Sorry Safari",
    "Buddies Thicker Than Water",
    "Carmen Get It!",
    "Pent-House Mouse",
    "The Cat Above and the Mouse Below",
    "Is There a Doctor in the Mouse?",
    "Much Ado About Mousing",
    "Snowbody Loves Me",
    "The Unshrinkable Jerry Mouse",
    "Ah, Sweet Mouse-Story of Life",
    "Tom-ic Energy",
    "Bad Day at Cat Rock",
    "The Brothers Carry-Mouse-Off",
    "Haunted Mouse",
    "I'm Just Wild About Jerry",
    "Of Feline Bondage",
    "Year of the Mouse",
    "The Cat's Me-Ouch!",
    "Duel Personality",
    "Jerry, Jerry, Quite Contrary",
    "Jerry-Go-Round",
    "Love Me, Love My Mouse",
    "Puss 'n' Boats",
    "Filet Meow",
    "Matinee Mouse",
    "The Oicker-Upper",
    "Advance and Be Mechanized",
    "Guided Mouse-ille",
    "Rock 'n' Rodent",
    "Cannery Rodent",
    "The Mouse from H.U.N.G.E.R.",
    "Surf-Bored Cat",
    "Shutter Bugged Cat",
    "Advance and Be Mechanized",
    "Purr-Chance to Dream"
]

# =========================================================
# ARCHIVE
# =========================================================

ARCHIVE_ITEM = "tom_and_jerry_1940_1958"

EPISODES_CACHE = {}


def get_archive_episodes():
    """
    Get available MP4 files from Internet Archive metadata.
    """

    global EPISODES_CACHE

    if EPISODES_CACHE:
        return EPISODES_CACHE

    try:
        url = f"https://archive.org/metadata/{ARCHIVE_ITEM}"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "TomJerry-Stremio-Addon/2.2"
            }
        )

        response.raise_for_status()

        data = response.json()
        files = data.get("files", [])

        mp4_files = []

        for file_info in files:
            filename = file_info.get("name", "")

            if filename.lower().endswith(".mp4"):
                mp4_files.append(file_info)

        mp4_files.sort(
            key=lambda x: x.get("name", "").lower()
        )

        for index, file_info in enumerate(mp4_files, start=1):

            filename = file_info.get("name")

            if not filename:
                continue

            filename_encoded = requests.utils.quote(
                filename,
                safe="/"
            )

            download_url = (
                f"https://archive.org/download/"
                f"{ARCHIVE_ITEM}/{filename_encoded}"
            )

            EPISODES_CACHE[index] = {
                "ep": index,
                "filename": filename,
                "url": download_url
            }

    except Exception as error:
        print("Archive error:", error)

    return EPISODES_CACHE


# =========================================================
# MANIFEST ENDPOINT
# =========================================================

@app.get("/manifest.json")
def get_manifest():

    return Response(
        content=json.dumps(
            MANIFEST,
            ensure_ascii=False
        ),
        media_type="application/json"
    )


# =========================================================
# CATALOG
# =========================================================

@app.get("/catalog/series/tj_catalog.json")
def get_catalog():

    meta = {
        "id": "tj_classic_1940",
        "type": "series",
        "name": "Tom and Jerry: The Classic Collection",
        "poster": SERIES_POSTER,
        "background": SERIES_BACKGROUND,
        "logo": SERIES_LOGO,
        "description": (
            "Tom and Jerry Classic Collection (1940-1958)"
        )
    }

    return Response(
        content=json.dumps(
            {"metas": [meta]},
            ensure_ascii=False
        ),
        media_type="application/json"
    )


# =========================================================
# META
# =========================================================

@app.get("/meta/series/{id}.json")
def get_meta(id: str):

    videos = []

    for i, title_en in enumerate(
        EPISODE_TITLES,
        start=1
    ):

        videos.append({
            "id": f"tj_classic_1940:1:{i}",
            "title": f"الحلقة {i}: {title_en}",
            "season": 1,
            "episode": i,
            "overview": (
                f"Tom and Jerry Classic - "
                f"Episode {i}: {title_en}"
            )
        })

    meta_data = {
        "id": "tj_classic_1940",
        "type": "series",
        "name": "Tom and Jerry: The Classic Collection",
        "poster": SERIES_POSTER,
        "background": SERIES_BACKGROUND,
        "logo": SERIES_LOGO,
        "description": (
            "Tom and Jerry Classic Collection"
        ),
        "videos": videos
    }

    return Response(
        content=json.dumps(
            {"meta": meta_data},
            ensure_ascii=False
        ),
        media_type="application/json"
    )


# =========================================================
# STREAM
# =========================================================

@app.get("/stream/series/{id}.json")
def get_streams(request: Request, id: str):

    streams = []

    try:

        clean_id = id.replace(".json", "")
        parts = clean_id.split(":")

        if len(parts) < 3:
            return Response(
                content=json.dumps(
                    {"streams": []}
                ),
                media_type="application/json"
            )

        ep_num = int(parts[2])

        if ep_num < 1 or ep_num > len(EPISODE_TITLES):
            return Response(
                content=json.dumps(
                    {"streams": []}
                ),
                media_type="application/json"
            )

        episodes = get_archive_episodes()

        episode = episodes.get(ep_num)

        if not episode:
            return Response(
                content=json.dumps(
                    {"streams": []},
                    ensure_ascii=False
                ),
                media_type="application/json"
            )

        mp4_url = episode["url"]
        episode_name = EPISODE_TITLES[ep_num - 1]

        streams.append({
            "name": "Direct MP4",
            "title": (
                f"تشغيل مباشر - "
                f"{episode_name}"
            ),
            "url": mp4_url,
            "behaviorHints": {
                "notWebReady": False
            }
        })

    except Exception as error:

        print("Stream error:", error)

    return Response(
        content=json.dumps(
            {"streams": streams},
            ensure_ascii=False
        ),
        media_type="application/json"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "addon": "Tom & Jerry Classic",
        "version": MANIFEST["version"],
        "episodes": len(EPISODE_TITLES)
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "episodes": len(EPISODE_TITLES)
    }
