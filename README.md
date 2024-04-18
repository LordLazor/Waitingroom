# Waitingroom Discord Bot

This is a simple Waiting Room Bot created for the final code challenge in Python on Codedex.

---

### config.json

```json
{
    "channel_name": "Waitingroom",  // The name of the channel as a string that the bot should connect to
    "sound_file": "sound.mp3",      // The name of the sound file as a string that the bot should play on loop while connected 
    "token": "ENTER YOUR BOT TOKEN" // Your Bot Token
}
```

---

### commands
* **/join** - The bot joins the channel specified in the config
* **/leave** - The bot leaves the current channel
* **/set_channel** - A string of the channel name
* **/set_sound** - A string of the sound file (you need to add the file extension)

The command **/set_channel** has all voice channels as options. The command **/set_sound** has presets as options.

---

Created for Codedex | Enjoy