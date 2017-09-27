# Introduction
This repo contains materials for the PyCon PL'17 presentation "Cruiser or sport bike? Teach your computer to categorize motorcycle images using transfer learning in TensorFlow".

I ran the code on Ubuntu 16.04, with Python 3.6.1. Package versions are listed in the "requirements.txt" file.


## Downloading the images
For downloading the images I used the `image_download.py` script:
```bash
$ python image_download.py motorcycle classic
$ python image_download.py motorcycle cross
$ python image_download.py motorcycle cruiser
$ python image_download.py motorcycle superbike
```

Note, that the script only downloads "free to use, share, or modify" images (see *usage rights* at https://www.google.com/advanced_image_search), and the results might not be sufficiently close to what you had in mind.

## Running "retrain.py"
The script has many arguments, most of which we'll want to specify only once, before the first run. However, several arguments (model architecture, number of steps, or whether or not image augmentation should be carried out) will be modified more often. Thus, I've written a wrapper for "retrain.py" with only three optional arguments: `--architecture`, `--num_steps`, and `--image_augmentation`. By running:
```bash
$ python retrain_wrap.py
```
we'll initiate transfer learning for the (default) "mobilenet_1.0_224" architecture, with 1000 steps, and without image augmentation. **NOTE** that image augmentation is very time consuming, and if your machine doesn't have a supported GPU, you will probably want to avoid image augmentation.


## Investigating the retraining process
The "retrain.py" saves summary statistics that can be easily viewed using TensorBoard:
```bash
$ tensorboard --logdir summaries
```


## Notebook
The rest of the demonstration is in the notebook `presentation.ipynb`.


## Contact
Questions / suggestions? Contact me *via* e-mail at: maciej.dziubinski@daftcode.pl
