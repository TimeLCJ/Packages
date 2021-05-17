import torch
import torch.nn

class Mish(torch.nn.Module):
    """
    相比ReLU, Mish是平滑的激活函数，平滑的激活函数允许更好的信息输入神经网络，从而得到更好地准确性和泛化性
    """
    def __init__(self):
        super().__init__()

    def forward(self, x):
        x = x * torch.tanh(torch.nn.functional.softplus(x))
        return x