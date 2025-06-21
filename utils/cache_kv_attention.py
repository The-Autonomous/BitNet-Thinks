import math
from typing import Optional
import torch
from torch import nn

class CachedSelfAttention(nn.Module):
    """Self-attention layer with key/value caching."""
    def __init__(self, embed_dim: int, num_heads: int) -> None:
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        head_dim = embed_dim // num_heads
        if head_dim * num_heads != embed_dim:
            raise ValueError("embed_dim must be divisible by num_heads")
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)
        self.register_buffer("_cache_k", None, persistent=False)
        self.register_buffer("_cache_v", None, persistent=False)

    def reset_cache(self) -> None:
        """Clear cached key/value tensors."""
        self._cache_k = None
        self._cache_v = None

    def forward(self, x: torch.Tensor, use_cache: bool = False) -> torch.Tensor:
        bsz, seq_len, _ = x.size()
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)

        if use_cache and self._cache_k is not None:
            k = torch.cat([self._cache_k, k], dim=1)
            v = torch.cat([self._cache_v, v], dim=1)

        if use_cache:
            self._cache_k = k.detach()
            self._cache_v = v.detach()

        q = q.view(bsz, seq_len, self.num_heads, -1).transpose(1, 2)
        k = k.view(bsz, -1, self.num_heads, -1).transpose(1, 2)
        v = v.view(bsz, -1, self.num_heads, -1).transpose(1, 2)

        scores = torch.matmul(q, k.transpose(-1, -2)) / math.sqrt(q.size(-1))
        attn = scores.softmax(dim=-1)
        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(bsz, seq_len, self.embed_dim)
        return self.out_proj(out)

if __name__ == "__main__":
    attn = CachedSelfAttention(embed_dim=16, num_heads=4)
    inp1 = torch.randn(1, 1, 16)
    out1 = attn(inp1, use_cache=True)
    inp2 = torch.randn(1, 1, 16)
    out2 = attn(inp2, use_cache=True)
    print("output shape with cache:", out2.shape)
