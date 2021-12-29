import pandas as pd
import numpy_financial as npf

def bk(acquisition_cost,
       insurance_yearly,
       taxes_yearly,
       consumption,
       fuel_price,
       repairs_yearly,
       millage_yearly,
       holding_period,
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
                                columns=['Randbedingungen: %s' %(label)])

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

    return (input_series, calc_df)

if __name__ == '__main__':
    (input_series, calc_df) = bk(15000,
       800,
       100,
       7,
       1.67,
       1000,
       18000,
       6,
       interest_rate=3.0,
       rest_value=3000,
       label='Maximus')
    print(input_series)
    print(calc_df.round(2))