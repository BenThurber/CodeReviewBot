from people import ID_TO_NAME
from random import sample
import pickle
import os

class IdChooser(object):
    
    def __init__(self, id_list, num_dup=3):
        """max_dup is the maximum number of duplicate users allowed in a 
        round.  max_dup == 1 means no duplicate users."""
        self._num_dup = num_dup
        self._is_new_round = False
        self.id_list = list(id_list)
        assert len(self.id_list) > 0
        self.sample = []
        self.new_round()
    
    
    def next(self, not_including=[]):
        """Get the next random user_id.  Doesn't pick user_ids in 
        not_including, and moves them to the next round if there are no other 
        ids left to choose."""
        
        # There must be >= 1 ids that are included
        assert len(not_including) < len(self.id_list)
        
        # If out of ids, start a new round
        if len(self.sample) <= 0:
            self.new_round()
            return self.next(not_including)
        
        # Extract unwanted contained in sample 
        exclusions = [user_id for user_id in self.sample if user_id in not_including]
        
        # Remove unwanted from sample
        for user_id in exclusions:
            self.sample.remove(user_id)
        
        # If out of ids after removing exclusions, start new round and carry_over exclusions
        if len(self.sample) <= 0:
            self.new_round(exclusions)
            return self.next(not_including)
        
        # Get next id
        next_id = self.sample.pop()
        
        # Add exclusions back to the sample
        self.sample.extend(exclusions)
        
        # Re-randomize
        self.sample = sample(self.sample, len(self.sample))
        
        return next_id
    
    
    def new_round(self, carry_over=[]):
        """carry_over are any ids that weren't able to be used in the last round"""
        self._is_new_round = True
        
        # Create fresh sample
        self.sample = sample(self.id_list, len(self.id_list))
        
        # Prevent any more than the maximum duplicates
        for user_id in set(carry_over):
            for _ in range(carry_over.count(user_id) - self._num_dup + 1):
                carry_over.remove(user_id)
        
        # Add Carry Over to the second to last space in the list (so its chosen first) 
        print(carry_over)
        self.sample[-1:-1] = carry_over  # Add in second to last slot
        #print(list(map(lambda x: ID_TO_NAME[x], self.sample)))
        
    
    def is_new_round(self):
        """I don't like the way this is implemented, but can't think of a 
        better way to do it.  Unreliable, relies on implementation of outside 
        code to work right."""
        result = self._is_new_round
        self._is_new_round = False
        return result
        


class PersistantIdChooser(IdChooser):
    
    def __init__(self, id_list, name, num_dup=3):
        self.name = name
        
        try:  # Try to load this object from a file
            other = self.load_obj(name)
            
            self._num_dup = other._num_dup
            self._is_new_round = other._is_new_round
            self.id_list = other.id_list
            self.sample = other.sample
            self.name = other.name
            
            #self = self.load_obj(name)  // Can't seem to get this to work
            
        except IOError:  # Create a new file if one doesn't exist
            super().__init__(id_list, num_dup)
            self._save_state()
    
    
    def new_round(self, carry_over=[]):
        super().new_round(carry_over)
        self.save_obj(self, self.name)
    
    
    def next(self, not_including=[]):
        index = super().next(not_including)
        print(list(map(lambda x: ID_TO_NAME[x], self.sample)))
        self.save_obj(self, self.name)
        return index
    
    
    def save_obj(self, obj, name):
        with open('obj/'+ name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
    
    def load_obj(self, name):
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)