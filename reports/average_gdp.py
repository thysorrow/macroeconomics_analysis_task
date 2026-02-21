from collections import defaultdict

from base import BaseReport

class AverageGDP(BaseReport):
    def get_name(self):
        return "average-gdp"

    def generate(self, file_content):
        country_gdp = defaultdict(list)

        for row in file_content:
            country_gdp[row['country']].append(float(row['gdp']))

        average_gdp = [
            {"country": country, "gdp": sum(gdps)/len(gdps)}
            for country, gdps in country_gdp.items()
        ]
        average_gdp.sort(key=lambda x: x['gdp'], reverse=True) 
        
        return average_gdp