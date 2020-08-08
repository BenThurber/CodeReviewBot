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
        print(list(map(lambda x: ID_TO_NAME[x], self.sample)))
        
    
    def is_new_round(self):
        """I don't like the way this is implemented, but can't think of a 
        better way to do it.  Unreliable, relies on implementation of outside 
        code to work right."""
        result = self._is_new_round
        self._is_new_round = False
        return result
        
    


class Sample(object):
    
    def __init__(self, sample_size):
        """
        sample_size  is the range of random numbers to return, included in 
        the set: range(sample_size)
        """
        assert sample_size > 0
        self.sample_size = sample_size
        self._i = 0
        self.new_sample()
    
    def new_sample(self):
        """Create a new internal sample (Called when the current sample 
        is exausted)"""
        self.indice_list = sample(range(self.sample_size), self.sample_size)
        self._i = 0;        
    
    def next(self):
        """Get the next random number"""
        if self.is_last():
            self.new_sample()
        
        index = self.indice_list[self._i]
        self._i += 1
        return index
    
    def is_first(self):
        """Has a new sample been started?"""
        return self._i == 0
    
    def is_last(self):
        """Has a new sample been started?"""
        return self._i >= len(self.indice_list)    
    
    def __repr__(self):
        """Return a string representation, including what index will be 
        retunred next.  (Hack implementation)"""
        i = self._i
        
        if (i >= len(self.indice_list)):
            return "i=last, {}".format(i, self.indice_list)
        
        s = ''
        if i != 0: s = ', '
        
        return "i={}, {}({}), {}".format(
            i, 
            str(self.indice_list[:i])[:-1]+s, 
            self.indice_list[i],
            str(self.indice_list[i+1:])[1:]
        )


class PersistantSample(Sample):
    """Creates a non-repeating random number (a sample) that (will) be stored 
    in a file such that when the program exits and is re-run, the sample will 
    carry on where it left off."""
    
    def __init__(self, sample_size, name):
        """
        sample_size  is the range of random numbers to return, included in 
        the set: range(sample_size)
        
        name  is a unique name given to the file used to store the samples 
        persistantly
        """
        self.name = name
        
        try:  # Try to load this object from a file
            other = self.load_obj(name)
            
            if sample_size != other.sample_size or other.is_last():
                raise IOError
            
            self.sample_size = other.sample_size
            self._i = other._i
            self.name = other.name
            self.indice_list = other.indice_list
            
            #self = self.load_obj(name)  // Can't seem to get this to work
            
        except IOError:  # Create a new file if one doesn't exist
            super().__init__(sample_size)
            self._save_state()
    
    
    def _save_state(self):
        """Save the current state of the object if it changes."""
        self.save_obj(self, self.name)
    
    
    def new_sample(self):
        super().new_sample()
        self._save_state()
    
    
    def next(self):
        index = super().next()
        self._save_state()
        return index
    
    
    def remaining(self):
        return self.indice_list[self._i:]
    
    
    def save_obj(self, obj, name):
        with open('obj/'+ name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
    
    def load_obj(self, name):
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)