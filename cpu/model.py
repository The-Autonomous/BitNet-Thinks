from dataclasses import dataclass

import torch
from torch import nn

from utils.cache_kv_attention import CachedSelfAttention


@dataclass
class ModelArgs:
    """Configuration for the simple CPU Transformer."""
    vocab_size: int = 50257
    dim: int = 768
    n_layers: int = 12
    n_heads: int = 12
    ffn_dim: int = 3072


class TransformerBlock(nn.Module):
    def __init__(self, args: ModelArgs) -> None:
        super().__init__()
        self.attn = CachedSelfAttention(args.dim, args.n_heads)
        self.ffn = nn.Sequential(
            nn.Linear(args.dim, args.ffn_dim),
            nn.GELU(),
            nn.Linear(args.ffn_dim, args.dim),
        )
        self.attn_norm = nn.LayerNorm(args.dim)
        self.ffn_norm = nn.LayerNorm(args.dim)

    def forward(self, x: torch.Tensor, use_cache: bool = False) -> torch.Tensor:
        h = x + self.attn(self.attn_norm(x), use_cache=use_cache)
        h = h + self.ffn(self.ffn_norm(h))
        return h


class Transformer(nn.Module):
    def __init__(self, args: ModelArgs) -> None:
        super().__init__()
        self.args = args
        self.tok_embeddings = nn.Embedding(args.vocab_size, args.dim)
        self.layers = nn.ModuleList([TransformerBlock(args) for _ in range(args.n_layers)])
        self.norm = nn.LayerNorm(args.dim)
        self.output = nn.Linear(args.dim, args.vocab_size, bias=False)

    def reset_cache(self) -> None:
        """Clear cached key/value tensors in all layers."""
        for layer in self.layers:
            layer.attn.reset_cache()

    def forward(self, token_ids: torch.Tensor, use_cache: bool = False) -> torch.Tensor:
        h = self.tok_embeddings(token_ids)
        for layer in self.layers:
            h = layer(h, use_cache=use_cache)
        logits = self.output(self.norm(h))
        return logits
