'''
Created on Sep 29, 2016

@author: joseph
'''
import time
import uuid
import json


class Initializer():
    def __init__(self, zk, zkroot, distributer):
        self.zk = zk
        self.zkroot = zkroot
        self.uuid = 'lock-' + uuid.uuid4().get_hex()
        self.distributer = distributer

    def initialize(self):
        self.register()
        time.sleep(30)
        self.vote()
        if self.is_elected():
            print 'i node-%d elected' % (self.node_id)
            self.distributer(self.zk, self.zkroot)._distribute()
        return self.get_alloted_config()

    def register(self):
        self.node_id = 0

    def vote(self):
        pass

    def is_elected(self):
        return True

    def finalize(self):
        pass

    def get_alloted_config(self):
        time.sleep(3)
        try:
            return json.load(open("._config.json"))
        except:
            return self.get_alloted_config()


class ConfigDistributer():
    def __init__(self, zk, zkroot):
        self.zk = zk
        self.zkroot = zkroot

    def distribution_algorithm(self, *args, **kwargs):
        raise NotImplementedError()

    def get_jobscount(self):
        return 1

    def _distribute(self):
        batches = self.distribution_algorithm()
        json.dump(batches[0], open("._config.json", "w"))


class DistributedJob():
    zkhost = None
    zkroot = None
    distributer = None

    def __init__(self, *args, **kwargs):
        self.__jobinit__(*args, **kwargs)
        self.zk = None
        self.initializer = Initializer(self.zk, self.zkroot, self.distributer)

    def _get_config(self):
        config = self.initializer.initialize()
        self.initializer.finalize()
        return config

    def start(self):
        config = self._get_config()
        if config is not None:
            try:
                for record in config:
                    self.run(record)
            except:
                import traceback
                traceback.print_exc()
        else:
            print "node %d recieved no configuration" % (self.initializer.node_id)

    def __jobinit__(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
