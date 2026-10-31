"""Типы данных (аналог types.ts): dataclass-модели и (де)сериализация.

JSON хранится в camelCase, как в исходном TypeScript-интерфейсе,
поэтому бэкапы совместимы с React-версией приложения.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


def new_id() -> str:
    return uuid.uuid4().hex[:8]


def _int(value: Any, lo: int, hi: int, default: int) -> int:
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default


@dataclass
class Stat:
    id: str
    name: str
    icon: str
    value: int = 5  # 1-10
    hint: str = ""  # подсказка «что это даёт»


@dataclass
class Effect:
    id: str
    name: str
    description: str = ""


@dataclass
class Mission:
    goal: str = ""
    success_criteria: str = ""
    reward: str = ""


@dataclass
class DiaryEntry:
    id: str
    date: str  # YYYY-MM-DD
    event: str
    stat_delta: str
    effect: str


@dataclass
class Character:
    name: str
    class_name: str = "Стратег"
    level: int = 1
    xp: int = 0  # 0-100
    stats: list[Stat] = field(default_factory=list)
    buffs: list[Effect] = field(default_factory=list)
    debuffs: list[Effect] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    mission: Mission = field(default_factory=Mission)
    diary: list[DiaryEntry] = field(default_factory=list)

    # ---------- сериализация ----------
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "className": self.class_name,
            "level": self.level,
            "xp": self.xp,
            "stats": [vars(s) for s in self.stats],
            "buffs": [vars(e) for e in self.buffs],
            "debuffs": [vars(e) for e in self.debuffs],
            "strengths": list(self.strengths),
            "weaknesses": list(self.weaknesses),
            "mission": {
                "goal": self.mission.goal,
                "successCriteria": self.mission.success_criteria,
                "reward": self.mission.reward,
            },
            "diary": [
                {"id": d.id, "date": d.date, "event": d.event,
                 "statDelta": d.stat_delta, "effect": d.effect}
                for d in self.diary
            ],
        }

    @staticmethod
    def from_dict(d: Any) -> "Character":
        """Разбирает и валидирует данные. При ошибке — ValueError."""
        if not isinstance(d, dict):
            raise ValueError("Ожидался JSON-объект")
        name = str(d.get("name", "")).strip()
        if not name:
            raise ValueError("Имя персонажа не может быть пустым")
        try:
            stats = [
                Stat(str(s.get("id") or new_id()), str(s["name"]), str(s.get("icon", "⭐")),
                     _int(s.get("value"), 1, 10, 5), str(s.get("hint", "")))
                for s in d.get("stats", [])
            ]
            if not stats:
                raise ValueError("Нет ни одного стата")

            def effects(key: str) -> list[Effect]:
                return [Effect(str(e.get("id") or new_id()), str(e["name"]),
                               str(e.get("description", ""))) for e in d.get(key, [])]

            m = d.get("mission") or {}
            return Character(
                name=name,
                class_name=str(d.get("className") or "Стратег"),
                level=_int(d.get("level"), 1, 10**6, 1),
                xp=_int(d.get("xp"), 0, 99, 0),
                stats=stats,
                buffs=effects("buffs"),
                debuffs=effects("debuffs"),
                strengths=[str(x) for x in d.get("strengths", [])],
                weaknesses=[str(x) for x in d.get("weaknesses", [])],
                mission=Mission(str(m.get("goal", "")), str(m.get("successCriteria", "")),
                                str(m.get("reward", ""))),
                diary=[
                    DiaryEntry(str(e.get("id") or new_id()), str(e.get("date", "")),
                               str(e["event"]), str(e.get("statDelta", "")),
                               str(e.get("effect", "")))
                    for e in d.get("diary", [])
                ],
            )
        except (KeyError, AttributeError, TypeError) as exc:
            raise ValueError(f"Некорректная структура данных: {exc}") from exc
