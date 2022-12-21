# **HammerBot Discord bot Framework (HDF)**

![HammerBot profile image](https://cdn.discordapp.com/avatars/1032295279346589718/c6da982d2c35434984023d7275da4374.png?size=256)

Hammerbot Discord bot Framework is a modular Discord bot framework that is founded on a directory based plugin approach. It uses [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html) for its structure and for the used plugins.

Creating a new bot for every little feature is tedious and unnecessary. This framework will help you reduce a significant portion of cognitive overhead to get a discord bot running.

---
## **Installation instructions**
To use HDF you first have to clone the repo and preferably setup a python venv to install requirements into

```
git clone https://github.com/rathmerdominik/hammerbot
cd hammerbot
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
cp config.dist.toml config.toml
```
---
## **Configuring the application**

Before you start the bot you have to put your Discord API token inside the `config.toml` file. To obtain an API Token please visit [this](https://discord.com/developers/applications/) site and create an Application there.

You will also have to put owner IDs in there. Normally that would be your discord ID or the IDs of your staff.

You can also configure the warning log level inside there as well with [these](https://docs.python.org/3/library/logging.html#logging-levels) values 

In case you need a different log formatting you can use [these](https://docs.python.org/3/library/logging.html#logging-levels) formatting options in the config

---

## **Installing a Plugin**

**If** the Plugin developer did everything right it is as easy as just putting the folder into the `hammerbot/modules` directory and starting the bot with `python app.py`

As a developer you can use the `core` module as a guideline how the entrypoint has to look like. 

It is **imperative** to use the same name for the entry point file as you did for the folder else the program will exit with a warning that the file could not be loaded. 

You are allowed to put any other file you wish inside your project e.g config files or similiar necesseties as long as the entry file exists

---
## **Usable commands**

*All commands work as slash commands when registered and synced with the command tree*
### HBF already comes with a set of pre-installed commands.

`restart_bot # Restart the entire bot process`

`close_bot # Closes the entire bot process`

### HBF also has the `core` module pre-packaged. This can be disabled or entirely removed but I recommend not to do that

### These commands are included in the core module
`get_all_modules # Prints all modules that were found`

`disable_module <module> # Disables a module for the current bot session`

`enable_module <module> # Enables a module`

`reload_module <module> # Reloads a module. Useful for development`

`sync # Syncs all commands to the command tree and therefore allows slash commands to be used`