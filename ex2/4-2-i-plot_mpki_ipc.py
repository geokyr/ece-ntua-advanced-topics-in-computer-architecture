#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import mstats

## For nbit predictors
predictors_to_plot = [ "  Nbit-16K-", "  2bitFSM" ]
outputDir = "/home/george/adv-ca/parsec-3.0/parsec_workspace/graphs/4-2i/"
mpki_Axis = []
mpki_dict = {}
outFilesDir = "/home/george/adv-ca/parsec-3.0/parsec_workspace/outputs/4-2/"

for outFile in os.listdir(outFilesDir):
	print("outFile", outFile)
	fp = open(outFilesDir + outFile)

	benchName = outFile.split('/')[-1]
	titleTokens = benchName.split('.')
	title = titleTokens[0] + '.' + titleTokens[1]

	x_Axis = []
	mpki_Axis = []
	line = fp.readline()
	while line:
		tokens = line.split()
		if line.startswith("Total Instructions:"):
			total_ins = long(tokens[2])
		else:
			for pred_prefix in predictors_to_plot:
				if line.startswith(pred_prefix):
					predictor_string = tokens[0].split(':')[0]
					correct_predictions = long(tokens[1])
					incorrect_predictions = long(tokens[2])
					x_Axis.append(predictor_string)
					val = (incorrect_predictions / (total_ins / 1000.0))
					mpki_Axis.append(val)
					mpki_dict.setdefault(predictor_string, []).append(val)

		line = fp.readline()

	fig, ax1 = plt.subplots()
	ax1.grid(True)

	print(mpki_Axis)
	xAx = np.arange(len(x_Axis))
	ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
	ax1.set_xticklabels(x_Axis, rotation=25)
	ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
	ax1.set_ylim(min(mpki_Axis) - 0.05, max(mpki_Axis) + 0.05)
	ax1.set_ylabel("$MPKI$")
	line1 = ax1.plot(mpki_Axis, label="mpki", color="red",marker='x')
	plt.title("MPKI for " + title)

	plt.savefig(outputDir + title.replace('.', '-') + '.png', bbox_inches="tight", frame=True, pad_inches=0.3)
	plt.cla()
	plt.clf()

avg_mpk = []
print(mpki_dict)
for key in x_Axis:
		avg_mpk.append(mstats.gmean(mpki_dict[key]))
fig, ax1 = plt.subplots()
ax1.grid(True)

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=25)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(avg_mpk) - 0.05 * min(avg_mpk), max(avg_mpk) + 0.05 * max(avg_mpk))
plt.title("Geometric Average MPKI")
ax1.set_ylabel("$MPKI$")
line2 = ax1.plot(avg_mpk, label="Geometric Mean mpki", color="green",marker='o')
plt.savefig(outputDir + 'mean.png', bbox_inches="tight", frame=True, pad_inches=0.3)