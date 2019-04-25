# py-crdt-collab-editor
CRDT based collaborative code/text editor.

## Requirements  
- flask 
- requests
- python3-crdt
  - The editor is dependent on the python3-crdt library which is available on pypi.org and can be installed using 
    ```python
    pip install python3-crdt
    ```
## Usage
Clone the project and then run the following commands
```python

flask run -p 8000 # In one terminal
# Open 127.0.0.1:8000 in browser window


flask run -p 8001 # In another terminal
# Open 127.0.0.1:8001 in another browser window
```
Experience the power of collaborative text editing.

