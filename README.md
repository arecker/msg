# MSG

The deployment tool that is a little like [salt](http://saltstack.com/), only not as good for you.

[![Build Status](http://travis-ci.org/arecker/msg.svg?branch=master)](http://travis-ci.org/arecker/msg) [![Coverage Status](https://coveralls.io/repos/arecker/msg/badge.svg?branch=master&service=github)](https://coveralls.io/github/arecker/msg?branch=master)

## Usage

Just create a configuration file that looks kind of like this:

```yml
# config.yml
# ----------

host:
  prod: 'my-prod-host'
  stage: 'my-stage-host'

servos:
  - handshake
  - install:
      packages:
        - build-essential
        - python
        - python-pip
```

Run the command

```shell
$ msg prod ./config.yml
```

And watch what happens on your server!

```shell
$ echo "Helloooooo from msg"
$ sudo apt-get install -y build-essential python python-pip
```
