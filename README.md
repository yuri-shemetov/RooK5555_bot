# Rook5555_bot

## Exemple for copy files

```bash
scp /home/yuri/folder/my_local_settings.py ssh root@195.58.54.37:/root/Rook5555_bot/src
```

## Start app

1. From Linux terminal: ssh root@195.58.54.37 and enter password
2. Steps: 
	a) cd Rook5555_bot 
	b) poetry shell
	c) cd src
	d) nohup python main.py startapp &

## Stop app:

    a) ps aux | grep main.py
    b) kill <PID>
    c) Force Kill (if necessary): kill -9 <PID> - 

## Sources

### for BTC
https://iancoleman.io/bip39/

### for USDT
https://www.iancoleman.net/tron-network/
https://trongrid.io/

### OpenSSL

/etc/ssl/openssl.cnf

``` bash
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```
