# Add the training directory to Python path so we can import data.py
import sys
import os
sys.path.append('/workspaces/knot_mosaics/training')

"""
PyTorch Binary Classification Neural Network for Matrix Input
This script trains a neural network to classify matrices as 0 or 1.
The matrix dimensions are automatically detected from the training data.

Required installations:
pip install torch torchvision numpy matplotlib scikit-learn
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import random

from training.data import data_pairs  # this is the data the model will be trained on



# Set random seeds for reproducibility
# Keep this so training the model on the same dataset will produce the same outcome
torch.manual_seed(42)
np.random.seed(42)
random.seed(42)

# Check if CUDA is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


class MatrixDataset(Dataset):
    """Custom Dataset for matrix inputs and binary labels"""

    def __init__(self, matrices, labels):
        self.matrices = torch.FloatTensor(matrices)
        self.labels = torch.FloatTensor(labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.matrices[idx], self.labels[idx]


class MatrixClassifier(nn.Module):
    """Neural Network for binary classification of matrices"""

    def __init__(self, input_size=25, hidden_sizes=[128, 64, 32], dropout_rate=0.2):
        super(MatrixClassifier, self).__init__()

        # Build the layers
        layers = []
        prev_size = input_size

        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.BatchNorm1d(hidden_size),
                nn.ReLU(),
                nn.Dropout(dropout_rate)
            ])
            prev_size = hidden_size

        # Output layer
        layers.append(nn.Linear(prev_size, 1))
        layers.append(nn.Sigmoid())

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        # Flatten the matrix to a vector (e.g., 5x5 -> 25 elements)
        x = x.view(x.size(0), -1)
        return self.model(x)


def load_your_data():
    """Load data from data.py file and detect matrix dimensions"""
    matrices = []  # Your matrices (any size)
    labels = []    # Your 0/1 labels

    # Load data_pairs from data.py
    for matrix, label in data_pairs:
        matrices.append(matrix)
        labels.append(label)

    matrices = np.array(matrices)
    labels = np.array(labels)

    # Detect matrix dimensions from the first matrix
    if len(matrices) > 0:
        matrix_shape = matrices[0].shape
        matrix_rows = matrix_shape[0] if len(matrix_shape) > 0 else 1
        matrix_cols = matrix_shape[1] if len(matrix_shape) > 1 else 1
    else:
        matrix_rows, matrix_cols = 0, 0

    return matrices, labels, matrix_rows, matrix_cols


def train_model(model, train_loader, val_loader, epochs=100, lr=0.001):
    """Train the neural network"""

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', patience=10, factor=0.5)

    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []

    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0
        train_preds = []
        train_targets = []

        for batch_matrices, batch_labels in train_loader:
            batch_matrices = batch_matrices.to(device)
            batch_labels = batch_labels.to(device)

            optimizer.zero_grad()
            outputs = model(batch_matrices).squeeze()
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            train_preds.extend((outputs > 0.5).cpu().numpy())
            train_targets.extend(batch_labels.cpu().numpy())

        # Validation phase
        model.eval()
        val_loss = 0
        val_preds = []
        val_targets = []

        with torch.no_grad():
            for batch_matrices, batch_labels in val_loader:
                batch_matrices = batch_matrices.to(device)
                batch_labels = batch_labels.to(device)

                outputs = model(batch_matrices).squeeze()
                loss = criterion(outputs, batch_labels)

                val_loss += loss.item()
                val_preds.extend((outputs > 0.5).cpu().numpy())
                val_targets.extend(batch_labels.cpu().numpy())

        # Calculate metrics
        avg_train_loss = train_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        train_acc = accuracy_score(train_targets, train_preds)
        val_acc = accuracy_score(val_targets, val_preds)

        train_losses.append(avg_train_loss)
        val_losses.append(avg_val_loss)
        train_accs.append(train_acc)
        val_accs.append(val_acc)

        # Update learning rate
        scheduler.step(avg_val_loss)

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{epochs}]')
            print(
                f'  Train Loss: {avg_train_loss:.4f}, Train Acc: {train_acc:.4f}')
            print(f'  Val Loss: {avg_val_loss:.4f}, Val Acc: {val_acc:.4f}')

    return train_losses, val_losses, train_accs, val_accs


def plot_training_history(train_losses, val_losses, train_accs, val_accs):
    """Plot training and validation metrics"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot losses
    ax1.plot(train_losses, label='Train Loss')
    ax1.plot(val_losses, label='Val Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True)

    # Plot accuracies
    ax2.plot(train_accs, label='Train Acc')
    ax2.plot(val_accs, label='Val Acc')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Training and Validation Accuracy')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


def predict_single_matrix(model, matrix):
    """Predict the class of a single matrix"""

    model.eval()
    with torch.no_grad():
        # Convert to tensor and add batch dimension
        matrix_tensor = torch.FloatTensor(matrix).unsqueeze(0).to(device)
        output = model(matrix_tensor).squeeze()
        prediction = 1 if output > 0.5 else 0
        confidence = output.item() if prediction == 1 else 1 - output.item()

    return prediction, confidence


def main(epochs=300,lr=0.001):
    """Main training and evaluation pipeline"""

    # Load your data from data.py
    print("Loading data from data.py...")
    matrices, labels, matrix_rows, matrix_cols = load_your_data()

    # Calculate input size from matrix dimensions
    input_size = matrix_rows * matrix_cols
    print(
        f"Detected matrix dimensions: {matrix_rows}x{matrix_cols} (input_size={input_size})")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        matrices, labels, test_size=0.2, random_state=42, stratify=labels
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")

    # Create datasets and dataloaders
    train_dataset = MatrixDataset(X_train, y_train)
    val_dataset = MatrixDataset(X_val, y_val)
    test_dataset = MatrixDataset(X_test, y_test)

    batch_size = 32
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False)

    # Initialize model
    model = MatrixClassifier(
        input_size=input_size,
        hidden_sizes=[128, 64, 32],
        dropout_rate=0.2
    ).to(device)

    # The below, if uncommented, prints the model architecture
    # print(f"\nModel architecture:")
    # print(model)

    # Train model
    print("\nTraining model...")
    train_losses, val_losses, train_accs, val_accs = train_model(
        model, train_loader, val_loader, epochs=epochs, lr=lr
    )

    # Evaluate on test set
    print("\nEvaluating on test set...")
    model.eval()
    test_preds = []
    test_targets = []

    with torch.no_grad():
        for batch_matrices, batch_labels in test_loader:
            batch_matrices = batch_matrices.to(device)
            outputs = model(batch_matrices).squeeze()
            predictions = (outputs > 0.5).cpu().numpy()
            test_preds.extend(predictions)
            test_targets.extend(batch_labels.numpy())

    print(f"Accuracy: {accuracy_score(test_targets, test_preds):.4f}")

    # Plot training history
    plot_training_history(train_losses, val_losses, train_accs, val_accs)

    # Save the trained model
    model_save_path = '/workspaces/knot_mosaics/training/matrix_classifier_model.pth'
    torch.save(model.state_dict(), model_save_path)
    print(f"\nModel saved as '{model_save_path}'")

    return model


def load_and_use_model(model_path='/workspaces/knot_mosaics/training/matrix_classifier_model.pth'):
    """Load a saved model and use it for prediction"""

    # Load data to detect matrix dimensions
    _, _, matrix_rows, matrix_cols = load_your_data()
    input_size = matrix_rows * matrix_cols

    # Initialize model with same architecture
    model = MatrixClassifier(
        input_size=input_size,
        hidden_sizes=[128, 64, 32],
        dropout_rate=0.2
    ).to(device)

    # Load saved weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    # Example usage with detected dimensions
    test_matrix = np.random.randint(0, 11, size=(matrix_rows, matrix_cols))
    prediction, confidence = predict_single_matrix(model, test_matrix)

    print(f"Test matrix ({matrix_rows}x{matrix_cols}):\n{test_matrix}")
    print(f"Prediction: {prediction}, Confidence: {confidence:.4f}")

    return model


#if __name__ == "__main__":
    # Train a new model
    # trained_model = main()

    # Or load and use an existing model
    # loaded_model = load_and_use_model('matrix_classifier_model.pth')