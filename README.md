# Plume Testnet 🤖

## Prerequisites

- Python 3.11
- Git

### 🛠️ Installation and setting up

1. ***Clone the repository on local machine:***

```bash
git clone https://github.com/StalkerBlack/Plume-Testnet
cd Plume-Testnet
```

2. ***Creating and activation virtual environment***

- Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
- macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. ***Installing dependencies***
```bash
pip install -r requirements.txt
```

4. ***Add proxies / private keys / CapMonster API Key***

- Add ***proxies*** in `data/proxies.txt` file
- Add ***private keys*** in `data/privates.txt` file
- Add ***CapMonster API Key*** in `config.py` file  ***->***  **[CapMonster site](https://capmonster.cloud/)**

5. ***If you want change settings***
```python
SLEEP_MODE = True                        # Sleep between wallets
SLEEP_TIME = (480, 900)                  # 8 - 15 minutes
SHUFFLE_WALLETS = True                   # Shuffle wallets or not
WALLETS_TO_WORK: int | tuple | list = 0
                                         # 0 - all wallets
                                         # 1 - current wallet
                                         # (1, 7) - certain wallets (1 wallets and 7 wallet)
                                         # [5, 25] - from 5 to 25 including
```

[//]: # (## Support ❤️)

[//]: # (*It you find any optimal solution or have any questions, please [Contact Us]&#40;https://t.me/degen_software&#41;*)

## Questions and suggestions

If you have any questions, suggestions and improvements, please write an issue, or write DM to *@munchen777* or *@missio_deo*

