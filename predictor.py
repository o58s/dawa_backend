import torch
import joblib
import numpy as np
import pandas as pd
from scipy import sparse
import torch.nn as nn
import torch.nn.functional as F



class DrugVAE(nn.Module):
    def __init__(self, input_dim=315, hidden_dims=[256, 128], latent_dim=128):
        super().__init__()
        encoder_layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            encoder_layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(0.3),
            ])
            prev_dim = h_dim
        self.encoder = nn.Sequential(*encoder_layers)
        self.fc_mu     = nn.Linear(hidden_dims[-1], latent_dim)
        self.fc_logvar = nn.Linear(hidden_dims[-1], latent_dim)

    def encode(self, x):
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_logvar(h)

    def get_embedding(self, x):
        mu, _ = self.encode(x)
        return mu


class LinkPredictor(nn.Module):
    def __init__(self, drug_dim=128, disease_dim=128, hidden_dims=[256, 128, 64]):
        super().__init__()
        layers = []
        prev_dim = drug_dim + disease_dim
        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(0.3),
            ])
            prev_dim = h_dim
        layers.append(nn.Linear(hidden_dims[-1], 1))
        self.network = nn.Sequential(*layers)

    def forward(self, drug_emb, disease_emb):
        x = torch.cat([drug_emb, disease_emb], dim=1)
        return self.network(x).squeeze(-1)


class Predictor:
    def __init__(self, artifacts_dir):
        print("Loading model artifacts...")

        # Load entity indices
        entity_index = pd.read_parquet(f"{artifacts_dir}/entity_indices.parquet")
        self.drug_index    = entity_index[entity_index['entity_type'] == 'drug'].reset_index(drop=True)
        self.disease_index = entity_index[entity_index['entity_type'] == 'disease'].reset_index(drop=True)

        # Build MESH ID → name lookup (fallback to ID if name is empty)
        self.disease_name_lookup = (
            self.disease_index
            .set_index('entity_id')['name']
            .to_dict()
        )

        # Load pre-computed embeddings
        self.drug_embs    = np.load(f"{artifacts_dir}/drug_embeddings.npy")
        self.disease_embs = np.load(f"{artifacts_dir}/disease_embeddings.npy")

        # Load classifier
        self.device = torch.device('cpu')
        self.classifier = LinkPredictor()
        self.classifier.load_state_dict(
            torch.load(f"{artifacts_dir}/best_classifier.pt", map_location='cpu')
        )
        self.classifier.eval()

        print("Model loaded successfully!")

    def predict_for_drug(self, drug_name: str, top_k: int = 20):
        # Look up drug by name
        mask = self.drug_index['name'].str.lower() == drug_name.lower()
        if not mask.any():
            return None, f"Drug '{drug_name}' not found"

        drug_local_idx = self.drug_index[mask].index[0]

        # Get drug embedding and repeat for all diseases
        drug_emb    = torch.FloatTensor(self.drug_embs[drug_local_idx]).unsqueeze(0)
        drug_emb    = drug_emb.repeat(len(self.disease_embs), 1)
        disease_emb = torch.FloatTensor(self.disease_embs)

        with torch.no_grad():
            logits = self.classifier(drug_emb, disease_emb)
            scores = torch.sigmoid(logits).numpy()

        # Rank and return top K
        top_idx = np.argsort(scores)[::-1][:top_k]
        results = [
            {
                "disease_id":   self.disease_index.iloc[i]['entity_id'],
                "disease_name": self.disease_name_lookup.get(
                                    self.disease_index.iloc[i]['entity_id']
                                ) or self.disease_index.iloc[i]['entity_id'],
                "score":        round(float(scores[i]), 4)
            }
            for i in top_idx
        ]
        return results, None