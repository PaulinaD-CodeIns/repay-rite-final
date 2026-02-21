# Styling imports and settings
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

# Math imports
from calculator import (
    calculate_monthly_payment,
    calculate_total_repayment,
    calculate_total_interest,
    calculate_impact_of_extra_payments,
    simulate_refinancing,
)


# Validation functions

def get_positive_float(prompt):
    """
    Prompts the user for a positive float.
    Repeats until valid input is provided.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print(Fore.RED + "Value must be greater than 0.")
            else:
                return value
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a numeric value.")


def get_positive_int(prompt):
    """
    Prompts the user for a positive integer.
    Repeats until valid input is provided.
    """
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print(Fore.RED + "Value must be greater than 0.")
            else:
                return value
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a whole number.")


def get_yes_no(prompt):
    """
    Prompts user for yes/no input.
    Repeats until valid response is provided.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "no"]:
            return response
        print(Fore.RED + "Please enter 'yes' or 'no'.")


# Extra payments section

def handle_extra_payments(principal, annual_interest_rate, loan_term_years):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== EXTRA PAYMENTS ===")

    extra = get_yes_no(
        "Are you aware that not all mortgage lenders allow extra monthly payments without conditions, "
        "and some require permission or specific contract terms? Would you still like to explore this option? (yes/no): "
    )

    if extra == "yes":
        extra_payment = get_positive_float("Enter the extra monthly payment amount: £")

        results = calculate_impact_of_extra_payments(
            principal, annual_interest_rate, loan_term_years, extra_payment
        )

        years = results["new_months"] // 12
        months = results["new_months"] % 12

        extra_table = [
            ["New Monthly Payment (incl. extra)", f"£{results['actual_monthly_outgoing']:,.2f}"],
            ["New Loan Term", f"{results['new_months']} months ({years} yrs, {months} mos)"],
            ["Total Payment with Extra", f"£{results['total_paid']:,.2f}"],
            ["Interest Saved", f"£{results['interest_saved']:,.2f}"]
        ]

        print(Fore.GREEN + "\nWITH EXTRA PAYMENTS:")
        print(tabulate(extra_table, headers=["Metric", "Value"], tablefmt="fancy_grid"))

    else:
        print(Fore.BLUE + "No extra payments applied.")


# Refinancing section

def handle_refinancing(principal, original_total_repayment):
    print(Fore.MAGENTA + Style.BRIGHT + "\n=== REFINANCING SIMULATION ===")

    new_rate = get_positive_float("Enter the new annual interest rate (in %): ")
    new_term = get_positive_int("Enter the new loan term in years: ")

    results = simulate_refinancing(
        principal, new_rate, new_term, original_total_repayment
    )

    refinance_table = [
        ["New Monthly Payment", f"£{results['new_monthly_payment']:,.2f}"],
        ["New Total Repayment", f"£{results['new_total_repayment']:,.2f}"],
        ["New Total Interest", f"£{results['new_total_interest']:,.2f}"]
    ]

    print(Fore.CYAN + "\nRESULTS OF REFINANCING:")
    print(tabulate(refinance_table, headers=["Description", "Amount"], tablefmt="fancy_grid"))

    if results["interest_difference"] > 0:
        print(Fore.GREEN + f"\nYou would save £{results['interest_difference']:,.2f} in interest compared to your original plan.")
    else:
        print(Fore.RED + f"\nThis refinancing would cost you an extra £{abs(results['interest_difference']):,.2f} in interest.")


# Main programme

def main():
    print(Fore.BLUE + Style.BRIGHT + "\n💰 Welcome to RepayRite - Your Mortgage Repayment Companion! 💰")

    # Validated inputs
    principal = get_positive_float("Enter the loan amount (Principal): £")
    annual_interest_rate = get_positive_float("Enter the annual interest rate (in %): ")
    loan_term_years = get_positive_int("Enter the loan term in years: ")

    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, loan_term_years)
    total_repayment = calculate_total_repayment(monthly_payment, loan_term_years)
    total_interest = calculate_total_interest(total_repayment, principal)

    summary_table = [
        ["Monthly Payment", f"£{monthly_payment:,.2f}"],
        [f"Total Repayment ({loan_term_years} years)", f"£{total_repayment:,.2f}"],
        ["Total Interest Paid", f"£{total_interest:,.2f}"]
    ]

    print(Fore.CYAN + Style.BRIGHT + "\n=== YOUR MORTGAGE SUMMARY ===")
    print(tabulate(summary_table, headers=["Description", "Amount"], tablefmt="fancy_grid"))

    # Extra payments
    extra_section = get_yes_no(
        "\nWould you like to explore how extra monthly payments could reduce your loan term? (yes/no): "
    )

    if extra_section == "yes":
        handle_extra_payments(
            principal, annual_interest_rate, loan_term_years
        )

    # Refinancing
    refinance_section = get_yes_no(
        "\nWould you like to explore how refinancing might impact your repayment? (yes/no): "
    )

    if refinance_section == "yes":
        handle_refinancing(principal, total_repayment)

    print(Fore.MAGENTA + Style.BRIGHT + "\nThank you for using RepayRite! We wish you smart and stress-free repayments. 💼")


if __name__ == "__main__":
    main()