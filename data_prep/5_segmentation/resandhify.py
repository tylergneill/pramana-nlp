to_do_list = [
'Dharmakīrti_Pramāṇavārttika.txt',
'Dharmakīrti_Pramāṇavārttikasvavṛtti.txt',
'Dharmakīrti_Vādanyāya.txt',
'Dharmakīrti_Sambandhaparīkṣā.txt',
]

import re

def resandhify(text):
	regex_replace = [
	[u'- +([^\n])','-\\1'],

	[u'[aā]-(ai|e)', 'ai'],
	[u'[aā]-(au|o)', 'au'],

	[u'[aā]-[aā]', u'ā'],
	[u'[aā]-[iī]', u'e'],
	[u'[aā]-[uū]', u'o'],
	[u'[aā]-[ṛṝ]', u'ar'],
	[u'[aā]-[ḷḹ]', u'al'],

	[u'rn ', 'r '],
	[u'([eo]) a', "\\1 '"],

	[u'[ṛ]-([aā])', u'r\\1'],
	[u'([aāiīuūṛeo])-([gjḍdbnmyrlvhkcṭtpśṣs])', '\\1\\2'],
	[u'([gjḍdbnm])-([aāiīuūṛeo])', '\\1\\2'],
	[u'([gjḍdbnml])-([gjḍdbnmyrlv])', '\\1\\2'],
	[u'd-h', 'ddh'],
	[u'c-ś', 'cch'],
	[u'([kcṭtpśṣs])-([kcṭtpśṣs])', '\\1\\2'],
	[u'([yrv])-([aāiīuūṛeo])', '\\1\\2'],

	]

	for r_r in regex_replace:
		text = re.sub(r_r[0], r_r[1], text)

	return text

test = 'a ā'
print(resandhify(test))
