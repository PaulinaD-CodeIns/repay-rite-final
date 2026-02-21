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


# Second section - extra monthly payments and their effect
def handle_extra_payments(principal, annual_interest_rate, loan_term_years, monthly_payment, total_repayment):
    print(Fore.YELLOW + Style.BRIGHT + "\n=== EXTRA PAYMENTS ===")
    extra = input(
        "Are you aware that not all mortgage lenders allow extra monthly payments without conditions, "
        "and some require permission or specific contract terms? Would you still like to explore this option? (yes/no): "
    ).strip().lower()

    if extra == "yes":
        try:
            extra_payment = float(input("Enter the extra monthly payment amount: £"))
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

        except ValueError:
            print(Fore.RED + "Invalid input for extra payments.")
    else:
        print(Fore.BLUE + "No extra payments applied.")


# Third section - refinancing simulation
def handle_refinancing(principal, original_total_repayment):
    try:
        print(Fore.MAGENTA + Style.BRIGHT + "\n=== REFINANCING SIMULATION ===")
        new_rate = float(input("Enter the new annual interest rate (in %): "))
        new_term = int(input("Enter the new loan term in years: "))

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

    except ValueError:
        print(Fore.RED + "Invalid input. Please enter numeric values.")


# First section - basic mortgage calculation
def main():
    print(Fore.BLUE + Style.BRIGHT + "\n💰 Welcome to RepayRite - Your Mortgage Repayment Companion! 💰")

    try:
        principal = float(input("Enter the loan amount (Principal): £"))
        annual_interest_rate = float(input("Enter the annual interest rate (in %): "))
        loan_term_years = int(input("Enter the loan term in years: "))

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

        # Extra payments section
        extra_section = input(
            "\nWould you like to explore how extra monthly payments could reduce your loan term? (yes/no): "
        ).strip().lower()

        if extra_section == "yes":
            handle_extra_payments(
                principal, annual_interest_rate, loan_term_years, monthly_payment, total_repayment
            )

        # Refinancing section
        refinance_section = input(
            "\nWould you like to explore how refinancing might impact your repayment? (yes/no): "
        ).strip().lower()

        if refinance_section == "yes":
            handle_refinancing(principal, total_repayment)

        print(Fore.MAGENTA + Style.BRIGHT + "\nThank you for using RepayRite! We wish you smart and stress-free repayments. 💼")

    except ValueError:
        print(Fore.RED + "Please enter valid numeric values.")


if __name__ == "__main__":
    main()
