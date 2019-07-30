import uuid
import time
from hashlib import blake2b
from ctypes import c_int, c_uint16, c_uint32, c_int64

class MUID:
    def __init__(self,id):
        #TODO decode string format into id if string type passed in
        self.id = id

    def __str__(self):
        b_ts = (self.id >> 32)
        # print("b_ts = ", hex(b_ts))

        b_source_id=self.id >> 20 & int('fff', 16)
        # print("b_source_id = ", hex(b_source_id))

        b_item_id=self.id >> 8 & int('fff', 16)
        # print("b_item_id = ", hex(b_item_id))

        b_seq=(self.id) & (int('ff', 16))
        # print("b_seq = ", hex(b_seq))
        str_id = ("%0x-%03x-%03x%02x" % (b_ts,  b_source_id, b_item_id, b_seq))
        return str_id

    def getId(self):
        return self.id     


class MUIDGenerator:
    def __init__(self):
        self.keyed_seq = {}
        self.source_key = uuid.getnode()

    def newID(self, item_key=None, source_key=None):
        if(source_key is None):
            source_key=self.source_key
        if(item_key is None):
            item_key=uuid.uuid4()

        #Create a blake2b hash generator based on 1 byte hash digest
        h1 = blake2b(digest_size=2)
        h1.update(str(source_key).encode('utf-8'))
        h_source_id = int(h1.hexdigest(), 16)
        h_source_id = h_source_id & int('0fff',16)  # Use just last 12bits of the digest

        ts = c_int(int(time.time())-1546300800)#20190101000000 epoch
        # ts = c_int(int(time.time()))  # standard epoch

        h2 = blake2b(digest_size=2)
        h2.update(str(item_key).encode('utf-8'))
        h_item_id = int(h2.hexdigest(), 16)
        # Use just last 12bits of the digest
        h_item_id = h_item_id & int('0fff', 16)

        #Check for key colision, and increment seq if needed
        k = (h_source_id << 12) | h_item_id
        # print(("%0x, %0x, %0x")%(h_source_id, h_item_id, k))
        if(k in self.keyed_seq):
            self.keyed_seq[k] = (self.keyed_seq[k] + 1) % 256
        else:
            #Default to 1 for now
            self.keyed_seq[k] = 1

        seq = c_uint16(self.keyed_seq[k])

        #Create a int64 to hold the id
        muid_int = c_int64(0)

        #First put TIMESTAMP at beginning of the 64bits
        muid_int.value = muid_int.value | (ts.value << 32)
        # print("%0x" % (muid_int.value))
        #Put SOURCEID in next 12bits
        muid_int.value = muid_int.value | (h_source_id << 20)
        # print("%0x" % (muid_int.value))
        #Put the ITEMID in next 12 bits
        muid_int.value = muid_int.value | (h_item_id << 8)
        # print("%0x" % (muid_int.value))
        #Put the SEQ in last 8 bits
        muid_int.value = muid_int.value | (seq.value & int('00ff', 16))
        # print("%0x" % (muid_int.value))

        return MUID(muid_int.value)       
