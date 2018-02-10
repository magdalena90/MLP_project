# MLP_project

Check the project's Wiki for more details of the content of the project

## Getting started

Clone this repo when logged in at **mlp1** or **mlp2**

```bash
git clone https://github.com/magdalena90/MLP_project
cd MLP_project
```

Then we need to create a new conda environment called **py27** with Python 2.7 and the requirements needed. It is assumed that you already have followed steps 1-5 in **installing requirements** section of https://github.com/CSTR-Edinburgh/mlpractical/blob/mlp2017-8/semester_2_materials/notes/gpu-cluster-quick-start.md 

```bash
bash create_environment.sh
```

## Downloading and processing images, splitting in training and validation sets

Then we proceed to cloning **pix2pix** repo and downloading and processing images. The first argument must be 1 if we want to clone the **pix2pix** repo or any other value if we have already cloned the repo. The second and third argument is for the number of images we want to donwload and the number of images we want to use a validation set, respectively. For example:

```bash
bash preprocessing.sh 1 500 100
```

## Training and testing a cGAN model


Now we are ready to use the cGAN training and launch the job to **Slurm**. Please note that we can modify the script using **vi** or **vim** in order to add or modify the parameters (flags) used by the **pix2pix**'s module main.py. I have set up 200 epochs as default, but it can be modified.

```bash
sbatch gpu_training.sh
```

A new folder inside **checkpoint** folder will be created among **pix2pix** repo files. This folder will contain the metadata for the model and will be updated periodically.

We can track the status of our job using the command **squeue** and monitor the printings to stdout of our job in the file **sample_experiment_outfile**, which is updated every 5 minutes.

After our job is complete, we can launch another job to apply our generator network to our validation set. Please note that this script is the same as before, except that we are using the flag __--phase test__ in **pix2pix**'s module main.py 

```bash
sbatch gpu_testing.sh
```

### Continue training an already trained model

The last line of the **gpu_training** script reads as follows:

```bash
python main.py --dataset_name imagenet --phase train --epoch 200 
```

Suppose after the model is trained, we would like to continue the training process for this model. Let's say we want our model to run for 100 more epochs, then we can modify the last line of **gpu_training** script as follows:

```bash
python main.py --dataset_name imagenet --phase train --epoch 300 --continue_train True
```

This way, the training procedure will continue based on the metadata contained in the **checkpoint** location.


## Copying outputs to local

The generated images will be inside **test** folder among **pix2pix** repo files. To get the images from mlp1/mlp2 to our computer we need to proceed as follows:

### From mlp1/mlp2 to DICE

```bash
cp test/* /afs/inf.ed.ac.uk/user/s17/<studentUUN>/some_target_path
```

### From DICE to local

```bash
scp <studentUUN>@student.ssh.inf.ed.ac.uk:/afs/inf.ed.ac.uk/user/s17/<studentUUN>/some_target_path /some_local_path
```
