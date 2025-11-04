# How to test

```bash
uv run -m helix_kernel.cli start --mux windows_terminal -p cmder
uv run -m helix_kernel.cli exec a=1+1
```

# Install as tool (to test)

```
uv tool install --editable . 

helix-kernel start ...
```

# Helix config

```toml
[keys.normal."+"]
k = ":sh helix-kernel start --mux windows_terminal -p cmder" 

[keys.normal."minus"]
"space" = ":pipe-to helix-kernel exec"
```
