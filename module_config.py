from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleConfig:
    name: str
    description: str
    version: str
