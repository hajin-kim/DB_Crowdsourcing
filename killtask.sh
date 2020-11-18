# usage:
# on ~/DB_Crowdsourcing/, use "sh killtask.sh" command at terminal
PORT=8000
sudo lsof -t -i tcp:${PORT} | xargs kill -9