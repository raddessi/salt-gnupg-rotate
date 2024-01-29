# Encrypt and rotate encryption on a Salt pillar

Let's generate some encrypted pillars and then rotate the keys on them.

## Setup

### Install packages

````{tab} pipx
```
pipx install salt-gnupg-rotate yq
```
````

````{tab} pip
```
pip install salt-gnupg-rotate yq
```
````

### Make tutorial directories to work in

We will create a new directory for some test pillars and a directory for a
temporary gnupg keyring:

````{tab} Linux
```shell
mkdir -p rotate-tutorial/{.gnupg/private-keys-v1.d,pillar}
cd rotate-tutorial
chmod 700 .gnupg
```
````

### Tell `gpg` to use this new keyring home directory

````{tab} Linux
```shell
export GNUPGHOME=$(pwd)/.gnupg
echo $GNUPGHOME
```
````

### Create the new keyring and list the keys

````{tab} Linux
```shell
# this will create the empty keyring
gpg --list-keys

# now we can create a new key
echo "Key-Type: 1
Key-Length: 2048
Subkey-Type: 1
Subkey-Length: 2048
Name-Real: salt-controller-key1
Name-Email: tutorial@foo.bar
Expire-Date: 0
%no-protection" | gpg --batch --gen-key
```
````

Now list the available secret keys, you should see the key
`salt-controller-key1`:

````{tab} Linux
```shell
gpg --list-secret-keys
```
````

## Create some encrypted files

Let's create a completely encrypted file with the contents `Hello!`, using the
encryption key `salt-controller-key1` and then verify that we can decrypt it:

````{tab} Linux
```shell
# create the encrypted file
echo -n 'Hello!' | gpg --encrypt --armor -r salt-controller-key1 > pillar/encrypted_file.gpg

# decrypt the file using the original key
cat pillar/encrypted_file.gpg| gpg --decrypt
```
````

Now let's create a yaml file with one value that has been encrypted:

````{tab} Linux
```shell
# encrypt some secret data
echo -n "my-secret-value" | gpg --encrypt --armor -r salt-controller-key1

# create a yaml pillar with an encrypted value
vim pillar/encrypted_pillar.sls
```
````

You will need to create a file with a structure similar to:

```yaml
my-secret-key: |
  -----BEGIN PGP MESSAGE-----

  <encrypted data>
  -----END PGP MESSAGE-----
```

Once the file has the correct format and encrypted data save and exit your
editor.

## Create a new secret key we can use to rotate encryption

````{tab} Linux
```shell
echo "Key-Type: 1
Key-Length: 2048
Subkey-Type: 1
Subkey-Length: 2048
Name-Real: salt-controller-key2
Name-Email: tutorial@foo.bar
Expire-Date: 0
%no-protection" | gpg --batch --gen-key
```
````

Now list the available secret keys, now you should see both of the keys
`salt-controller-key1` and `salt-controller-key2`:

````{tab} Linux
```shell
gpg --list-secret-keys
```
````

## Rotate encryption using `salt-gnupg-rotate`

First you can just verify that the script can decrypt and re-encrypt the data
using the specified key `salt-controller-key2` for re-encryption without errors
by running without the `--write` flag:

````{tab} Linux
```shell
salt-gnupg-rotate \
    --directory ./pillar \
    --decryption-gpg-homedir .gnupg \
    --encryption-gpg-homedir .gnupg \
    -r salt-controller-key2
```
````

This should run without error, listing each of the files loaded from the
`pillar/` directory.

Now let's re-run that same command but at a higher logging verbosity so that we
can see the contents of the decrypted and re-encrypted blocks in the files:

````{tab} Linux
```shell
salt-gnupg-rotate \
    --directory ./pillar \
    --decryption-gpg-homedir .gnupg \
    --encryption-gpg-homedir .gnupg \
    -r salt-controller-key2 \
    -l trace
```
````

Let's actually write the changes out to disk this time after re-encryption:

````{tab} Linux
```shell
salt-gnupg-rotate \
    --directory ./pillar \
    --decryption-gpg-homedir .gnupg \
    --encryption-gpg-homedir .gnupg \
    -r salt-controller-key2 \
    --write
```
````

## Check that the encrypted data was rotated

To do this we will delete the key that was originally used to encrypt the
pillars `salt-controller-key1` and then try to decode them using only the new
key `salt-controller-key2`.

First let's delete the key `salt-controller-key1``:

````{tab} Linux
```shell
fingerprint=$(gpg --list-keys salt-controller-key1 | grep -Ev '^(pub|sub|uid)' | head -n1 | awk '{print $1}')
gpg --batch --yes --delete-secret-key "${fingerprint}"
gpg --batch --yes --delete-key "${fingerprint}"
```
````

Now let's try to decrypt the encrypted data:

````{tab} Linux
```shell
cat pillar/encrypted_file.gpg | gpg --decrypt
cat pillar/encrypted_pillar.sls | yq '."my-secret-key"' -r | gpg --decrypt
```
````

Both of the values should decrypted using the new key `salt-controller-key2` 🚀
