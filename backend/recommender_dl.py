from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import torch


class NCF(torch.nn.Module):
    def __init__(self, n_users: int, n_items: int, emb_size: int = 64):
        super().__init__()
        self.u_emb = torch.nn.Embedding(n_users, emb_size)
        self.i_emb = torch.nn.Embedding(n_items, emb_size)
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(emb_size * 2, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 1),
            torch.nn.Sigmoid(),
        )

    def forward(self, u, i):
        x = torch.cat([self.u_emb(u), self.i_emb(i)], dim=1)
        return self.fc(x).squeeze()


class DLRecommender:
    def __init__(self, ckpt_path: str | Path):
        ckpt_path = Path(ckpt_path)
        if not ckpt_path.exists():
            raise FileNotFoundError(f"Model checkpoint not found: {ckpt_path}")

        ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)

        self.user2idx: Dict[int, int] = {}
        for k, v in ckpt["user2idx"].items():
            try:
                self.user2idx[int(k)] = v
            except ValueError:
                continue

        self.item2idx: Dict[str, int] = {str(k): int(v) for k, v in ckpt["item2idx"].items()}
        self.idx2item: Dict[int, str] = {v: k for k, v in self.item2idx.items()}

        n_users = max(self.user2idx.values()) + 1
        n_items = max(self.item2idx.values()) + 1

        self.model = NCF(n_users, n_items).eval()
        self.model.load_state_dict(ckpt["model"])

    @torch.inference_mode()
    def recommend(self, user_id: int | str, top_k: int = 5) -> List[Dict[str, float]]:
        try:
            uid_key = int(user_id)
        except ValueError:
            return []

        if uid_key not in self.user2idx:
            return []

        u_idx_val = self.user2idx[uid_key]
        u_idx = torch.full((len(self.item2idx),), u_idx_val, dtype=torch.long)
        i_idx = torch.arange(len(self.item2idx), dtype=torch.long)

        scores = self.model(u_idx, i_idx)
        scores_np = scores.detach().numpy()

        top_idx = torch.topk(scores, top_k).indices.tolist()

        results = []
        for i in top_idx:
            item = self.idx2item.get(i)
            if item:
                results.append({"item": item, "score": round(float(scores_np[i]), 4)})
        return results
