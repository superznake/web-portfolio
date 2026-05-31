#!/bin/bash
docker rm -f web_portfolio
git stash
git pull origin main
chmod +x upd.sh
docker build -t web_portfolio:latest .
docker run --name web_portfolio -p 0.0.0.0:62000:62000 -v $(pwd):/app web_portfolio:latest