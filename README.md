# Temporary Credentials for AWS account

Create an alias in your bash_profile:

`alias tc='python ~/path/to/temp_creds.py'`

## Options
`-p` or `--profile`

Provide the profile that you want to use and the script will create temporary credentials for you

## Usage
`tc -p <profile name>`

## Example
_The following credentials are just for demostration_
`tc -p tempcreds`

### Output

```bash
There are no temporary credentials for this profile
Creating a section for this profile..
Existing access key : placeholder
Existing secret key : placeholder
Creating temporary credentials for kubeguide account...
Writing new credentials to file..
New access key : ASIAIEJ62UQVIGY53ZEA
New secret key : sJjBbDdbf13rrSW2BBdEd1IjkqCI6RRYULDpTKwh
New token : FQoDYXdzEB4aDChLsU9pvh73uOh1oSKGAkoK6Dm6dx8MXUDURQtpkgzdO69eSoTDuZzSkdFaheQBjhfgRTvKI0bQYRzqeSug39SRjNQOTcakM1fLSbjKlLqGD3MizNpkiMx+/2WO+AabLfMX6wzim5JoAsV7w7FwRt3TeCwnMmOvqlIzLKdCOm1BAxpWtEzPVwVRQhoA7rL7a5hOX2H/69Fh62T2ybMqnnmsGFJHuxAb1SaGx3dmzpLpVrR5/9UeTuXyHfl5KdsXMRcBEX3G49WGxiGLi3Q9CCcqNYskB0b4hCIwALHhnANfc85gt5bnNkjFLPC2FlkUf9vOOCtZr1f9AjE2jixNMCNXV73rFuGpZw9Pn3vvD0L9a0BCLTcoxqz22AU=
```

### AWS config file

An example of how the ~/.aws/config should look like before you run the `temp_creds.py`:

```bash
[profile mysourceprofile]
output = text
region = eu-west-2

[profile tempcreds]
role_arn = arn:aws:iam::123456789012:role/role-name
source_profile = mysourceprofile
output = text
region = eu-west-2
```

### AWS credentials file

An example of how the ~/.aws/credentials file should look like before you run the script:

```bash
[mysourceprofile]
aws_access_key_id = <ACCESS KEY>
aws_secret_access_key = <SECRET KEY>
```

After running the script, the credentials file should look like this:

```bash
[mysourceprofile]
aws_access_key_id = <ACCESS KEY>
aws_secret_access_key = <SECRET KEY>

[tempcreds-temp]
aws_access_key_id = <NEW ACCESS KEY>
aws_secret_access_key = <NEW SECRET KEY>
aws_session_token = <NEW SESSION TOKEN>
```
