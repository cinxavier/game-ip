venv="venv"

if [ ! -d ./$venv ]; then
  python3 -m venv "$venv"
else
  echo "venv ja existe"
fi

if [ -d ./$venv ]; then
  echo "iniciando instalações"
  source "./$venv/bin/activate"
  pip install -r req.txt
  python3 run_map_maker.py
fi
echo "pronto."