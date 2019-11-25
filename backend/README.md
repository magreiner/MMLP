# Medical Machine Learning Platform (MMLP) Backend

## Run backend:
```bash
workon MMLP
python3 app.py

# Update the ssh-checkout-key in repo/backend
# This key is used when a model git repo is accessed to authenticate

# Check the config in repo/backend/mmlp/config.py
```

## Ensure Python 3.7 is available
For ubuntu 18.04 this might help:


sudo add-apt-repository -y ppa:ubuntu-toolchain-r/ppa

sudo apt-fast install -y python3.7 python3.7-dbg python3.7-dev python3.7-venv


sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2
sudo update-alternatives --config python3

cd /usr/lib/python3/dist-packages
sudo ln -s apt_pkg.cpython-36m-x86_64-linux-gnu.so apt_pkg.cpython-37m-x86_64-linux-gnu.so

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && sudo python3.7 get-pip.py && rm get-pip.py

sudo pip3.7 install cython virtualenvwrapper pylint
mkvirtualenv MMLP
pip3.7 install -r requirements.txt
```
