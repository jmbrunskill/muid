import muid
# Create 4096 ids against 3 servers and 10 items
# This shouldn't create any duplicates

dups = {}

SOURCES = ['Server1', 'Server2', 'Server3']
ITEMS = ['ITEM1',
         'ITEM2',
        'ITEM3',
        'ITEM4',
        'ITEM5',
        'ITEM6',
        'ITEM7',
        'ITEM8',
        'ITEM9',
        'ITEM10'
        ]
idgen = muid.MUIDGenerator()
for i in range(4096):
    it = ITEMS[i % len(ITEMS)]
    sr = SOURCES[i % len(SOURCES)]
    id = idgen.newID(it,sr)
    if(str(id) in dups):
        print("Duplicated ID :", id, i)
    else:
        dups[str(id)]=id



