import os
import sys
from sys import argv
from pathlib import Path
from base64 import b64encode, b64decode

try:
    from asciimatics.event import KeyboardEvent
    from asciimatics.widgets import (Frame, ListBox, Layout, FileBrowser, Divider, Text, Button, TextBox, Widget, Label, PopUpDialog)
    from asciimatics.scene import Scene
    from asciimatics.screen import Screen
    from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto import Random
except ImportError:
    print('ERROR: Couldn\'t find required modules!')
    if input('Do you want to install them now? (y/n): ') == 'y':
        os.system('pip3 install asciimatics pycrypto')
        raise SystemExit

__author__ = 'Sagar Kumar'
__version__ = '0.1.2'

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

#CBC method with PKCS#7 padding
class Crypt:
    def __init__(self, salt=Random.new().read(AES.block_size)):
        self.salt = salt
        self.enc_dec_method = 'latin-1'

    def encrypt(self, src, key, encode=True):
        src = src.encode()
        key = SHA256.new(key.encode()).digest()
        aes_obj = AES.new(key, AES.MODE_CBC, self.salt)
        padd = AES.block_size - len(src) % AES.block_size
        src += bytes([padd]) * padd
        hx_enc = self.salt + aes_obj.encrypt(src)
        return b64encode(hx_enc).decode(self.enc_dec_method) if encode else hx_enc

    def decrypt(self, src, key, decode=True):
        if decode:
            str_tmp = b64decode(src.encode(self.enc_dec_method))
        key = SHA256.new(key.encode()).digest()
        salt = str_tmp[:AES.block_size]
        aes_obj = AES.new(key, AES.MODE_CBC, salt)
        str_dec = aes_obj.decrypt(str_tmp[AES.block_size:])
        padd = str_dec[-1]
        if str_dec[-padd:] != bytes([padd]) * padd:
            pass
        return str_dec[:-padd].decode(self.enc_dec_method)

def win_ansi_init():
    if __import__('platform').system().lower() == 'windows':
        from ctypes import windll, c_int, byref
        stdout_h = windll.kernel32.GetStdHandle(c_int(-11))
        mode = c_int(0)
        windll.kernel32.GetConsoleMode(c_int(stdout_h), byref(mode))
        mode = c_int(mode.value | 4)
        windll.kernel32.SetConsoleMode(c_int(stdout_h), mode)

class CryptModel:
    src = None
    key = None
    res = None

class Simple_Crypt(Frame):
    def __init__(self, screen, desc):
        super(Simple_Crypt, self).__init__(screen,
                                   screen.height * 2 // 3,
                                   screen.width * 2 // 3,
                                   hover_focus=True,
                                   can_scroll=False,
                                   title="Cryptify")
        self.set_theme("monochrome")
        self.crypt = Crypt()
        self.desc = desc
        self._main()

    def _main(self):
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.src = TextBox(
            Widget.FILL_FRAME, f'{self.desc}:', self.desc.lower(), as_string=True, line_wrap=True)
        self.key = Text("Key:", "key", hide_char='*')
        layout.add_widget(self.src)
        layout.add_widget(self.key)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def _ok(self):
        CryptModel.src = self.src.value
        CryptModel.key = self.key.value
        if self.desc.lower() == 'encrypt':
            CryptModel.res = self.crypt.encrypt(repr(CryptModel.src), CryptModel.key)
        else:
            CryptModel.res = '\n'.join(self.crypt.decrypt(CryptModel.src, CryptModel.key).strip("'").split('\\n'))
        raise NextScene("end")

    @staticmethod
    def _cancel():
        raise StopApplication("")

class Simple_Crypt_Res(Frame):
    def __init__(self, screen, desc):
        super(Simple_Crypt_Res, self).__init__(screen,
                                   screen.height * 2 // 3,
                                   screen.width * 2 // 3,
                                   on_load=self._reload,
                                   hover_focus=True,
                                   can_scroll=False,
                                   title="Cryptify")
        self.set_theme("monochrome")
        self.desc = desc
        self._main()

    def _main(self):
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.src = TextBox(
            Widget.FILL_FRAME, f'{self.desc}ed:', self.desc.lower(), as_string=True, line_wrap=True)
        layout.add_widget(self.src)
        layout2 = Layout([1,1])
        self.add_layout(layout2)
        layout2.add_widget(Divider(),0)
        layout2.add_widget(Divider(),1)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Copy", self._cpy), 1)
        self.fix()

    def _reload(self):
        #self.src.disabled = True
        self.src.value = CryptModel.res

    def _cpy(self):
        if __import__('platform').system().lower() == 'windows':
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(CryptModel.res, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()

    def _ok(self):
        raise StopApplication("")

class File_Select(Frame):
    def __init__(self, screen, *args):
        super(File_Select, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="Cryptify")

        self.set_theme("monochrome")
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)

        self._list = FileBrowser(Widget.FILL_FRAME,
                                 os.path.abspath("."),
                                 name="mc_list",
                                 on_select=self.popup)
        layout.add_widget(Label("Please select the file to {}.".format(args[0].lower())))
        layout.add_widget(Divider())
        layout.add_widget(self._list)
        layout.add_widget(Divider())
        layout.add_widget(Label("Press Enter to select or `q` to quit."))

        self.fix()

    def popup(self):
        #self._scene.add_effect(
        #    PopUpDialog(self._screen, "You selected: {}".format(self._list.value), ["OK"]))
        CryptModel.src = self._list.value
        raise NextScene("end")

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        return super(File_Select, self).process_event(event)

class File_Crypt(Frame):
    def __init__(self, screen, desc):
        super(File_Crypt, self).__init__(screen,
                                   screen.height // 5,
                                   screen.width // 2,
                                   hover_focus=True,
                                   can_scroll=False,
                                   title="Cryptify")
        self.set_theme("monochrome")
        self.crypt = Crypt()
        self.desc = desc
        self._main()

    def _main(self):
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.key = Text("Key:", "key", hide_char='*')
        layout.add_widget(self.key)
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider(),0)
        layout2.add_widget(Divider(),1)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def _ok(self):
        try:
            if CryptModel.src is None:
                src = argv[2]
            else:
                src = CryptModel.src
            with open(src, 'r+', encoding='utf-8') as f:
                CryptModel.key = self.key.value
                if self.desc.lower() == 'encrypt':
                    CryptModel.src = f.readlines()
                    enc = self.crypt.encrypt(repr('\n'.join([i.strip('\n') for i in CryptModel.src])), CryptModel.key)
                else:
                    CryptModel.src = f.read()
                    enc = '\n'.join(self.crypt.decrypt(CryptModel.src.strip(),CryptModel.key).strip("'").split("\\n"))
                f.truncate(0)
                f.seek(0)
                f.write(enc)
            if enc != None:
                raise EOFError
        except EOFError:
            raise NextScene("pass")
        except:
            raise NextScene("fail")

    @staticmethod
    def _cancel():
        raise StopApplication("")

class Crypt_Bubble(Frame):
    def __init__(self, screen, msg):
        super(Crypt_Bubble, self).__init__(screen,
                                        screen.height // 5,
                                        screen.width // 2,
                                        on_load=self._load,
                                        hover_focus=True,
                                        can_scroll=False)
        self.msg = msg
        if self.msg.lower() == 'failure':
            self.set_theme('warning')
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.msgbox = Label('',align='^')
        layout.add_widget(self.msgbox)
        layout2 = Layout([100])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        self.fix()

    def _load(self):
        self.msgbox.text = self.msg

    @staticmethod
    def _ok():
        raise StopApplication("")

class File_Edit_Auth(File_Crypt):
    def _ok(self):
        CryptModel.key = self.key.value
        raise NextScene("edit")

class File_Edit(Frame):
    def __init__(self, screen, desc):
        super(File_Edit, self).__init__(screen,
                                   screen.height * 2 // 3,
                                   screen.width * 2 // 3,
                                   on_load=self._reload,
                                   hover_focus=True,
                                   can_scroll=False,
                                   title="Cryptify")
        self.set_theme("monochrome")
        self.crypt = Crypt()
        self.desc = desc
        self._main()

    def _main(self):
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.src = TextBox(
            Widget.FILL_FRAME, f'{self.desc}:', self.desc.lower(), as_string=True, line_wrap=True)
        layout.add_widget(self.src)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 1)
        self.fix()

    def _reload(self):
        try:
            if argv[2]:
                self.srcf, CryptModel.src = argv[2], argv[2]
                
        except:
            self.srcf = CryptModel.src
        finally:
            if not (CryptModel.src is None or CryptModel.key is None):
                with open(self.srcf, 'r+', encoding='utf-8') as f:
                    dec = f.read()
                    dec = '\n'.join(self.crypt.decrypt(dec.strip(),CryptModel.key).strip("'").split("\\n"))
                self.src.value = dec

    def _ok(self):
        with open(self.srcf, 'w', encoding='utf-8') as f:
            print(self.src.value)
            wrt = self.crypt.encrypt(repr('\n'.join([i.strip('\n') for i in self.src.value.split('\n')])), CryptModel.key)
            f.write(wrt)
        raise StopApplication("")

    @staticmethod
    def _cancel():
        raise StopApplication("")

def __show__(func):
    def inner(*args, **kwargs):
        last_scene = None
        while True:
            try:
                Screen.wrapper(func, catch_interrupt=True, arguments=[last_scene])
                raise SystemExit
            except ResizeScreenError as e:
                last_scene = e.scene
    return inner


def start(desc, *args, **kwargs):
    try:
        if kwargs['end']: pass
    except:
        kwargs['end'] = None
    try:
        if kwargs['add']: pass
    except:
        kwargs['add'] = None
    @__show__
    def _init(screen, scene):
        scenes = [
            Scene([kwargs['start'](screen, desc)], -1, name="main")
        ]
        if not kwargs['end'] is None:
            scenes.append(Scene([kwargs['end'](screen, desc)], -1, name="end"))
        if not kwargs['add'] is None:
            for i in kwargs['add']:
                scenes.append(Scene([i[0](screen, i[2])], -1, name=i[1]))

        screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)
    _init()

def _main():
    pram = ["-e", "-d", "-ef", "-df", "-t"]
    try:
        if (len(argv[1:]) >= 2 and (argv[1] in pram[:2]+['-V'])) or (len(argv[1:]) >= 3 and (argv[1] in pram[2:])):
            print(f"{color.RED+color.UNDERLINE}ERROR:{color.END+color.YELLOW} Improper command{color.END}")
            exit(1)
        if len(argv[1:]) == 0:
            raise Exception
        if argv[1] == '-V' and len(argv[1:]) == 1:
            print(f"{color.YELLOW+color.BOLD}cpt {color.BLUE+__version__+color.END}")
            raise SystemExit
        if argv[1] not in pram:
            print(f"{color.RED+color.UNDERLINE}ERROR:{color.END+color.YELLOW} Command not found \"{argv[1]}\"{color.END}")
            exit(1)
        #if (argv[1] in pram[2:]) and len(argv[1:]) == 1:
        #    raise Exception
        if argv[1] in pram[2:] and len(argv[1:]) != 1:
            if not Path(argv[2]).is_file():
                raise FileNotFoundError

        if argv[1] == pram[0]:
            start("Encrypt", start=Simple_Crypt, end=Simple_Crypt_Res)
        if argv[1] == pram[1]:
            start("Decrypt", start=Simple_Crypt, end=Simple_Crypt_Res)
        if argv[1] == pram[2] and len(argv[1:]) == 1:
            start("Encrypt", start=File_Select, end=File_Crypt, add=[[Crypt_Bubble,"pass","SUCCESS"],[Crypt_Bubble,"fail","FAILURE"]])
        if argv[1] == pram[2]:
            start("Encrypt", start=File_Crypt, add=[[Crypt_Bubble,"pass","SUCCESS"],[Crypt_Bubble,"fail","FAILURE"]])
        if argv[1] == pram[3] and len(argv[1:]) == 1:
            start("Decrypt", start=File_Select, end=File_Crypt, add=[[Crypt_Bubble,"pass","SUCCESS"],[Crypt_Bubble,"fail","FAILURE"]])
        if argv[1] == pram[3]:
            start("Decrypt", start=File_Crypt, add=[[Crypt_Bubble,"pass","SUCCESS"],[Crypt_Bubble,"fail","FAILURE"]])
        if argv[1] == pram[4] and len(argv[1:]) == 1:
            start("Edit", start=File_Select, end=File_Edit_Auth, add=[[File_Edit,"edit","Edit"]])
        if argv[1] == pram[4]:
            start("Edit", start=File_Edit_Auth, add=[[File_Edit,"edit","Edit"]])
    except FileNotFoundError:
        print(color.UNDERLINE+color.RED+'ERROR:',color.YELLOW+' No such file or directory exists.',sep=color.END,end=color.END+'\n')
        exit(1)
    except Exception:
        print(f"""{color.RED+color.UNDERLINE}Usage:{color.END+color.CYAN+color.BOLD} cpt {color.END+color.YELLOW}<command> [options] [-V version]{color.END+color.GREEN}\n
        Commands:{color.END+color.YELLOW}
        -e            Linear-text Encryption
        -d            Linear-text Decryption
        -ef [path]    File based Encryption
        -df [path]    File based Decryption
        -t [path]     Edit Encrypted files""",end=color.END+'\n')
        exit(1)

if __name__ == '__main__':
    win_ansi_init()
    _main()
