import ast
from pathlib import Path
from typing import List, Dict, Tuple, Union
import pandas as pd


class FPGrowthRecommender:
    def __init__(self, rule_path: Union[str, Path]):
        rule_path = Path(rule_path)
        if not rule_path.exists():
            raise FileNotFoundError(f"Rules file not found: {rule_path}")

        rules = pd.read_csv(rule_path)

        required_cols = {"antecedent", "consequent", "confidence"}
        if not required_cols.issubset(rules.columns):
            raise ValueError("rules.csv must have antecedent, consequent, confidence columns")

        # Parse the antecedent column which may contain stringified lists
        def parse(value) -> List[str]:
            try:
                parsed = ast.literal_eval(str(value))
                if isinstance(parsed, list):
                    return [str(x).strip().lower() for x in parsed]
            except Exception:
                pass
            return [str(value).strip().lower()]

        rules["antecedent"] = rules["antecedent"].apply(parse)
        rules["consequent"] = rules["consequent"].astype(str).str.strip().str.lower()


        # Sort rules by confidence descending
        rules = rules.sort_values("confidence", ascending=False, ignore_index=True)

        # Build lookup table
        self._lookup: Dict[str, List[Tuple[str, float]]] = {}
        for _, row in rules.iterrows():
            for item in row["antecedent"]:
                if row["consequent"]:
                    self._lookup.setdefault(item, []).append((row["consequent"], row["confidence"]))

    def recommend(self, item: str, top_k: int = 5) -> List[Dict[str, float]]:
        key = item.strip().lower()
        pool = self._lookup.get(key)

        # fallback: partial match if exact not found
        if pool is None:
            pool = []
            for k, v in self._lookup.items():
                if key in k:
                    pool.extend(v)

        if not pool:
            return []

        seen = set()
        results = []
        for cons, conf in pool:
            if cons not in seen and cons != key:
                seen.add(cons)
                results.append({"item": cons, "score": round(conf, 4)})
            if len(results) >= top_k:
                break

        return results

    def available_items(self) -> List[str]:
        return sorted(self._lookup.keys())