#!/usr/bin/env python3
"""Simple BitNet CPU demo using key/value caching."""

import argparse
from pathlib import Path

import torch

from .model import ModelArgs, Transformer
from gpu.tokenizer import Tokenizer


def load_model(checkpoint: str) -> Transformer:
    args = ModelArgs()
    model = Transformer(args)
    state = torch.load(checkpoint, map_location="cpu")
    missing, unexpected = model.load_state_dict(state, strict=False)
    if missing:
        print(f"Missing keys: {missing}")
    if unexpected:
        print(f"Unexpected keys: {unexpected}")
    model.eval()
    return model


def generate(model: Transformer, tokenizer: Tokenizer, prompt: str, steps: int) -> str:
    tokens = tokenizer.encode(prompt, bos=True, eos=False)
    inp = torch.tensor(tokens, dtype=torch.long).unsqueeze(0)
    model.reset_cache()
    with torch.no_grad():
        logits = model(inp, use_cache=True)
        for _ in range(steps):
            next_token = logits[0, -1].argmax()
            tokens.append(int(next_token))
            inp = next_token.view(1, 1)
            logits = model(inp, use_cache=True)
    return tokenizer.decode(tokens)


def main() -> None:
    cli = argparse.ArgumentParser(description="BitNet-b1.58 CPU demo")
    cli.add_argument("checkpoint", help="Path to PyTorch checkpoint")
    cli.add_argument("prompt", nargs="?", default="Hello")
    cli.add_argument("--steps", type=int, default=20)
    args = cli.parse_args()

    tokenizer = Tokenizer(str(Path("gpu") / "tokenizer.model"))
    model = load_model(args.checkpoint)

    output = generate(model, tokenizer, args.prompt, args.steps)
    print(output)


if __name__ == "__main__":
    main()
