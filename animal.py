from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Animal:
    unique_id: str
    name: str
    species: str
    sex: str
    birth_date: str
    color: str
    weight: int
    origin: str
    arrival_date: str

    def habitat_name(self) -> str:
        return f"{self.species.capitalize()} Habitat"

    def report_line(self) -> str:
        return (
            f"{self.unique_id}; {self.name}; birth date: {self.birth_date}; "
            f"{self.color}; {self.sex}; {self.weight} pounds; from {self.origin}; "
            f"arrived {self.arrival_date}"
        )
