# lego-stock-checker
Check for LEGO items coming back into stock

# Installing dependencies

I recommend using the included requirements.txt to install dependencies in a virtualenv. eg:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

OR

```
poetry install
poetry shell
```

# Running

```
cp lego_stock_checker_conf.py.example lego_stock_checker_conf.py
./lego_stock_checker.py
```
