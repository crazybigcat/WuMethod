from QuantumIntelligence.BasicFunSZZ.Polynomial import Polynomial
from QuantumIntelligence.BasicFunSZZ.Geometry import Geometry
from QuantumIntelligence.AutomatedTheoremProving.WuMethod import WuMethod

# Initialize the Geometry class with a sufficient number of variable slots
device = 'cpu'
g = Geometry(device=device)

# Define a list of point names
# point_name_list = ['A', 'B', 'C', 'H', 'D', 'E', 'F', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']
point_name_list = ['A', 'B', 'C', 'H', 'D', 'E', 'F', 'A1', 'B1', 'C1', 'C2']

# Add the points to the Geometry instance with sequential indices
for idx, point_name in enumerate(point_name_list):
    g.add_point(point_name, 2*idx, 2*idx+1)

# zero relation
eA0 = g.equal_zero('A', 0)[0]
eA1 = g.equal_zero('A', 1)[0]
eB0 = g.equal_zero('B', 0)[0]
eF0 = g.equal_zero('F', 0)[0]
eC10 = g.equal_zero('C1', 0)[0]
eC20 = g.equal_zero('C2', 0)[0]

# midpoint relation
mD = g.midpoint('D', 'C', 'B')
mE = g.midpoint('E', 'C', 'A')
mF = g.midpoint('F', 'A', 'B')

# orthocenter relation
perpAH, perpBH, perpCH = g.orthocenter('H', 'A', 'B', 'C')

# collinear relation
colA1 = g.collinear2D('A1', 'B', 'C')[0]
# colA2 = g.collinear2D('A2', 'B', 'A1')[0]
colB1 = g.collinear2D('B1', 'A', 'C')[0]
# colB2 = g.collinear2D('B2', 'A', 'C')[0]
colC1 = g.collinear2D('C1', 'A', 'B')[0]
colC2 = g.collinear2D('C2', 'A', 'B')[0]

# on circle relation
oncA1 = g.point_on_circle('A1', 'D', 'H')[0]
# oncA2 = g.point_on_circle('A2', 'D', 'A1')[0]
oncB1 = g.point_on_circle('B1', 'E', 'H')[0]
# oncB2 = g.point_on_circle('B2', 'E', 'H')[0]
oncC1 = g.point_on_circle('C1', 'F', 'H')[0]
oncC2 = g.point_on_circle('C2', 'F', 'C1')[0]

# C1, C2, B1, A1 are concyclic
con = g.concyclic('C1', 'C2', 'B1', 'A1')[0]

# Print the points to verify
print(g)

W = WuMethod()
h0 = perpAH
h1 = perpBH
h0 = W.pseudo_divide(h0, h1, 7)
h0.reduce_variable()
h2, h3 = mD
h4, h5 = mE
h6, h7 = mF
h8tmp = oncA1
h9 = colA1
h8 = W.eliminate_variable(h8tmp, h9, 15)
h10tmp = oncB1
h11 = colB1
h10 = W.eliminate_variable(h10tmp, h11, 17)
h13 = oncC1
h12tmp = colC1
h12 = W.eliminate_variable_iteratively(h12tmp, [eA0, eA1, eB0],[0, 1, 2])
h12.reduce_variable()
print(h12, '!!!!!')
# h13 = W.eliminate_variable_iteratively(h13tmp, [h12], [19])
# h13 = W.eliminate_variable_iteratively(h13tmp, [h0, h1], [4, 5])
h14tmp = colC2
h14 = W.eliminate_variable_iteratively(h14tmp, [eA0, eA1, eB0],[0, 1, 2])
h14.reduce_variable()
h15tmp = oncC2
h15 = oncC2
h15 = W.eliminate_variable_iteratively(h15tmp, [h14, h12], [20, 18])
h15.simplify_coe()
# print(h14)

# get h15 from mathematics
h15 = Polynomial.from_string('x22 + x20 - x4', device=device)
# h14 = Polynomial.from_string('x21x5^2+x25x5^2-x5^3+x21x6^2+x25x6^2-x5x6^2')
# h10 = Polynomial.from_string('x15^3-2x10x15x16+x15x16^2+x15^2x17+x16^2x17+2x10x15x4-2x16x17x4-x15x4^2+x17x4^2-x15^2x5')
h_dict = {21: h15, 20: h14, 19: h13, 18: h12, 17: h11, 16: h10, 15: h9, 14: h8,
          13: h7, 12: h6, 11: h5, 10: h4, 9: h3, 8: h2, 7: h1, 6: h0}

for ii in h_dict.keys():
    h_dict[ii] = W.eliminate_variable_iteratively(h_dict[ii], [eA0, eA1, eB0],[0, 1, 2])

for ii in h_dict.keys():
    for jj in [13, 12, 11, 10, 9, 8, 7]:
        if ii > jj:
            h_dict[ii] = W.eliminate_variable_iteratively(h_dict[ii], [h_dict[jj]], [jj])

for ii in h_dict.keys():
    h_dict[ii].simplify_coe()
    print(ii, h_dict[ii].nonzero_var_indices(), h_dict[ii].terms.shape)
    print(h_dict[ii])

rr = con
print(rr)
# rr21 =
print(rr.terms.shape)
for ii in range(21, 5, -1):
    rr = W.eliminate_variable(rr, h_dict[ii], ii)
    rr.simplify_coe()
    rr.reduce_variable()
    print(ii, rr.terms.shape)
    # if ii == 15:
    #     print(rr)
    if rr.terms.shape[0] < 10:
        print(ii, rr)
print(rr)