import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style("whitegrid", {'axes.grid' : False})

print os.getcwd()


if os.path.isdir('outputs') is not True:
    print("Creating 'outputs' directory for images.")
    os.mkdir('outputs')


def mod_diagnostics(model, data, identifier):

    fitted = model.fit()
    dep = model.endog_names
    indep_names = ""

    # create a string containing list of indep names for output files
    for name in model.exog_names[1:]:  # we don't want 0 element as that is the intercept
        indep_names += "{0}_".format(name)

    # Want to include name of DataFrame in the output filename but currently DataFrame does not have a name attribute
    # So for now use nobs from fitted
    samplesize = str(int(fitted.nobs))

    f1 = open(os.path.join('outputs/ols_outputs', "{0}-{1}-{2}OLS_Sample{3}_Summary.txt".format\
        (identifier, dep, indep_names, samplesize)), "w")
    f1.write(fitted.summary().as_text())
    f1.close()

    # calculate standardized residuals ourselves
    fitted_sr = (fitted.resid / np.std(fitted.resid))

    # Histogram of residuals
    ax = plt.hist(fitted.resid)
    plt.xlabel('Residuals')
    plt.savefig(os.path.join('outputs/ols_outputs', '{0}-{1}-{2}OLS-Sample{3}_ResidHist.png'.format\
        (identifier, dep, indep_names, samplesize)), bbox_inches='tight')
    plt.close()

    # standardized residuals vs fitted values
    ax = plt.plot(fitted.fittedvalues, fitted_sr, 'bo')
    plt.axhline(linestyle='dashed', c='black')
    plt.xlabel('Fitted Values')
    plt.ylabel('Standardized Residuals')
    plt.savefig(os.path.join('outputs/ols_outputs', '{0}-{1}-{2}OLS-Sample{3}_StdResid.png'.format\
        (identifier, dep, indep_names, samplesize)), bbox_inches='tight')
    plt.close()


    if len(model.exog_names) == 2:  # univariate model (with intercept)

        indep = model.exog_names[1]

        # scatter plot with regression line
        ax = plt.plot(data[indep], data[dep], 'bo')
        x = np.arange(data[indep].min(), data[indep].max(), 0.1)  # list of values to plot the regression line using
        plt.plot(x, fitted.params[1] * x + fitted.params[0], '-',
                 c='black')  # plot a line using the standard equation with parms from the model

        plt.xlabel(indep)
        plt.ylabel(dep)
        plt.savefig(os.path.join('outputs/ols_outputs', '{0}-{1}-{2}OLS_Sample{3}_Regression.png'.format\
            (identifier, dep, indep, samplesize)), bbox_inches='tight')
        plt.close()


# CONTROL DATA ANALYSIS (DIDNT REALLY WORK...)
df = pd.read_csv("input2.csv")

# print df.head()

ct = df[["windDir", "windSpeed", "duration"]]

# SEABORN DISTPLOTS FOR CONTROL
for i in ct:
    fig = plt.figure(figsize=(10,10))
    fig = plt.hist(ct[i])
    plt.title(i + " Dist Plot")
    if i == "windDir":
        plt.xlabel('Degrees')
    elif i == "windSpeed":
        plt.xlabel("m/s")
    elif i == "duration":
        plt.xlabel('days')
    plt.savefig(os.path.join('outputs', '{0}-Distribution.png'.format(i)), bbox_inches='tight')
    plt.close()

fig = plt.figure(figsize=(10,10))
fig = plt.scatter(df["ignX"], df["ignY"])
plt.title("Ignition point map")
plt.savefig(os.path.join('outputs', "ignition-point-map.png"), bbox_inches='tight')
plt.close()

df2 = pd.read_csv("descriptives.csv")
print df2.head()

bp = df2[["avgBP", "avgTop10pctBP", "avgFirePathLength"]]
fs = df2[["avgFireSize", "avgTop10pctFireSize", "maxFireSize"]]

# for i in bp:
#     plt.plot(bp[i])
#     plt.show()

# for i in fs:
#     plt.plot(fs[i])
#     plt.show()


f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(5, 10))
ax1.plot(df2['intervention'], bp["avgBP"])
ax1.set_title("Mean BP")
ax1.set_ylim([min(bp["avgBP"])-(0.05*min(bp["avgBP"])), max(bp["avgBP"]) + (0.05*max(bp["avgBP"]))])
ax2.plot(df2['intervention'], bp["avgTop10pctBP"])
ax2.set_title("Mean Top 10% BP")
ax2.set_ylabel("# Cells")
ax2.set_ylim([min(bp["avgTop10pctBP"])-(0.05*min(bp["avgTop10pctBP"])), max(bp["avgTop10pctBP"]) + (0.05*max(bp["avgTop10pctBP"]))])
ax3.plot(df2['intervention'], bp["avgFirePathLength"])
ax3.set_title("Mean Fire Path Length")
ax3.set_ylim([min(bp["avgFirePathLength"])-(0.05*min(bp["avgFirePathLength"])), max(bp["avgFirePathLength"]) + (0.05*max(bp["avgFirePathLength"]))])

f.subplots_adjust(hspace=0.25)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.xlabel("% Intervention")
plt.savefig(os.path.join('outputs', "bp-linegraph.png"), bbox_inches='tight')

f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(5, 10))
ax1.plot(df2['intervention'], fs["avgFireSize"])
ax1.set_title("Mean Fire Size")
ax1.set_ylim([min(fs["avgFireSize"])-(0.05*min(fs["avgFireSize"])), max(fs["avgFireSize"]) + (0.05*max(fs["avgFireSize"]))])
ax2.plot(df2['intervention'], fs["avgTop10pctFireSize"])
ax2.set_title("Mean Top 10% Fire Size")
ax2.set_ylabel("# Cells")
ax2.set_ylim([min(fs["avgTop10pctFireSize"])-(0.05*min(fs["avgTop10pctFireSize"])), max(fs["avgTop10pctFireSize"]) + (0.05*max(fs["avgTop10pctFireSize"]))])
ax3.plot(df2['intervention'], fs["maxFireSize"])
ax3.set_title("Max Fire Size")
ax3.set_ylim([min(fs["maxFireSize"])-(0.05*min(fs["maxFireSize"])), max(fs["maxFireSize"]) + (0.05*max(fs["maxFireSize"]))])

f.subplots_adjust(hspace=0.25)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
plt.xlabel("% Intervention")
plt.savefig(os.path.join('outputs', "fs-linegraph.png"), bbox_inches='tight')

'''

# MAIN DATA ANALYSIS, GENERATES LIN REG PLOTS, DIST PLOTS, CORR HEATMAPS, LIN REG MODEL
adv = 1
for i in study_sites:
    df1 = df_preprcs(i, 1)
    j = [2, 3]
    for num in j:
        df_temp = df_preprcs(i, num)
        df1 = df1.append(df_temp)

    df1['log_slp_deg'] = np.log10(df1.slp_deg)

    for d in target_vars:
        df1.loc[:, d + '_z_scr'] = pd.Series(df1[d] - df1[d].mean()) / df1[d].std()
    print 'done with ' + str(adv) + ' not broken yet! ' + i

    df1.to_csv(i + '_processed.csv')
    

    zdf = df1[['num_sp_z_scr', 'shan_i_z_scr', 'gc_health_z_scr', 'dist_m_z_scr',
                'elv_m_z_scr', 'sol_wm2_z_scr', 'log_slp_deg_z_scr', 'no2_z_scr']]

    # DIFFERENCE TESTING
    shan_i_diff_test = sci.mannwhitneyu(ctrl['shan-i'], df1['shan_i'])
    # print "site " + str(adv) + ' shan i difference test: ', shan_i_diff_test 
    gc_health_diff_test = sci.mannwhitneyu(ctrl['gc_health'], df1['gc_health'])
    # print "site " + str(adv) + ' gc health difference test: ',  gc_health_diff_test

    # Correlation matrix heatmap
    corrmat = zdf.corr()
    f, ax = plt.subplots(figsize=[12, 10])
    ax = sns.heatmap(corrmat)
    plt.savefig(os.path.join('outputs/heatmaps', '{0}-corrplt_test.png'.format\
        (i)), bbox_inches='tight')
    plt.close()

    # Seaborn distplots
    for z in zdf:
        fig = plt.figure()
        fig = plt.hist(zdf[z])
        plt.savefig(os.path.join('outputs/distplot', '{0}-{1}-Distribution.png'.format\
            (i, z)), bbox_inches='tight')
        plt.close()

    reg_x_vars = ['shan_i_z_scr', 'gc_health_z_scr']
    reg_y_vars = ['dist_m', 'elv_m_z_scr', 'sol_wm2_z_scr', 'log_slp_deg_z_scr', 'no2_z_scr']

    # Linear Regression Plots
    for x in reg_x_vars:
        # OLS Modelling
        mod = sm.OLS.from_formula\
        (x + ' ~ elv_m_z_scr + sol_wm2_z_scr + log_slp_deg_z_scr + no2_z_scr', data=df1)
        mod_fitted = mod.fit()
        print mod_fitted.summary()
        mod_diagnostics(mod, df1, i)

        for y in reg_y_vars:
            ax = sns.regplot(df1[x], df1[y])
            plt.xlabel(x)
            plt.ylabel(y)
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
                item.set_fontsize(20)
            for item in ax.get_xticklabels() + ax.get_yticklabels():
                item.set_fontsize(14)
            plt.savefig(os.path.join('outputs/linreg', '{0}-{1}-{2}-regplot.png'.format\
                (i, x, y)), bbox_inches='tight')
            plt.close()
    adv += 1
'''
