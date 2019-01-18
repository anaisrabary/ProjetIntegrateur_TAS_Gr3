# Projet Intégrateur TAS

## Summary
* [Bibliographic](biblio)
* [Deployment](deployment)

## Attention:
* Using library **SystemML** to deploy Keras in Spark has an error on import (test in Python 3 failed)

## SSH's GPU access:

1. Access in ssh
```bash
ssh <login>@insa-<machine-id>
```
**machine-id**: 10585 10583

Type password of your INSA login

1. **conda** is not available in your terminal, you have to reload the bash:
```bash
source ~/.bashrc
```
Check conda:
```bash
conda --version
```
