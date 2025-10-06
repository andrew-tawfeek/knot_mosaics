# KnotAI

## Architecture

This is a feedforward neural network for binary classification of matrices using supervised learning.

**Mathematical Structure:**
- Input layer: Flattens $n \times m$ matrix to vector $\mathbf{x} \in \mathbb{R}^{nm}$
- Hidden layers: Three fully connected layers with dimensions $128 \to 64 \to 32$
- Each hidden layer applies: $\mathbf{h}_i = \text{ReLU}(\text{BN}(\mathbf{W}_i\mathbf{h}_{i-1} + \mathbf{b}_i))$ with dropout
- Output layer: $\hat{y} = \sigma(\mathbf{w}^T\mathbf{h}_3 + b)$ where $\sigma$ is sigmoid
- Loss function: Binary cross-entropy $\mathcal{L} = -[y\log\hat{y} + (1-y)\log(1-\hat{y})]$
- Optimization: Adam with learning rate scheduling

**Components:**
- **Batch Normalization (BN):** Normalizes layer inputs to $\text{BN}(\mathbf{z}) = \gamma \frac{\mathbf{z} - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} + \beta$ where $\mu_B, \sigma_B^2$ are batch statistics. Reduces internal covariate shift and stabilizes gradient flow.
- **ReLU activations:** $\text{ReLU}(z) = \max(0, z)$ introduces non-linearity while maintaining gradient flow for positive inputs.
- **Dropout (rate=0.2):** Randomly zeros 20% of activations during training. Forces network to learn redundant representations, preventing co-adaptation of neurons.
- **Sigmoid output:** $\sigma(z) = \frac{1}{1 + e^{-z}}$ maps logits to $[0,1]$, interpretable as class probability.
- **Adam optimizer:** Adaptive learning rate method combining momentum ($\mathbf{m}_t = \beta_1\mathbf{m}_{t-1} + (1-\beta_1)\nabla\mathcal{L}$) and RMSprop ($\mathbf{v}_t = \beta_2\mathbf{v}_{t-1} + (1-\beta_2)(\nabla\mathcal{L})^2$). Updates: $\theta_t = \theta_{t-1} - \alpha \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon}$ with bias correction.