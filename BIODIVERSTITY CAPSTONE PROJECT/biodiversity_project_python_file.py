# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 12:28:25 2018

@author: Andrei
"""

import codecademylib
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

#inspecting DataFrame

species = pd.read_csv('species_info.csv')
#print species.head()

#viewing number or type of unique species/statuses

species_count = species.scientific_name.nunique()
#print species_count

species_type = species.category.unique()
#print species_type

conservation_statuses = \
species.conservation_status.unique()
#print conservation_statuses

#numbers by conservation status

conservation_counts = \
species.groupby('conservation_status').\
scientific_name.nunique().reset_index()
#print conservation_counts

species.fillna('No Intervention', inplace = True)

conservation_counts_fixed = \
species.groupby('conservation_status').\
scientific_name.nunique().reset_index()
#print conservation_counts_fixed

protection_counts = \
species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')

#creating bar chart with modified axes
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts\
        .scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts\
                   .conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()

#adding column to DataFrame, pivoting, eventually 
#seeing what percentage of each category is protected
#with a view of testing the differences

species['is_protected'] = \
species.conservation_status.apply(
  lambda x: False if x == 'No Intervention' else True)

category_counts = species.groupby(
  ['category','is_protected'])\
.scientific_name.count().reset_index()
#print category_counts.head()

category_pivot = category_counts.pivot(
  columns = 'is_protected', 
  index = 'category', 
  values = 'scientific_name').reset_index()
#print ''
#print category_pivot

category_pivot.columns = \
['category','not_protected','protected']

category_pivot['percent_protected'] = \
category_pivot.protected / (category_pivot.protected + \
                            category_pivot.not_protected)
#print ''
#print category_pivot

category_pivot.columns = \
['category','not_protected','protected']

category_pivot['percent_protected'] = \
category_pivot.protected / (category_pivot.protected + \
                            category_pivot.not_protected)
#print ''
#print category_pivot

#testing for statistical difference using a chi2 test 
#since we have categorical data from two sources

contingency = [[30,146],[75,413]]

a,pval,b,c = chi2_contingency(contingency)
#print pval
# pval not less than 0.05 so not a significant difference

contingency1 = [[30,146],[5,73]]
x,pval_reptile_mammal,y,z = \
chi2_contingency(contingency1)
#print pval_reptile_mammal
# pval less than 0.05 so a significant difference

contingency2 = [[5,328],[46,4216]]
a2,pval_nonvasc_vasc,b2,c2 = \
chi2_contingency(contingency2)
#print pval_nonvasc_vasc
#pval not less than 0.05 so not a significant difference

contingency3 = [[30,146],[7,72]]
a3,pval_amph_mammal,b3,c3 = \
chi2_contingency(contingency3)
#print pval_amph_mammal
#pval not less than 0.05 so not a significant difference

contingency4 = [[11,115],[30,146]]
a4,pval_fish_mammal,b4,c4 = \
chi2_contingency(contingency4)
#print pval_fish_mammal
#pval not less than 0.05 so not a significant difference

contingency5 = [[75,413],[5,73]]
a5,pval_bird_reptile,b5,c5 = \
chi2_contingency(contingency5)
#print pval_bird_reptile
#pval not less than 0.05 so not a significant difference

contingency6 = [[75,413],[46,4216]]
a6,pval_bird_vasc,b6,c6 = \
chi2_contingency(contingency6)
#print pval_bird_vasc
# pval less than 0.05 so a significant difference


###


#SHEEP OBSERVATIONS AND FOOT AND MOUTH DISEASE

#inspecting DataFrame

observations = pd.read_csv('observations.csv')
#print observations.head()

#obtaining sheep data from DataFrame

species['is_sheep'] = species.common_names.apply(
  lambda x: True if 'Sheep' in x else False)

species_is_sheep = species[species.is_sheep == True]
#print species_is_sheep

sheep_species = \
species[(species.is_sheep == True) & \
        (species.category == 'Mammal')]
#print sheep_species

#merging to combine all data on sheep

sheep_observations = pd.merge(
  sheep_species, observations)
#print sheep_observations.head()

obs_by_park = sheep_observations.groupby('park_name')\
.observations.sum().reset_index()
#print obs_by_park

#creating bar chart and labelling axes
plt.figure(figsize = (16,4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)), \
        obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()

#determining sample size needed to test for foot and mouth prevalence changes

baseline = 0.15
minimum_detectable_effect = 100 * 0.05/0.15
sample_size_per_variant = 870
yellowstone_weeks_observing = sample_size_per_variant/507.
bryce_weeks_observing = sample_size_per_variant/250.
great_smoky_weeks_observing = sample_size_per_variant/149.
yosemite_weeks_observing = sample_size_per_variant/282.

#print bryce_weeks_observing, great_smoky_weeks_observing,\
yellowstone_weeks_observing, yosemite_weeks_observing