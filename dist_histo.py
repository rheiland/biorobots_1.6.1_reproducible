import sys
import string
from pyMCDS import pyMCDS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

argc=len(sys.argv)
print('argv=',sys.argv)
print('argv[0]=',sys.argv[0])
#p1=string.atof(sys.argv[1])

#mcds = pyMCDS('output00000000.xml','output');
#mcds = pyMCDS('output00000002.xml')
fname = "output%08d.xml" % int(sys.argv[1])
mcds = pyMCDS(fname)

#In [7]: mcds.data['discrete_cells'].keys()
#Out[7]: dict_keys(['ID', 'position_x', 'position_y', 'position_z', 'total_volume', 'cell_type', 'cycle_model', 'current_phase', 'elapsed_time_in_phase', 'nuclear_volume', 'cytoplasmic_volume', 'fluid_fraction', 'calcified_fraction', 'orientation_x', 'orientation_y', 'orientation_z', 'polarity', 'migration_speed', 'motility_vector_x', 'motility_vector_y', 'motility_vector_z', 'migration_bias', 'motility_bias_direction_x', 'motility_bias_direction_y', 'motility_bias_direction_z', 'persistence_time', 'motility_reserved', 'receptor', 'elastic_coefficient'])


tval = int(mcds.get_time())
print('time = ',tval)
cx = mcds.data['discrete_cells']['position_x']
cy = mcds.data['discrete_cells']['position_y']
print('x size =',cx.size)
print('y size =',cy.size)
bad_max = 5000
#idx_bad = np.where((cx > bad_max) ^ (cy > bad_max))
#print('idx_bad=',idx_bad)


#cycle = mcds.data['discrete_cells']['cycle_model']
#cycle = cycle.astype( int )

# static int worker_ID = 0;
# static int cargo_ID = 1;
# static int linker_ID = 2; 
# static int director_ID = 3;
cell_type = mcds.data['discrete_cells']['cell_type']
cell_type = cell_type.astype(int)
print('cell_type size =',cell_type.size)
print('cell_type =',cell_type)

#idx_director = np.where(cell_type == 3)   # a tuple
idx_director = np.where(cell_type == 3)[0]   # 15
idx_cargo = np.where(cell_type == 1)[0]   # 400
idx_worker = np.where(cell_type == 0)[0]   # 50

dist_cargo = np.zeros(len(idx_cargo))

print('idx_director = ',idx_director)
print('len idx_director = ',len(idx_director))
# print('idx_cargo = ',idx_cargo)
print('len idx_cargo = ',len(idx_cargo))
print('idx_worker = ',idx_worker)
print('len idx_worker = ',len(idx_worker))

cell_id = mcds.data['discrete_cells']['ID']

#live = np.argwhere( (cycle < 100) & (cell_type==0) ).flatten()
#dead = np.argwhere( cycle >= 100 ).flatten()
#endo = np.argwhere( cell_type==1 ).flatten()

receptor = mcds.data['discrete_cells']['receptor']
print('receptor (custom_data) value = ', receptor)

#for idx in range(15, len(receptor)):
dist2_max = 0.0
for idx in range(15, len(receptor)):
    # if ((cell_type[idx] == 1) and (receptor[idx] == 0)):  # have I reached a director cell?
    if (cell_type[idx] == 1):    # cargo?
        cx_cell = cx[idx]
        cy_cell = cy[idx]
        dist2_min = 1.e6
        for jdx in range(0, len(idx_director)):
            cx_dir = cx[jdx]
            cy_dir = cy[jdx]
            dx = cx_cell - cx_dir
            dy = cy_cell - cy_dir
            dist2 = (dx*dx) + (dy*dy)
            if (dist2 < dist2_min):
                dist2_min = dist2
            if (dist2 > dist2_max):
                dist2_max = dist2
        print(idx, np.sqrt(dist2_min))
        dist_cargo[idx-15] = np.sqrt(dist2_min)

print('max dist= ', np.sqrt(dist2_max))
print('dist_cargo = ', dist_cargo)

#print(cx.size,cy.size,cell_type.size, receptor.size)

num_bins = 40
#plt.xlim(0, 100,10)
#n, bins, patches = plt.hist(dist_cargo, num_bins, density=True, facecolor='g', alpha=0.75)
#counts, bins = np.histogram(dist_cargo)
#plt.hist(bins[:-1], bins, weights=counts)
#plt.hist(dist_cargo, bins='auto')
bins = np.arange(0,500,25)
#plt.hist(dist_cargo, bins='auto')
plt.hist(dist_cargo, bins=bins)
plt.xlim(left=0)
plt.ylim(top=180)
title_str = str(tval) + ' mins' 
plt.title(title_str)
plt.xlabel('Histogram: distance(cargo cell, nearest director)')
plt.ylabel('# of cargo cells')
plt.show()