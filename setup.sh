venv="venv"

if [ ! -d ./$venv ]; then
  python3 -m venv $venv
fi

if [ -d ./$venv ]; then
  source $PWD
  /$venv/bin/active
  pip install -r req.txt
  python3 run_map_maker.py
fi