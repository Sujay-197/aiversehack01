from datetime import datetime
from backend.models import BeliefState, Experiment, Outcome, BeliefUpdate

class Reflector:
    """
    The Learning Loop component.
    Analyzes outcomes and updates the BeliefState (The Failure Passport).
    """

    def reflect(self, belief_state: BeliefState, experiment: Experiment, outcome: Outcome) -> BeliefState:
        """
        Updates the belief state in-place (or returns modified) based on the outcome.
        """
        target_attr = experiment.belief_id
        if not target_attr or target_attr not in belief_state.beliefs:
            print(f"[Reflector] Warning: Linked belief '{target_attr}' not found in state.")
            return belief_state

        belief = belief_state.beliefs[target_attr]
        old_conf = belief.confidence
        new_conf = old_conf
        reason = ""

        # Learning Logic (Calibration)
        if outcome.result == "rejection":
            # Rejection implies our hypothesis was wrong or insufficient.
            # Decay factor depends on experiment type.
            # If we were verifying (High Conf), a rejection is a STRONG negative signal.
            if experiment.type == "verification":
                penalty = 0.15
            else:
                penalty = 0.05
            
            new_conf = max(0.0, old_conf - penalty)
            reason = f"Rejected from '{experiment.type}' experiment. Feedback: {outcome.feedback or 'None'}"

        elif outcome.result == "interview":
            # Interview confirms our hypothesis!
            boost = 0.1
            new_conf = min(1.0, old_conf + boost)
            reason = f"Earned Interview! Validation of '{experiment.type}' expectation."

        elif outcome.result == "ghosted":
            # Weak negative signal
            new_conf = max(0.0, old_conf - 0.02)
            reason = "Ghosted. slight decay."

        # Apply Update
        if new_conf != old_conf:
            belief.confidence = new_conf
            belief.history.append(BeliefUpdate(
                old_confidence=old_conf,
                new_confidence=new_conf,
                reason=reason,
                timestamp=datetime.now()
            ))
            print(f"[Reflector] Updated '{target_attr}': {old_conf:.2f} -> {new_conf:.2f} | Reason: {reason}")
        
        return belief_state
