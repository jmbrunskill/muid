import time
import uuid
from ctypes import c_int, c_uint16,c_uint32, c_int64
from hashlib import blake2b
import timeit


def nextId(source_key, item_key, i):
    #Create a blake2b hash generator based on 1 byte hash digest
    h1 = blake2b(digest_size=1)
    h1.update(str(source_key).encode('utf-8'))
    h_source_id = int(h1.hexdigest(),16)
    #0 out first bit of digest
    h_source_id = h_source_id & int('01111111',2)

    ts = c_int(int(time.time()))
    h2 = blake2b(digest_size=1)
    h2.update(str(item_key).encode('utf-8'))
    h_item_id = int(h2.hexdigest(), 16)

    seq = c_uint16(i)

    #Create a int64 to hold the id
    muid_int = c_int64(0)

    #First put TIMESTAMP at beginning of the 64bits
    muid_int.value = muid_int.value | (ts.value << 32)

    #Put SOURCEID in next (8bits)
    muid_int.value = muid_int.value | (h_source_id << 24)
    #Put the ITEMID in next 8 bits
    muid_int.value = muid_int.value | (h_item_id << 16)
    #Put the SEQ in last 16 bits
    muid_int.value = muid_int.value | (seq.value)

    b_ts = (muid_int.value >> 32)
    # print("b_ts = ", hex(b_ts))

    b_source_id = muid_int.value >> 24 & int('ff', 16)
    # print("b_source_id = ", hex(b_source_id))

    b_item_id = muid_int.value >> 16 & int('ff', 16)
    # print("b_item_id = ", hex(b_item_id))

    b_seq = (muid_int.value) & (int('ffff', 16))
    # print("b_seq = ", hex(b_seq))


    # print("%s:%s = %0x-%0x-%0x-%0x" %
    #       (source_key, item_key,  int(ts.value), h_source_id, h_item_id, seq.value))
    # print("%s:%s (%i)= %0x-%0x-%0x-%0x" %
    #       (source_key, item_key, muid_int.value, b_ts, b_source_id, b_item_id, b_seq))
    return muid_int.value

dups = {}

ITEMS = ['A01LT001',
        'A01LT002',
        'A01LT003',
        'A01LT004',
        'A01LT005',
        'A01LT006',
        'A01LT007',
        'A01LT008',
        'A01LT009',
        'A01LT010'
        ]
for i in range(256000):
    it = ITEMS[i % 10]
    id = nextId("SOURCE%0d" % (i), it, i)
    # id = nextId("NZS001", "test", i)
    if(id in dups):
        print("Duplicated ID :", id, i)
    else:
        dups[id]=id
