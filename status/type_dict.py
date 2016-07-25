'''
The following is the reference dictionary/mapping of the 24 status categories (including null), 
and is used by classification.py to map indices to actual names of the categories. 
Note - This is also NOT a configurable file and its contents should NOT be changed. 
This file is imported as a module and should not be directly referenced.
''' 
type = {
    0 	:	'abandon',
	1 	:	'const_des',
	2	:	'decommissioned',
	3	:	'distance',
	4	:	'electricity',
	5	:	'flooded',
	6	:	'Functional',
	7	:	'funds_maintain',
	8	:	'lowdem_alt',
	9	:	'mechanic',
	10	:	'missingparts',
	11	:	'mng_other',
	12	:	'',
	13	:	'overcrowding',
	14	:	'quality',
	15	:	'quantity_other',
	16	:	'rationing',
	17	:	'repair_fail',
	18	:	'siting',
	19	:	'technical_other',
	20	:	'underconst',
	21	:	'vague',
	22	:	'vandalism',
	23	:	'water_resource',
}