<p align="center">
<a href="https://github.com/sgrkmr/ciphit"><img alt="Ciphit" src="https://user-images.githubusercontent.com/57829219/84270533-7492e380-ab48-11ea-9270-8531ea72ac6e.png"></a>
</p>

<p align="center">
<a href="https://pypi.org/project/ciphit/"><img alt="PyPi" src="https://img.shields.io/pypi/v/ciphit.svg"></a>
<a href="https://pypi.org/project/ciphit/"><img alt="Downloads" src="https://img.shields.io/pypi/dm/ciphit.svg"></a>
<a href="https://github.com/sgrkmr/ciphit/commits/master"><img alt="Commits" src="https://img.shields.io/github/last-commit/sgrkmr/ciphit"></a>
<a href="https://pypi.python.org/pypi/ciphit/"><img alt="python3" src="https://img.shields.io/pypi/pyversions/ciphit.svg"></a>
<!--<a href="https://GitHub.com/sgrkmr/ciphit/graphs/contributors/"><img alt="Contributors" src="https://img.shields.io/github/contributors/sgrkmr/ciphit.svg"></a>-->
<a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/github/license/sgrkmr/ciphit.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

<h1 align="center">⚠️DEPRECATED⚠️</h1>

<p align="center">
<code>ciphit</code> is a basic cryptography cli-tool, Currently only supports AES-CBC.
</p>

---
<!--
# Screenshots
![scrn](https://user-images.githubusercontent.com/57829219/84272798-81fd9d00-ab4b-11ea-89e2-c712a16c00a3.png)
-->

## Installation and Usage
### Installation

_ciphit_ can be installed by running `pip install ciphit`.

#### Install from GitHub

If you want to install from GitHub, use:

`pip install git+git://github.com/sgrkmr/ciphit`

### Usage

### Command line options

Currently _ciphit_ doesn't provide many options. You can list them by running `ciphit --help`:

```text
Usage: ciphit [OPTIONS]

Options:
  Encode/Decode: [mutually_exclusive, required]
    -e, --encode
    -d, --decode
    --edit                        To edit Encrypted/Encoded files created by
                                  ciphit.

  -k, --key TEXT                  The key with which text is Encoded/Decoded.
  Text/File: [mutually_exclusive]
    -t, --text TEXT               The text you want to Encode/Decode.
    -f, --file FILENAME
  --help                          Show this message and exit.
```

<p><b>Make sure you run these commands in Terminal/CMD or any other shell you use.</b></p>

## Examples

Same commands in _ciphit_ can be used in different variants, for eg:

### Decoding `-d`/`--decode`

- Passing all parameters, i.e. `-k` for _key_, `-t` for _text_

```console
$ ciphit -dk password -t "BAxEtd2AO8EGuqIbmVbFQwABhqCAAAAAAF9-z7EjDVV13bKOTLIF-FDXF921sNfGhnSShod4CFHezycHLXQ08AqvBwQoT1zmOd9jt2gZf3VBSHyzfyrsdnvnQ-r5jJPpUKHTlWsZ7i-CW10LmhHzfsBXuQ7b9A4E5DD4EtY="
Final result: Just so you know, this is a text.
```

- Passing only _text_

```console
$ ciphit -dt "BAxEtd2AO8EGuqIbmVbFQwABhqCAAAAAAF9-z7EjDVV13bKOTLIF-FDXF921sNfGhnSShod4CFHezycHLXQ08AqvBwQoT1zmOd9jt2gZf3VBSHyzfyrsdnvnQ-r5jJPpUKHTlWsZ7i-CW10LmhHzfsBXuQ7b9A4E5DD4EtY="
Key:
Repeat for confirmation:
Final result: Just so you know, this is a text.
```

- **OR** You can just pass `-d`/`--decode`, other parameters will be asked as a prompt:

```console
$ ciphit -d
Key:
Repeat for confirmation:
Opening editor # Enter the ciphered text in editor then save & exit.
Press any key to continue ...
Final result: Just so you know, this is a text.
```

Similarly other commands can be used.

## License
Licensed under [MIT](https://opensource.org/licenses/MIT).
