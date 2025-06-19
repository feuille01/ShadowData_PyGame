import json
from pathlib import Path

class HighScoreManager:
    FILE_PATH = Path("highscores.json")
    MAX_ENTRIES = 5

    def __init__(self):
        # при инициализации загружаем существующий файл если есть
        if self.FILE_PATH.exists():
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                self.records = json.load(file)
        else:
            self.records = {}


    def add_record(self, level_idx: int, name: str, score: int, documents: int, time_str: str, hacked: int):
        # Добавляет новую запись и выделяет топ-5 по очкам.
        key = str(level_idx)
        rec = {
            "name": name,
            "score": score,
            "documents": documents,
            "time": time_str,
            "hacked": hacked
        }
        lst = self.records.get(key, [])
        lst.append(rec)
        # сортируем по score (по убыванию), оставляя топ-5
        lst.sort(key=lambda r: r["score"], reverse=True)
        self.records[key] = lst[: self.MAX_ENTRIES]
        # сохранение
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)


    def get_records(self, level_idx: int):
        """Возвращает список рекордов для данного уровня."""
        return self.records.get(str(level_idx), [])
