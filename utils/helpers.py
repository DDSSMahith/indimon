import pandas as pd
import json
import re

# ==================================================
# Name normalization (REGEX-BASED, SINGLE SOURCE)
# ==================================================
def normalize_name(name: str) -> str:
    """
    Normalizes Pokémon names across CSV, learnsets, sprites.
    Examples:
    - Mr. Mime     -> mrmime
    - Farfetch’d  -> farfetchd
    - Ho-Oh       -> hooh
    """
    return re.sub(r"[^a-z0-9]", "", name.lower())


# ==================================================
# Load Pokémon base stats + types
# Uses YOUR pokemon.csv schema:
# HP, Att, Def, Spa, Spd, Spe
# ==================================================
def load_pokemon_data(path):
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace(".", "", regex=False)
    )

    pokemon = {}

    for _, row in df.iterrows():
        key = normalize_name(row["name"])

        # Types
        types = [row["type_1"]]
        if pd.notna(row["type_2"]):
            types.append(row["type_2"])

        # Stats (PHYSICAL + SPECIAL CORRECT)
        stats = {
            "hp": int(row["hp"]),
            "attack": int(row["att"]),
            "defense": int(row["def"]),
            "sp_attack": int(row["spa"]),
            "sp_defense": int(row["spd"]),
            "speed": int(row["spe"]),
        }

        pokemon[key] = {
            "types": types,
            "stats": stats
        }

    return pokemon


# ==================================================
# Load moves (ROBUST CSV HANDLING)
# Handles: 100%, —, missing power, damage_class/category
# ==================================================
def load_moves(path):
    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # Detect category column
    if "category" in df.columns:
        category_col = "category"
    elif "damage_class" in df.columns:
        category_col = "damage_class"
    else:
        category_col = None

    moves = {}

    for _, row in df.iterrows():
        # Power
        power = 0
        if not pd.isna(row.get("power")):
            try:
                power = int(row["power"])
            except ValueError:
                power = 0

        # Accuracy
        accuracy = 100
        if not pd.isna(row.get("accuracy")):
            acc = str(row["accuracy"]).replace("%", "").strip()
            if acc.isdigit():
                accuracy = int(acc)

        # Category
        if category_col:
            raw = str(row[category_col]).lower()
            if "phys" in raw:
                category = "Physical"
            elif "spec" in raw:
                category = "Special"
            else:
                category = "Status"
        else:
            category = "Status"

        moves[row["name"].lower()] = {
            "type": row["type"],
            "power": power,
            "accuracy": accuracy,
            "category": category
        }

    return moves


# ==================================================
# Load abilities
# ==================================================
def load_abilities(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [a["name"] for a in data]


# ==================================================
# Load learnsets.js (SHOWDOWN-STYLE PARSER)
# ==================================================
def load_learnsets(path):
    """
    Parses custom learnsets format:
    {
      "bulbasaur"; [
        "tackle",
        "growl",
        ...
      ],
      ...
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    learnsets = {}

    # Match: "pokemon"; [ ... ]
    blocks = re.findall(
        r'"([^"]+)"\s*;\s*\[(.*?)\]',
        text,
        re.S
    )

    for name, moves_block in blocks:
        key = normalize_name(name)

        # Extract all move strings
        moves = re.findall(r'"([^"]+)"', moves_block)

        learnsets[key] = [m.lower() for m in moves]

    if not learnsets:
        raise RuntimeError(
            "Learnsets parsing failed — no Pokémon found. "
            "Check learnsets.js format."
        )

    return learnsets

