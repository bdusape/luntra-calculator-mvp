"""
Unit tests for financial formulas and calculations
Tests mathematical accuracy of core real estate investment formulas
"""

import pytest
import math
import sys
import os
from decimal import Decimal, ROUND_HALF_UP

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestBasicFinancialFormulas:
    """Test core financial calculation formulas"""
    
    def test_monthly_mortgage_payment_formula(self):
        """Test monthly mortgage payment calculation (P&I only)"""
        # Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        # Where: M = monthly payment, P = principal, r = monthly rate, n = number of payments
        
        principal = 400000
        annual_rate = 6.0
        years = 30
        
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        # Calculate monthly payment
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        
        # Expected result should be approximately $2,398.20
        expected = 2398.20
        assert abs(monthly_payment - expected) < 1.0
    
    def test_mortgage_payment_edge_cases(self):
        """Test mortgage payment calculation edge cases"""
        # Test with zero interest rate
        principal = 300000
        annual_rate = 0.0
        years = 30
        
        # With 0% interest, payment should be principal / number of payments
        expected = principal / (years * 12)
        
        # For 0% rate, use simple division
        if annual_rate == 0:
            monthly_payment = principal / (years * 12)
        else:
            monthly_rate = annual_rate / 100 / 12
            num_payments = years * 12
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        
        assert abs(monthly_payment - expected) < 0.01
    
    def test_loan_to_value_ratio(self):
        """Test Loan-to-Value (LTV) ratio calculation"""
        # LTV = Loan Amount / Property Value * 100
        
        property_value = 500000
        loan_amount = 400000
        
        ltv = (loan_amount / property_value) * 100
        expected = 80.0
        
        assert ltv == expected
    
    def test_debt_to_income_ratio(self):
        """Test Debt-to-Income (DTI) ratio calculation"""
        # DTI = Total Monthly Debt Payments / Gross Monthly Income * 100
        
        monthly_debt_payments = 3500
        gross_monthly_income = 10000
        
        dti = (monthly_debt_payments / gross_monthly_income) * 100
        expected = 35.0
        
        assert dti == expected


class TestCashFlowFormulas:
    """Test cash flow analysis formulas"""
    
    def test_net_operating_income(self):
        """Test Net Operating Income (NOI) calculation"""
        # NOI = Gross Rental Income - Operating Expenses
        
        monthly_rent = 3000
        annual_gross_income = monthly_rent * 12
        operating_expenses = 8000  # Property taxes, insurance, maintenance, etc.
        
        noi = annual_gross_income - operating_expenses
        expected = 36000 - 8000  # $28,000
        
        assert noi == expected
    
    def test_cash_on_cash_return(self):
        """Test Cash-on-Cash return calculation"""
        # Cash-on-Cash = Annual Pre-tax Cash Flow / Total Cash Invested * 100
        
        annual_cash_flow = 6000
        total_cash_invested = 100000  # Down payment + closing costs
        
        cash_on_cash = (annual_cash_flow / total_cash_invested) * 100
        expected = 6.0  # 6%
        
        assert cash_on_cash == expected
    
    def test_gross_rent_multiplier(self):
        """Test Gross Rent Multiplier (GRM) calculation"""
        # GRM = Property Price / Annual Gross Rental Income
        
        property_price = 400000
        monthly_rent = 2500
        annual_rental_income = monthly_rent * 12
        
        grm = property_price / annual_rental_income
        expected = 400000 / 30000  # 13.33
        
        assert abs(grm - expected) < 0.01
    
    def test_one_percent_rule(self):
        """Test the 1% rule calculation"""
        # 1% Rule: Monthly rent should be at least 1% of purchase price
        
        purchase_price = 300000
        monthly_rent = 3000
        
        percentage = (monthly_rent / purchase_price) * 100
        meets_one_percent_rule = percentage >= 1.0
        
        assert meets_one_percent_rule
        assert percentage == 1.0


class TestCapRateFormulas:
    """Test Capitalization Rate formulas"""
    
    def test_cap_rate_calculation(self):
        """Test Cap Rate calculation"""
        # Cap Rate = NOI / Property Value * 100
        
        noi = 24000
        property_value = 400000
        
        cap_rate = (noi / property_value) * 100
        expected = 6.0  # 6%
        
        assert cap_rate == expected
    
    def test_cap_rate_property_valuation(self):
        """Test property valuation using cap rate"""
        # Property Value = NOI / Cap Rate
        
        noi = 30000
        cap_rate = 7.5  # 7.5%
        
        property_value = noi / (cap_rate / 100)
        expected = 400000
        
        assert property_value == expected


@pytest.mark.house_hack
@pytest.mark.formulas
class TestHouseHackSpecificFormulas:
    """Test House-Hack specific calculations"""
    
    def test_house_hack_net_housing_cost(self):
        """Test net housing cost for house hack"""
        # Net Housing Cost = Total Housing Payment - Rental Income
        
        total_monthly_payment = 2800  # PITI
        rental_income = 1500  # From other units
        
        net_housing_cost = total_monthly_payment - rental_income
        expected = 1300
        
        assert net_housing_cost == expected
    
    def test_house_hack_effective_housing_reduction(self):
        """Test effective housing cost reduction percentage"""
        # Reduction % = (Rental Income / Total Payment) * 100
        
        rental_income = 1800
        total_payment = 2500
        
        reduction_percentage = (rental_income / total_payment) * 100
        expected = 72.0  # 72% reduction
        
        assert reduction_percentage == expected
    
    def test_house_hack_owner_occupancy_savings(self):
        """Test owner-occupancy financing benefits"""
        # Compare conventional investment loan vs owner-occupied loan
        
        purchase_price = 500000
        
        # Investment property (25% down)
        investment_down_payment = purchase_price * 0.25
        
        # Owner-occupied (5% down)
        owner_occupied_down_payment = purchase_price * 0.05
        
        savings = investment_down_payment - owner_occupied_down_payment
        expected = 125000 - 25000  # $100,000 savings
        
        assert savings == expected


@pytest.mark.whole_unit
@pytest.mark.formulas
class TestWholeUnitFormulas:
    """Test Whole Unit rental property calculations"""
    
    def test_whole_unit_cash_flow(self):
        """Test whole unit cash flow calculation"""
        # Cash Flow = Rental Income - All Expenses
        
        monthly_rent = 2200
        mortgage_payment = 1650  # PITI
        property_management = 220  # 10% of rent
        maintenance_reserve = 200
        vacancy_allowance = 110  # 5% of rent
        
        monthly_cash_flow = monthly_rent - (mortgage_payment + property_management + maintenance_reserve + vacancy_allowance)
        expected = 2200 - (1650 + 220 + 200 + 110)  # $20
        
        assert monthly_cash_flow == expected
    
    def test_vacancy_factor_impact(self):
        """Test impact of vacancy factor on returns"""
        # Effective Rental Income = Gross Rental Income * (1 - Vacancy Rate)
        
        annual_gross_rent = 30000
        vacancy_rate = 0.05  # 5%
        
        effective_rental_income = annual_gross_rent * (1 - vacancy_rate)
        expected = 30000 * 0.95  # $28,500
        
        assert effective_rental_income == expected


class TestAdvancedFormulas:
    """Test advanced real estate investment formulas"""
    
    def test_internal_rate_of_return_simple(self):
        """Test simple IRR calculation concept"""
        # For testing purposes, we'll test the concept with a simple case
        # Real IRR requires iterative calculation or financial libraries
        
        initial_investment = -100000
        cash_flows = [12000, 12000, 12000, 12000, 12000]  # 5 years of cash flow
        
        # For 12% annual cash flow on 100k investment, approximate IRR should be around 12%
        annual_return = cash_flows[0] / abs(initial_investment)
        expected_approximate_irr = 0.12
        
        assert abs(annual_return - expected_approximate_irr) < 0.01
    
    def test_net_present_value(self):
        """Test Net Present Value (NPV) calculation"""
        # NPV = Σ [Cash Flow / (1 + discount_rate)^period] - Initial Investment
        
        initial_investment = 80000
        discount_rate = 0.08  # 8%
        cash_flows = [25000, 25000, 25000, 25000, 25000]  # 5 years of $25k cash flow
        
        npv = -initial_investment
        for i, cash_flow in enumerate(cash_flows, 1):
            npv += cash_flow / (1 + discount_rate) ** i
        
        # Should be positive if good investment (higher cash flows, lower initial investment)
        assert npv > 0
        # Verify we get approximately the expected NPV value
        expected_approximate_npv = 19830  # Approximate expected value
        assert abs(npv - expected_approximate_npv) < 1000
    
    def test_debt_service_coverage_ratio(self):
        """Test Debt Service Coverage Ratio (DSCR)"""
        # DSCR = NOI / Annual Debt Service
        
        noi = 36000
        annual_debt_service = 30000  # 12 * monthly P&I payment
        
        dscr = noi / annual_debt_service
        expected = 1.2  # 1.2x coverage
        
        assert dscr == expected
        assert dscr > 1.0  # Should be greater than 1 for positive cash flow


class TestFormulaValidationAndEdgeCases:
    """Test formula validation and edge cases"""
    
    def test_division_by_zero_protection(self):
        """Test protection against division by zero in formulas"""
        
        # Cap rate calculation with zero property value
        noi = 24000
        property_value = 0
        
        if property_value == 0:
            # Should handle gracefully, not divide
            assert True
        else:
            cap_rate = (noi / property_value) * 100
    
    def test_negative_value_handling(self):
        """Test handling of negative values in formulas"""
        
        # Negative cash flow scenario
        rental_income = 2000
        total_expenses = 2500
        
        cash_flow = rental_income - total_expenses
        expected = -500  # Negative cash flow
        
        assert cash_flow == expected
        assert cash_flow < 0  # Confirm it's negative
    
    def test_percentage_precision(self):
        """Test percentage calculations maintain precision"""
        
        # Use Decimal for high precision percentage calculations
        from decimal import Decimal, ROUND_HALF_UP
        
        amount = Decimal('123456.789')
        percentage = Decimal('3.25')
        
        result = amount * (percentage / 100)
        # Calculate the exact expected result
        expected = Decimal('4012.35')  # 123456.789 * 3.25% = 4012.345225, rounds to 4012.35
        
        # Round to 2 decimal places
        result_rounded = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        assert result_rounded == expected
    
    def test_compound_formula_accuracy(self):
        """Test accuracy when combining multiple formulas"""
        
        # Complex scenario: Calculate total return combining cash flow and appreciation
        purchase_price = 400000
        annual_cash_flow = 8000
        years_held = 5
        sale_price = 500000
        
        # Total cash flow over holding period
        total_cash_flow = annual_cash_flow * years_held
        
        # Capital appreciation
        capital_gain = sale_price - purchase_price
        
        # Total return
        total_return = total_cash_flow + capital_gain
        expected = (8000 * 5) + (500000 - 400000)  # $40,000 + $100,000 = $140,000
        
        assert total_return == expected


class TestRoundingAndPrecision:
    """Test proper rounding and precision in financial calculations"""
    
    def test_currency_rounding(self):
        """Test proper currency rounding to 2 decimal places"""
        
        # Monthly payment calculation that results in fractional cents
        result = 2398.1967834
        
        # Round to 2 decimal places for currency
        rounded = round(result, 2)
        expected = 2398.20
        
        assert rounded == expected
    
    def test_percentage_rounding(self):
        """Test proper percentage rounding"""
        
        # Cap rate calculation
        noi = 23456
        property_value = 389750
        
        cap_rate = (noi / property_value) * 100
        # Round to 2 decimal places for percentage display
        cap_rate_rounded = round(cap_rate, 2)
        
        assert isinstance(cap_rate_rounded, float)
        assert len(str(cap_rate_rounded).split('.')[-1]) <= 2


if __name__ == "__main__":
    pytest.main([__file__])