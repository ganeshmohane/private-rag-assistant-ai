## follow this steps to setup CodeBase
1. navigate into codebase directory
```bash
 cd codebase
```
2. install uv package manager
```bash
pip install uv
```
3. create virtual env -
```bash
uv venv .venv
```
4. activate venv -
```bash
.venv/scripts/activate  # for windows
```
5. install requirements -
```bash
uv pip install -r requirements.txt
```

## client 
- cd into client directory
- run command - 
```bash
streamlit run streamlit-main.py
```

## server
- cd into server directory
- run command -  
```bash
uv run uvicorn main:app --reload
```
