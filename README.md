# travianium
UPDATE: This is most likely outdated, however if you want to build your own bot you can see it as an example.

Automated Travian game using Selenium+Python.


To run it you would need to setup a chatbot on telegram. The idea of this bot was to fully run Travian just by interacting with Telegram. By sending a specific command you could operate the bot, for example you could get info about the village or run auto-farmer. 

List of implemented commands:

    'Available commands:'
    'info - get current resources, storage capacity, incoming attack and building queue status'
    'army - get current stationary troops'
    'notifier - turn on/off notifier. New message will be sent whenever:'
    '     -your village is under attack'
    '     -hero and adventure are both available'
    '     -a new building has been finished'
    '     -storage is over 90% capacity'
    'farmer - turn on/off farmer. Raids villages/oasis defined in farm_list.txt in a cycle. Sleeps '
    'for random time when no troops are available.'
    'builder - builds buildings defined in build_queue in order. Does not build resource fields or '
    'construct new buildings.'
