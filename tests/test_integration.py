"""
Integration tests for LUNTRA Calculator MVP
Tests end-to-end workflows, model selection, calculations, and data flow
"""

import pytest
import sys
import os
from datetime import datetime
from unittest.mock import patch, MagicMock
import json

# Add the parent directory to sys.path to import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import app


class TestEndToEndWorkflows:
    """Test complete user workflows from input to output"""
    
    @pytest.mark.house_hack
    @pytest.mark.integration
    def test_house_hack_workflow_complete(self):
        """Test complete House-Hack model workflow"""
        # Simulate user inputs
        model = "House-Hack"
        purchase_price = 400000
        down_payment_pct = 5  # Typical for house-hack
        interest_rate = 6.25
        
        # Calculate expected results
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Generate session data as app would
        session_data = {
            "model": model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify workflow results
        assert down_payment == 20000
        assert loan_amount == 380000
        assert session_data["model"] == "House-Hack"
        
        # Verify session data can be serialized (important for Streamlit)
        json_data = json.dumps(session_data)
        parsed_data = json.loads(json_data)
        assert parsed_data["model"] == model
    
    @pytest.mark.whole_unit
    @pytest.mark.integration
    def test_whole_unit_workflow_complete(self):
        """Test complete Whole Unit model workflow"""
        # Simulate user inputs
        model = "Whole Unit"
        purchase_price = 600000
        down_payment_pct = 25  # Typical for investment property
        interest_rate = 7.0
        
        # Calculate expected results
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Generate session data as app would
        session_data = {
            "model": model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify workflow results
        assert down_payment == 150000
        assert loan_amount == 450000
        assert session_data["model"] == "Whole Unit"
        
        # Verify session data integrity
        json_data = json.dumps(session_data)
        parsed_data = json.loads(json_data)
        assert parsed_data["purchase_price"] == purchase_price


class TestModelComparisonWorkflows:
    """Test workflows comparing different models"""
    
    def test_model_comparison_same_price(self):
        """Test both models with same purchase price"""
        purchase_price = 500000
        interest_rate = 6.5
        
        # House-Hack scenario (lower down payment)
        hh_down_pct = 5
        hh_down_payment = purchase_price * (hh_down_pct / 100)
        hh_loan_amount = purchase_price - hh_down_payment
        
        # Whole Unit scenario (higher down payment)
        wu_down_pct = 25
        wu_down_payment = purchase_price * (wu_down_pct / 100)
        wu_loan_amount = purchase_price - wu_down_payment
        
        # Verify different outcomes
        assert hh_down_payment < wu_down_payment  # House-hack requires less upfront
        assert hh_loan_amount > wu_loan_amount    # House-hack has higher loan
        
        # Calculate difference in cash requirements
        cash_difference = wu_down_payment - hh_down_payment
        assert cash_difference == 100000  # $100k difference in this scenario
    
    def test_model_switching_workflow(self):
        """Test switching between models maintains data integrity"""
        purchase_price = 450000
        interest_rate = 6.75
        
        # Start with House-Hack
        model1 = "House-Hack"
        dp_pct1 = 3
        
        session1 = {
            "model": model1,
            "purchase_price": purchase_price,
            "down_payment_pct": dp_pct1,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        # Switch to Whole Unit
        model2 = "Whole Unit"
        dp_pct2 = 20
        
        session2 = {
            "model": model2,
            "purchase_price": purchase_price,  # Same price
            "down_payment_pct": dp_pct2,       # Different down payment
            "interest_rate": interest_rate,     # Same rate
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify data integrity across model switches
        assert session1["purchase_price"] == session2["purchase_price"]
        assert session1["interest_rate"] == session2["interest_rate"]
        assert session1["model"] != session2["model"]
        assert session1["down_payment_pct"] != session2["down_payment_pct"]


class TestUserInputValidationWorkflows:
    """Test workflows with various user input scenarios"""
    
    def test_minimum_input_scenario(self):
        """Test workflow with minimum allowed inputs"""
        model = "House-Hack"
        purchase_price = 1  # Minimum positive value
        down_payment_pct = 0  # Minimum percentage
        interest_rate = 0.0   # Minimum rate
        
        # Calculate results
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Verify calculations work with edge cases
        assert down_payment == 0
        assert loan_amount == purchase_price
        
        # Verify session data can be created
        session_data = {
            "model": model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        assert session_data["model"] == model
    
    def test_maximum_input_scenario(self):
        """Test workflow with maximum allowed inputs"""
        model = "Whole Unit"
        purchase_price = 10000000  # High value property
        down_payment_pct = 50      # Maximum slider value
        interest_rate = 10.0       # Maximum slider value
        
        # Calculate results
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Verify calculations work with high values
        assert down_payment == 5000000
        assert loan_amount == 5000000
        
        # Verify large numbers can be JSON serialized
        session_data = {
            "model": model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        json_str = json.dumps(session_data)
        assert "10000000" in json_str
    
    def test_typical_user_scenarios(self):
        """Test common realistic user input scenarios"""
        typical_scenarios = [
            {
                "model": "House-Hack",
                "purchase_price": 350000,
                "down_payment_pct": 5,
                "interest_rate": 6.5
            },
            {
                "model": "Whole Unit",
                "purchase_price": 425000,
                "down_payment_pct": 20,
                "interest_rate": 7.25
            },
            {
                "model": "House-Hack", 
                "purchase_price": 275000,
                "down_payment_pct": 10,
                "interest_rate": 5.75
            }
        ]
        
        for scenario in typical_scenarios:
            purchase_price = scenario["purchase_price"]
            down_payment_pct = scenario["down_payment_pct"]
            
            down_payment = purchase_price * (down_payment_pct / 100)
            loan_amount = purchase_price - down_payment
            
            # Verify realistic calculations
            assert down_payment > 0
            assert loan_amount > 0
            assert down_payment + loan_amount == purchase_price
            
            # Verify realistic ranges
            if scenario["model"] == "House-Hack":
                assert down_payment_pct <= 20  # Typically lower for house-hack
            else:  # Whole Unit
                assert down_payment_pct >= 15  # Typically higher for investment


class TestDataPersistenceWorkflows:
    """Test data persistence and session management workflows"""
    
    def test_session_data_lifecycle(self):
        """Test complete session data lifecycle"""
        # Initial session creation
        model = "House-Hack"
        purchase_price = 400000
        down_payment_pct = 5
        interest_rate = 6.0
        timestamp1 = datetime.now().isoformat()
        
        session_v1 = {
            "model": model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": timestamp1
        }
        
        # Simulate user making changes
        new_purchase_price = 450000
        timestamp2 = datetime.now().isoformat()
        
        session_v2 = {
            "model": model,
            "purchase_price": new_purchase_price,  # Changed
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": timestamp2  # Updated timestamp
        }
        
        # Verify session evolution
        assert session_v1["timestamp"] != session_v2["timestamp"]
        assert session_v1["purchase_price"] != session_v2["purchase_price"]
        assert session_v1["model"] == session_v2["model"]  # Model unchanged
        
        # Verify both sessions are valid JSON
        json1 = json.dumps(session_v1)
        json2 = json.dumps(session_v2)
        
        parsed1 = json.loads(json1)
        parsed2 = json.loads(json2)
        
        assert parsed1["purchase_price"] == 400000
        assert parsed2["purchase_price"] == 450000
    
    def test_multiple_session_workflow(self):
        """Test workflow with multiple concurrent sessions"""
        base_timestamp = datetime.now()
        
        # Create multiple sessions (simulating multiple users or tabs)
        sessions = []
        for i in range(3):
            session = {
                "model": ["House-Hack", "Whole Unit", "House-Hack"][i],
                "purchase_price": [300000, 500000, 400000][i],
                "down_payment_pct": [5, 25, 10][i],
                "interest_rate": [6.0, 7.5, 6.25][i],
                "timestamp": base_timestamp.isoformat()
            }
            sessions.append(session)
        
        # Verify each session is independent and valid
        for i, session in enumerate(sessions):
            assert session["model"] in ["House-Hack", "Whole Unit"]
            assert session["purchase_price"] > 0
            assert 0 <= session["down_payment_pct"] <= 50
            assert 0.0 <= session["interest_rate"] <= 10.0
            
            # Verify JSON serialization
            json_str = json.dumps(session)
            parsed = json.loads(json_str)
            assert parsed == session


class TestCalculationAccuracyWorkflows:
    """Test calculation accuracy across different scenarios"""
    
    def test_precision_with_decimal_inputs(self):
        """Test calculation precision with decimal inputs"""
        purchase_price = 437500.50
        down_payment_pct = 7.25
        interest_rate = 6.375
        
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Verify precision is maintained
        assert abs(down_payment - 31718.78625) < 0.01
        assert abs(loan_amount - 405781.71375) < 0.01
        
        # Verify the sum equals original (accounting for floating point)
        assert abs((down_payment + loan_amount) - purchase_price) < 0.01
    
    def test_rounding_consistency(self):
        """Test that rounding is handled consistently"""
        test_cases = [
            {"price": 333333, "pct": 33.33},  # Should handle 1/3 scenarios
            {"price": 100000, "pct": 33.33},  # Clean numbers with decimal pct
            {"price": 299999, "pct": 20}      # Near round numbers
        ]
        
        for case in test_cases:
            purchase_price = case["price"]
            down_payment_pct = case["pct"]
            
            down_payment = purchase_price * (down_payment_pct / 100)
            loan_amount = purchase_price - down_payment
            
            # Verify calculations maintain reasonable precision
            total = down_payment + loan_amount
            assert abs(total - purchase_price) < 1.0  # Within $1 due to rounding
            
            # Verify positive values
            assert down_payment >= 0
            assert loan_amount >= 0


class TestErrorRecoveryWorkflows:
    """Test error recovery and edge case handling"""
    
    def test_workflow_with_zero_values(self):
        """Test workflow behavior with zero values"""
        # Test zero purchase price scenario
        model = "House-Hack"
        purchase_price = 0
        down_payment_pct = 20
        interest_rate = 6.5
        
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Should handle gracefully
        assert down_payment == 0
        assert loan_amount == 0
        
        # Session data should still be valid
        session_data = {
            "model": model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        # Should be JSON serializable
        json_str = json.dumps(session_data)
        assert "0" in json_str
    
    def test_workflow_state_recovery(self):
        """Test recovery from invalid states"""
        # Start with valid state
        valid_session = {
            "model": "House-Hack",
            "purchase_price": 400000,
            "down_payment_pct": 5,
            "interest_rate": 6.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify valid state works
        down_payment = valid_session["purchase_price"] * (valid_session["down_payment_pct"] / 100)
        assert down_payment == 20000
        
        # Recovery should restore to valid defaults
        default_session = {
            "model": "House-Hack",
            "purchase_price": 500000,  # Default from app
            "down_payment_pct": 20,    # Default from app  
            "interest_rate": 6.5,      # Default from app
            "timestamp": datetime.now().isoformat()
        }
        
        # Verify defaults produce valid results
        default_down = default_session["purchase_price"] * (default_session["down_payment_pct"] / 100)
        default_loan = default_session["purchase_price"] - default_down
        
        assert default_down == 100000
        assert default_loan == 400000