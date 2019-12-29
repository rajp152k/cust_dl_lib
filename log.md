# PROGRESSION LOG

## setup

	- set up git and colab to interact 
	- python and log files edited on my pc
	- ipynbs edited on colab
	- created a testing framework
		- shows all the exceptions 

# Core objectives:
	
	- create a simple neural net with all the functionalities implemented from scratch
	- once a functionality has been written, can use the corresponding on from standard libraries
	- sample case: MNIST : a relatively shallower deep neural net : for testing and learning purposes
	- followed by implementation of compentent architectures built from scratch

## Matrix multiplication:

	- progression: looping--:element wise operation--:broadcasting--:einstein summations
	- testing on MNIST
		- creating a forward pass with a weight matrix 

## Propogation:

	- implementing forward and backward passes for a single hidden layer
	- studied effects of initialisation 
		- read the Kaiming He initialisation paper
	- maintaining variance of activations close to 1 
		- to allow deeper networks to converge efficiently
	- implemented linear and the ReLU layer and refactored as classes
	- can use nn.Linear and nn.ReLU from now onwards from torch

## Batches:
	
	- refactor the code a  bit to make it more readable:
		- optimizer class created
	- implemented the cross entropy loss function : combining negative log loss and softmax 
	- yielding data : batch processing capabilities introduced 

## Model Flexibility:

	- refactored some code to make dataloaders more compact 
	- introducing callback functionality: a step towards using hooks
		- allows lots of testing and experimentation 
	- created a runner to allow for compact passage of hyperparameters to again allow for convenient updates when experimenting
	 

## Scheduling 

	- adding annealing capabilities 
		- using the callback functionality gained in the previous update
	- also tested the recorder class for storage of losses and learning rates

## LR Finder
	
	- adding an Lr finder to initialise properly using the callback functionality just added
	
