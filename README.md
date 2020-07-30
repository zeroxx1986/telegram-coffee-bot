# telegram-coffee-bot

### An interactive bot for telegram to schedule events in group chats. (especially, drinking coffee together with friends)

![CI](https://github.com/zeroxx1986/telegram-coffee-bot/workflows/CI/badge.svg)

---

### Requirements:

- [Python 3.x](https://www.python.org/download/releases/3.0/)
- pip
  - part of default windows installation
  - linux users can get it via `sudo apt install python3-pip`
- virtualenv<br>
  `pip install virtualenv`

### Usage:

1. **Make sure you use `virtualenv`.**<br>
     Install it with `pip install virtualenv`, then in the repo root, execute `virtualenv venv`.

2. **Install all dependencies first.**<br>
     Do it via `pip install -r requirements.txt` from repo root.

3. **Have `requirements.txt` up-to-date.**<br>
     After you add a new library via `pip install xxxx`, make sure you update `requirements.txt` too via `pip freeze --local > requirements.txt`

4. **Execute unittests**<br>
     Run `python -m pytest` from repo root.
     
### Nice to know:

We are using [Pytest](https://docs.pytest.org/en/stable/) for testing. Read all about it :)
