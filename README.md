# PyShows

PyShows is a tool for keeping up to date with your favorite tv shows.
With 5 simple steps you'll never have to worry about downloading the episodes when they are released.

### Clone or download the repository & install requirements
Download the repository and put the content in a path that won't change
Make sure you have python2.7 installed and the latest version of pip.
Run the following command:
```sh
pip install -r requirements.txt
```

### Edit shows.json to contain the shows you are watching
Edit the file to have the shows you are watching and the next episode to download.
You only have to do this once, the script will update the file each time it runs. However, you can always add/remove shows from the file :)
Here's an example:
```json
{
    "Family Guy": {
        "episode": 5,
        "season": 15
    },
    "Supernatural": {
        "episode": 5,
        "season": 12
    },
    "Westworld": {
        "episode": 6,
        "season": 1
    }
}
```

### Configure uTorrent's web api
In uTorrent's settings turn on the WebUI and choose a port, username and password.
And also set the default downloads folder. (e.g. The folder that plex will scan for tv shows)

### Edit config.py with your uTorrent credentials
```python
UTORRENT_USER = 'user'
UTORRENT_PASS = 'pass'
UTORRENT_URL = '127.0.0.1'
UTORRENT_PORT = 57274
```

### For mac or linux create a cron (For windows try a different scheduling options)
Run the following command:
```sh
crontab -e
```
This will open an editor where you will write the cron. This example will run the cron every day at 6 a.m.
```sh
0 6 * * *	cd <downloaded repository path> && ./main.py > /tmp/pyshows.log 2> /tmp/pyshows.err.log
```

That's It!
----
Now everyday at 6 a.m. the script will check for new new episodes and download them.

**Enjoy!**
