if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/imVipin/findpdf.git /findpdf
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /findpdf
fi
cd /findpdf
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
