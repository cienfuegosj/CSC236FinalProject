class pos(object):
    '''
    Quick Explanation of what a position object is.
    
    '''
    
    def __init__(self, row=0, col=0):
        '''
        Constructor method for the position class.
        Pre: row and col must be positive integers.
        Post: instance variables are set up. This is a void function.
        '''
        if row >= 0 and col >= 0:
            self.row = row
            self.col = col
        else:
            raise ValueError("Row and Column arguments must be positive integers.")