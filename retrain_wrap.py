import os
import click


@click.command('Run "retrain.py" from tensorflow examples')
@click.option('--architecture', '-a', required=False, default='mobilenet_1.0_224',
              help='Neural network architecture (should be either "inception"'
              ' or "mobilenet")')
@click.option('--image_augmentation', '-i', required=False, default=False,
              help='Use image augmentation (retraining'
              'takes significantly more time)')
@click.option('--num_steps', '-n', required=False, default=1000,
              help='Number of steps')
def main(architecture, image_augmentation, num_steps):
    cmd = [
        'python tensorflow/tensorflow/examples/image_retraining/retrain.py',
        '--model_dir models',
        '--bottleneck_dir bottlenecks',
        '--summaries_dir summaries',
        '--image_dir pictures_from_queries',
        '--output_graph output_graph.pb',
	'--output_labels labels.txt',
        '--print_misclassified_test_images True',
        '--architecture {}'.format(architecture),
        '--how_many_training_steps {}'.format(num_steps),
    ]

    if image_augmentation:
        cmd += [
            '--flip_left_right True',
            '--random_crop 10',
            '--random_scale 10',
            '--random_brightness 10',
        ]

    cmd = ' '.join(cmd)
    print('Running command:\n{}\n'.format(cmd))
    os.system(cmd)


if __name__=='__main__':
    main()
