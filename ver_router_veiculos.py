import os

for root, dirs, files in os.walk(r'C:\fleet-cloud\app'):
    for f in files:
        if 'vehicle' in f.lower() and f.endswith('.py') and 'cache' not in root:
            path = os.path.join(root, f)
            print(f'\n=== {path} ===')
            with open(path, 'r', encoding='utf-8') as fp:
                print(fp.read())
