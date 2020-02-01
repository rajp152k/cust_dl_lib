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
	
## Hooks:
	
	- getting into hooking the statistics of the parameters and the parameters themeselves using the callback functionality just created
	- then  implementing a class that mimics ,to an extent, the inbuilt functionality of pytorch hooks
	- testing the hooking functionality for the initialization of parameters by different norms: kaiming uniform and standard, for instance
	- Testing these on convolution layers rather than the fully connected layers that have been used in the previous exports

## Normalization:

	- discuss mainly about batch norm and it short  comings after adding the functionality 
	- discuss other alternatives and their limitations
	- come up with a batch norm using a running average for the trainable parameters concerned in the training phase as well rather than just the inference phase 

## LSUV:
	
	- another way to initialize the layers dynamically depending on the past acitvations
	- easier than kaiming uniform/normal and just dividing the stds and subtracting the means from biases to obtain a near zero mean and a variance very close to one.

## Datablock API:

	- recreating the convenience to manage data in different forms.
	- from handling, splitting, labelling, vocab creation to any other functionality: added for convenience

## Optimizer:
	
	- creating a generic base optimizer class to allow for minow tweaks resulting in the desired outcome.
	- Building adam first using the generic class:
		- exponentially weighted moving average for the step
		- debias it 
	- Then building a recent optimizer: LAMB : fork of adam for a layer-wise approach

## Minor updates:
	
	- refactoring runner and learner into one learner
