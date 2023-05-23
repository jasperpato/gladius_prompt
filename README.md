# Gladius Prompt

A parser and read–eval–print (REPL) loop for the GLADIUS command syntax described in the project spec for CITS5501 Sem 1 2023.

Responds with 'OK' on valid commands and 'Error' on invalid commands.

If an invalid line is given within the "air book req" command, the command is aborted and 'Error' is printed.

This program uses only standard libraries and can be executed with python3.8+ with

```console
python3 src/gladius_prompt.py
```

It is also available on Docker Hub as an image.

### Run from Docker

Must be run in interactive mode.

```console
docker pull dey45/gladius_prompt
docker run -it dey45/gladius_prompt
```

### Run from GitHub

```console
git clone https://github.com/jasperpato/gladius_prompt
cd gladius_prompt
python3 src/gladius_prompt.py
```

### Example commands

- shop flight fares AAA AAB OneWay C 2023-08-01
- air book req

  seg AAA AAB AA1 2023-08-01 C 5

  EOC

### Test

```console
python3 -m unittest tests/test_gladius_prompt.py
```

Jasper Paterson 22736341
