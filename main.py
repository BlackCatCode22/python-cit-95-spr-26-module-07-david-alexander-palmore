from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from bear import Bear
from hyena import Hyena
from lion import Lion
from tiger import Tiger

BASE_DIR = Path(__file__).resolve().parent
ARRIVING_FILE = BASE_DIR / "arrivingAnimals.txt"
NAMES_FILE = BASE_DIR / "animalNames.txt"
OUTPUT_FILE = BASE_DIR / "zooPopulation.txt"
ARRIVAL_DATE = "2024-03-26"
CURRENT_YEAR = 2024

SEASON_TO_MONTH_DAY = {
    "spring": (3, 21),
    "summer": (6, 21),
    "fall": (9, 21),
    "winter": (12, 21),
    "unknown birth season": (1, 1),
}

SPECIES_TO_CLASS = {
    "hyena": Hyena,
    "lion": Lion,
    "tiger": Tiger,
    "bear": Bear,
}

SPECIES_TO_PREFIX = {
    "hyena": "HY",
    "lion": "LI",
    "tiger": "TI",
    "bear": "BE",
}


def load_name_lists(file_path: Path) -> Dict[str, List[str]]:
    name_lists: Dict[str, List[str]] = {}
    current_species = None

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.endswith("Names:"):
            current_species = line.replace(" Names:", "").strip().lower()
            name_lists[current_species] = []
            continue

        if current_species is None:
            continue

        names = [name.strip() for name in line.split(",") if name.strip()]
        name_lists[current_species].extend(names)

    return name_lists


def parse_animal_line(line: str) -> dict:
    parts = [part.strip() for part in line.split(",")]
    if len(parts) < 5:
        raise ValueError(f"Unexpected animal record format: {line}")

    age_sex_species = parts[0].split()
    age = int(age_sex_species[0])
    sex = age_sex_species[3]
    species = age_sex_species[4]

    season = parts[1].replace("born in ", "").strip().lower()
    color = parts[2].replace(" color", "").strip()
    weight = int(parts[3].replace(" pounds", "").strip())
    origin = parts[4].replace("from ", "").strip()
    if len(parts) > 5:
        origin = origin + ", " + ", ".join(part.strip() for part in parts[5:])

    return {
        "age": age,
        "sex": sex,
        "species": species,
        "season": season,
        "color": color,
        "weight": weight,
        "origin": origin,
    }


def gen_birth_date(age: int, season: str, current_year: int = CURRENT_YEAR) -> str:
    birth_year = current_year - age
    month, day = SEASON_TO_MONTH_DAY.get(season, (1, 1))
    return f"{birth_year:04d}-{month:02d}-{day:02d}"


def gen_unique_id(species: str, counters: Dict[str, int]) -> str:
    counters[species] += 1
    prefix = SPECIES_TO_PREFIX[species]
    return f"{prefix}{counters[species]:02d}"


def build_animals() -> List[object]:
    name_lists = load_name_lists(NAMES_FILE)
    counters = {species: 0 for species in SPECIES_TO_PREFIX}
    name_indexes = {species: 0 for species in SPECIES_TO_PREFIX}
    animals = []

    for raw_line in ARRIVING_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        data = parse_animal_line(line)
        species = data["species"]
        animal_class = SPECIES_TO_CLASS[species]

        unique_id = gen_unique_id(species, counters)
        assigned_name = name_lists[species][name_indexes[species]]
        name_indexes[species] += 1
        birth_date = gen_birth_date(data["age"], data["season"])

        animal = animal_class(
            unique_id=unique_id,
            name=assigned_name,
            species=species,
            sex=data["sex"],
            birth_date=birth_date,
            color=data["color"],
            weight=data["weight"],
            origin=data["origin"],
            arrival_date=ARRIVAL_DATE,
        )
        animals.append(animal)

    return animals


def write_report(animals: List[object], file_path: Path) -> None:
    grouped = {"hyena": [], "lion": [], "tiger": [], "bear": []}
    for animal in animals:
        grouped[animal.species].append(animal)

    lines: List[str] = []
    for species in ["hyena", "lion", "tiger", "bear"]:
        lines.append(f"{species.capitalize()} Habitat:")
        for animal in grouped[species]:
            lines.append(animal.report_line())
        lines.append("")

    file_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    animals = build_animals()
    write_report(animals, OUTPUT_FILE)
    print(f"Created report: {OUTPUT_FILE.name}")
    print(f"Animals loaded: {len(animals)}")


if __name__ == "__main__":
    main()
