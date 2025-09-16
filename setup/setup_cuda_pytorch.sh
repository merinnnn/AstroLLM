#!/bin/bash
set -e

echo "[1/5] Updating system..."
sudo apt-get update && sudo apt-get upgrade -y

echo "[2/5] Adding NVIDIA CUDA 12.1 repo..."
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"

echo "[3/5] Installing CUDA Toolkit 12.1..."
sudo apt-get update
sudo apt-get install -y cuda-toolkit-12-1

echo "[4/5] Setting environment variables..."
if ! grep -q "cuda-12.1" ~/.bashrc; then
    echo 'export PATH=/usr/local/cuda-12.1/bin${PATH:+:${PATH}}' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
fi
source ~/.bashrc

echo "[5/5] Installing PyTorch with CUDA 12.1..."
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo "Setup complete!"
echo "Test with: python -c 'import torch; print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))'"
