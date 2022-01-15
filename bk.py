from numpy import singlecomplex
import pandas as pd
import numpy_financial as npf

def df_style(val):
    return "font-weight: bold"


class Operating_Cost():
    """Betriebskosten calculates montly costs for leasing and buying cars."""
    
    def __init__(self, input_frame, calc_frame):
        self.input_frame = input_frame
        self.calc_frame = calc_frame
        
    @classmethod
    def buy_cost(cls, acquisition_cost=0,
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
        """BetriebsKosten Calculator"""

        interest = npf.pmt(interest_rate/12/100,
                        12*holding_period,
                        acquisition_cost) * -1 * 12*holding_period - acquisition_cost

        total_millage = millage_yearly*holding_period
        total_consumption = total_millage*consumption/100 * fuel_price

        input_series = pd.DataFrame(data=[acquisition_cost,
                                        interest_rate,
                                        rest_value,
                                        insurance_yearly,
                                        taxes_yearly,
                                        consumption,
                                        fuel_price,
                                        repairs_yearly,
                                        millage_yearly,
                                        total_millage,
                                        holding_period],
                                    index=['Anschaffungskosten [€]',
                                        'Finanzierungszins [%]',
                                        'Restwert [€]',
                                        'Versicherungskosten [€/a]',
                                        'Steuern [€/a]',
                                        'Verbrauch in %s/100 km' %(fuel_unit),
                                        'Durchschnittlicher Spritpreis über Haltedauer [€/%s]' %(fuel_unit),
                                        'Reparatur und Wartungskosten [€/a]',
                                        'Jahreslaufleistung [km]',
                                        'Gesamtlaufleistung [km]',
                                        'Haltedauer [a]'],
                                    columns=['Randbedingungen'])
        input_series.name = label
        
        index = ['Anschaffungskosten',
                'Zinsen',
                'Versicherung',
                'Steuern',
                'Reparaturen',
                'Verbrauch']
        total = [acquisition_cost,
                interest,
                insurance_yearly*holding_period,
                taxes_yearly*holding_period,
                repairs_yearly*holding_period,
                total_consumption]

        calc_df = pd.DataFrame(data=total,
                            index=index,
                            columns=['Gesamt'])
        calc_df['Jährlich'] = calc_df.Gesamt/holding_period
        calc_df['Monatlich'] = calc_df['Jährlich']/12
        calc_df['per KM'] = calc_df.Gesamt/total_millage

        calc_sum = calc_df.sum()
        calc_sum.name = 'SUMME'
        calc_df = calc_df.append(calc_sum)
        if rest_value > 0.:
            rest_Ser = pd.Series(data=[-rest_value,
                                    -rest_value/holding_period,
                                    -rest_value/holding_period/12,
                                    -rest_value/total_millage],
                                name='Restwert',
                                index=['Gesamt',
                                        'Jährlich',
                                        'Monatlich',
                                        'per KM'])
            calc_df = calc_df.append(rest_Ser)

            grand_total = calc_df.loc['SUMME'] + calc_df.loc['Restwert']
            grand_total.name = 'Summe mit Restwert'
            calc_df = calc_df.append(grand_total)

        calc_df.Name = label

        # get a handle on the row that starts with `"Total"`, i.e., the last row here
        last_row = pd.IndexSlice[calc_df.index[calc_df.index == 'SUMME'], :]
        # and apply styling to it via the `subset` arg; first arg is styler function above
        calc_df.style.applymap(df_style, subset=last_row)

        #input_series = input_series[input_series.Randbedingungen != 0]
        #calc_df = calc_df.loc[(calc_df!=0).any(axis=1)]
        #calc_df = calc_df.dropna()

        return cls(input_series, calc_df)
    
    def get_frames(self):
        return (self.input_frame, self.calc_frame)
        

if __name__ == '__main__':
    bk = Operating_Cost.buy_cost(acquisition_cost=3300,
                                 insurance_yearly=361.76,
                                 taxes_yearly=64,
                                 consumption=6.6,
                                 fuel_price=1.36,
                                 repairs_yearly=395.40,
                                 millage_yearly=3216,
                                 holding_period=5.5,
                                 interest_rate=0.0,
                                 rest_value=2000,
                                 label='Micra')
    (input_series, calc_df) = bk.get_frames()
    
    print(input_series)
    print(calc_df.round(2))