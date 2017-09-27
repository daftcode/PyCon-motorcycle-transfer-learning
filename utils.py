import os
import glob

import numpy as np
import pandas as pd
import tensorflow as tf


def read_bottlenecks(bottleneck_dir='bottlenecks', model_name='inception_v3'):
    bottleneck_subdirectories = glob.glob(os.path.join(bottleneck_dir, '*'))
    return pd.concat(
        map(
            lambda subdir: _read_one_bottleneck(subdir, model_name),
            bottleneck_subdirectories
        ),
    ignore_index=True)


def _read_one_bottleneck(subdirectory, model_name):
    filenames = glob.glob(os.path.join(subdirectory, '*'+model_name+'.txt'))
    bottleneck_activations =  pd.concat(map(
        lambda filename: pd.read_csv(filename, header=None),
        filenames
    ))
    bottleneck_activations['filename'] = filenames
    bottleneck_activations['label'] = (bottleneck_activations['filename']
                                       .apply(lambda x: x.split('/')[-2]))
    return bottleneck_activations


def load_graph(architecture):
    if architecture=='inception_v3':
        graph_filename = 'good_inc_graph.pb'
    elif architecture=='mobilenet_1.0_224':
        graph_filename = 'good_mob224_graph.pb'
    else:
        raise Exception('Architecture "{}" not handled in this example'
                        .format(architecture))

    graph_def = tf.GraphDef()
    with open(graph_filename, 'rb') as graph_file:
        graph_def.ParseFromString(graph_file.read())
    tf.import_graph_def(graph_def, name='')


class GraphWrap:
    '''A wrapper for the graph that provides the API required by LIME (in
    particular, the `predict` method needs to take a list of images as input)
    '''

    def __init__(self, sess, resized_input_tensor_name):
        self.sess = sess
        self.softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        self.resized_input_tensor = sess.graph.get_tensor_by_name(resized_input_tensor_name)

    def _predict_one(self, image):
        return self.sess.run(self.softmax_tensor,
                             {self.resized_input_tensor: np.expand_dims(image, 0)})

    def predict(self, images):
        predictions = np.concatenate([self._predict_one(image) for image in images])
        return predictions
