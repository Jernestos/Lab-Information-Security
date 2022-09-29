import math
import random
from fpylll import LLL
from fpylll import BKZ
from fpylll import IntegerMatrix
from fpylll import CVP
from fpylll import SVP
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

import copy

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
def bits_to_int(h_as_bits): #TODO read the bits in reverse? Should be okay, it's a copy paste from the week 2 module
    val = 0
    for i in range(len(h_as_bits)):
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
    x = mod_inv(r, q) * (k * s - h) % q
    return x

def recover_x_repeated_nonce(h_1, r_1, s_1, h_2, r_2, s_2, q):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA
    # The function is given the (hashed-message, signature) pairs (h_1, r_1, s_1) and (h_2, r_2, s_2) generated using the same nonce
    # The function should compute and return the secret signing key x
    x = ((h_1 * s_2 - h_2 * s_1) * mod_inv(r_2 * s_1 - r_1 * s_2, q)) % q
    return x


def MSB_to_Padded_Int(N, L, list_k_MSB):
    # Implement a function that does the following: 
    # Let a is the integer represented by the L most significant bits of the nonce k 
    # The function should return a.2^{N - L} + 2^{N -L -1}
    res = bits_to_int(list_k_MSB) * (2**(N - L)) + 2**(N - L - 1)
    return res

def LSB_to_Int(list_k_LSB):
    # Implement a function that does the following: 
    # Let a is the integer represented by the L least significant bits of the nonce k 
    # The function should return a
    res = bits_to_int(list_k_LSB)
    return res

def setup_hnp_single_sample(N, L, list_k_MSB, h, r, s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement a function that sets up a single instance for the hidden number problem (HNP)
    # The function is given a list of the L most significant bts of the N-bit nonce k, along with (h, r, s) and the base point order q
    # The function should return (t, u) computed as described in the lectures
    # In the case of EC-Schnorr, r may be set to h
    if algorithm == "ecdsa" and givenbits == "msbs":
        s_inv = mod_inv(s, q)
        t = (r * s_inv) % q #yes, mod q as in slides 23
        z = (h * s_inv) % q #also mod q
        a = MSB_to_Padded_Int(N, L, list_k_MSB) 
        u = (a - z) % q #mod q???
        #slide 24
        if not (u < int(u/2)):
            u -= q
        return (t, u)
    elif algorithm == "ecdsa" and givenbits == "lsbs":
        s_inv = mod_inv(s, q)
        two_pow_L_inv = mod_inv(2**L, q)
        t = (s_inv * r * two_pow_L_inv) % q #similar as above
        a = LSB_to_Int(list_k_MSB)
        u = ((a - s_inv * h) * two_pow_L_inv) % q #here use mod q for u because of s_inv
        #slide 24
        if not (u < int(u/2)):
            u -= q
        return (t, u)
    elif algorithm == "ecschnorr" and givenbits == "msbs":
        u = (MSB_to_Padded_Int(N, L, list_k_MSB) - s) % q#mod q?
        t = h
        #slide 24
        if not (u < int(u/2)):
            u -= q
        return (t, u)
    elif algorithm == "ecschnorr" and givenbits == "lsbs":
        two_pow_L_inv = mod_inv(2**L, q)
        a = LSB_to_Int(list_k_MSB)
        t = (h * two_pow_L_inv) % q
        u = ((a - s) * two_pow_L_inv) % q
        #slide 24
        if not (u < int(u/2)):
            u -= q
        return (t, u)
    else:
        raise RuntimeError("setup_hnp_single_sample: Invalid choice of algorithm and/or givenbits")

def setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement a function that sets up n = num_Samples many instances for the hidden number problem (HNP)
    # For each instance, the function is given a list the L most significant bits of the N-bit nonce k, along with (h, r, s) and the base point order q
    # The function should return a list of t values and a list of u values computed as described in the lectures
    # Hint: Use the function you implemented above to set up the t and u values for each instance
    # In the case of EC-Schnorr, list_r may be set to list_h
    t_list = []
    u_list = []
    for i in range(num_Samples):
        (t, u) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
        t_list.append(t)
        u_list.append(u)
    return (t_list, u_list)

def hnp_to_cvp(N, L, num_Samples, list_t, list_u, q):
    # Implement a function that takes as input an instance of HNP and converts it into an instance of the closest vector problem (CVP)
    # The function is given as input a list of t values, a list of u values and the base point order q
    # The function should return the CVP basis matrix B (to be implemented as a nested list) and the CVP target vector u (to be implemented as a list)
    # NOTE: The basis matrix B and the CVP target vector u should be scaled appropriately. Refer lecture slides and lab sheet for more details 
    factor = 2**(L + 1)
    q_x_factor = q * factor #q scaled by factor
    dim = 1 + num_Samples
    B_cvp_matrix = []
    for i in range(num_Samples):
        temp_row = [0] * dim
        temp_row[i] = q_x_factor
        B_cvp_matrix.append(temp_row)
    
    t_list = copy.deepcopy(list_t)
    for i in range(num_Samples):
        t_list[i] *= factor
    t_list.append(1)
    B_cvp_matrix.append(t_list)

    u_list = copy.deepcopy(list_u)
    for i in range(num_Samples):
        u_list[i] *= factor
    u_list.append(0)

    return (B_cvp_matrix, u_list)


def cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u):
    # Implement a function that takes as input an instance of CVP and converts it into an instance of the shortest vector problem (SVP)
    # Your function should use the Kannan embedding technique in the lecture slides
    # The function is given as input a CVP basis matrix B and the CVP target vector u
    # The function should use the Kannan embedding technique to output the corresponding SVP basis matrix B' of apropriate dimensions.
    # The SVP basis matrix B' should again be implemented as a nested list
    n = num_Samples
    cvp_basis_B_ = copy.deepcopy(cvp_basis_B)
    for row in cvp_basis_B_:
        row.append(0)

    #Gaussian heuristic slide 18
    #Kannan's embedding technique slide 34 (uses 1/2 as additional factor)
    one_half_factor = (1/2)
    n_n_constant = ((n+1) / (2 * math.pi * math.e))**(1/2)
    scaled_q = cvp_basis_B_[0][0] 

    scaled_q_powded = scaled_q**(n/(n+1))
    M = round(one_half_factor * n_n_constant * scaled_q_powded)

    cvp_list_u_ = copy.deepcopy(cvp_list_u)
    cvp_list_u_.append(M)
    cvp_basis_B_.append(cvp_list_u_)
    return cvp_basis_B_


def solve_cvp(cvp_basis_B, cvp_list_u):
    # Implement a function that takes as input an instance of CVP and solves it using in-built CVP-solver functions from the fpylll library
    # The function is given as input a CVP basis matrix B and the CVP target vector u
    # The function should output the solution vector v (to be implemented as a list)
    # NOTE: The basis matrix B should be processed appropriately before being passes to the fpylll CVP-solver. See lab sheet for more details
    fpylll_cvp_basis_B = IntegerMatrix.from_matrix(cvp_basis_B)
    LLL.reduction(fpylll_cvp_basis_B)
    cvp_solution_v = list(CVP.closest_vector(fpylll_cvp_basis_B, cvp_list_u, method="fast"))
    return cvp_solution_v
    

def solve_svp(svp_basis_B):
    # Implement a function that takes as input an instance of SVP and solves it using in-built SVP-solver functions from the fpylll library
    # The function is given as input the SVP basis matrix B
    # The function should output a list of candidate vectors that may contain x as a coefficient
    # NOTE: Recall from the lecture and also from the exercise session that for ECDSA cryptanalysis based on partial nonces, you might want
    #       your function to include in the list of candidate vectors the *second* shortest vector (or even a later one). 
    # If required, figure out how to get the in-built SVP-solver functions from the fpylll library to return the second (or later) shortest vector
    fpylll_svp_basis_B = IntegerMatrix.from_matrix(svp_basis_B)
    LLL.reduction(fpylll_svp_basis_B)
    shortest_vector_candidates = []
    for row in fpylll_svp_basis_B:
        shortest_vector_candidates.append(list(row))
    return shortest_vector_candidates #return all candidates


def recover_x_partial_nonce_CVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q)
    
    fpylll_cvp_basis_B = IntegerMatrix.from_matrix(cvp_basis_B)
    C = LLL.reduction(fpylll_cvp_basis_B)
    cvp_solution_v = list(CVP.closest_vector(C, cvp_list_u, method="fast"))
    return cvp_solution_v[-1] % q
    
    #v_List = solve_cvp(cvp_basis_B, cvp_list_u)
    # The function should recover the secret signing key x from the output of the CVP solver and return it
    #return v_List[-1] % q

def recover_x_partial_nonce_SVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q)
    svp_basis_B = cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u)
    list_of_f_List = solve_svp(svp_basis_B)
    # The function should recover the secret signing key x from the output of the SVP solver and return it
    f_m = list_of_f_List[1] #second element, a list
    f = f_m[:-1] #remove the element M
    u = cvp_list_u[:-1] #modified cvp_list_u in cvp_to_svp; remove M
    x = u[-1] - f[-1]
    return x % q



# testing code: do not modify

from module_1_ECDSA_Cryptanalysis_tests import run_tests

run_tests(recover_x_known_nonce,
    recover_x_repeated_nonce,
    recover_x_partial_nonce_CVP,
    recover_x_partial_nonce_SVP
)
