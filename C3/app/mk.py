import matplotlib
matplotlib.use('Agg')

data = [ ('han',597986), ('hon',267923), ('hen',24013), ('denna',18299), ('denne',3232)] 

#data = [ ("data1", 34), ("data2", 22),
#         ("data3", 11), ( "data4", 28),
#         ("data5", 57), ( "data6", 39),
#         ("data7", 23), ( "data8", 98)]

N = len( data )
x = np.arange(1, N+1)
y = [ num for (s, num) in data ]
labels = [ s for (s, num) in data ]
width = 1
bar1 = plt.bar( x, y, width, color="y" )
plt.ylabel( 'Intensity' )
plt.xticks(x + width/2.0, labels )

plt.savefig('plot.png')
