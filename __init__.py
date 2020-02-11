if __name__=='__main__':
    import os, sys
    if not  sys.version_info[0] == 3:
        print('Python3 required!')
        exit(0)
    import importlib
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mod = importlib.import_module('cpt.__main__')
    attr = {i:j for i,j in mod.__dict__.items()}
    locals().update(attr)
    win_ansi_init()
    _main()
