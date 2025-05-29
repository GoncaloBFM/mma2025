## Local
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



## Snellius
### Connect to Snellius
```
ssh <user>@snellius.surf.nl 
```

### Setup project
```
git clone https://github.com/GoncaloBFM/mma2025
cd mma2025
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

### Access compute node
```
srun --partition=<partition name> --gpus=1 --ntasks=1 --cpus-per-task=1 --time=00:20:00 --pty bash -i (other parameters are possible see instructions on Snellius below)
```

### Run server on Snellius
On the root directory of the project run:
```
export PYTHONPATH="$PYTHONPATH:$PWD" 
python src/main.py
```

### Connect to server on your local machine
```
ssh -L 8050:127.0.0.1:8050 -J <user>@snellius.surf.nl <user>@<partition>
```

After the Dash server is running open http://127.0.0.1:8050/ on your browser.


## Plotly and Dash tutorials
- Dash in 20 minutes: https://dash.plotly.com/tutorial
- Plotly plots gallery: https://plotly.com/python/

## Snellius tutorials
- Basics: https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial1/Lisa_Cluster.html
- Resources: https://servicedesk.surf.nl/wiki/spaces/WIKI/pages/30660209/Snellius+partitions+and+accounting




