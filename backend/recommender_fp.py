from __future__ import annotations

import ast
from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd


class FPGrowthRecommender:
    def __init__(self, rule_path: str | Path):
        rule_path = Path(rule_path)
        if not rule_path.exists():
            raise FileNotFoundError(f"Rules file not found: {rule_path}")

        rules = pd.read_csv(rule_path)
        if not {"antecedent", "consequent", "confidence"}.issubset(rules.columns):
            raise ValueError("rules.csv must have antecedent, consequent, confidence columns")

        def parse(val) -> List[str]:
            try:
                res = ast.literal_eval(str(val))
                if isinstance(res, list):
                    return [str(i).strip().lower() for i in res]
            except Exception:
                pass
            return [str(val).strip().lower()]

        rules["antecedent"] = rules["antecedent"].apply(parse)
        rules["consequent"] = rules["consequent"].astype(str).str.lower().str.strip()
        rules = rules.sort_values("confidence", ascending=False, ignore_index=True)

        self._lookup: Dict[str, List[Tuple[str, float]]] = {}
        for _, row in rules.iterrows():
            for a in row["antecedent"]:
                if row["consequent"]:
                    self._lookup.setdefault(a, []).append((row["consequent"], row["confidence"]))

    def recommend(self, item: str, top_k: int = 5) -> List[Dict[str, float]]:
        key = item.strip().lower()
        pool = self._lookup.get(key)

        if pool is None:
            # fallback: partial match
            pool = []
            for k, v in self._lookup.items():
                if key in k:
                    pool.extend(v)

        if not pool:
            return []

        seen, results = set(), []
        for cons, conf in pool:
            if cons not in seen and cons != key:
                seen.add(cons)
                results.append((cons, conf))
            if len(results) >= top_k:
                break

        return [{"item": cons, "score": round(conf, 4)} for cons, conf in results]

    def available_items(self) -> List[str]:
        return sorted(self._lookup.keys())
