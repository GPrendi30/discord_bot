import redis
from python_on_whales import docker
from os import path
import os

class Memory:
    '''
    
    '''
    
    def __init__(self, loc):
    
        self.port = 8989  
        self.__init_memory(loc)        
        self.memory = self.__connect_memory()
        self.__load_memory(loc)
        #os.remove(loc + "/appendonly.aof")
        
        
    
    def __init_memory(self, loc):
        try:
            docker.run("redis", volumes=[(loc + "/", '/data')] , publish=[(self.port, 6379)], detach=True, name='Prophet-Memory')
        except:
            docker.start('Prophet-Memory')
            print('Prophet is alive')
    
    
    def __connect_memory(self):
        return redis.Redis('localhost', port=self.port)
    
    
    def __load_memory(self, loc):
        location = loc + '/mem.rdb'
        if not path.isfile(location):
            self.memory.config_set('dbfilename', 'mem.rdb')
            self.__create_memory()
            
        else:
            self.memory.config_set('dbfilename', 'mem.rdb')
            self.__load_rdb()
            
            
    def __load_rdb(self):
        self.memory.config_set('appendonly', 'no')
        docker.restart(['Prophet-Memory'])
        self.memory = self.__connect_memory()
        
        self.memory.bgrewriteaof()
        self.memory.config_set('appendonly', 'yes')
        docker.restart(['Prophet-Memory'])
        
        self.memory = self.__connect_memory()
    
    def __create_memory(self):
        self.memory.hset('input_hash', "user:channel", "chnl-key")
        self.memory.hset('gen_hash', "gen:channel", "gen:chnl") 
    
    
    def save_mem(self):
        self.memory.save()
    
     
    
    def add_user_input(self, channel, el):
        hash_key = 'input_hash'
        prefix = 'user'
        key = prefix + ":" + channel
        if self.memory.hexists(hash_key, key):
            ch_key = self.memory.hget(hash_key, key)
            self.memory.rpush(ch_key, el)
        else:
            ch_key = hash(channel)
            self.memory.hset(hash_key, key, ch_key)
            self.memory.rpush(ch_key, el)
        
    
    def get_user_inputs(self, channel):
        hash_key = 'input_hash'
        prefix = 'user'
        key = prefix + ":" + channel
        if self.memory.hexists(hash_key, key):
            ch_key = self.memory.hget(hash_key, key)
            lln = self.memory.llen(ch_key)
            a = self.memory.lrange(ch_key, 0, lln)
            return [str(c)[2:-1] for c in a]
        else:
            return []            
    
    def add_gen_response(self, channel, el):
        hash_key = 'gen_hash'
        prefix = 'gen'
        key = prefix + ":" + channel
        if self.memory.hexists(hash_key, key):
            ch_key = self.memory.hget(hash_key, key)
            self.memory.rpush(ch_key, el)
        else:
            ch_key = hash(channel)
            self.memory.hset(hash_key, key, ch_key)
            self.memory.rpush(ch_key, el)
    
    def get_responses(self, channel):
        hash_key = 'gen_hash'
        prefix = 'gen'
        key = prefix + ":" + channel
        if self.memory.hexists(hash_key, key):
            ch_key = self.memory.hget(hash_key, key)
            lln = self.memory.llen(ch_key)
            a = self.memory.lrange(ch_key, 0, lln)
            return [str(c)[2:-1] for c in a]
        else:
            #print(self.memory.hgetall(hash_key))
            return []
        
    def add_user(self, el):
        self.memory.sadd('users', el)
    
    def get_genkeys(self):
        l = self.memory.hgetall('gen_hash')
        l = [str(x)[2:-1] for x in l]
        return l


#docker.run("redis", volumes=[(path.abspath('Brain/memory/cell') + "/", '/data')] , publish=[(8989, 6379)], detach=True, name='Prophet-Memory')

