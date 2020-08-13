import argparse
import json
import numpy as np
import os
import torch
from src.pt_config import CONTENT_FEATURE_LAYERS
from src.pt_config import STYLE_FEATURE_LAYERS
from src.pt_transfer import transfer as pt_transfer
from src.utils import print_out

LANGUAGES = {
    'pt': 'PyTorch',
    'tf': 'TensorFlow'
}
STYLE_WEIGHTS_NAMES = [
    'conv1_1',
    'conv2_1',
    'conv3_1',
    'conv4_1',
    'conv4_1'
]
CONTENT_TYPES = list(CONTENT_FEATURE_LAYERS.keys())
STYLE_TYPES = list(STYLE_FEATURE_LAYERS.keys())


def set_seed(args, language='pt'):
    np.random.seed(args.seed)

    if language == 'pt':
        torch.manual_seed(args.seed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--content_image_path",
        default=None,
        type=str,
        required=True,
        help="The content image path as p (picture)",
    )
    parser.add_argument(
        "--content_type",
        default='d',
        type=str,
        help="The content type must be in the list: " + ", ".join(CONTENT_TYPES),
    )
    parser.add_argument(
        "--style_image_path",
        default=None,
        type=str,
        required=True,
        help="The style image path as a (artwork)",
    )
    parser.add_argument(
        "--style_type",
        default='e',
        type=str,
        help="The style type must be in the list: " + ", ".join(STYLE_TYPES),
    )
    parser.add_argument(
        "--language",
        default='pt',
        type=str,
        required=True,
        help="Language name selected in the list: " + ", ".join(LANGUAGES.keys()),
    )
    parser.add_argument(
        "--style_weights",
        default='0.2,0.2,0.2,0.2,0.2',
        type=str,
        help="Style weights must be declared as list of int for all layers: " + ", ".join(STYLE_WEIGHTS_NAMES),
    )

    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--beta", type=float, default=1e4)
    parser.add_argument("--steps", type=int, default=2000)
    parser.add_argument("--log_every_step", type=int, default=200)
    parser.add_argument("--learning_rate", type=float, default=1e-3)

    parser.add_argument("--save_dir", type=str, default='')

    parser.add_argument("--seed", type=int, default=42, help="random seed for initialization")

    args = parser.parse_args()
    set_seed(args)

    content_image_path = args.content_image_path
    content_type = args.content_type
    style_image_path = args.style_image_path
    style_type = args.style_type
    language = args.language
    style_weights = [float(w) for w in args.style_weights.split(',')]
    alpha = args.alpha
    beta = args.beta
    steps = args.steps
    log_every_step = args.log_every_step
    learning_rate = args.learning_rate
    save_dir = args.save_dir

    if language == 'pt':
        print()
        print_out('Transfer parameters:', params=vars(args))
        history = pt_transfer(
            content_image_path,
            style_image_path,
            steps=steps,
            log_every_step=log_every_step,
            learning_rate=learning_rate,
            content_type=content_type,
            style_type=style_type,
            style_weights=style_weights,
            alpha=alpha,
            beta=beta,
            save_dir=save_dir)

        if isinstance(save_dir, str) and len(save_dir) > 0:
            history_path = os.path.join(save_dir, 'history.json')
            print_out('Save history to:', params={'history_path': history_path})
            with open(history_path, 'w') as f:
                json.dump(history, f)


if __name__ == '__main__':
    main()