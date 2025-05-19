## Running without Docker
### Setup
```
git clone https://github.com/GoncaloBFM/mma2025
cd mma2025
python -m venv .venv
source .venv/bin/activate (for Windows run: .venv\Scripts\activate)
pip install -r requirements.txt
```

### Run
On the root directory of the project run:
```
export PYTHONPATH="$PYTHONPATH:$PWD" (for Windows run: set PYTHONPATH=%CD%)
python src/main.py
```

After the Dash server is running open http://127.0.0.1:8050/ on your browser.

## Plotly and Dash tutorials
- Dash in 20 minutes: https://dash.plotly.com/tutorial
- Plotly plots gallery: https://plotly.com/python/
