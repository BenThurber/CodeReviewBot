from random import sample
import pickle
import os

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