import math
import random
from fpylll import LLL
from fpylll import BKZ
from fpylll import IntegerMatrix
from fpylll import CVP
from fpylll import SVP
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

import copy #part of standard library

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
#problem is here
def bits_to_int(h_as_bits): #TODO read the bits in reverse? Should be okay, it's a copy paste from the week 2 module
    # binary_string = "".join([str(i) for i in list_k_LSB])
    # a = int(binary_string, 2)
    bitseq = []
    for b in h_as_bits:
        bitseq.append(str(b))
    bitstring = "0b" + "".join(bitseq)
    return int(bitstring, 2)
    #the approach below does not work at all - somehow it prevents cvp.closest_vector from terminating/slows it down extremly
    # val = 0
    # for i in range(len(h_as_bits)):
    #     val = val * 2
    #     if(h_as_bits[i] == '1'):
    #         val = val + 1
    # return val

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

def recover_x_known_nonce(k, h, r, s, q): #checked
    # Implement the "known nonce" cryptanalytic attack on ECDSA
    # The function is given the nonce k, (h, r, s) and the base point order q
    # The function should compute and return the secret signing key x
    x = mod_inv(r, q) * (k * s - h) % q #from slides
    return x

def recover_x_repeated_nonce(h_1, r_1, s_1, h_2, r_2, s_2, q): #checked
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA
    # The function is given the (hashed-message, signature) pairs (h_1, r_1, s_1) and (h_2, r_2, s_2) generated using the same nonce
    # The function should compute and return the secret signing key x
    x = ((h_1 * s_2 - h_2 * s_1) * mod_inv(r_2 * s_1 - r_1 * s_2, q)) % q #from slides
    return x


def MSB_to_Padded_Int(N, L, list_k_MSB): #checked
    # Implement a function that does the following: 
    # Let a is the integer represented by the L most significant bits of the nonce k 
    # The function should return a.2^{N - L} + 2^{N -L -1}
    res = bits_to_int(list_k_MSB) * (2**(N - L)) + 2**(N - L - 1)
    return res

def LSB_to_Int(list_k_LSB): #checked
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
    #input sanity check? - according to moodle forum not needed as we can assume we work with correct input (assuming that answer applies to all labs)
    if algorithm == "ecdsa" and givenbits == "msbs":
        s_inv = mod_inv(s, q)
        t = (r * s_inv) % q #yes, mod q as in slides 23
        z = (h * s_inv) % q #also mod q
        a = MSB_to_Padded_Int(N, L, list_k_MSB) 
        u = (a - z) % q #mod q???
        #slide 24
        # if not (u < round(q/2)):
        #     u -= q
        return (t, u)
    elif algorithm == "ecdsa" and givenbits == "lsbs":
        #from equation (1) (see module pdf): isolate k, substitute k with the form involving a_head and e; isolate e and bring everything that has not x as factor to the same side as e.
        #so we first get k = s^(-1)*h + s^(-1)*r*x mod q
        #then substitute k with form involving a_head and e;
        #rearrange such that we get
        #e + (a_head + s^(-1)*h)*inv(2^L) = r*s^(-1)*inv(2^L, q)*x mod q
        #e + u                            = t * x
        #Hope that 2^L has inverse in mod q
        s_inv = mod_inv(s, q)
        two_pow_L_inv = mod_inv(2**L, q)
        t = (s_inv * r * two_pow_L_inv) % q #similar as above
        a = LSB_to_Int(list_k_MSB)
        u = ((a - s_inv * h) * two_pow_L_inv) % q #here use mod q for u because of s_inv
        #slide 24
        # if not (u < round(q/2)):
        #     u -= q
        return (t, u)
    elif algorithm == "ecschnorr" and givenbits == "msbs":
        # In the case of EC-Schnorr, r may be set to h
        #Idea: use same strategy: reformulate signing equation to known t and u values
        #rearrange schnorr signature equation for s to solve for k
        #k = s + hx mod q
        #substitute k for MSB form involving a and e; subtract s from both sides
        #we get hx = a * 2^(N-L) + 2^(N - L - 1) -s + e
        #        tx = u + e
        u = (MSB_to_Padded_Int(N, L, list_k_MSB) - s) % q#mod q?
        #slide 24
        # if not (u < round(q/2)):
        #     u -= q
        t = h
        #r = h; the signature algorithm for schnor does not contain r
        return (t, u)
    elif algorithm == "ecschnorr" and givenbits == "lsbs":
        #nearly same procedure as in the ecdsa, lsbs case
        #rearrange schnorr signature equation for s to solve for k
        #k = s + hx mod q
        #substitute k for MSB form involving a and e; subtract s from both sides; multiply by inv(2^L, q) to get
        #e + (a - s) * inv(2^L, q) = x * h * inv(2^L, q)
        #e +            u          = t * x
        #Hope that 2^L has inverse in mod q

        #r = h; the signature algorithm for schnor does not contain r
        two_pow_L_inv = mod_inv(2**L, q)
        a = LSB_to_Int(list_k_MSB)
        t = (h * two_pow_L_inv) % q
        u = ((a - s) * two_pow_L_inv) % q
        #slide 24
        # if not (u < round(q/2)):
        #     u -= q
        return (t, u)
    else:
        raise RuntimeError("setup_hnp_single_sample: Invalid choice of algorithm and/or givenbits")

def setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement a function that sets up n = num_Samples many instances for the hidden number problem (HNP)
    # For each instance, the function is given a list the L most significant bits of the N-bit nonce k, along with (h, r, s) and the base point order q
    # The function should return a list of t values and a list of u values computed as described in the lectures
    # Hint: Use the function you implemented above to set up the t and u values for each instance
    # In the case of EC-Schnorr, list_r may be set to list_h
    # sanity checks on input values e.g. list length == num_Samples - need to do that?
    t_list = []
    u_list = []
    if algorithm == "ecdsa" and givenbits == "msbs":
        for i in range(num_Samples):
            (t, u) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
            t_list.append(t)
            u_list.append(u)
        return (t_list, u_list)
    elif algorithm == "ecdsa" and givenbits == "lsbs":
        #idea: since setup_hnp_single_sample takes care of generating (t, u) lists depending on givenbits and algorithm, just reuse this code and adapt it if necessary for ecschnorr
        for i in range(num_Samples):
            (t, u) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
            t_list.append(t)
            u_list.append(u)
        return (t_list, u_list)
    elif algorithm == "ecschnorr" and givenbits == "msbs":
        # In the case of EC-Schnorr, list_r may be set to list_h
        #list_r = list_h #don't even use list_r for schnorr for our purposes; so it does not really matter here
        for i in range(num_Samples):
            (t, u) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
            t_list.append(t)
            u_list.append(u)
        return (t_list, u_list)
    elif algorithm == "ecschnorr" and givenbits == "lsbs":
        for i in range(num_Samples):
            (t, u) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
            t_list.append(t)
            u_list.append(u)
        return (t_list, u_list)
    else:
        raise RuntimeError("setup_hnp_single_sample: Invalid choice of algorithm and/or givenbits")

def hnp_to_cvp(N, L, num_Samples, list_t, list_u, q):
    # Implement a function that takes as input an instance of HNP and converts it into an instance of the closest vector problem (CVP)
    # The function is given as input a list of t values, a list of u values and the base point order q
    # The function should return the CVP basis matrix B (to be implemented as a nested list) and the CVP target vector u (to be implemented as a list)
    # NOTE: The basis matrix B and the CVP target vector u should be scaled appropriately. Refer lecture slides and lab sheet for more details 
    
    #Question 1: TODO I think that is not possible. Integer x is between 1 and q - 1, inclusive.
    #Question 2: Does not work (tested on cocalc); typerror; real numbers not supported
    #Question 3: Find a factor c such that every element of the basis matrix/target vector multiplied with c yields an integer.
    #TODO sanity check on input values?
    # From lab task: [...] should be scaled .... contain only integral entries (if required)
    # -> multiply by some factor such that matrix and vector only contains integers

    factor = 2**(L + 1)
    q_x_factor = q * factor #q scaled by factor
    dim = 1 + num_Samples
    B_cvp_matrix = []
    #from lecture we know that base_matrix_B is a square matrix (num_Samples+1) * (num_Samples+1) = dim * dim
    for i in range(num_Samples):
        temp_row = [0] * dim
        temp_row[i] = q_x_factor #scaling
        B_cvp_matrix.append(temp_row) #construct and add row to matrix (except last row of matrix)
    
    t_list = copy.deepcopy(list_t) #make deep copy to prevent issues with references
    for i in range(num_Samples): #"t" row of matrix
        t_list[i] *= factor #scaling
    t_list.append(1) #rightmost, lowermost element; originally 1/2**(L + 1)
    B_cvp_matrix.append(t_list) #matrix complete

    #correct so far
    #matrix has correct form and type

    u_list = copy.deepcopy(list_u) #make deep copy to prevent issues with references
    for i in range(num_Samples): #u vector
        u_list[i] *= factor
    u_list.append(0)

    return (B_cvp_matrix, u_list) #(list of lists, list) #module pdf descriptions; B and u are now scaled


def cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u):
    # Implement a function that takes as input an instance of CVP and converts it into an instance of the shortest vector problem (SVP)
    # Your function should use the Kannan embedding technique in the lecture slides
    # The function is given as input a CVP basis matrix B and the CVP target vector u
    # The function should use the Kannan embedding technique to output the corresponding SVP basis matrix B' of apropriate dimensions.
    # The SVP basis matrix B' should again be implemented as a nested list
    n = num_Samples
    cvp_basis_B_ = copy.deepcopy(cvp_basis_B) #make deep copy to prevent issues with references
    for row in cvp_basis_B_:
        row.append(0) #add column of zeros to the right of the matrix

    #Gaussian heuristic slide 18
    #Kannan's embedding technique slide 34 (uses 1/2 as additional factor)
    one_half_factor = (1/2)
    n_n_constant = ((n+1) / (2 * math.pi * math.e))**(1/2)
    scaled_q = cvp_basis_B_[0][0]

    scaled_q_powded = scaled_q**(n/(n+1))
    #M = round(n_n_constant * scaled_q_powded)
    #M = round(one_half_factor * n_n_constant * scaled_q_powded)

    #Use M = (1/2) lambda; lambda = sqrt((n+1)/(2*pi*e)) * del(L)**(1/n+1); del(L) = M*(q*2**(L+1))**n
    #solve for M
    #doesn't work
    # exponent = ((n + 1) / n)
    # one_half_factor = (1 / 2)**exponent
    # constant_n = ((n + 1) / (2 * math.pi * math.e))**((n + 1) / 2 * n)
    # scaled_q = cvp_basis_B_[0][0]
    # M = round(one_half_factor * constant_n * scaled_q)

    #this works
    #M = scaled_q // 2**(L+1) #M = q

    M = 2**N #works too
    
    #this works too
#    q = cvp_basis_B[0][0]
#    power = num_Samples/(num_Samples+1)
#    M = int(q**power*(1/num_Samples+1)/math.sqrt(2*math.pi*math.e))

    #doesn't work
    # power = num_Samples/(num_Samples+1) # because the num_Samples is the qs and then we have the 1
    # det_power_over_n = scaled_q**power#+1
    # constant = ((num_Samples+1)/2*math.pi*math.e)**(1/2)
    # M = int(2/constant*det_power_over_n)**num_Samples # calculated M for when lamb_1/2 = M

    #doesn't work
    # one_half_factor = (1/2)**((n+2)/(n+1))
    # n_n_constant = ((n+2) / (2 * math.pi * math.e))**((n+2)/2*(n+1))
    # scaled_q = cvp_basis_B_[0][0]
    # scaled_q_powded = scaled_q**(n/(n+1))

    #doesn't work
    # M = round(((n + 1)**(0.5)) * (2**N))

    #doesn't work
    #M = round((scaled_q // 2**(L + 1))/2)

    #does not work
    #first version for svp basis
    # one_half_factor = (1/2)**((n+2) / (n+1))
    # n_n_constant = ((n+2) / (2 * math.pi * math.e))**((n+2)/2)
    # scaled_q = cvp_basis_B_[0][0] #upper left element; q * 2^(L + 1)
    # scaled_q_powded = scaled_q**(n/(n+1))
    # M = round(n_n_constant * scaled_q_powded)

    cvp_list_u_ = copy.deepcopy(cvp_list_u) #make deep copy to prevent issues with references
    cvp_list_u_.append(M) #add right most lower element M to matrix
    cvp_basis_B_.append(cvp_list_u_) #add u to matrix
    return cvp_basis_B_

#    #Question 6: M <= lambda1 * (1/2), where lambda from gaussian heuristics
#    #Question 7: Since we scale the elements of the basis matrix, there is no need to scale M, I think.

#    #What we need: M being an integer - either by scaling or round up/down; scaling with correct factor too difficult to find (limited by machine precision) -> just round up/down.
#    #From slides:
#    #M = ||f|| <= lambda1 / 2; For lambda (after scaling, after using the Kannen embedding technique)
#    #lambda1 = ((n+2)/(2*pi*e))^(1/2) * det(L_svp)^(1/(n+2)) #from slides - Gaussian Heuristic
#    #det(L_svp) = (2^(L+1) * q)^n * M
#    #Putting this together: M = ||f|| <= (1/2) * ((n+2)/(2*pi*e))^(1/2) * ((2^(L+1) * q)^n * M)^(1/(n+2))
#    #Then we can solve for M <= (1/2)^((n+2)/(n+1))*((n+2)/(2*pi*e))^(n+2/2) * (2^(L+1) * q)^(n/(n+1))
#    #Another candidate is to consider L_cvp, and not L_svp for a potential M value.
#    #Similar computation shows that M <= (1/2) * ((n+1)/(2*pi*e))^(1/2) * (2^(L+1) * q)^(n/(n+1))
#    #Untested version
#    n = num_Samples
    #first version for svp basis
#    one_half_factor = (1/2)**((n+2) / (n+1))
#    n_n_constant = ((n+2) / (2 * math.pi * math.e))**((n+2)/2)
#    scaled_q = cvp_basis_B[0][0] #upper left element; q * 2^(L + 1)
#    scaled_q_powded = scaled_q**(n/(n+1))
#    M = round(one_half_factor * n_n_constant * scaled_q_powded)
    
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
    #From cocalc testing: LLL acts directly on the matrix itself; it changes the provided input
    fpylll_cvp_basis_B = IntegerMatrix.from_matrix(cvp_basis_B)
    LLL.reduction(fpylll_cvp_basis_B)
    #https://github.com/fplll/fpylll/blob/master/src/fpylll/fplll/svpcvp.pyx, there are some flags for CVP.closest_vector for argument method: "fast" or "proved".
    cvp_solution_v = list(CVP.closest_vector(fpylll_cvp_basis_B, cvp_list_u, method="fast")) #u as list is okay
    return cvp_solution_v
#    #From slide 21: LLL often exactly solves SVP
#    B = LLL.reduction(cvp_basis_B) #BKZ.reduction(cvp_basis_B, BKZ.Param(block_size)) - block_size?
#    v = list(CVP.closest_vector(B, cvp_list_u)) #without list, it's just a multi-dim tuple
#    return v #list
    

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
    #Question 8: Suggested by paper above; also see observation below
    #Question 9: From lecture slides and exercise, norm(f) <= sqrt(n + 1) * 2**(N - L - 1); using suggestion from qustion 10, no, I think?#TODO
    #Question 10: Yes, see below
    #Observe (through experimentation on cocalc): The first row of B and SVP.shortest_vector(svp_basis_B, method="fast", max_aux_solutions=0) 
    #yield the same vector; holds also for SVP.shortest_vector(svp_basis_B, method="proved", max_aux_solutions=0); 
    #Furthermore, the rows of B are sorted in a specific manner; norm increasing; the norm-wise greatest vector is the last row
    #idea: use LLL reduce svp_basis_B -> fpylll_svp_basis_B gives you rows
    fpylll_svp_basis_B = IntegerMatrix.from_matrix(svp_basis_B)
    LLL.reduction(fpylll_svp_basis_B)
    shortest_vector_candidates = []
    for row in fpylll_svp_basis_B:
        shortest_vector_candidates.append(list(row))
    return shortest_vector_candidates[1:] #return all candidates but the first
    #can determine which rows to use more flexibly
    #raise NotImplementedError()
    #https://github.com/fplll/fplll/blob/master/fplll/svpcvp.cpp
    
#    B = LLL.reduction(svp_basis_B)
#    #https://github.com/fplll/fpylll/blob/master/src/fpylll/fplll/svpcvp.pyx
#    #v = SVP.shortest_vector(IntegerMatrix B, method="fast", int flags=SVP_DEFAULT, pruning=True, preprocess=True, max_aux_solutions=0)
#    #:param max_aux_solutions: maximum number of additional short-ish solutions to return
#    #From slide 21: LLL often exactly solves SVP

def recover_x_partial_nonce_CVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits, algorithm)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q)
    
    # fpylll_cvp_basis_B = IntegerMatrix.from_matrix(cvp_basis_B)
    # C = LLL.reduction(fpylll_cvp_basis_B)
    # cvp_solution_v = list(CVP.closest_vector(C, cvp_list_u, method="fast"))
    # return cvp_solution_v[-1] % q
    
    v_List = solve_cvp(cvp_basis_B, cvp_list_u)
    # The function should recover the secret signing key x from the output of the CVP solver and return it
    #Question 11: We get back x directly (thanks to scaling by 2^(L+1)) by just reading out the last element
    x = v_List[-1] % q
#    if check_x(x, Q):
#        # print("Correct x") #spams console
#        pass
#    else:
#        print("Incorrect x")
#        raise RuntimeError("recover_x_partial_nonce_CVP: Wrong x") 
    return x
    # return v_List[-1] % q

def recover_x_partial_nonce_SVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"):
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits, algorithm)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q)
    svp_basis_B = cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u)
    list_of_f_List = solve_svp(svp_basis_B)
    #Questions 9 and 10 above; use questions hints and possible answer to solve this.
    # The function should recover the secret signing key x from the output of the SVP solver and return it
    #f = list_of_f_List[0][:-1] #second element, a list, remove the element M
    # x = cvp_list_u[-1] - f[-1]
    # return x % q
    #from slides: u - f; then take last element as x
    #from slides what we do is 0 - (-x) (for element in question)
    x = -list_of_f_List[0][:-1][-1] % q #second row of svp lll reduced basis, truncuate to last element (exlcuding M) and extract x (-x to be precise), mod q
#    if check_x(x, Q):
#        # print("Correct x") #spams console
#        pass
#    else:
#        print("Incorrect x")
#        raise RuntimeError("recover_x_partial_nonce_CVP: Wrong x") 
    return x
    #for non-deep copy approach
    # u = cvp_list_u[:-1] #modified cvp_list_u in cvp_to_svp; remove M
    # x = u[-1] - f[-1]
    # return x % q



# testing code: do not modify

from module_1_ECDSA_Cryptanalysis_tests import run_tests

run_tests(recover_x_known_nonce,
    recover_x_repeated_nonce,
    recover_x_partial_nonce_CVP,
    recover_x_partial_nonce_SVP
)
