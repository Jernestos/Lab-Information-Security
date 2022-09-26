import math
import random
from fpylll import LLL
from fpylll import BKZ
from fpylll import IntegerMatrix
from fpylll import CVP
from fpylll import SVP
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

#Question 10:
#Question 11:
#Question 12:
    
#copy paste egcd, mod_inv and bits_to_int (modified) from module_1_ECC_ECDSA, prewritten code
# Euclidean algorithm for gcd computation
# Output: gcd g, Bezout's coefficient s, t such that g = s * a + t * b
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

# Modular inversion computation
def mod_inv(a, p):
    if a < 0:
        return p - mod_inv(-a, p)
    g, x, y = egcd(a, p)
    if g != 1:
        raise ArithmeticError("Modular inverse does not exist")
    else:
        return x % p

# Function to map a truncated bit string to an integer
# No modulo q
def bits_to_int(h_as_bits):
    val = 0
    len = int(math.log(q, 2) + 1)
    for i in range(len):
        val = val * 2
        if(h_as_bits[i] == '1'):
            val = val + 1
    return val

def check_x(x, Q):
    """ Given a guess for the secret key x and a public key Q = [x]P,
        checks if the guess is correct.

        :params x:  secret key, as an int
        :params Q:  public key, as a tuple of two ints (Q_x, Q_y)
    """
    x = int(x)
    if x <= 0:
        return False
    Q_x, Q_y = Q
    sk = ec.derive_private_key(x, ec.SECP256R1())
    pk = sk.public_key()
    xP = pk.public_numbers()
    return xP.x == Q_x and xP.y == Q_y

def recover_x_known_nonce(k, h, r, s, q):
    # Implement the "known nonce" cryptanalytic attack on ECDSA
    # The function is given the nonce k, (h, r, s) and the base point order q
    # The function should compute and return the secret signing key x
#    raise NotImplementedError()
    #from slides
    x = mod_inv(r, q) * (k * s - h) % q
    return x

def recover_x_repeated_nonce(h_1, r_1, s_1, h_2, r_2, s_2, q):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA
    # The function is given the (hashed-message, signature) pairs (h_1, r_1, s_1) and (h_2, r_2, s_2) generated using the same nonce
    # The function should compute and return the secret signing key x
#    raise NotImplementedError()
    x = ((h_1 * s_2 - h_2 * s_1) * mod_inv(r_2 * s_1 - r_1 * s_2, q)) % q
    return x


def MSB_to_Padded_Int(N, L, list_k_MSB):
    # Implement a function that does the following: 
    # Let a is the integer represented by the L most significant bits of the nonce k 
    # The function should return a.2^{N - L} + 2^{N -L -1}
#    raise NotImplementedError()
    res = bits_to_int(list_k_MSB) * (2**(N - L)) + 2**(N - L - 1)
    return res

def LSB_to_Int(list_k_LSB):
    # Implement a function that does the following: 
    # Let a is the integer represented by the L least significant bits of the nonce k 
    # The function should return a
#    raise NotImplementedError()
    res = bits_to_int(list_k_MSB)
    return res

def setup_hnp_single_sample(N, L, list_k_MSB, h, r, s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement a function that sets up a single instance for the hidden number problem (HNP)
    # The function is given a list of the L most significant bts of the N-bit nonce k, along with (h, r, s) and the base point order q
    # The function should return (t, u) computed as described in the lectures
    # In the case of EC-Schnorr, r may be set to h
#    raise NotImplementedError()
    if algorithm == "ecdsa":
        if givenbits == "msbs":
            s_inv = mod_inv(s, q)
            t = r * s_inv % q
            z = h * s_inv % q
            a = MSB_to_Padded_Int(N, L, list_k_MSB)
            u = (a - z) % q #TODO check for modulo q
            return (t, u)
            
        elif givenbits == "lsbs":
            #TODO
            raise NotImplementedError()
        else:
            RuntimeError("setup_hnp_single_sample: Invalid givenbits argument.")
    elif algorithm == "ecschnorr":
        if givenbits == "msbs":
            #TODO
            raise NotImplementedError()
        elif givenbits == "lsbs":
            #TODO
            raise NotImplementedError()
        else:
            RuntimeError("setup_hnp_single_sample: Invalid givenbits argument.")
    else:
        raise RuntimeError("setup_hnp_single_sample: Invalid algorithm.")

def setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement a function that sets up n = num_Samples many instances for the hidden number problem (HNP)
    # For each instance, the function is given a list the L most significant bits of the N-bit nonce k, along with (h, r, s) and the base point order q
    # The function should return a list of t values and a list of u values computed as described in the lectures
    # Hint: Use the function you implemented above to set up the t and u values for each instance
    # In the case of EC-Schnorr, list_r may be set to list_h
#    raise NotImplementedError()
    #TODO sanity checks on input values e.g. list length == num_Samples
    t_list = []
    u_list = []
    if algorithm == "ecdsa":
        if givenbits == "msbs":
            for i in range(num_Samples):
                (t_i, u_i) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
                t_list.append(t_i)
                u_list.append(u_i)
            return (t_list, u_list)
        elif givenbits == "lsbs":
            #TODO
            raise NotImplementedError()
        else:
            RuntimeError("setup_hnp_all_samples: Invalid givenbits argument.")
    elif algorithm == "ecschnorr":
        if givenbits == "msbs":
            #TODO
            raise NotImplementedError()
        elif givenbits == "lsbs":
            #TODO
            raise NotImplementedError()
        else:
            RuntimeError("setup_hnp_all_samples: Invalid givenbits argument.")
    else:
        raise RuntimeError("setup_hnp_all_samples: Invalid algorithm.")


#from fpylll import IntegerMatrix

def hnp_to_cvp(N, L, num_Samples, list_t, list_u, q):
    # Implement a function that takes as input an instance of HNP and converts it into an instance of the closest vector problem (CVP)
    # The function is given as input a list of t values, a list of u values and the base point order q
    # The function should return the CVP basis matrix B (to be implemented as a nested list) and the CVP target vector u (to be implemented as a list)
    # NOTE: The basis matrix B and the CVP target vector u should be scaled appropriately. Refer lecture slides and lab sheet for more details
#    raise NotImplementedError()
    #Question 1: TODO I think that is not possible. Integer x is between 1 and q - 1, inclusive.
    #Question 2: Does not work (tested on cocalc); typerror; real numbers not supported
    #Question 3: Find a factor c such that every element of the basis matrix/target vector multiplied with c yields an integer.
    #TODO sanity check on input values?
    # From lab task: [...] should be scaled .... contain only integral entries (if required)
    # -> multiply by some factor such that matrix and vector only contains integers
    factor = 2**(L + 1)
    q_x_factor = q * factor
    #construct matrix B
    dim = num_Samples + 1
    base_matrix_B = []
    for i in range(num_Samples):
        temp_row = [0] * dim
        temp_row[i] = q_x_factor #q
        base_matrix_B.append(temp_row) #construct row of matrix (except last row)
    
    temp_row = [0] * dim #last row of matrix
    for i in range(num_Samples):
        temp_row[i] = list_t[i] * factor
    temp_row[num_Samples] = 1 #rightmost, lowermost element; originally 1/2**(L + 1)
    base_matrix_B.append(temp_row)
    
    #compute vector u
    cvp_target_vector_u = [0] * matrix_size
    for i in range(matrix_size):
        cvp_target_vector_u[i] = list_u[i] * factor #set u
    
    return (base_matrix_B, cvp_target_vector_u) #(list of lists, list)

    
def cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u):
    # Implement a function that takes as input an instance of CVP and converts it into an instance of the shortest vector problem (SVP)
    # Your function should use the Kannan embedding technique in the lecture slides
    # The function is given as input a CVP basis matrix B and the CVP target vector u
    # The function should use the Kannan embedding technique to output the corresponding SVP basis matrix B' of apropriate dimensions.
    # The SVP basis matrix B' should again be implemented as a nested list
#    raise NotImplementedError()
    
    #Question 6:
    #Question 7:
        
    #use slide 34 of week 3
    svp_basis_matrix_B_primed = copy.deepcopy(cvp_basis_B) #recall: entries scaled by factor = 2**(L + 1) in hnp_to_cvp
    for row in svp_basis_matrix_B_primed:
        row.append(0)
    
    #M = ||f|| <= lambda1 / 2; lambda1 = (n/(2*pi*e))^(1/2) * det(L)^(1/n) #from slides - Gaussian Heuristic
    M = 42 #TODO
    last_row = copy.deepcopy(cvp_list_u) #construct last row of B_primed
    last_row.append(M)
    
    svp_basis_matrix_B_primed.append(last_row)
    
    return svp_basis_matrix_B_primed #(list of lists)
    

def solve_cvp(cvp_basis_B, cvp_list_u):
    # Implement a function that takes as input an instance of CVP and solves it using in-built CVP-solver functions from the fpylll library
    # The function is given as input a CVP basis matrix B and the CVP target vector u
    # The function should output the solution vector v (to be implemented as a list)
    # NOTE: The basis matrix B should be processed appropriately before being passes to the fpylll CVP-solver. See lab sheet for more details
    #Notes: From hint for question 5, and from slides about lattice reduction, there are 2 reduction algorithms, LLL and BKZ. 
    #How to use SVP and CVP tools on https://github.com/fplll/fpylll/blob/master/docs/tutorial.rst
    #https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch18.pdf
    #https://cseweb.ucsd.edu/classes/wi12/cse206A-a/lec3.pdf
    #https://www.researchgate.net/publication/225240686_Lattice_Attacks_on_Digital_Signature_Schemes
    #These three sources give the idea to use a reduced basis, using LLL
    #Question 4: Question 5 suggests to use some kind of preprocessing and the hint gives it away; use LLL or BKZ as preprocessing of cvp_basis_B; the papers above suggest to use LLL.
    #Question 5:
#    raise NotImplementedError()
    B = LLL.reduction(cvp_basis_B) #BKZ.reduction(cvp_basis_B, BKZ.Param(block_size)) - block_size?
    v = list(CVP.closest_vector(B, cvp_list_u)) #without list, it's just a multi-dim tuple
    return v #list

def solve_svp(svp_basis_B):
    # Implement a function that takes as input an instance of SVP and solves it using in-built SVP-solver functions from the fpylll library
    # The function is given as input the SVP basis matrix B
    # The function should output a list of candidate vectors that may contain x as a coefficient
    # NOTE: Recall from the lecture and also from the exercise session that for ECDSA cryptanalysis based on partial nonces, you might want
    #       your function to include in the list of candidate vectors the *second* shortest vector (or even a later one). 
    # If required, figure out how to get the in-built SVP-solver functions from the fpylll library to return the second (or later) shortest vector
    #In the task pdf, it is stated "should output a lattice basis containing the solution vector f"
    #https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch18.pdf; this source suggest to reduce svp_basis_B via LLL as a first step
    #https://martinralbrecht.wordpress.com/2016/04/03/fpylll/ svp usage
    #Question 8: Suggested by paper above
    #Question 9: From lecture slides and exercise, norm(f) <= sqrt(n + 1) * 2**(N - L - 1) #TODO
#    raise NotImplementedError()
    B = LLL.reduction(svp_basis_B)
    #v = SVP.shortest_vector(IntegerMatrix B)
    #Observe: first row of B and v match (experimentally tested on cocalc). -> B yields candidate vectors.
    result = []
    for ele in B:
        result.append(list(ele))
    return result[1:] #omit first vector; #list of lists
    


def recover_x_partial_nonce_CVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q) #(list of lists, list)
    #v_List = solve_cvp(cvp_basis_B, cvp_list_u) #original version
    v_List = solve_cvp(IntegerMatrix.from_matrix(cvp_basis_B), cvp_list_u) #have to use this (instead of list of lists)
    # The function should recover the secret signing key x from the output of the CVP solver and return it
    x = v_List[-1]
    return x
#    raise NotImplementedError()

def recover_x_partial_nonce_SVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q)
    svp_basis_B = cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u)
    list_of_f_List = solve_svp(svp_basis_B)
    # The function should recover the secret signing key x from the output of the SVP solver and return it
    raise NotImplementedError()



# testing code: do not modify

from module_1_ECDSA_Cryptanalysis_tests import run_tests

run_tests(recover_x_known_nonce,
    recover_x_repeated_nonce,
    recover_x_partial_nonce_CVP,
    recover_x_partial_nonce_SVP
)
