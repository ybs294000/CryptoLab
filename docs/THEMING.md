# Theming

CryptoLab uses a single dark professional theme built from:

- `.streamlit/config.toml` for Streamlit-native theme values
- `utils/theme_css.py` for CSS variables and widget overrides
- `utils/branding.py` for the shared logo treatment

## Current approach

The CSS injector follows the same pattern used in the reference files:

- Define `:root` variables for the palette
- Override Streamlit widget selectors with those variables
- Keep the page background simple and stable
- Use Material icons in Streamlit labels, not inside raw HTML

## Key files

- `utils/theme_css.py`
- `utils/branding.py`
- `.streamlit/config.toml`
- `tmp/theme_css.py`
- `tmp/theme.py`
- `tmp/config.toml`

## Design rules in the current UI

- Flat dark page background, no large shell gradient
- Elevated cards and panels with restrained borders
- Blue primary actions and clear focus states
- Consistent file uploader, tabs, metrics, and input styling
- Logo reused in the sidebar and branded page headers

## Safe way to continue iterating

1. Update palette tokens in `utils/theme_css.py`
2. Keep `.streamlit/config.toml` aligned with the same colors
3. Re-run:

```bash
python tests\run_tests.py
```

4. Manually inspect:

```bash
streamlit run app.py
```
