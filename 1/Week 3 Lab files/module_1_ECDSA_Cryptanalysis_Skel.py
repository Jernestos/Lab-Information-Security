import math
import random
from fpylll import LLL
from fpylll import BKZ
from fpylll import IntegerMatrix
from fpylll import CVP
from fpylll import SVP
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

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
def bits_to_int(h_as_bits): #checked - workes correctly
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
    #input sanity check? - according to moodle forum not needed as we can assume we work with correct input (assuming that answer applies to all labs)
    if algorithm == "ecdsa":
        if givenbits == "msbs": #checked - ok
            s_inv = mod_inv(s, q)
            t = r * s_inv % q
            z = h * s_inv % q
            a = MSB_to_Padded_Int(N, L, list_k_MSB)
            u = (a - z) % q #TODO check for modulo q
            return (t, u)
        elif givenbits == "lsbs": #checked
            #from equation (1) (see module pdf): isolate k, substitute k with the form involving a_head and e; isolate e and bring everything that has not x as factor to the same side as e.
            #so we first get k = s^(-1)*h + s^(-1)*r*x mod q
            #then substitute k with form involving a_head and e;
            #rearrange such that we get
            #e + (a_head + s^(-1)*h)*inv(2^L) = r*s^(-1)*inv(2^L, q)*x mod q
            #e + u                            = t * x
            #Hope that 2^L has inverse in mod q
            a = LSB_to_Int(list_k_MSB) #modulo q? - No.
            s_inv = mod_inv(s, q)
            two_pow_L_inv = mod_inv(2**L, q)
            u = (a - s_inv * h) * two_pow_L_inv % q
            t = (r * s_inv) * two_pow_L_inv % q
            return (t, u)
        else:
            RuntimeError("setup_hnp_single_sample: Invalid givenbits argument.")
    elif algorithm == "ecschnorr":
        # In the case of EC-Schnorr, r may be set to h
        #Idea: use same strategy: reformulate signing equation to known t and u values
        if givenbits == "msbs": #checked
            #rearrange schnorr signature equation for s to solve for k
            #k = s + hx mod q
            #substitute k for MSB form involving a and e; subtract s from both sides
            #we get hx = a * 2^(N-L) + 2^(N - L - 1) -s + e
            #        tx = u + e
            u = (MSB_to_Padded_Int(N, L, list_k_MSB) - s) % q
            #r = h; the signature algorithm for schnor does not contain r
            t = h
            return (t, u)
        elif givenbits == "lsbs": #checked
            #nearly same procedure as in the ecdsa, lsbs case
            #rearrange schnorr signature equation for s to solve for k
            #k = s + hx mod q
            #substitute k for MSB form involving a and e; subtract s from both sides; multiply by inv(2^L, q) to get
            #e + (a - s) * inv(2^L, q) = x * h * inv(2^L, q)
            #e +            u          = t * x
            #Hope that 2^L has inverse in mod q
            a = LSB_to_Int(list_k_MSB)
            two_pow_L_inv = mod_inv(2**L, q)
            #r = h; the signature algorithm for schnor does not contain r
            t = h * two_pow_L_inv % q
            u = (a - s) * two_pow_L_inv % q
            return (t, u)
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
            #idea: since setup_hnp_single_sample takes care of generating (t, u) lists depending on givenbits and algorithm, just reuse this code and adapt it if necessary for ecschnorr
            for i in range(num_Samples):
                (t_i, u_i) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
                t_list.append(t_i)
                u_list.append(u_i)
            return (t_list, u_list)
        else:
            RuntimeError("setup_hnp_all_samples: Invalid givenbits argument.")
    elif algorithm == "ecschnorr":
        # In the case of EC-Schnorr, list_r may be set to list_h
        #list_r = list_h #don't even use list_r for schnorr for our purposes; so it does not really matter here
        if givenbits == "msbs":
            for i in range(num_Samples):
                (t_i, u_i) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
                t_list.append(t_i)
                u_list.append(u_i)
            return (t_list, u_list)
        elif givenbits == "lsbs":
            for i in range(num_Samples):
                (t_i, u_i) = setup_hnp_single_sample(N, L, listoflists_k_MSB[i], list_h[i], list_r[i], list_s[i], q, givenbits, algorithm)
                t_list.append(t_i)
                u_list.append(u_i)
            return (t_list, u_list)
        else:
            RuntimeError("setup_hnp_all_samples: Invalid givenbits argument.")
    else:
        raise RuntimeError("setup_hnp_all_samples: Invalid algorithm.")


#from fpylll import IntegerMatrix

def hnp_to_cvp(N, L, num_Samples, list_t, list_u, q): #checked
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
    base_matrix_B.append(temp_row) #matrix complete
    
    #compute vector u
    cvp_target_vector_u = [0] * dim
    for i in range(num_Samples):
        cvp_target_vector_u[i] = list_u[i] * factor #set u
    
    return (base_matrix_B, cvp_target_vector_u) #(list of lists, list)

    
def cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u): #TODO
    # Implement a function that takes as input an instance of CVP and converts it into an instance of the shortest vector problem (SVP)
    # Your function should use the Kannan embedding technique in the lecture slides
    # The function is given as input a CVP basis matrix B and the CVP target vector u
    # The function should use the Kannan embedding technique to output the corresponding SVP basis matrix B' of apropriate dimensions.
    # The SVP basis matrix B' should again be implemented as a nested list
#    raise NotImplementedError()
    
    #Question 6: M <= lambda1 * (1/2), where lambda from gaussian heuristics
    #Question 7: Since we scale the elements of the basis matrix, there is no need to scale M, I think.
        
    #use slide 34 of week 3
    #too slow?
    svp_basis_matrix_B_primed = copy.deepcopy(cvp_basis_B) #recall: entries scaled by factor = 2**(L + 1) in hnp_to_cvp
    for row in svp_basis_matrix_B_primed:
        row.append(0) #one extra column full of zeroes, appended to the right-side of matrix
    
    #reference issues - need original matrix?
#    for row in cvp_basis_B:
#        row.append(0)
    
    #What we need: M being an integer - either by scaling or round up/down; scaling with correct factor too difficult to find (limited by machine precision) -> just round up/down.
    #From slides:
    #M = ||f|| <= lambda1 / 2; For lambda (after scaling, after using the Kannen embedding technique)
    #lambda1 = ((n+2)/(2*pi*e))^(1/2) * det(L_svp)^(1/(n+2)) #from slides - Gaussian Heuristic
    #det(L_svp) = (2^(L+1) * q)^n * M
    #Putting this together: M = ||f|| <= (1/2) * ((n+2)/(2*pi*e))^(1/2) * ((2^(L+1) * q)^n * M)^(1/(n+2))
    #Then we can solve for M <= (1/2)^((n+2)/(n+1))*((n+2)/(2*pi*e))^(n+2/2) * (2^(L+1) * q)^(n/(n+1))
    #Another candidate is to consider L_cvp, and not L_svp for a potential M value.
    #Similar computation shows that M <= (1/2) * ((n+1)/(2*pi*e))^(1/2) * (2^(L+1) * q)^(n/(n+1))
    n = num_Samples
    #first version for svp basis
    one_half_factor = (1/2)**((n+2) / (n+1))
    n_n_constant = ((n+2) / (2 * math.pi * math.e))**((n+2)/2)
    scaled_q = cvp_basis_B[0][0] #upper left element; q * 2^(L + 1)
    scaled_q_powded = scaled_q**(n/(n+1))
    M = round(one_half_factor * n_n_constant * scaled_q_powded)
    
    #second version for svp basis
    one_half_factor = (1/2)
    n_n_constant = ((n+1) / (2 * math.pi * math.e))
    scaled_q = cvp_basis_B[0][0] #upper left element; q * 2^(L + 1)
    scaled_q_powded = scaled_q**(n/(n+1))
    M = round(one_half_factor * n_n_constant * scaled_q_powded)
    
    #too slow?
    last_row = copy.deepcopy(cvp_list_u) #construct last row of B_primed
    last_row.append(M) #right lower element of basis for svp
    svp_basis_matrix_B_primed.append(last_row) #basis for svp done
    return svp_basis_matrix_B_primed #(list of lists)
    
    #reference issues - need original matrix?
#    cvp_list_u.append(M)
#    cvp_basis_B.append(cvp_list_u)
#    return cvp_basis_B
    

    

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
    #From slide 21: LLL often exactly solves SVP
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
    #Question 8: Suggested by paper above; also see observation below
    #Question 9: From lecture slides and exercise, norm(f) <= sqrt(n + 1) * 2**(N - L - 1); using suggestion from qustion 10, no, I think?#TODO
    #Question 10: Yes, see below
#    raise NotImplementedError()
    #https://github.com/fplll/fplll/blob/master/fplll/svpcvp.cpp
    B = LLL.reduction(svp_basis_B)
    #https://github.com/fplll/fpylll/blob/master/src/fpylll/fplll/svpcvp.pyx
    #v = SVP.shortest_vector(IntegerMatrix B, method="fast", int flags=SVP_DEFAULT, pruning=True, preprocess=True, max_aux_solutions=0)
    #:param max_aux_solutions: maximum number of additional short-ish solutions to return
    
    #From slide 21: LLL often exactly solves SVP
    #Observe (through experimentation on cocalc): The first row of B and SVP.shortest_vector(svp_basis_B, method="fast", max_aux_solutions=0) yield the same vector; holds also for SVP.shortest_vector(svp_basis_B, method="proved", max_aux_solutions=0); Furthermore, the rows of B are sorted in a specific manner; norm increasing; the norm-wise greatest vector is the last row
    #idea: Use use rows of B as potential candidates
    result = [] #use question 10
    for ele in B:
        result.append(list(ele))
    return result[1:] #return entire B (excl. first row) and then adapt code appropriatly; via this way, can determine which rows to use more flexibly

def recover_x_partial_nonce_CVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"): #checked
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q) #(list of lists, list)
    #Question 11: We get back x directly (thanks to scaling) by just reading out the last element
    #v_List = solve_cvp(cvp_basis_B, cvp_list_u) #original version
    v_List = solve_cvp(IntegerMatrix.from_matrix(cvp_basis_B), cvp_list_u) #have to use this (instead of list of lists)
#    raise NotImplementedError()
    # The function should recover the secret signing key x from the output of the CVP solver and return it
    x = v_List[-1] #modulo q?
#    b = check_x(Q, x)
    b = check_x(Q, x % q)
    if b:
        print("success!")
    else:
        print(Q, end=" ")
        print("recover_x_partial_nonce_CVP failure")
        #RuntimeError("recover_x_partial_nonce_CVP failure")
    return x % q
#    raise NotImplementedError()

def recover_x_partial_nonce_SVP(Q, N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q, givenbits="msbs", algorithm="ecdsa"): #TODO
    # Implement the "repeated nonces" cryptanalytic attack on ECDSA and EC-Schnorr using the in-built CVP-solver functions from the fpylll library
    # The function is partially implemented for you. Note that it invokes some of the functions that you have already implemented
    list_t, list_u = setup_hnp_all_samples(N, L, num_Samples, listoflists_k_MSB, list_h, list_r, list_s, q)
    cvp_basis_B, cvp_list_u = hnp_to_cvp(N, L, num_Samples, list_t, list_u, q)
    svp_basis_B = cvp_to_svp(N, L, num_Samples, cvp_basis_B, cvp_list_u)
    #Questions 9 and 10 above; use questions hints and possible answer to solve this.
#    list_of_f_List = solve_svp(svp_basis_B) #originally
    list_of_f_List = solve_svp(IntegerMatrix.from_matrix(svp_basis_B))
    # The function should recover the secret signing key x from the output of the SVP solver and return it
    #which element to extract from list_of_f_List?  By question 10, (and construction), use the first one.
#    raise NotImplementedError()
    f_n_m = list_of_f_List[0]
    #from slides
    f = f_n_m[:-1]
    v = cvp_list_u - f
    x = v[-1] #last element is x
#    b = check_x(Q, x)
    b = check_x(Q, x % q)
    if b:
        print("success!")
    else:
        print(Q, end=" ")
        print("recover_x_partial_nonce_SVP failure")
        #RuntimeError("recover_x_partial_nonce_SVP failure")
    return x % q
#    raise NotImplementedError()
#to run tests, must implement all functions; not just leave some with raise NotImplementedError()

# testing code: do not modify

from module_1_ECDSA_Cryptanalysis_tests import run_tests

run_tests(recover_x_known_nonce,
    recover_x_repeated_nonce,
    recover_x_partial_nonce_CVP,
    recover_x_partial_nonce_SVP
)
