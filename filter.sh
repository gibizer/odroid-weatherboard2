sudo systemctl stop weatherboard.service 
sleep 3
python3 filter.py 
sudo systemctl restart weatherboard.service 

