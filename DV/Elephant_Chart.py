#!/usr/bin/env python
# coding: utf-8

# # Create the Elephant Curve
# 
# Create your own "elephant chart" of the percentage change of income, measured over percentiles of the world population ranked by income.
# 
# The data is available as the [Lakner-Milanovic 2013 World Panel Income Distribution (LM-WPID)](http://www.worldbank.org/en/research/brief/World-Panel-Income-Distribution). This database measures the annual income of an individual across several dimensions including country and income decile group. First we'll load pyplot from matplotlib to plot the data, and then pandas to wrangle the data...

# In[37]:


import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# We'll be using the Pandas python library, and you can find the documentation for Pandas at this link.
# 
# https://pandas.pydata.org/docs/
# 
# The documentation includes the following useful tutorials.
# 
# * [10 minutes to pandas](https://pandas.pydata.org/docs/getting_started/10min.html)
# 
# * [Essential basic functionality](https://pandas.pydata.org/docs/getting_started/basics.html)

# In[38]:


import pandas as pd


# Now we can load the world panel income distribution database from a local copy of this [csv file](http://pubdocs.worldbank.org/en/972401475765303436/LM-WPID-web.csv).

# In[39]:


lmwpid = pd.read_csv('LMWPIDweb.csv')


# In[40]:


lmwpid


# The fields are described in detail by this [metafile description](http://pubdocs.worldbank.org/pubdocs/publicdoc/2015/10/895211444154092188/Description-Lakner-Milanovic-database-2.pdf). Here are the important fields for this assignment.
# 
# * **RRinc** is a measure of the average annual income of an individual in this country in this income decile group. The units are 2005 PPP which corresponds approximately to US dollars in the year 2005.
# 
# * **bin_year** is the year dimension (1988, 1993, 1998, 2003, 2008) of the measurements.
# 
# * **group** provides the income decile group of the measurement, from 1 to 10, where 1 means RRinc measures the average annual income of someone in the bottom 10% of earners in this country that year, and 10 means the measure was for the average income of the top 10% of that country that year.
# 
# * **pop** is a measure of the population of the people in a country's income decile group for that year, in units of one million (so e.g. a value of 0.1 corresponds to 100,000 people). Since this is the population of a decile group, it will be 10% of the population of the country (which is reported in the totpop field).
# 
# * **country** is the name of the country the measurement was taken in. (Don't aggregate across this dimension if filtering mysample = 1)
# 
# * **mysample** separates high-population countries into regions. Filter on this, selecting either 0 or 1 (but not both). If mysample is 0 then the measure is reported for each country as a whole and you can aggregate across the "country" field. If mysample is 1 then the highly populated countries of China, India and Indonesia are separated into rural and urban subsets. Both of these subsets will have the same name in the country field, but their country codes will be different. For example, if mysample is 1, then China's rural data is reported under country code CHN-R and its urban data is reported under country code CHN-U, but both share the same country name "China."
# 
# * **contcod** is a three-letter country code, plus differentiation between rural and urban if mysample = 1. Safest to aggregate over contcod instead of country.

# ## Step 1
# 
# First, create a dataframe called lm1988 that is a table of only the 1988 data with mysample = 1. The only columns we will need are RRinc and pop, and these will respresent the measurement for each income decile group and country code in the 1988 mysample=1 data.
# 
# See this link below for instructions on how to query specific rows in a dataframe, including how to query on multiple conditions.
# 
# https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html#how-do-i-filter-specific-rows-from-a-dataframe

# In[41]:


'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
lm1988 = lmwpid.loc[(lmwpid['bin_year'] == 1988) & lmwpid['mysample'] == 1, ['pop','RRinc']]


# In[42]:


"""Your result should have 750 rows"""
assert(lm1988.shape[0] == 750)


# In[43]:


"""Your result should have the 'RRinc' and 'pop' fields"""
assert('pop' in lm1988.columns)
assert('RRinc' in lm1988.columns)


# In[44]:


"""China for mysample = 1 should have a 1988 entry for this"""
assert(lm1988[(lm1988['RRinc'] == 157)].shape[0] == 1)
"""but should not have an entry for this mysample = 0 data"""
assert(lm1988[(lm1988['RRinc'] == 161)].shape[0] == 0)


# ## Step 2
# 
# Sort the lm1988 dataframe in order of increasing RRinc, and create a new calculated field called runningpop that is the cumulative total of the pop field for the current row of the table and all rows before it.
# 
# Two Pandas methods that are helpful with this are sort_values() and cumsum().

# In[45]:


'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
lm1988 = lm1988.sort_values(['RRinc'])
pop_column = lm1988['pop']
lm1988['runningpop'] = pop_column.cumsum()


# In[46]:


'''RRinc should be monotonic (sorted in non-decreasing order)'''
assert(lm1988['RRinc'].is_monotonic)


# In[47]:


'''runningpop should be monotonic (sorted in non-decreasing order)'''
assert(lm1988['runningpop'].is_monotonic)
'''and the following test should work for any row'''
assert(lm1988.iloc[3]['runningpop'] + lm1988.iloc[4]['pop'] == lm1988.iloc[4]['runningpop'])


# In[48]:


'''The first thee values should match these (rounded to six decimal places)'''
assert((lm1988.iloc[0].round(6) == pd.Series({'pop': 0.852521, 'RRinc': 82,'runningpop': 0.852521})).all())
assert((lm1988.iloc[1].round(6) == pd.Series({'pop': 1.648236, 'RRinc': 85,'runningpop': 2.500758})).all())
assert((lm1988.iloc[2].round(6) == pd.Series({'pop': 0.518956, 'RRinc': 87,'runningpop': 3.019714})).all())


# ## Step 3
# 
# Use the Pandas cut() method to create a new field called "quintile" that contains an integer value from zero to 19 indicating which of 20 buckets each row belongs to, where each bucket represents approximately the same population, with bucket zero holding the bottom 5% of the world population according to RRinc, and bucket 19 holding the top 5% of the world population according to RRinc.

# In[49]:


'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
lm1988['quintile'] = pd.cut(lm1988['runningpop'], bins= 20, labels=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] )


# In[50]:


'''The following RRinc records should fall into the following quintiles'''
assert(lm1988[lm1988['RRinc'] == 82]['quintile'].values[0] == 0)
assert(lm1988[lm1988['RRinc'] == 660]['quintile'].values[0] == 10)
assert(lm1988[lm1988['RRinc'] == 43279]['quintile'].values[0] == 19)


# ## Step 4
# 
# Use the Pandas groupby() method to create q1988 which is a 20 row dataframe grouped by 'quintile'. Each row of q1988 represents a single quintile, and has a 'RRinc' field value set to the mean of the 'RRinc' field values in lm1988 that share that 'quintile' value.

# In[51]:


'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
q1988 = lm1988[['RRinc','quintile']].groupby(lm1988['quintile']).mean()
q1988.reset_index(inplace=True ,drop=True)


# In[52]:


'''The first three quintiles should have the following mean RRinc values'''
assert(q1988.at[0,'RRinc'].round(2) == 146.65)
assert(q1988.at[1,'RRinc'].round(2) == 220.87)
assert(q1988.at[2,'RRinc'].round(2) == 267.8)


# ## Step 5
# 
# Do the same thing to create lm2008 and q2008 for the 2008 data with mysample = 1.

# In[53]:


'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
lm2008 = lmwpid.loc[(lmwpid['bin_year'] == 2008) & lmwpid['mysample'] == 1, ['pop','RRinc']]
lm2008 = lm2008.sort_values(['RRinc'])
pop_column = lm2008['pop']
lm2008['runningpop'] = pop_column.cumsum()
lm2008['quintile'] = pd.cut(lm2008['runningpop'], bins= 20, labels=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] )
q2008 = lm2008[['RRinc','quintile']].groupby(lm2008['quintile']).mean()
q2008.reset_index(inplace=True ,drop=True)


# In[54]:


'''The first three 2008 quintiles should have the following mean RRinc values'''
assert(q2008.at[0,'RRinc'].round(2) == 177.99)
assert(q2008.at[1,'RRinc'].round(2) == 307.16)
assert(q2008.at[2,'RRinc'].round(2) == 380.08)


# ## Step 6
# 
# Create a new dataframe called 'elephant' that consists of twenty rows, with each row showing for that quantile the change in RRinc in 2008 relative to RRinc in 1988.

# In[55]:


'''Enter your solution below the YOUR CODE HERE comment,'''
'''by replacing the "raise NotImplementedError()" with your code.'''
elephant = (q2008['RRinc'] - q1988['RRinc'])/q1988['RRinc']


# In[56]:


'''The first three elephant values should be the following relative RRinc growth ratios'''
assert(elephant.at[0].round(3) == 0.214)
assert(elephant.at[1].round(3) == 0.391)
assert(elephant.at[2].round(3) == 0.419)


# In[57]:


'''If all goes right, you should see this plot at the end'''
elephant.plot()


# In[ ]:
