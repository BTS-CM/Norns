# Norns

The norns are three oscillating algorithm based assets on the BTS DEX. They are 120 degrees offset from one another and have an amplitude of 12.612612612% over a period of 28 days.

Check out the simulator spreadsheet to visualise the norns configuration.

Before you can publish price feeds for the Norns, you'll need to be added to the 'approved list of price feed publishers' within each of the asset's smartcoin settings.

### Installation & Usage

The reference price feed Python3 script is implemented using the python-bitshares library, it was designed and tested with Ubuntu in mind so the following instructions may not work for alternative operating systems.

#### Setup Ubuntu software dependencies

`sudo apt-get install virtualenv git libffi-dev libssl-dev python-dev python3-dev python3-pip`

#### Create a virtual environment

Used to keep your Python environment isolated from one another.

```
mkdir Norn_Env
virtualenv -p python3 Norn_Env
echo "source ./Norn_Env/bin/activate" > access_norn_environment.sh
chmod +x access_norn_environment.sh
source access_norn_environment.sh # To activate the environment
```

#### Install Python packages

The following python packages are required for publishing Hertz price feeds.

To properly install the python packages, you must be within the created python virtual environment we created in the previous step. You can do this via `source access_norn_environment.sh`, if successful your terminal prompt will show `(Norn_Env) username@computer_name:~$`.

```
pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install --upgrade wheel
pip3 install requests
pip3 install pendulum
pip3 install bitshares
```

If any of the above commands fail, pip3 will inform you of any missing dependencies you need to install. Please post an issue to this repo for improving docs if this occurs, thanks.

#### Download, configure & test the Norns price feed scripts

From within your user's home directory run the following command:

```
git clone https://github.com/BTS-CM/Norns.git Norns
cd Norns/
```

If you've never used python-bitshares before and haven't created a local wallet then configure the `create_wallet.py` file, providing a `LOCAL_WALLET_PASSWORD` (doesn't need to be your Bitshares password) and the `PRICE_FEED_PUBLISHER_ACTIVE_KEY` (Extracted from the wallet), then run the 'create_wallet.py' script via `python3 create_wallet.py` once.

If you already have created a local python-bitshares wallet, proceed to the next step.

There are two price feed scripts to pick from:

* `parallel_feed.py` : Attempts to publish every block using Pool multiprocessing module. Recommended!
* `feed.py` : No parallel mechanisms, feed publishes over multiple blocks.

The price feed script file requires minor configuration:
Change 'LOCAL_WALLET_PASSWORD' (locally created python-bitshares password, not your real witness account password) and 'account_name' (price feed publisher account name).

Once configured, depending on what script you chose to use, run either the command `python3 feed.py` to publish a single Hertz price feed, or `python3 parallel_feed.py` to test publishing many price feeds.

#### Install the Systemd service

Once you've successfully tested the Hertz price feed script you should consider configuring a SystemD service and timer in order to regularly publish price feeds. The first step is alter the contents of the service file to provide the `username` you're running the script under.

Once you've configured the service file, copy the `norns_feed.service` to the appropriate systemd linux folder using the following command:

```
cp norns_feed.service /etc/systemd/system/norns_feed.service
```

Once you've copied the files to the appropriate folder, run the following commands:

```
sudo systemctl daemon-reload
sudo systemctl enable norns_feed.service
sudo systemctl start norns_feed.service
```

#### Debugging your price feed

If you're experiencing issues with the price feed, run the following command to get a debug error log output:
```
sudo systemctl status norns_feed.service
```

Report any errors to this github, or on the Telegram channel.

You could try the following commands to reset the service:
```
sudo systemctl daemon-reload
sudo systemctl restart norns_feed.service
```
