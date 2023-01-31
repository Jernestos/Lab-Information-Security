package dlog_cdh;

import java.math.BigInteger;

import cdh.CDH_Challenge;
import dlog.DLog_Challenge;
import dlog.I_DLog_Challenger;
import genericGroups.IGroupElement;

/**
 * This is the file you need to implement.
 * 
 * Implement the method {@code run} of this class.
 * Do not change the constructor of this class.
 */
public class DLog_CDH_Reduction extends A_DLog_CDH_Reduction<IGroupElement, BigInteger> {

    /**
     * Do NOT change or remove this constructor. When your reduction can not provide
     * a working standard constructor, the TestRunner will not be able to test your
     * code and you will get zero points.
     */
    public DLog_CDH_Reduction() {
        // Do not add any code here!
    }
    
    
    /**
     * You will need this field.
     */
    public CDH_Challenge<IGroupElement> cdh_challenge;
    
    
    /**
     * Save here the group generator of the DLog challenge given to you.
     */
    public IGroupElement generator;
    public IGroupElement h;
    public IGroupElement e;
    
    public BigInteger groupOrder;
    public int[] primes;
    public BigInteger multiplicativeGenerator;
    public int[] values;
    public BigInteger composed;
    
    public Boolean debugging;
    
  
    public void setup(DLog_Challenge<IGroupElement> challenge) {
      //this.cdh_challenge = challenge;
      this.cdh_challenge = null;
      this.generator = challenge.generator;
      this.h = challenge.x;
      
      this.groupOrder = challenge.generator.getGroupOrder();
      this.e = this.generator.power(this.groupOrder);
      // Make use of the fact that the group order is of the form 1 + p1 * ... * pn
      // for many small primes pi !!
      //int[] primes = PrimesHelper.getDecompositionOfPhi(groupOrder);
      this.primes = PrimesHelper.getDecompositionOfPhi(this.groupOrder); //prime factors of groupOrder - 1
      
      // Also, make use of a generator of the multiplicative group mod p.
      this.multiplicativeGenerator = PrimesHelper.getGenerator(this.groupOrder);
      
      // You can also use the method of CRTHelper
      this.values = new int[this.primes.length];
      this.composed = CRTHelper.crtCompose(this.values, this.primes);
      
      this.debugging = false;
      
    }
    
    @Override
    public BigInteger run(I_DLog_Challenger<IGroupElement> challenger) {
        // This is one of the both methods you need to implement.

        // By the following call you will receive a DLog challenge.
        DLog_Challenge<IGroupElement> challenge = challenger.getChallenge();
        setup(challenge);
        
        if(this.e.equals(challenge.x)) {
          return BigInteger.ZERO;
        }
        
        // System.out.println(this.groupOrder);
        // if(this.e.equals(this.e.invert())) {
        //   System.out.println("ok"); //TRUE
        // }
        
        // Also, make use of a generator of the multiplicative group mod p. DONE
        // this.multiplicativeGenerator = PrimesHelper.getGenerator(this.groupOrder); //z
        
        //get list of primes of (groupOrder - 1); DONE
        //public int[] primes; this.primes = PrimesHelper.getDecompositionOfPhi(this.groupOrder);
        
        //okay, works now.
        // IGroupElement test = cdh_power(this.generator.power(BigInteger.valueOf(2)), BigInteger.valueOf(10));
        // if (test.equals(this.generator.power(BigInteger.valueOf(1024)))) {
        //   System.out.println("ok");
        // }
        
        BigInteger z = this.multiplicativeGenerator; //{1,z,z^2,...,z^grouporder-2 mod group order}={1,2,...,grouporder-1}
        IGroupElement g_z = this.generator.power(z);
        var this_primes_length = this.primes.length;
        BigInteger p_minus_1 = this.groupOrder.subtract(BigInteger.ONE);
        
        if (this.debugging) {
          System.out.print("z = ");
          System.out.println(z);
        
          if (this.e.equals(g_z.power(this.groupOrder))) {
            System.out.println("OK"); //TRUE
          }
          System.out.println(this.groupOrder);
          System.out.println(p_minus_1);
          for (int i = 0; i < this_primes_length; i++) {
            System.out.print(primes[i]);
            System.out.print(" ");
          }
          System.out.println("");
        }
      
        //IGroupElement[] group_ele_crt_lhs_x = new IGroupElement[this_primes_length];
        int[] crt_lhs_k = new int[this_primes_length];
        
        for (int i = 0; i < this_primes_length; i++) {
          int pi = primes[i];
          BigInteger p_i = BigInteger.valueOf(pi);
          BigInteger exp_i = p_minus_1.divide(p_i);
          
          IGroupElement h_i = cdh_power(this.h, exp_i);
          
          for (int k = 0; k < pi; k++) {
            BigInteger exp_i_k = exp_i.multiply(BigInteger.valueOf(k));
            IGroupElement g_i = cdh_power(g_z, exp_i_k);
            if (g_i.equals(h_i)) {
              crt_lhs_k[i] = k;
              if (this.debugging) {
                System.out.print("MATCH with ");
                System.out.println(k);
              }
            }
          }
        }
        
        BigInteger k = CRTHelper.crtCompose(crt_lhs_k, this.primes);
        BigInteger x = z.modPow(k, this.groupOrder);
        return x;
        
        
        
        
        // for (int i = 0; i < this_primes_length; i++) {
        //   int qi = primes[i];
        //   BigInteger q_i = BigInteger.valueOf(qi);
        //   BigInteger exponent_i = p_minus_1.divide(q_i);
        //   IGroupElement h_ele = cdh_power(this.h, exponent_i);
          
        //   if(this.debugging) {
        //     System.out.print("qi = ");
        //     System.out.println(qi);
            
        //     System.out.print("exponent_i = ");
        //     System.out.println(exponent_i);
        //   }
          
        //   for (int k = 0; k < qi; ++k) {
            
        //     BigInteger k_exponent_i = exponent_i.multiply(BigInteger.valueOf(k));
        //     IGroupElement g_z_ele = cdh_power(g_z, k_exponent_i);
        //     if (h_ele.equals(g_z_ele)) {
              
        //       if(this.debugging) {
        //         System.out.print("MATCH! with ");
        //         System.out.println(k);
        //       }
              
        //       crt_lhs_x[i] = k_exponent_i.intValue();
        //       // crt_lhs_x[i] = z.modPow(k_exponent_i, q_i).intValue();
              
        //     }
            
            
        //   }
        // }
        
        //x_i mod q_i = x => CRT to recover x
        //BigInteger x = CRTHelper.crtCompose(crt_lhs_x, this.primes);
        //System.out.println(challenger.checkSolution(x));
        
        
        
        // IGroupElement g_z = this.generator.power(this.multiplicativeGenerator);
        // //System.out.println(g_z);
        // var this_primes_length = this.primes.length;
        // BigInteger p_minus_1 = this.groupOrder.subtract(BigInteger.ONE);
        // BigInteger e_i;
        // BigInteger exp_i_k;
        // int q_i_int;
        
        // IGroupElement g_z_exp_i_k;
        
        // IGroupElement[] group_ele_crt_lhs_x = new IGroupElement[this_primes_length];
        // BigInteger[] crt_lhs_x = new BigInteger[this_primes_length];
        
        // for (int i = 0; i < this_primes_length; i++) {
        //   q_i_int = primes[i];
        //   //System.out.println(q_i_int);
        //   BigInteger q_i = BigInteger.valueOf(q_i_int);
        //   e_i = p_minus_1.divide(q_i); //compute exponent e_i
        //   //System.out.println(e_i);
        //   for (int k = 0; k < q_i_int; k++) {
        //     exp_i_k = e_i.multiply(BigInteger.valueOf(k));
        //     g_z_exp_i_k = this.cdh_power(g_z, exp_i_k);
        //     if (this.h.equals(g_z_exp_i_k)) {
        //       group_ele_crt_lhs_x[i] = g_z_exp_i_k;
        //       crt_lhs_x[i] = exp_i_k; 
        //       System.out.println("OK");
        //     }
        //   }
        // }
        
        // for (int i = 0; i < this_primes_length; i++) {
        //   System.out.println(crt_lhs_x[i]);
        // }
        
        
        
        
        
        //compute (p - 1) / q_i for all q_i in primes
        //public int[] values; this.values = new int[this.primes.length];
        
        // 
        
        // BigInteger[] exponent_list = new BigInteger[this_primes_length];
        
        // IGroupElement[] g_exp_list = new IGroupElement[this_primes_length];
        // IGroupElement[] h_exp_list = new IGroupElement[this_primes_length];
      
        // BigInteger e_i;
        
        // BigInteger[] crt_lhs_x = new BigInteger[this_primes_length];
        
        // BigInteger p_minus_1 = this.groupOrder.subtract(BigInteger.ONE);
        
        // for (int i = 0; i < this_primes_length; i++) {
        //   BigInteger q_i = BigInteger.valueOf(primes[i]);
        //   e_i = p_minus_1.divide(q_i); //compute exponent e_i
        //   exponent_list[i] = e_i;
        //   //exponentiate g^x = h with exponent e_i (=> (g^(e_i))^x = h^e_i)
        //   g_exp_i = this.generator.power(e_i);
        //   h_exp_i = this.power(e_i);
          
        //   g_exp_list[i] = g_exp_i;
        //   h_exp_list[i] = h_exp_i;
          
        //   //generate list and find exponent x_i
          
        // }
        
        
        
        
        
        
        //this.generator = challenge.generator;

        // You may assume that adversary is a perfect adversary.
        // I.e., cdh_solution will always be of the form g^(x * y) when you give the
        // adversary g, g^x and g^y in the getChallenge method below.

        // your reduction does not need to be tight. I.e., you may call
        // adversary.run(this) multiple times.

        //BigInteger groupOrder = challenge.generator.getGroupOrder();
        
        // Make use of the fact that the group order is of the form 1 + p1 * ... * pn
        // for many small primes pi !!
        //int[] primes = PrimesHelper.getDecompositionOfPhi(groupOrder);
        
        // Also, make use of a generator of the multiplicative group mod p.
        //BigInteger multiplicativeGenerator = PrimesHelper.getGenerator(groupOrder);

        // You can also use the method of CRTHelper
        //int[] values = new int[primes.length];
        //BigInteger composed = CRTHelper.crtCompose(values, primes);

        //return BigInteger.ZERO;
    }

    @Override
    public CDH_Challenge<IGroupElement> getChallenge() {
        // There is not really a reason to change any of the code of this method.
        return this.cdh_challenge;
    }

    /**
     * For your own convenience, you should write a cdh method for yourself that,
     * when given group elements g^x and g^y, returns a group element g^(x*y)
     * (where g is the generator from the DLog challenge).
     */
    private IGroupElement cdh(IGroupElement x, IGroupElement y) {
        // Use the run method of your CDH adversary to have it solve CDH-challenges:
        CDH_Challenge<IGroupElement> backup_cdh_challenge = this.cdh_challenge;
        this.cdh_challenge = new CDH_Challenge(this.generator, x, y);
        
        IGroupElement cdh_solution = adversary.run(this);
        this.cdh_challenge = backup_cdh_challenge; //restore from backup
        
        // You should specify the challenge in the cdh_challenge field of this class.
        // So, the above getChallenge method returns the correct cdh challenge to
        // adversary.
        return cdh_solution;
    }

    /**
     * For your own convenience, you should write a cdh_power method for yourself
     * that,
     * when given a group element g^x and a number k, returns a group element
     * g^(x^k) (where g is the generator from the DLog challenge).
     */
    private IGroupElement cdh_power(IGroupElement x, BigInteger exponent) {
        // For this method, use your cdh method and think of aritmetic algorithms for
        // fast exponentiation.
        // Use the methods exponent.bitLength() and exponent.testBit(n)!
        if (exponent.equals(BigInteger.ZERO)) {
          return this.generator;
        }
        if (exponent.equals(BigInteger.ONE)) {
          return x;
        }
        
        IGroupElement solution = this.generator;
        
        String bitstring = exponent.toString(2);
        var string_length = bitstring.length();
        //System.out.println(bitstring);
        //System.out.println(exponent.testBit(3));
        //int summe = 0;
        
        for (int i = 0; i < string_length; i++) {
          solution = this.cdh(solution, solution); //double
          //summe *= 2;
          if (bitstring.charAt(i) == '1') {
            solution = this.cdh(solution, x);
            //summe += 1;
          }
        }
        //System.out.println(summe);
        return solution;
    }
}
