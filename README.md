# Temporary Credentials for AWS account

`asm` is a small CLI tool that allows you to assume your desired role and sets your new credentials in your `aws` directory for you. You can hold multiple profiles for different purposes that point to different `aws` configuration files. In the same profile your can have multiple roles that you can assume and you can select them from the CLI.

When you install `asm`, a directory will be created that is used by the CLI tool under your home directory `~/.assume/`. In there the state file exists that holds information about your current state like the profile you are using, the role you want to assume etc..

```yaml
account: '111122234455'
profile: myprofile
role: myrole
user: myuser
```

## Options and Usage

**choose** : will let you choose a profile you created with a specific user and role
- `asm choose <profile> --user <user> --role <role>`

**whoami** : will tell you which is your current profile
- `asm whoami`

**generate** : will create new credentials for the role you want to assume
- `asm generate`

**show** : will give you the active credentials under the current profile. You can see all credentials, active or not with the flag `--all`
- `asm show`
- `asm show --all`

**clean** : 
- `asm clean`

**config** : can create a profile if you have non selected. `asm` will then give you a series of attributes to fill in to create the profile. If you do have a profile selected already, you can get the value for specific attributes or set a specific attribute to a new value. Last but not least you can add or remove an AWS profile in your current profile.
- `asm config`
- `asm config --get <attribute>`
- `asm config --set <attribute>=<new value>` 
- `asm config --add-profile <user>.<role>:<account>`
- `asm config --delete-profile <user>.<role>` to delete one role
- `asm config --delete-profile <user>` to delete all roles

**help** : will give you the `--help` output
- `asm help`

## Install for development

You can easily install using `pip` for local development.

command : `pip install . -vvv` for extended output on what happens under the hood


## Profile structure

```yaml config: /Users/giorgosdimitirou/.aws/config
credentials: /Users/giorgosdimitirou/.aws/credentials
credentials_profile:
  myuser:
    Admin: '111122234455'
duration: '86400'
name: clz
output: table
region: eu-west-1
```
```yaml
credentials   : the path to your credentials file
myuser        : the user you want to use to assume your desired role
Admin         : the role you want to assume
111122234455  : the account the role is in
duration      : how long the temporary credentials will last for
name          : the name of the profile (has nothing to do with AWS)
output        : your desired output (text, table, json, etc)
region        : the region you are calling apis against
```