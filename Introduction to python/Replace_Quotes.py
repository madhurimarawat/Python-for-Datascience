'''

Here we are trying to convert the list element stored in single quotes with
that to stored in double quotes. Also the output is string as in list elements are by default enclosed in single quotes.

'''

# Either define list of columns or directly store from df.columns

# List df_columns contains the columns of the dataframe
df_columns = ['Column 1','Column 2','Column 3','Column 4','Column 5','Column 6']

# Empty string to Store Result
df_columns_string = ''


# Traversing elements and adding double quotes
for i in df_columns:

	# For the last element we do not need to append comma
	if i == df_columns[-1]:

		# Here element is appended with double quotes
		ele = '"' + i + '"'

		# Added in final list
		# Not Added comma as it is the last element
		df_columns_string = df_columns_string + ele

	else:
		# Here element is appended with double quotes
		ele = '"' + i + '"'

		# Added in final list
		# Added comma to distinguish next element
		df_columns_string = df_columns_string + ele + ',' + ' '



# Printing Final Output
# This can directly be copied in grafana variable
print("Columns after converting to double quotes string is:\n")
print(df_columns_string)