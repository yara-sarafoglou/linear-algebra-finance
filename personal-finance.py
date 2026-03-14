# ============================================================
# Linear Algebra for Personal Finance  —  simple version
# Author: Yara Sarafoglou 
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# TOOL 1 — BUDGET
# Question: I earn €1200. Each category has a percentage.
# How many euros is each category?
# ============================================================

# My income
income = 1200

# My budget categories and their percentages
names   = ["Rent", "Food", "Transport", "Savings", "Leisure"]
percent = [   35,     20,          10,        20,        15]

# Convert percentages to euros  (this is the "linear algebra" part:
# we solve  x = percentage/100 * income  for each category)
euros = []
for p in percent:
    amount = p / 100 * income   # simple multiplication
    euros.append(amount)

# Print results
print("=== BUDGET ===")
for i in range(len(names)):
    print(f"  {names[i]}: €{euros[i]}")

# Draw a pie chart and save it
plt.figure()
plt.pie(euros, labels=names, autopct="%1.0f%%")
plt.title("My monthly budget")
plt.savefig("budget.png")
plt.show()


# ============================================================
# TOOL 2 — LOAN
# Question: I borrow €10 000 at 4% per year over 48 months.
# How much interest do I pay each month?
# ============================================================

# Loan settings
loan          = 10000
annual_rate   = 0.04    # 4%
months        = 48

# Monthly interest rate
monthly_rate  = annual_rate / 12

# Fixed monthly payment formula (standard bank formula)
r             = 1 + monthly_rate
payment       = loan * (monthly_rate * r**months) / (r**months - 1)

print("\n=== LOAN ===")
print(f"  Monthly payment: €{payment:.2f}")

# Go through each month and track interest vs principal
balance    = loan
interests  = []    # money that goes to the bank
principals = []    # money that reduces my debt

for month in range(months):
    interest  = balance * monthly_rate       # interest this month
    principal = payment - interest           # what reduces my debt
    balance   = balance - principal          # new balance
    interests.append(interest)
    principals.append(principal)

print(f"  Total interest paid: €{sum(interests):.2f}")

# Draw a stacked bar chart
x = list(range(1, months + 1))
plt.figure()
plt.bar(x, principals, label="Principal", color="#7F77DD")
plt.bar(x, interests,  label="Interest",  color="#D85A30", bottom=principals)
plt.xlabel("Month")
plt.ylabel("€")
plt.title("Loan repayment — month by month")
plt.legend()
plt.savefig("loan.png")
plt.show()


# ============================================================
# TOOL 3 — PORTFOLIO
# Question: I have 4 investments with different returns.
# I want an overall return of 7%. How do I split my money?
#
# This uses a real linear system:
#   w1 + w2 + w3 + w4 = 1          (weights sum to 100%)
#   w1*r1 + w2*r2 + w3*r3 + w4*r4 = 0.07   (target return)
# ============================================================

# My investments and their yearly returns
assets  = ["Bonds", "ETF", "Stocks", "Cash"]
returns = np.array([0.03,  0.08,    0.12, 0.01])

target = 0.07   # I want 7% overall return

# Build the matrix A (2 rows = 2 equations, 4 columns = 4 unknowns)
A = np.array([
    returns,          # row 1: return equation
    [1, 1, 1, 1]      # row 2: weights must sum to 1
])

# Build the vector b (right-hand side of the equations)
b = np.array([target, 1.0])

# Ask numpy to solve the system (best possible solution)
weights, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

# Remove any negative weights (no borrowing allowed)
weights = np.maximum(weights, 0)

# Make sure weights still sum to 1 after the cleanup
weights = weights / weights.sum()

# Print results
print("\n=== PORTFOLIO ===")
for i in range(len(assets)):
    print(f"  {assets[i]}: {weights[i]*100:.1f}%")
print(f"  Achieved return: {(returns @ weights)*100:.2f}%")

# Draw a bar chart
plt.figure()
plt.bar(assets, weights * 100, color=["#7F77DD", "#1D9E75", "#D85A30", "#BA7517"])
plt.ylabel("Allocation (%)")
plt.title("Portfolio — how to split my money")
plt.savefig("portfolio.png")
plt.show()

print("\nDone! 3 files saved: budget.png, loan.png, portfolio.png")
