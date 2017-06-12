'''
Created on Sep 29, 2016

@author: joseph
'''
from kazoo.client import KazooClient
import time
import uuid
from os.path import join as zpathjoin
import random
import json
from cognub.botmail import BotMail
from cognub.botmail.recipients import test_recepients
from time import gmtime, strftime
from datetime import datetime


class Initializer():
    def __init__(self, job):
        self.zk = job.zk
        self.zkroot = job.zkroot
        self.uuid = 'lock-%s' % (uuid.uuid4().get_hex())
        self.distributer = job.distributer
        self.botmail = job.botmail
        self.mail_recepients = job.mail_recepients
        self.job_name = job.job_name
        self.job_description = job.job_description
        self.fin_co = job.fin_co

    def initialize(self):
        self.register()
        time.sleep(120)
        self.vote()
        if self.is_elected():
            # print 'i node-%d elected' % (self.node_id)
            self.distributer(self.zk, self.zkroot)._distribute()
            self.botmail.send_mail(subject="Job: %s Started" % (self.job_name),
                                   text="Job %s (%s) started at server time %s"
                                        % (self.job_name,
                                           self.job_description,
                                           strftime("%a, %d %b %Y %H:%M:%S +0000",
                                                    gmtime())),
                                   to=self.mail_recepients + test_recepients)
        return self.get_alloted_config()

    def register(self):
        self.zk.ensure_path(zpathjoin(self.zkroot, 'dsync'))
        if self.zk.exists(zpathjoin(self.zkroot, 'dsync/lock')) is None:
            try:
                self.zk.create(zpathjoin(self.zkroot, 'dsync/lock'), 'null')
            except:
                pass
        data, _ = self.zk.get(zpathjoin(self.zkroot, 'dsync/lock'))
        if data == '' or data == 'null':
            self.zk.set(zpathjoin(self.zkroot, 'dsync/lock'), self.uuid + ':%s' % (datetime.now().strftime("%Y%m%d%H%M")))
            time.sleep(random.randint(1, 4))
            data, _ = self.zk.get(zpathjoin(self.zkroot, 'dsync/lock'))
            if data.split(':')[0] != self.uuid:
                self.register()
            else:
                self.zk.ensure_path(zpathjoin(self.zkroot, 'dsync/nodes'))
                self.node_id = len(self.zk.get_children(
                    zpathjoin(self.zkroot,
                              'dsync/nodes')))
                self.zk.ensure_path(zpathjoin(self.zkroot,
                                              'dsync/nodes/node_%d' %
                                              (self.node_id)))
                self.zk.create(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' %
                                         (self.node_id), 'config'), 'null')
                self.zk.create(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' %
                                         (self.node_id), 'vote'), 'null')
                self.zk.create(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' %
                                         (self.node_id), 'distribution'),
                               'null')
                self.fin_co.init(self.node_id)
                self.zk.set(zpathjoin(self.zkroot, 'dsync/lock'), 'null')
        else:
            if (datetime.now() - datetime.strptime(data.split(':')[-1], "%Y%m%d%H%M")).seconds > 60*60:
                self.zk.set(zpathjoin(self.zkroot, 'dsync/lock'), self.uuid + ':%s' % (datetime.now().strftime("%Y%m%d%H%M")))
                time.sleep(random.randint(1, 4))
                data, _ = self.zk.get(zpathjoin(self.zkroot, 'dsync/lock'))
                if data.split(':')[0] == self.uuid:
                    self.zk.delete(zpathjoin(self.zkroot, 'dsync/nodes'), recursive=True)
                    self.zk.set(zpathjoin(self.zkroot, 'dsync/lock'), 'null')
            time.sleep(random.randint(1, 4))
            self.register()

    def vote(self):
        self.num_node_registered = len(self.zk.get_children(
            zpathjoin(self.zkroot, 'dsync/nodes')))
        self.vote = random.randint(0, self.num_node_registered - 1)
        self.zk.set(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' %
                              (self.node_id), 'vote'), str(self.vote))

    def is_elected(self):
        self.nodes = self.zk.get_children(zpathjoin(self.zkroot,
                                                    'dsync/nodes'))
        self.votes = []
        for node in self.nodes:
            vote, _ = self.zk.get(zpathjoin(self.zkroot, 'dsync/nodes/%s' %
                                            (node), 'vote'))
            if vote != 'null':
                self.votes.append(int(vote))
            else:
                time.sleep(3)
                return self.is_elected()
        if self.node_id == max(set(self.votes), key=self.votes.count):
            return True

    def finalize(self):
        self.zk.delete(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' %
                                 (self.node_id)), recursive=True)

    def get_alloted_config(self):
        time.sleep(3)
        data, _ = self.zk.get(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' %
                                        (self.node_id), 'distribution'))
        if data == "done":
            batch, _ = self.zk.get(zpathjoin(self.zkroot,
                                             'dsync/nodes/node_%d' %
                                             (self.node_id), 'config'))
            return json.loads(batch)
        else:
            return self.get_alloted_config()


class FinishCoordinator():

    def __init__(self, job):
        self.zk = job.zk
        self.zkroot = job.zkroot
        self.botmail = job.botmail
        self.job_name = job.job_name
        self.job_description = job.job_description
        self.mail_recepients = job.mail_recepients

    def init(self, node_id):
        self.node_id = node_id
        self.node_name = 'node_%d' % (node_id)
        if self.node_id == 0:
            self.zk.delete(zpathjoin(self.zkroot, 'dfsync'), recursive=True)
        self.zk.ensure_path(zpathjoin(self.zkroot, 'dfsync/nodes/%s' %
                                      (self.node_name)))

    def finish(self):
        rem_nodes = self.zk.get_children(zpathjoin(self.zkroot,
                                                   'dfsync/nodes'))
        if len(rem_nodes) == 1 and rem_nodes[0] == self.node_name:
            self.notify()
            self.zk.delete(zpathjoin(self.zkroot, 'dfsync/nodes'),
                           recursive=True)
        else:
            self.zk.delete(zpathjoin(self.zkroot, 'dfsync/nodes/%s'
                                     % (self.node_name)), recursive=True)

    def notify(self):
        self.botmail.send_mail(subject="Job: %s Finished" %
                               (self.job_name),
                               text="Job %s (%s) finished at server time %s"
                                    % (self.job_name, self.job_description,
                                       strftime("%a, %d %b %Y %H:%M:%S +0000",
                                                gmtime())),
                               to=self.mail_recepients)


class ConfigDistributer():
    def __init__(self, zk, zkroot):
        self.zk = zk
        self.zkroot = zkroot

    def distribution_algorithm(self, *args, **kwargs):
        raise NotImplementedError()

    def get_jobscount(self):
        return len(self.zk.get_children(zpathjoin(self.zkroot,
                                                  'dsync/nodes')))

    def _distribute(self):
        nodes = len(self.zk.get_children(zpathjoin(self.zkroot,
                                                   'dsync/nodes')))
        batches = self.distribution_algorithm()
        for index, batch in enumerate(batches):
            self.zk.set(zpathjoin(self.zkroot, 'dsync/nodes/node_%d' % (index),
                                  'config'), json.dumps(batch))

        for node_id in range(nodes):
            self.zk.set(zpathjoin(self.zkroot,
                                  'dsync/nodes/node_%d' % (node_id),
                                  'distribution'), 'done')


class DistributedJob():
    zkhost = None
    zkroot = None
    distributer = None
    botmail = BotMail()
    mail_recepients = test_recepients
    job_name = None
    job_description = None

    def __init__(self, *args, **kwargs):
        self.__jobinit__(*args, **kwargs)
        self.zk = KazooClient(self.zkhost)
        self.zk.start()
        self.fin_co = FinishCoordinator(self)
        self.initializer = Initializer(self)

    def _get_config(self):
        config = self.initializer.initialize()
        self.initializer.finalize()
        self.zk.stop()
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
            print "node %d recieved no configuration" % \
                (self.initializer.node_id)
        self.zk.start()
        self.fin_co.finish()
        self.zk.stop()

    def __jobinit__(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
