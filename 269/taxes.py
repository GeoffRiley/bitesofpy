"""Tax Bracket Calculator

Here is the break-down on how much a US citizen's income was
taxed in 2019

      $0 - $9,700   10%
  $9,701 - $39,475  12%
 $39,476 - $84,200  22%
 $84,201 - $160,725 24%
$160,726 - $204,100 32%
$204,101 - $510,300 35%
$510,301 +          37%

For example someone earning $40,000 would
pay $4,658.50, not $40,000 x 22% = $8,800!

    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50

More detail can be found here:
https://www.nerdwallet.com/blog/taxes/federal-income-tax-brackets/

Sample output from running the code in the if/main clause:

          Summary Report
==================================
 Taxable Income:        40,000.00
     Taxes Owed:         4,658.50
       Tax Rate:           11.65%

         Taxes Breakdown
==================================
    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50
"""
from dataclasses import dataclass, field
from typing import List, NamedTuple

Bracket = NamedTuple("Bracket", [("end", int), ("rate", float)])
Taxed = NamedTuple("Taxed", [("amount", float), ("rate", float), ("tax", float)])
BRACKET = [
    Bracket(9_700, 0.1),
    Bracket(39_475, 0.12),
    Bracket(84_200, 0.22),
    Bracket(160_725, 0.24),
    Bracket(204_100, 0.32),
    Bracket(510_300, 0.35),
    Bracket(510_301, 0.37),
]


@dataclass
class Taxes:
    """Taxes class

    Given a taxable income and optional tax bracket, it will
    calculate how much taxes are owed to Uncle Sam.

    """
    income: int
    bracket: List[Bracket] = None
    tax_amounts: List[Taxed] = field(default_factory=list)

    def __post_init__(self):
        if self.bracket is None:
            self.bracket = BRACKET
        for lo, hi in zip([Bracket(0, 0.0)] + self.bracket,
                          self.bracket[:-1] + [Bracket(self.income, self.bracket[-1].rate)]):
            if self.income > hi.end:
                self.tax_amounts.append(Taxed(band := (hi.end - lo.end), hi.rate, band * hi.rate))
            else:
                self.tax_amounts.append(Taxed(band := (self.income - lo.end), hi.rate, band * hi.rate))
                break

    def __str__(self) -> str:
        """Summary Report

        Returns:
            str -- Summary report

            Example:

                      Summary Report          
            ==================================
             Taxable Income:        40,000.00
                 Taxes Owed:         4,658.50
                   Tax Rate:           11.65%
        """
        return f'''          Summary Report          
==================================
 Taxable Income: {self.income:>17.2f}
     Taxes Owed: {self.taxes:>17.2f}
       Tax Rate: {self.tax_rate:>16.2f}%
'''

    def report(self):
        """Prints taxes breakdown report"""
        print(str(self))
        print('         Taxes Breakdown')
        print('=' * 35)
        for tx in self.tax_amounts:
            amt = f'{tx.amount:,.2f} x {tx.rate:,.2f}'
            print(f'{amt:>20} = {tx.tax:>10,.2f}')
        print('-' * 35)
        print(f'{"Total":>20} = {self.taxes:>10,.2f}')

    @property
    def taxes(self) -> float:
        """Calculates the taxes owed

        As it's calculating the taxes, it is also populating the tax_amounts list
        which stores the Taxed named tuples.

        Returns:
            float -- The amount of taxes owed
        """
        return sum(tx.tax for tx in self.tax_amounts)

    @property
    def total(self) -> float:
        """Calculates total taxes owed

        Returns:
            float -- Total taxes owed
        """
        return self.taxes

    @property
    def tax_rate(self) -> float:
        """Calculates the actual tax rate

        Returns:
            float -- Tax rate
        """
        return round(self.total / self.income * 10000.0) / 100


if __name__ == "__main__":
    salary = 40_000
    t = Taxes(salary)
    t.report()
