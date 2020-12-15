import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

def hidden_init(layer):
    fan_in = layer.weight.data.size()[0]
    lim = 1. / np.sqrt(fan_in)
    return (-lim, lim)

class Actor(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed, fc1_units=400, fc2_units=300):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(Actor, self).__init__()
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, fc1_units)
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.fc3 = nn.Linear(fc2_units, action_size)
        self.reset_parameters()
        
        #add batch norms
        self.bn1 = nn.BatchNorm1d(fc1_units)
        self.bn2 = nn.BatchNorm1d(fc2_units)     
        self.bn3 = nn.BatchNorm1d(action_size)   

    def reset_parameters(self):
        self.fc1.weight.data.uniform_(*hidden_init(self.fc1))
        self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
        self.fc3.weight.data.uniform_(-3e-3, 3e-3)

    def forward(self, state):
        """Build an actor (policy) network that maps states -> actions."""
        
        if state.ndim == 1:
            state = state.view(1, state.size(0))
        
        x = self.fc1(state)
        #x = self.bn1(x)
        x = F.relu(x)
        
        x = self.fc2(x)
        #x = self.bn2(x)
        x = F.relu(x)
        
        x = self.fc3(x)
        #x = self.bn3(x)
        
        return torch.tanh(x)


class Critic(nn.Module):
    """Critic (Value) Model."""

    def __init__(self, state_size, action_size, seed, fcs1_units=400, fc2_units=300):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fcs1_units (int): Number of nodes in the first hidden layer
            fc2_units (int): Number of nodes in the second hidden layer
        """
        super(Critic, self).__init__()
        self.seed = torch.manual_seed(seed)
        
        #Q1
        self.fcs1q1 = nn.Linear(state_size+action_size, fcs1_units)
        self.fc2q1 = nn.Linear(fcs1_units, fc2_units)
        self.fc3q1 = nn.Linear(fc2_units, 1)
        
        self.bn1q1 = nn.BatchNorm1d(fcs1_units)
        self.bn2q1 = nn.BatchNorm1d(fc2_units)     
        #self.bn3q1 = nn.BatchNorm1d(1)  
        
        #Q2
        #self.fcs1q2 = nn.Linear(state_size+action_size, fcs1_units)
        #self.fc2q2 = nn.Linear(fcs1_units, fc2_units)
        #self.fc3q2 = nn.Linear(fc2_units, 1)
        
        #self.bn1q2 = nn.BatchNorm1d(fcs1_units)
        #self.bn2q2 = nn.BatchNorm1d(fc2_units)     
        #self.bn3q2 = nn.BatchNorm1d(1)  
        
        self.reset_parameters()

    def reset_parameters(self):
        self.fcs1q1.weight.data.uniform_(*hidden_init(self.fcs1q1))
        self.fc2q1.weight.data.uniform_(*hidden_init(self.fc2q1))
        self.fc3q1.weight.data.uniform_(-3e-3, 3e-3)
        
        #self.fcs1q2.weight.data.uniform_(*hidden_init(self.fcs1q2))
        #self.fc2q2.weight.data.uniform_(*hidden_init(self.fc2q2))
        #self.fc3q2.weight.data.uniform_(-3e-3, 3e-3)

    def forward(self, state, action):
        """Build a duel critic (value) network that maps (state, action) pairs -> Q-values."""
        
        state_action = torch.cat((state, action), dim=1)
        
        q1 = F.relu(self.fcs1q1(state_action))
        q1 = F.relu(self.fc2q1(q1))
        q1 = self.fc3q1(q1)
        
        #q2 = F.relu(self.bn1q2(self.fcs1q2(state_action)))
        #q2 = F.relu(self.bn2q2(self.fc2q2(q2)))
        #q2 = self.fc3q2(q2)
        
        return q1#, q2