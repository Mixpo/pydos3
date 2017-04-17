# pydos3
Credential helper for Docker from AWS S3. Credentials will be stored, encrypted, in your preferred S3 bucket under a namespaced prefix. Keeps plaintext Docker credentials off your machine.

## Install

### Prerequisites
* If you are running this on an AWS instance, setup an IAM role with read and write access to the bucket you wish to store your credentials in. For non-AWS machines, ensure your AWS credentials are configured at `~/.aws/credentials`.
* Install boto3 (`[sudo] pip install boto3`)

### Setup
Copy `./pydos3-template` to your $HOME directory as `.pydos3`. Edit this file, adding your preferred bucket and key prefix to store credentials under.

Copy or Symlink `docker-credential-pydos3.py` to `/usr/local/bin/docker-credential-pydos3`. Note that this helper will use the python found at /usr/bin/python. If you have Python installed elsewhere, copy this file to `/usr/local/bin/docker-credential-pydos3` and change the shebang path on line 1.

Setup your Docker client to use this credential helper by modifying your `~/.docker/config.json` to be `{"credsStore": "pydos3"}`

## Manual Testing
If you'd like to verify pydos3 works with your bucket, you can test the interaction by hand.
```bash
$ cat tests/mocks/store | python ./docker-credential-pydos3.py store
$ cat tests/mocks/get | python ./docker-credential-pydos3.py get
{
	"ServerURL": "https://index.docker.io/v1",
	"Username": "david",
	"Secret": "passw0rd1"
}
$ cat tests/mocks/erase | python ./docker-credential-pydos3.py erase
$ cat tests/mocks/get | python ./docker-credential-pydos3.py get
{}
```

## Todo
* Testing
* Improved Error handling (Docker expects error messages to be sent via STDOUT. We need to catch more Exceptions and route the error to STDOUT)
