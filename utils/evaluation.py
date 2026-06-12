"""
utils/evaluation.py — Smart Paddy AI: Model Evaluation & Research Metrics
Place at: smart_paddy_ai/utils/evaluation.py

Provides:
  - Confusion matrix
  - Classification report (precision, recall, F1)
  - ROC curves (one-vs-rest)
  - Per-class metrics display for Streamlit
"""

import os
import io
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
)

CONFUSION_MATRIX_PATH = "model/confusion_matrix.png"
TRAINING_CURVES_PATH  = "model/training_curves.png"
CLASS_IDX_PATH        = "model/class_indices.json"


def _get_class_names() -> list[str]:
    """Load class names from saved index file."""
    if os.path.exists(CLASS_IDX_PATH):
        with open(CLASS_IDX_PATH) as f:
            idx = json.load(f)
        return [k for k, _ in sorted(idx.items(), key=lambda x: x[1])]
    return []


def plot_confusion_matrix(
    y_true: list[int],
    y_pred: list[int],
    class_names: list[str] | None = None,
    save_path: str | None = None,
) -> bytes:
    """
    Plot and return confusion matrix as PNG bytes.

    Parameters
    ----------
    y_true      : list of true class indices
    y_pred      : list of predicted class indices
    class_names : optional label list
    save_path   : optional path to save PNG

    Returns
    -------
    PNG image bytes
    """
    if class_names is None:
        class_names = _get_class_names() or [str(i) for i in range(max(y_true) + 1)]

    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm_norm,
        annot=cm,
        fmt="d",
        cmap="Greens",
        xticklabels=class_names,
        yticklabels=class_names,
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold", pad=12)
    ax.set_ylabel("True Label", fontsize=11)
    ax.set_xlabel("Predicted Label", fontsize=11)
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def compute_classification_report(
    y_true: list[int],
    y_pred: list[int],
    class_names: list[str] | None = None,
) -> dict:
    """
    Return classification metrics as a structured dict.

    Returns
    -------
    dict with keys: per_class (dict), accuracy (float), macro_avg, weighted_avg
    """
    if class_names is None:
        class_names = _get_class_names() or [str(i) for i in range(max(y_true) + 1)]

    report = classification_report(
        y_true, y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    per_class = {
        name: {
            "precision": round(report[name]["precision"] * 100, 1),
            "recall":    round(report[name]["recall"]    * 100, 1),
            "f1":        round(report[name]["f1-score"]  * 100, 1),
            "support":   int(report[name]["support"]),
        }
        for name in class_names
    }

    return {
        "per_class":    per_class,
        "accuracy":     round(report["accuracy"] * 100, 2),
        "macro_avg":    {k: round(v * 100, 1) for k, v in report["macro avg"].items() if k != "support"},
        "weighted_avg": {k: round(v * 100, 1) for k, v in report["weighted avg"].items() if k != "support"},
    }


def plot_roc_curves(
    y_true_binarised: np.ndarray,
    y_prob:           np.ndarray,
    class_names:      list[str] | None = None,
) -> bytes:
    """
    Plot one-vs-rest ROC curves for all classes.

    Parameters
    ----------
    y_true_binarised : (n_samples, n_classes) binary matrix
    y_prob           : (n_samples, n_classes) probability matrix
    class_names      : optional label list

    Returns
    -------
    PNG bytes
    """
    if class_names is None:
        class_names = _get_class_names()

    n_classes = y_true_binarised.shape[1]
    colors_   = plt.cm.Set1(np.linspace(0, 0.8, n_classes))

    fig, ax = plt.subplots(figsize=(8, 6))

    for i, (cls, col) in enumerate(zip(class_names, colors_)):
        fpr, tpr, _ = roc_curve(y_true_binarised[:, i], y_prob[:, i])
        roc_auc     = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=col, lw=2, label=f"{cls} (AUC = {roc_auc:.2f})")

    ax.plot([0, 1], [0, 1], "k--", lw=1.5, label="Random Classifier")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate", fontsize=11)
    ax.set_ylabel("True Positive Rate", fontsize=11)
    ax.set_title("ROC Curves (One-vs-Rest)", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def load_training_plots() -> tuple[bytes | None, bytes | None]:
    """
    Load saved training curve and confusion matrix PNGs.

    Returns
    -------
    (training_curves_bytes, confusion_matrix_bytes) — None if file missing.
    """
    def _load(path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        return None

    return _load(TRAINING_CURVES_PATH), _load(CONFUSION_MATRIX_PATH)