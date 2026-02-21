def calculate_monthly_payment(principal, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12

    if monthly_interest_rate == 0:
        monthly_payment = principal / number_of_payments
    else:
        monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate)**number_of_payments) / ((1 + monthly_interest_rate)**number_of_payments - 1)

    return monthly_payment


def calculate_total_repayment(monthly_payment, loan_term_years):
    return monthly_payment * loan_term_years * 12


def calculate_total_interest(total_repayment, principal):
    return total_repayment - principal


def calculate_impact_of_extra_payments(principal, annual_interest_rate, loan_term_years, extra_payment):
    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, loan_term_years)
    monthly_interest_rate = annual_interest_rate / 100 / 12
    balance = principal
    total_paid = 0
    months = 0

    while balance > 0:
        interest = balance * monthly_interest_rate
        principal_paid = (monthly_payment + extra_payment) - interest
        if principal_paid <= 0:
            break
        balance -= principal_paid
        total_paid += (monthly_payment + extra_payment)
        months += 1

    total_without_extra = monthly_payment * loan_term_years * 12
    interest_saved = total_without_extra - total_paid

    return {
        "actual_monthly_outgoing": monthly_payment + extra_payment,
        "new_months": months,
        "total_paid": total_paid,
        "interest_saved": interest_saved
    }


def simulate_refinancing(principal, new_interest_rate, new_loan_term_years, original_total_repayment):
    new_monthly_payment = calculate_monthly_payment(principal, new_interest_rate, new_loan_term_years)
    new_total_repayment = calculate_total_repayment(new_monthly_payment, new_loan_term_years)
    new_total_interest = calculate_total_interest(new_total_repayment, principal)
    interest_difference = original_total_repayment - new_total_repayment

    return {
        "new_monthly_payment": new_monthly_payment,
        "new_total_repayment": new_total_repayment,
        "new_total_interest": new_total_interest,
        "interest_difference": interest_difference
    }