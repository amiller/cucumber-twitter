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
