Cucumber
========

Prototype wallet for web2 accounts.

- Each account is represented by an NFT

- The passwords for the accounts are stored in a TEE coprocessor

- Non-ruggable account transfer. Owner can fully encumber the account before selling it.

- Grant exclusive access to AI agents

- Attested log of how the account is used

- Owner can create teleports and give them out

- Muti-operator and migration provided by Dstack-replicatoor


Running in automation development mode
=================================

The main develpoment step is to load a browser to the relevant state (e.g., just presented captcha or asked to respond to an email challenge to login).

The basic workflow is to load a local browser with Selenium, ideally with an interactive repl like Ipython.

This way the browser can remain visible in the background, and we can rapidly iterate on the selectors and actions.


Running in Docker
=================
```bash
docker run --rm -it -v $(pwd)/auth.json:/workdir/auth.json -v $(pwd)/screens:/workdir/screens cucumber
```


Running (in dev environment)
============================
Set `host.env` according to `host.example`
```bash
docker build -t cucumber . && docker compose up
```
Run in a separate terminal:
```bash
bash test.sh
```
