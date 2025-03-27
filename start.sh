#!/bin/bash

python run.py 8061 &

jupyter notebook --ip 0.0.0.0 --NotebookApp.token='' --NotebookApp.password='' --no-browser --notebook-dir "./notebooks/" --allow-root --port=8062
