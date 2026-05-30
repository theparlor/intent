#!/usr/bin/env python3
"""
test_flight_model.py — D-WIRE deterministic flight model tests

These tests ENCODE THE THESIS of the flight model:
- STALL is the worse crash (valueless safe action ≠ comfortable default)
- Thrust (T = strategic_value × λ) is the value term
- OVERSPEED when Gravity exceeds Lift
- Uncertainty demotion preserves the probe/shadow-autonomy recommendation
- λ throttle shifts bands upward

Run: python3 test_flight_model.py
"""

import os
import sys
import unittest

# Ensure we import from the same directory as this test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flight_model import (
    FlightModel,
    Envelope,
    load_variance_estimate,
    BAND_CUTOFFS,
    DISPERSION_DEMOTE,
    OVERSPEED_MARGIN,
    STALL_MARGIN,
)


class TestHighValueAirworthy(unittest.TestCase):
    """Test 1: High strategic value + high Lift + low Gravity → AIRWORTHY L3/L4."""

    def test_bold_safe_action_is_airworthy_high_band(self):
        fm = FlightModel(
            strategic_value=0.9,
            blast_radius=0.15,
            irreversibility=0.10,
            exposure=0.15,
            containment_posture=0.85,
            detection_speed=0.80,
            recovery_options=0.80,
            lam=1.0,
            drag=0.10,
            max_dispersion=0.10,  # low dispersion — panel converges
        )
        result = fm.compute()

        self.assertEqual(result["envelope"], Envelope.AIRWORTHY)
        self.assertIn(result["band"], ("L3", "L4"), msg=f"Expected L3 or L4, got {result['band']}")

    def test_no_stall_flag_when_airworthy(self):
        fm = FlightModel(
            strategic_value=0.9,
            blast_radius=0.15,
            irreversibility=0.10,
            exposure=0.15,
            containment_posture=0.85,
            detection_speed=0.80,
            recovery_options=0.80,
            lam=1.0,
            drag=0.10,
            max_dispersion=0.10,
        )
        result = fm.compute()
        self.assertNotIn("STALL", result["recommended_action"].upper())


class TestValueTermStall(unittest.TestCase):
    """
    Test 2 — THE VALUE-TERM TEST (thesis anchor).

    When strategic_value ≈ 0.05 and everything else is perfectly safe
    (W tiny, L high), the envelope MUST be STALL — not a comfortable safe L0.
    A valueless action that produces no stall is the failure mode the model
    was built to prevent. If this test passes, the value term works.
    """

    def test_low_value_produces_stall_not_comfortable_default(self):
        fm = FlightModel(
            strategic_value=0.05,   # near-zero strategic value
            blast_radius=0.05,      # tiny gravity
            irreversibility=0.05,
            exposure=0.05,
            containment_posture=0.95,  # excellent containment
            detection_speed=0.95,
            recovery_options=0.95,
            lam=1.0,
            drag=0.10,
            max_dispersion=0.05,
        )
        result = fm.compute()

        self.assertEqual(
            result["envelope"],
            Envelope.STALL,
            msg=(
                "A near-zero strategic_value action must STALL — not a comfortable safe default. "
                f"Got envelope={result['envelope']}, band={result['band']}. "
                "If this fails, the value term is absent and the model operationalizes caution, not strategy."
            ),
        )
        self.assertEqual(result["band"], "L0")

        action_upper = result["recommended_action"].upper()
        self.assertTrue(
            "STALL" in action_upper or "RAISE" in action_upper or "THROTTLE" in action_upper
            or "BRAVERY" in action_upper or "LAMBDA" in action_upper or "CAUTION" in action_upper
            or "DOES NOT CLEAR" in action_upper or "WORSE CRASH" in action_upper,
            msg=f"STALL action must mention the stall condition. Got: {result['recommended_action']}",
        )
        # The action must NOT frame the stall as a comfortable/acceptable resting state.
        # We check for the positive framing pattern "is a safe default" (affirmative without negation),
        # not the negation "NOT a safe default" which is exactly what we WANT.
        action_lower = result["recommended_action"].lower()
        self.assertNotIn(
            "is a safe default",
            action_lower,
            msg="STALL action must not frame do-nothing as a safe default (without negation)",
        )
        # Also ensure the word "comfortable" doesn't appear in an affirmative framing
        # (checking "comfortable default" — the affirmative form we're guarding against)
        self.assertNotIn(
            "comfortable default",
            action_lower,
            msg="STALL action must not describe as 'comfortable default'",
        )

    def test_stall_band_is_L0_not_higher(self):
        fm = FlightModel(
            strategic_value=0.02,
            blast_radius=0.01,
            irreversibility=0.01,
            exposure=0.01,
            containment_posture=0.99,
            detection_speed=0.99,
            recovery_options=0.99,
            lam=1.0,
            drag=0.15,
            max_dispersion=0.05,
        )
        result = fm.compute()
        self.assertEqual(result["band"], "L0")
        self.assertEqual(result["envelope"], Envelope.STALL)


class TestOverspeed(unittest.TestCase):
    """Test 3: High Gravity + low Lift → OVERSPEED → L0, action mentions Lift."""

    def test_high_gravity_low_lift_is_overspeed(self):
        fm = FlightModel(
            strategic_value=0.8,
            blast_radius=0.9,
            irreversibility=0.9,
            exposure=0.9,
            containment_posture=0.15,
            detection_speed=0.20,
            recovery_options=0.25,
            lam=1.0,
            drag=0.10,
            max_dispersion=0.10,
        )
        result = fm.compute()

        self.assertEqual(result["envelope"], Envelope.OVERSPEED)
        self.assertEqual(result["band"], "L0")

        action_upper = result["recommended_action"].upper()
        self.assertIn(
            "LIFT",
            action_upper,
            msg=f"OVERSPEED action must mention Lift investment. Got: {result['recommended_action']}",
        )

    def test_overspeed_gravity_exceeds_lift(self):
        fm = FlightModel(
            strategic_value=0.5,
            blast_radius=0.9,
            irreversibility=0.9,
            exposure=0.9,
            containment_posture=0.20,
            detection_speed=0.20,
            recovery_options=0.20,
            lam=1.0,
            drag=0.10,
            max_dispersion=0.10,
        )
        result = fm.compute()
        # W = 0.9 × 0.9 × 0.9 = 0.729; L = mean(0.20,0.20,0.20) = 0.20; W > L
        self.assertGreater(result["W"], result["L"])
        self.assertEqual(result["envelope"], Envelope.OVERSPEED)


class TestThrottleTest(unittest.TestCase):
    """
    Test 4 — THROTTLE TEST.

    A moderate case at λ=1 lands at some band. The SAME case at λ=2 must land at
    a strictly HIGHER or equal band, AND a stalling case at λ=1 must move to
    AIRWORTHY at λ=2 (raising bravery increases thrust past the stall threshold).
    """

    def _make_moderate(self, lam):
        return FlightModel(
            strategic_value=0.40,
            blast_radius=0.30,
            irreversibility=0.25,
            exposure=0.30,
            containment_posture=0.60,
            detection_speed=0.65,
            recovery_options=0.55,
            lam=lam,
            drag=0.10,
            max_dispersion=0.15,
        )

    def _make_stalling(self, lam):
        # strategic_value=0.10 → T=0.10 at λ=1, T=0.20 at λ=2
        # drag=0.15 → stalls at λ=1 (0.10 <= 0.15); airworthy at λ=2 (0.20 > 0.15)
        return FlightModel(
            strategic_value=0.10,
            blast_radius=0.10,
            irreversibility=0.10,
            exposure=0.10,
            containment_posture=0.70,
            detection_speed=0.70,
            recovery_options=0.70,
            lam=lam,
            drag=0.15,
            max_dispersion=0.10,
        )

    BAND_ORDER = ["L0", "L1", "L2", "L3", "L4"]

    def test_higher_lambda_does_not_lower_band(self):
        r1 = self._make_moderate(lam=1.0).compute()
        r2 = self._make_moderate(lam=2.0).compute()

        b1 = self.BAND_ORDER.index(r1["band"])
        b2 = self.BAND_ORDER.index(r2["band"])

        self.assertGreaterEqual(
            b2, b1,
            msg=f"λ=2 should not lower the band below λ=1: {r1['band']} → {r2['band']}",
        )

    def test_lambda_lifts_stall_to_airworthy(self):
        r_stall = self._make_stalling(lam=1.0).compute()
        r_air = self._make_stalling(lam=2.0).compute()

        self.assertEqual(
            r_stall["envelope"],
            Envelope.STALL,
            msg=f"Expected STALL at λ=1, got {r_stall['envelope']}. Check drag/strategic_value setup.",
        )
        self.assertEqual(
            r_air["envelope"],
            Envelope.AIRWORTHY,
            msg=f"Expected AIRWORTHY at λ=2, got {r_air['envelope']}. Throttle should lift thrust past drag.",
        )


class TestUncertaintyDemotion(unittest.TestCase):
    """
    Test 5 — UNCERTAINTY DEMOTION.

    An otherwise-L3 airworthy case with max_dispersion=0.6 must be demoted to L2,
    and the recommended_action must mention probe or shadow-autonomy.
    """

    def _make_l3_case(self, max_dispersion):
        # Calibrated to land at L3 pre-demotion: margin needs to be in [0.35, 0.55)
        # W low, L high, T > D
        return FlightModel(
            strategic_value=0.80,
            blast_radius=0.20,
            irreversibility=0.20,
            exposure=0.20,
            containment_posture=0.75,
            detection_speed=0.75,
            recovery_options=0.75,
            lam=1.0,
            drag=0.10,
            max_dispersion=max_dispersion,
        )

    def test_high_dispersion_demotes_band(self):
        r_low_disp = self._make_l3_case(max_dispersion=0.10).compute()
        r_high_disp = self._make_l3_case(max_dispersion=0.60).compute()

        # Pre-demotion case should be L3 or L4
        self.assertIn(r_low_disp["band"], ("L3", "L4"),
                      msg=f"Base case should be L3/L4, got {r_low_disp['band']}")

        # High-dispersion case must be demoted by one band
        BAND_ORDER = ["L0", "L1", "L2", "L3", "L4"]
        b_low = BAND_ORDER.index(r_low_disp["band"])
        b_high = BAND_ORDER.index(r_high_disp["band"])
        self.assertEqual(
            b_high, b_low - 1,
            msg=(
                f"High dispersion should demote by 1 band: "
                f"{r_low_disp['band']}→expected {BAND_ORDER[b_low-1]}, got {r_high_disp['band']}"
            ),
        )

    def test_high_dispersion_mentions_probe_or_shadow(self):
        r = self._make_l3_case(max_dispersion=0.60).compute()
        action_lower = r["recommended_action"].lower()
        self.assertTrue(
            "probe" in action_lower or "shadow" in action_lower,
            msg=f"High-dispersion action should mention probe/shadow-autonomy. Got: {r['recommended_action']}",
        )


class TestEndToEndSampleFile(unittest.TestCase):
    """Test 6: Parse shipped sample-variance-estimate.yaml end-to-end → valid band."""

    def test_sample_file_produces_valid_result(self):
        sample_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "sample-variance-estimate.yaml",
        )
        self.assertTrue(os.path.exists(sample_path), f"Sample file missing: {sample_path}")

        facets, meta = load_variance_estimate(sample_path)

        VALID_FACETS = {
            "strategic_value", "blast_radius", "irreversibility", "exposure",
            "containment_posture", "detection_speed", "recovery_options",
        }
        for f in VALID_FACETS:
            self.assertIn(f, facets, msg=f"Missing facet: {f}")
            val = facets[f]
            self.assertIsInstance(val, float)
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)

        self.assertIn("max_dispersion", meta)
        self.assertIn("routing_hint", meta)

        fm = FlightModel(
            strategic_value=facets["strategic_value"],
            blast_radius=facets["blast_radius"],
            irreversibility=facets["irreversibility"],
            exposure=facets["exposure"],
            containment_posture=facets["containment_posture"],
            detection_speed=facets["detection_speed"],
            recovery_options=facets["recovery_options"],
            drag=0.10,
            max_dispersion=meta["max_dispersion"],
        )
        result = fm.compute()

        VALID_BANDS = {"L0", "L1", "L2", "L3", "L4"}
        self.assertIn(result["band"], VALID_BANDS)
        VALID_ENVELOPES = {Envelope.AIRWORTHY, Envelope.STALL, Envelope.OVERSPEED}
        self.assertIn(result["envelope"], VALID_ENVELOPES)


class TestFallbackParser(unittest.TestCase):
    """
    Test 7: Fallback YAML parser yields same facet values as pyyaml
    (or tests the fallback path directly when pyyaml is absent).
    """

    def test_fallback_parser_on_sample(self):
        """
        Import the fallback parser directly and compare its output against the
        load_variance_estimate result on the sample file.
        """
        from flight_model import _fallback_load_variance_estimate, load_variance_estimate

        sample_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "sample-variance-estimate.yaml",
        )

        facets_main, meta_main = load_variance_estimate(sample_path)
        facets_fb, meta_fb = _fallback_load_variance_estimate(sample_path)

        VALID_FACETS = [
            "strategic_value", "blast_radius", "irreversibility", "exposure",
            "containment_posture", "detection_speed", "recovery_options",
        ]
        for f in VALID_FACETS:
            self.assertIn(f, facets_fb, msg=f"Fallback missing facet {f}")
            self.assertAlmostEqual(
                facets_main[f],
                facets_fb[f],
                places=3,
                msg=f"Fallback mismatch on {f}: main={facets_main[f]}, fallback={facets_fb[f]}",
            )

        # max_dispersion should match
        self.assertAlmostEqual(
            meta_main["max_dispersion"],
            meta_fb["max_dispersion"],
            places=3,
            msg="Fallback max_dispersion mismatch",
        )


class TestInvariants(unittest.TestCase):
    """Additional invariant checks: band ordering, binding constraint, inputs preserved."""

    def test_result_includes_all_required_keys(self):
        fm = FlightModel(
            strategic_value=0.5, blast_radius=0.3, irreversibility=0.3, exposure=0.3,
            containment_posture=0.6, detection_speed=0.6, recovery_options=0.6,
            lam=1.0, drag=0.10, max_dispersion=0.15,
        )
        result = fm.compute()
        required = {"inputs", "W", "T", "L", "D", "envelope", "band",
                    "binding_constraint", "recommended_action", "uncertainty"}
        for key in required:
            self.assertIn(key, result, msg=f"Missing key: {key}")

    def test_inputs_preserved_in_result(self):
        fm = FlightModel(
            strategic_value=0.7, blast_radius=0.2, irreversibility=0.2, exposure=0.2,
            containment_posture=0.7, detection_speed=0.7, recovery_options=0.7,
            lam=1.5, drag=0.12, max_dispersion=0.20,
        )
        result = fm.compute()
        self.assertAlmostEqual(result["inputs"]["strategic_value"], 0.7)
        self.assertAlmostEqual(result["inputs"]["lam"], 1.5)

    def test_stall_uses_envelope_flag(self):
        """STALL envelope should always produce band=L0."""
        fm = FlightModel(
            strategic_value=0.05,
            blast_radius=0.10, irreversibility=0.10, exposure=0.10,
            containment_posture=0.80, detection_speed=0.80, recovery_options=0.80,
            lam=1.0, drag=0.20,
            max_dispersion=0.05,
        )
        result = fm.compute()
        if result["envelope"] == Envelope.STALL:
            self.assertEqual(result["band"], "L0")

    def test_airworthy_band_increases_with_margin(self):
        """Wider margin → higher band (all else equal)."""
        # Wide margin case
        fm_wide = FlightModel(
            strategic_value=0.95,
            blast_radius=0.05, irreversibility=0.05, exposure=0.05,
            containment_posture=0.95, detection_speed=0.95, recovery_options=0.95,
            lam=1.0, drag=0.05, max_dispersion=0.05,
        )
        # Narrow margin case (barely airworthy)
        fm_narrow = FlightModel(
            strategic_value=0.35,
            blast_radius=0.30, irreversibility=0.30, exposure=0.30,
            containment_posture=0.40, detection_speed=0.40, recovery_options=0.40,
            lam=1.0, drag=0.10, max_dispersion=0.05,
        )
        r_wide = fm_wide.compute()
        r_narrow = fm_narrow.compute()

        BAND_ORDER = ["L0", "L1", "L2", "L3", "L4"]
        if r_wide["envelope"] == Envelope.AIRWORTHY and r_narrow["envelope"] == Envelope.AIRWORTHY:
            b_wide = BAND_ORDER.index(r_wide["band"])
            b_narrow = BAND_ORDER.index(r_narrow["band"])
            self.assertGreaterEqual(b_wide, b_narrow,
                                    msg=f"Wide-margin should not produce lower band than narrow: {r_wide['band']} vs {r_narrow['band']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
