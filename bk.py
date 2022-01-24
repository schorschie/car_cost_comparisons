# from unicodedata import name
from numpy import singlecomplex
import pandas as pd
import numpy_financial as npf

def df_style(val):
    return "font-weight: bold"


class Operating_Cost():
    """Betriebskosten calculates monthly costs for leasing and buying cars."""
    
    def __init__(self,
                 input_frame=pd.DataFrame(),
                 total=[],
                 holding_period=1,
                 total_millage=1):

        index = ['Raten',
                'Versicherung',
                'Steuern',
                'Reparaturen',
                'Verbrauch',
                'Summe',
                'Anzahlung',
                'Restwert',
                'Gesamtsumme']
        calc_df = pd.DataFrame(data=total,
                            index=index,
                            columns=['Gesamt'])
        calc_df['Jährlich'] = calc_df.Gesamt/holding_period
        calc_df['Monatlich'] = calc_df['Jährlich']/12
        calc_df['per KM'] = calc_df.Gesamt/total_millage

        if hasattr(input_frame, 'name'):
            calc_df.Name = input_frame.name
        
        self.input_frame = input_frame
        self.calc_frame = calc_df
    
    @classmethod
    def lease(cls,
              instalment=0.0,
              government_funding=0.0,
              down_payment=0.0,
              insurance_yearly=0.0,
              taxes_yearly=0.0,
              consumption=0.0,
              fuel_price=0.0,
              repairs_yearly=0.0,
              millage_yearly=0,
              holding_period=0,
              fuel_unit='l',
              label=''):
        """Calculated operating cost of a leasing car."""
        
        financing_total = instalment * 12 * holding_period
        insurance_total = insurance_yearly * holding_period
        taxes_total = taxes_yearly * holding_period
        repairs_total = repairs_yearly * holding_period
        millage_total = millage_yearly * holding_period

        consumption_total = millage_total * consumption/100 * fuel_price

        total = financing_total + \
                insurance_total + \
                taxes_total + \
                repairs_total + \
                consumption_total
                
        real_down_payment = down_payment - government_funding

        input_series = pd.DataFrame(data=[instalment,
                                          down_payment,
                                          government_funding,
                                          real_down_payment,
                                          insurance_yearly,
                                          taxes_yearly,
                                          consumption,
                                          fuel_price,
                                          repairs_yearly,
                                          millage_yearly,
                                          holding_period,
                                          millage_total],
                                    index=['Leasingrate [€]',
                                        'Anzahlung [€]',
                                        'davon staatliche Förderung [€]',
                                        'Reale Anzahlung [€]',
                                        'Versicherungskosten [€/a]',
                                        'Steuern [€/a]',
                                        'Verbrauch in %s/100 km' %(fuel_unit),
                                        'Durchschnittlicher Spritpreis über Haltedauer [€/%s]' %(fuel_unit),
                                        'Reparatur und Wartungskosten [€/a]',
                                        'Jahreslaufleistung [km]',
                                        'Haltedauer [a]',
                                        'Gesamtlaufleistung [km]'],
                                    columns=['Randbedingungen'])
        input_series.name = 'Leasingkosten ' + label
        
        total = [financing_total,
                 insurance_total,
                 taxes_total,
                 repairs_total,
                 consumption_total,
                 total,
                 real_down_payment,
                 0,
                 total + real_down_payment]


        return cls(input_series, total, holding_period, millage_total)

    @classmethod
    def buy(cls,
            acquisition_cost=0,
            government_funding=0,
            down_payment=0,
            insurance_yearly=0,
            taxes_yearly=0,
            consumption=0,
            fuel_price=0,
            repairs_yearly=0,
            millage_yearly=0,
            holding_period=0,
            interest_rate=0.0,
            rest_value=0.0,
            fuel_unit='l',
            label=''):
        """Calculated operating cost for a bought car.

        Args:
            acquisition_cost (float, optional): The acquisition cost of the car. Defaults to 0.
            government_funding (float, optional): If available a government funding, payd
            out once a the beginning.
            Defaults to 0.
            down_payment (float, optional): A possible down payment. Defaults to 0.
            insurance_yearly (float, optional): Yearly insurance costs. Defaults to 0.
            taxes_yearly (float, optional): Yearly taxes. Defaults to 0.
            consumption (float, optional): The consumption of the car in Units per 100km.
            Defaults to 0.
            fuel_price (float, optional): The average fuel price for one unit over the
            holding period.
            Defaults to 0.
            repairs_yearly (float, optional): The estimated yearly maintenance cost. Defaults to 0.
            millage_yearly (int, optional): The expected yearly millage in km/miles. Defaults to 0.
            holding_period (int, optional): The expected period until sale of the car. Defaults
            to 0.
            interest_rate (float, optional): if necessary, the interest rate for a credit. Defaults
            to 0.0.
            rest_value (float, optional): The rest value of the car at the end of the
            holding period. Defaults
            to 0.0.
            fuel_unit (str, optional): The unit of the fuel. Defaults to 'l'.
            label (str, optional): A description label for the car. Defaults to ''.

        Returns:
            [Operating_Cost]: A class holding input and output data frame
        """

        financing_amount = acquisition_cost - down_payment
        financing_total = npf.pmt(interest_rate/12/100,
                        12*holding_period,
                        financing_amount) * -1 * 12*holding_period

        insurance_total = insurance_yearly * holding_period
        taxes_total = taxes_yearly * holding_period
        repairs_total = repairs_yearly * holding_period

        millage_total = millage_yearly * holding_period
        consumption_total= millage_total * consumption/100 * fuel_price

        total = financing_total + \
                insurance_total + \
                taxes_total + \
                repairs_total + \
                consumption_total

        real_down_payment = down_payment - government_funding

        input_series = pd.DataFrame(data=[acquisition_cost,
                                          down_payment,
                                          government_funding,
                                          real_down_payment,
                                          interest_rate,
                                          rest_value,
                                          insurance_yearly,
                                          taxes_yearly,
                                          consumption,
                                          fuel_price,
                                          repairs_yearly,
                                          millage_yearly,
                                          holding_period,
                                          millage_total,
                                          financing_amount],
                                    index=['Anschaffungskosten [€]',
                                        'Anzahlung [€]',
                                        'davon staatliche Förderung [€]',
                                        'Reale Anzahlung [€]',
                                        'Finanzierungszins [%]',
                                        'Restwert [€]',
                                        'Versicherungskosten [€/a]',
                                        'Steuern [€/a]',
                                        'Verbrauch in %s/100 km' %(fuel_unit),
                                        'Durchschnittlicher Spritpreis über Haltedauer [€/%s]' %(fuel_unit),
                                        'Reparatur und Wartungskosten [€/a]',
                                        'Jahreslaufleistung [km]',
                                        'Haltedauer [a]',
                                        'Gesamtlaufleistung [km]',
                                        'Finanzierungsbetrag [€]'],
                                    columns=['Randbedingungen'])
        input_series.name = 'Kaufkosten ' + label
        
        total = [financing_total,
                 insurance_total,
                 taxes_total,
                 repairs_total,
                 consumption_total,
                 total,
                 real_down_payment,
                 -rest_value,
                 total + real_down_payment - rest_value]


        return cls(input_series, total, holding_period, millage_total)
    
    def get_frames(self):
        return (self.input_frame, self.calc_frame)
        

if __name__ == '__main__':
    # bk = Operating_Cost.buy(acquisition_cost=3300,
    #                              insurance_yearly=361.76,
    #                              taxes_yearly=64,
    #                              consumption=6.6,
    #                              fuel_price=1.36,
    #                              repairs_yearly=395.40,
    #                              millage_yearly=3216,
    #                              holding_period=5.5,
    #                              interest_rate=0.0,
    #                              rest_value=2000,
    #                              label='Micra')
    # (input_series, calc_df) = bk.get_frames()
    
    bk = Operating_Cost.buy(acquisition_cost=43970.,
                            government_funding=6000.,
                            down_payment=15970.0,
                            interest_rate=2.0,
                            rest_value=8500,
                            insurance_yearly=601.16,
                            taxes_yearly=0.0,
                            consumption=15.0,
                            fuel_price=0.31,
                            repairs_yearly=500,
                            millage_yearly=15000,
                            holding_period=7,
                            label='Tesla Model 3')
    (input_series, calc_df) = bk.get_frames()

    print('\n\n')
    print(input_series.name)
    print('=' * len(input_series.name))
    print('\n')
    print(input_series)
    print('\n')
    print(calc_df.round(2))

    bk = Operating_Cost.lease(instalment=272,
                              government_funding=6000,
                              down_payment=13000,
                              insurance_yearly=601.16,
                              taxes_yearly=0.0,
                              consumption=15.0,
                              fuel_price=0.31,
                              repairs_yearly=500,
                              millage_yearly=15000,
                              holding_period=4,
                              label='Tesla Model 3')
    (input_series, calc_df) = bk.get_frames()

    print('\n\n')
    print(input_series.name)
    print('=' * len(input_series.name))
    print('\n')
    print(input_series)
    print('\n')
    print(calc_df.round(2))