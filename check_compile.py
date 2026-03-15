import py_compile
import sys
files = [
    'app.py',
    'src/ui.py',
    'src/service.py',
    'src/repository.py',
    'src/queries.py',
    'src/db.py',
    'src/config.py',
    'src/utils.py',
]
failed = False
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print(f + ' -> OK')
    except Exception as e:
        print(f + ' -> ERROR')
        print(e)
        failed = True
if failed:
    sys.exit(1)
else:
    print('ALL OK')
