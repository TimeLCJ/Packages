import torch
import loggging
import sys
import os

try:
    pass # torch train
except KeyboardInterrupt:
    torch.save(model.state_dict(), 'INTERRUPTED.pth')
    logging.info('Saved interrupt')
    try:
        sys.exit(0)
    except:
        os._exit(0)