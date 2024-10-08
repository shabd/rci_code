# import numpy as np
import statistics


class FeroChromeAnalysis:
    
    def __init__(self):
        self.name = "Ferro Chrome"
        self.known_samples = {
            "NIST64C": {"Constant": 0.68},
            "SARM144": {"Constant": 0.4902},
        }
        self.known_values = [68.0,49.02]
        self.factor_average = None 
        self.tested_samples = []
        self.know_sample_results = []
    
    def calculate_factors(self, value_dict):
        self.know_sample_results = []

        factors = []
        
        # 1. First calculate all  the factors for CRMS
        for sample, values in value_dict.items():
            grams, ml  = values
            factor = grams * self.known_samples[sample]['Constant']/ ml
            self.known_samples[sample]['Factor'] = factor
            factors.append(factor)

            
        # 2. Get the average 
        self.factor_average = sum(factors)/ len(factors)
        # self.standard_deviation = np.std(factors)
        # self.coefficient_of_variation = (self.standard_deviation / self.factor_average) * 100
        self.standard_deviation = statistics.stdev(factors)
        mean_value = statistics.mean(factors)
        self.coefficient_of_variation = (self.standard_deviation / mean_value) * 100


        i=0
        # 3. We need to cal %Cr and the bias 
        for sample, values in value_dict.items():
            grams, ml = values 
            percent_cr = (self.factor_average *ml)/grams*100
            bias = (percent_cr - self.known_values[i])
            self.known_samples[sample].update({
                "%Cr": percent_cr,
                "Known Value" : self.known_values[i],
                "Bias": bias
            })
        
            self.know_sample_results.append([
                            sample, grams, ml, round(self.known_samples[sample]['Factor'] , 6), round(percent_cr, 2), self.known_values[i], round(bias, 2)
                        ])
            i+=1
            
        return self.know_sample_results
    
    def add_and_calculate_sample(self, ref_id, grams, ml,edit=False,index=None):
        if not self.factor_average:
            raise ValueError("Average factor has not been calculated. Please run calculate_factors first.")

        cal_percent_cr = (self.factor_average * ml) / grams * 100
        if edit:
            self.tested_samples[index] = [ref_id, float(grams), ml, round(cal_percent_cr, 2)]
        else:
            self.tested_samples.append([ref_id, float(grams), ml, round(cal_percent_cr, 2)])
        return self.tested_samples



# analysis = FeroChromeAnalysis()

# # Calculating factors, %Cr, and bias for known samples
# analysis.calculate_factors({
#     "NIST64C": (0.2001, 45.98, 68.00),
#     "SARM144": (0.2000, 33.24, 49.02),
# })

# # Output the results for the known samples
# for sample, info in analysis.known_samples.items():
#     print(f"{sample}: Factor={info['Factor']}, %Cr={info['%Cr']}, Bias={info['Bias'],}")
#     print(analysis.factor_average)

# analysis.add_and_calculate_sample("RCI1234", 0.2004, 40.25)
# print(analysis.tested_samples)
# # analysis.add_and_calculate_sample("RCI1235", 0.2003, 18.07)


