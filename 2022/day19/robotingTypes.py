from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class BluePrint:
    blueprintId: int
    oreRobotCost: int
    clayRobotCost: int
    obsidianRobotOreCost: int
    obsidianRobotClayCost: int
    geodeRobotOreCost: int
    geodeRobotObsidianCost: int


@dataclass(frozen=True)
class Resources:
    ore: int
    clay: int
    obsidian: int
    geode: int


@dataclass(frozen=True)
class Robots:
    ore: int
    clay: int
    obsidian: int
    geode: int


class RobotType(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4
