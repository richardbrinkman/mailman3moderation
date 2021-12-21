# mailman3moderation

Mailman is free software for managing electronic mail discussion and e-newsletter lists. 
It consists of a web page for maillist configuration as well as a core that does the heavy
lifting of actually sending the mails.

One of the tasks of a maillist owner is to ensure that no spam is being send over the list.
Mailman has the concept of moderation where the maillist owner acts as a human spam filter
for (parts of) the emails that are being send to the list. Handling this moderation is
usually done with the web interface.

The Python script in this project, however, provides a command line interface to the Mailman
moderation. Especially if the maillist owner has to moderate a large collection of lists,
this script will reduce the time he/she spends on moderation.

For version 2 of Mailman, there exists a command line tool called
[listadmin](https://sourceforge.net/projects/listadmin/) which is written in Perl.
This Python script is a similar tool for version 3 of Mailman.

## Installation

Simply clone this tool from github by invoking this command in a shell:

```sh
git clone https://github.com/richardbrinkman/mailman3moderation.git
```

It will create a mailman3moderation directory in the current directory with the script
itself (`moderate.py`) and a sample configuration script (`config_sample.py`). Copy the latter
to a new file called `config.py` and adjust the settings within it.

## Usage

Simply run

```sh
python3 moderate.py
```

from within the `mailman3moderation` directory.
It will scan all the maillists found on the server. For all the waiting moderation requests
an entry pops up, showing the bare essentials, like subject and sender. You have then the option
to show the headers and/or the body prior to accepting, discarding or rejecting the mail.
