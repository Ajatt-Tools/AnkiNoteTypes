# AnkiNoteTypes

[![Chat](https://img.shields.io/badge/chat-join-green.svg)](https://tatsumoto-ren.github.io/blog/join-our-community.html)
[![Channel](https://shields.io/badge/channel-subscribe-blue?logo=telegram&color=3faee8)](https://t.me/ajatt_tools)
[![Patreon](https://img.shields.io/badge/patreon-support-orange)](https://www.patreon.com/bePatron?u=43555128)

A collection of user-created note types for Anki 2.1. It includes a super user-friendly mechanism of importing and exporting them, and everyone is welcome to add their templates by making a pull request.

## Installation

### GNU/Linux

Install [Python](https://wiki.archlinux.org/title/Python) 3.10 or later if you haven't already.

### Windows

Install Python from the Microsoft Store or check if you already have the good version putting on your file explorer search bar
````
%LOCALAPPDATA%\Microsoft\WindowsApps\python3
````
If you have the correct version, you can just close the python's window that just popped up and execute the [following commands](https://github.com/Ajatt-Tools/AnkiNoteTypes?tab=readme-ov-file#importing)

**Make sure to add python3 in your PATH**

**The path you need to add should look like C:\Users\[YourUsername]\AppData\Local\Microsoft\WindowsApps\python3**

If you don't have the python installed, when you'll put this command into the search bar, it will open a microsoft store window directly on the correct python version and you just need to click Download

After doing this step, you can make sure that everything is good by opening the command prompt with ``Windows+R``, ``cmd`` and put the command:

```
python3 -m
```

If everything's good, you should get a response like : ``Argument expected for the -m option``

When you're done, you can import the different available note types [here](https://github.com/Ajatt-Tools/AnkiNoteTypes?tab=readme-ov-file#importing)

## Usage

Make sure Anki is running, and you have
[AnkiConnect](https://ankiweb.net/shared/info/2055492159)
installed.

Clone the repository and `cd` into it.
If you have never cloned a repository before,
you need to install [git](https://git-scm.com/).
If you have `git` installed,
open your terminal and type the following commands.

```
git clone "https://github.com/Ajatt-Tools/AnkiNoteTypes.git"
cd AnkiNoteTypes
```

### Importing

To import one of the
[available Note Types](https://github.com/Ajatt-Tools/AnkiNoteTypes/tree/main/templates)
to Anki, run:

```
./antp.sh import
```

https://user-images.githubusercontent.com/69171671/143988488-ff70960c-840c-48e2-90d3-a24468da8942.mp4

### Updating

If you imported a note type from this collection before,
it received an update,
and you want to import the new version, run:

```
./antp.sh update
```

### Exporting

To export one of your Note Types, run:

```
./antp.sh export
```

Then write a helpful readme and commit your changes:

```
git add templates fonts && git commit
```

After committing your template, please [create a pull request](https://github.com/Ajatt-Tools/AnkiNoteTypes/pulls).
