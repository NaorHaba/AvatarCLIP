import torch

from website.messages import Messages
from website.logger import get_logger

logger = get_logger(__name__)


if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
    logger.info(Messages.CUDA_DEFAULT_TENSOR_TYPE_INFO)


def convert_to_FBX():
    pass