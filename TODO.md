## `ciphit` What's Next?

> **note:** further work on the proj will continue from ~June 2021

### Todo

- [x] move from `asciimatics` to `click` & ~~`py-cui`~~
- [x] use `poetry`
- [ ] have `-e/--encode`, `-d/--decode`, `--edit` as commands instead of options
- [ ] change `encode` -> `encrypt` & `decode` -> `decrypt`
- [ ] use `edit` command only for files and remove the necessity to use `-f` with `edit` for passing the file path, do this:
    - `edit <path>` instead of `--edit -f <path>`
- [ ] make an interface for easy integration of ciphers, crypto, etc..
    * core/
    	* Crypto/
    	* Ciphers/
    * iface/
    	* `__init__.py`
    	* `structure.py` <!--# or something-->
    	* `_modules.py`
    	* `_config.py`
    	* `_registry.py`
- [ ] add more ciphers
    * morse
    * binary
    * hexadecimal
    * ceaser
    * ...
