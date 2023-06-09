import numpy as np

class Client(object):
    
    def __init__(self, id, group=None, train_data={'x':[],'y':[]}, eval_data={'x':[],'y':[]}, dynamic_lam=0, model=None):
        self.model = model
        self.id = id # integer
        self.group = group

        train_len = len(train_data['x'])

        if dynamic_lam: 
            self.train_data = {'x': train_data['x'][:int(train_len * 0.9)],
                                'y': train_data['y'][:int(train_len * 0.9)]}
            self.val_data = {'x': train_data['x'][int(train_len * 0.9):],
                            'y': train_data['y'][int(train_len * 0.9):]}
        else:
            self.train_data = train_data
            self.val_data = eval_data

        self.test_data = eval_data

        self.train_samples = len(self.train_data['y'])
        self.val_samples = len(self.val_data['y'])
        self.test_samples = len(self.test_data['y'])

    def set_params(self, model_params):
        '''set model parameters'''
        self.model.set_params(model_params)

    def get_params(self):
        '''get model parameters'''
        return self.model.get_params()

    def get_grads(self, mini_batch_data):
        '''get model gradient'''
        return self.model.get_gradients(mini_batch_data)

    def get_data_grads(self, data):
        return self.model.get_data_gradients(data)

    def get_loss(self):
        return self.model.get_loss(self.train_data)

    def get_val_loss(self):
        return self.model.get_loss(self.val_data)

    def get_val_accuracy(self):
        tot_correct, loss = self.model.test(self.val_data)
        return tot_correct * 1.0 / self.val_samples

    def get_softmax(self):
        return self.model.get_softmax(self.train_data)

    def get_kl_grads(self, output2):
        return self.model.get_kl_gradients(self.train_data, output2)

    def solve_grad(self):
        '''get model gradient with cost'''
        bytes_w = self.model.size
        grads = self.model.get_gradients(self.train_data)
        comp = self.model.flops * self.train_samples
        bytes_r = self.model.size
        return ((self.train_samples, grads), (bytes_w, comp, bytes_r))

    def solve_inner(self, num_epochs=1, batch_size=10):
        '''Solves local optimization problem
        
        Return:
            1: num_samples: number of samples used in training
            1: soln: local optimization solution
            2: bytes read: number of bytes received
            2: comp: number of FLOPs executed in training process
            2: bytes_write: number of bytes transmitted
        '''

        bytes_w = self.model.size
        soln, comp = self.model.solve_inner(self.train_data, num_epochs, batch_size)
        bytes_r = self.model.size
        return (self.train_samples, soln), (bytes_w, comp, bytes_r)

    def solve_sgd(self, mini_batch_data):
        '''
        run one iteration of mini-batch SGD
        '''
        grads, loss, weights = self.model.solve_sgd(mini_batch_data)
        return (self.train_samples, weights), (self.train_samples, grads), loss

    def train_error(self):

        tot_correct, loss = self.model.test(self.train_data)
        return tot_correct, loss, self.train_samples


    def test(self):
        '''tests current model on local eval_data

        Return:
            tot_correct: total #correct predictions
            test_samples: int
        '''
        tot_correct, loss = self.model.test(self.test_data)
        return tot_correct, loss, self.test_samples
    
    def test_with_mce(self):
        '''tests current model on local eval_data
        
        Return
            tot_correct: total
            test_samples: int
            mce: float
        '''
        total_correct, loss, conf_avg, bin_correct, bin_total = self.model.test_with_mce(self.test_data)
        return total_correct, loss, self.test_samples, conf_avg, bin_correct, bin_total
    
    def test_on_positive_male(self):
        '''tests current model on positive examples only in local eval_data to get TPR
        
        Return:
            tot_correct: total
            test_samples: int
        '''
        pos_test_data = {'x': [], 'y': []}
        for i in range(len(self.test_data['y'])):
            if self.test_data['y'][i][0] == 1 and self.test_data['x'][i][3] == 1:
                pos_test_data['x'].append(self.test_data['x'][i])
                pos_test_data['y'].append(self.test_data['y'][i])
        
        tot_correct, loss = self.model.test(pos_test_data)
        return tot_correct, loss, len(pos_test_data['y'])
    
    def test_on_positive_female(self):
        '''tests current model on positive examples only in local eval_data to get TPR
        
        Return:
            tot_correct: total
            test_samples: int
        '''
        pos_test_data = {'x': [], 'y': []}
        for i in range(len(self.test_data['y'])):
            if self.test_data['y'][i][0] == 1 and self.test_data['x'][i][3] == 0:
                pos_test_data['x'].append(self.test_data['x'][i])
                pos_test_data['y'].append(self.test_data['y'][i])
        tot_correct, loss = self.model.test(pos_test_data)
        return tot_correct, loss, len(pos_test_data['y'])
        
    def validate(self):
        tot_correct, loss = self.model.test(self.val_data)
        return tot_correct, self.val_samples