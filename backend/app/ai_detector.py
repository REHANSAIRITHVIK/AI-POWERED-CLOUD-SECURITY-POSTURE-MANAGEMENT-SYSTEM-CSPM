# ai_detector.py
"""
Simple AI detector: uses heuristic + toy ML model (LogisticRegression on synthetic
examples). This is intentionally simple so you can extend later with real data.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import json

class AIDetector:
    def __init__(self):
        # instantiate vectorizer and classifier
        self.vec = TfidfVectorizer()
        self.clf = LogisticRegression()
        self._trained = False
        self._train_on_synthetic_samples()

    def _train_on_synthetic_samples(self):
        # synthetic training dataset (you should replace with real labeled CSPM data)
        samples = [
            '{"type":"s3","acl":"public-read","encryption":false, "versioning":false}',
            '{"type":"s3","acl":"private","encryption":true, "versioning":true}',
            '{"type":"vm","port22":true,"os":"linux","public_ip":true}',
            '{"type":"vm","port22":false,"public_ip":false}',
            '{"type":"iam","policy":"*","principals":"*"}',
            '{"type":"iam","policy":"allow_read","principals":"specific"}'
        ]
        # labels: 1 means risky, 0 means ok
        labels = [1,0,1,0,1,0]
        X = self.vec.fit_transform(samples)
        self.clf.fit(X, labels)
        self._trained = True

    def score_config(self, config: dict) -> float:
        """
        Returns a risk score between 0 and 1.
        We stringify certain keys to feed to vectorizer.
        """
        text = json.dumps(config, sort_keys=True)
        X = self.vec.transform([text])
        prob = self.clf.predict_proba(X)[0][1]  # probability of risky=1
        # clamp
        return float(prob)

    def explain(self, config: dict) -> str:
        # simple heuristic explanation
        c = config
        reasons = []
        # s3-like checks
        t = c.get("type","").lower()
        if t == "s3" or t == "storage":
            if c.get("acl", "").lower() in ("public-read", "public-read-write", "public"):
                reasons.append("Public ACL (public-read/public)")
            if not c.get("encryption", True):
                reasons.append("No encryption at rest")
            if not c.get("versioning", False):
                reasons.append("Versioning not enabled")
        if t in ("vm","instance","ec2"):
            if c.get("open_ports"):
                if 22 in c.get("open_ports", []) or "22" in map(str, c.get("open_ports", [])):
                    reasons.append("SSH port open to the internet")
            if c.get("public_ip", False):
                reasons.append("Publicly accessible instance")
        if "policy" in c:
            p = str(c.get("policy", "")).lower()
            if p.strip() == "*" or "allow all" in p or "iam:*" in p:
                reasons.append("Overly permissive IAM policy")
        if not reasons:
            reasons.append("Model flagged risk based on learned patterns")
        return "; ".join(reasons)
