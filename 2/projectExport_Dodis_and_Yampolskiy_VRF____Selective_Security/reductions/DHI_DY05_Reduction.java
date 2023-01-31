package reductions;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import algebra.SimplePolynomial;
import dhi.DHI_Challenge;
import dhi.I_DHI_Challenger;
import dy05.DY05_PK;
import dy05.I_Selective_DY05_Adversary;
import genericGroups.IGroupElement;


public class DHI_DY05_Reduction implements I_DHI_DY05_Reduction {
    // Do not remove this field!
    private final I_Selective_DY05_Adversary adversary;

    public DHI_DY05_Reduction(I_Selective_DY05_Adversary adversary) {
        // Do not change this constructor!
        this.adversary = adversary;
    }
    
    public DHI_Challenge challenge;
    public IGroupElement generator;
    public IGroupElement e;
    public BigInteger p; //Zp
    public int list_size; //q + 1 is size of list
    public int q;
    
    public int x_star;
    public SimplePolynomial f;
    
    public IGroupElement[] list_g_pow_betas;
    
    public Boolean debugging;
    
    public void setup(DHI_Challenge challenge) {
      this.generator = challenge.get(0);
      this.e = this.generator.power(BigInteger.ZERO);
      this.p = this.generator.getGroupOrder();
      this.list_size = challenge.size();
      this.q = this.list_size - 1; //effective power alpha^q
    }
    
    public BigInteger[] compute_y() {
      
      BigInteger[] gammas = new BigInteger[this.q];
      BigInteger solution = f.get(this.q - 1);
      gammas[this.q - 1] = solution;
      
      for(int c_index = this.q - 2; c_index >= 0; --c_index) {
        solution = f.get(c_index).subtract(solution.multiply(BigInteger.valueOf(x_star)));
        solution = solution.mod(this.p);
        gammas[c_index] = solution; 
      }
      
      return gammas;
    }
    
    
    
    @Override
    public IGroupElement run(I_DHI_Challenger challenger) {
        // Write Code here!
        this.debugging = false;
        this.challenge = challenger.getChallenge();
        //var generator = challenge.get(0);
        //var order = generator.getGroupOrder();
        setup(challenge);

        //You can use the SimplePolynomial class to solve this task
        // var f = new SimplePolynomial(this.p, 0, 1);
        // System.out.println(f);
        // var g = new SimplePolynomial(this.p, 0, 1);
        // System.out.println(g);
        
        // var h = f.add(g);
        // System.out.println(h);
        // System.out.println(this.p);
        IGroupElement forgery = adversary.run(this);
        if (this.debugging) {
          System.out.print("Forgery: ");
          System.out.println(forgery);  
        }
        //forgery is of form g^{1/(x + beta)}
        // System.out.print("q: ");
        // System.out.println(this.q);
        
        
        BigInteger[] gammas = compute_y();
        
        IGroupElement solution = forgery;
        for(int j = 0; j <= this.q - 2; ++j) {
          solution = solution.multiply(this.list_g_pow_betas[j].power(gammas[j+1].negate()));
        }
        
        BigInteger y_1 = gammas[0];
        BigInteger y_1_inv = y_1.modInverse(this.p);
        
        solution = solution.power(y_1_inv);
        
        return solution;
        
        
        //BigInteger y_1_inv = y_1.modInverse(this.p);
        // SimplePolynomial z_plus_xi = new SimplePolynomial(this.p, 0, 1).shift(this.x_star);
        // SimplePolynomial g = this.f.div(z_plus_xi);
        
        // BigInteger c0 = this.f.get(0);
        // BigInteger y0 = g.get(0);
        
        // BigInteger y_1 = c0.subtract(y0.multiply(BigInteger.valueOf(this.x_star))).mod(this.p);
        // BigInteger y_1_inv = y_1.modInverse(this.p);
        
        // System.out.println(this.f);
        
        // // BigInteger y_1_over_xstar = g.eval(BigInteger.ZERO).mod(this.p);
        // // BigInteger y_1 = y_1_over_xstar.multiply(BigInteger.valueOf(this.x_star)).mod(this.p);
        // // BigInteger y_1_inv = y_1.modInverse(this.p);
        
        // IGroupElement solution = this.e;
        
        
        // //c_coef[d] = g.get(d).negate();
        
        // for(int j = 0; j <= this.q - 2; ++j) {
        //   solution = solution.multiply(this.list_g_pow_betas[j].power(g.get(j).negate()));
        // }
        
        // solution = solution.multiply(forgery);
        // solution = solution.power(y_1_inv);
        
        //return solution;
        
        // System.out.print("Poly: ");
        // System.out.println(g);
        
        // BigInteger d0 = this.f.get(0);
        // BigInteger y0 = g.get(0);
        
        // // BigInteger y_1 = d0.subtract(y0.multiply(BigInteger.valueOf(x_star)));
        // // y_1 = y_1.mod(this.p); //ring modulo p
        // BigInteger y_1_inv = this.f.get(0).modInverse(this.p);
        // //System.out.println(y_1);
        
        // IGroupElement solution = this.e;
        
        
        // //c_coef[d] = g.get(d).negate();
        
        // for(int j = 0; j <= this.q - 2; ++j) {
        //   solution = solution.multiply(this.list_g_pow_betas[j].power(g.get(j).negate()));
        // }
        
        // solution = solution.multiply(forgery);
        // solution = solution.power(y_1_inv);
    
        //return this.generator;
    }

    @Override
    public void receiveChallengePreimage(int _challenge_preimage) throws Exception {
        // Write Code here!
        this.x_star = _challenge_preimage;
        if (this.debugging) {
          System.out.println(this.x_star);
        }
        // System.out.print("receive challenge: ");
        // if (_challenge_preimage == 0) {
        //   throw new ArithmeticException("_challenge_preimage has value 0");
        // }
        // else {
        //   this.x_star = _challenge_preimage;
        //   System.out.println(this.x_star);
        // }
        
        
        // System.out.print("receive challenge: ");
        // this.x_star = _challenge_preimage;
        // if (this.x_star == 20) {
        //   System.out.println("HEY ASDF ASDF ASDF 20000 200 ADF");
        //   System.out.print("Looky at challengy: ");
        // }
        // System.out.println(this.x_star);
    }

    @Override
    public IGroupElement eval(int preimage) {
        // Write Code here!
        if (this.debugging) {
          System.out.println("Eval");
        }
        
        SimplePolynomial z_plus_xi = new SimplePolynomial(this.p, 0, 1).shift(preimage);
        SimplePolynomial f_i = this.f.div(z_plus_xi);
        
        BigInteger[] d_coef = new BigInteger[this.q];
        
        for(int j = 0; j < this.q - 1; ++j) { //j <= q - 2
          d_coef[j] = f_i.get(j);
        }
        
        IGroupElement signature = this.e;
        
        for(int j = 0; j < this.q - 1; ++j) {
          signature = signature.multiply(list_g_pow_betas[j].power(d_coef[j]));
        }
      
        return signature;
  
    }
    
    public int[] get_binof_coef(int power) {
      int[] table = new int[power + 1];
      
      table[0] = 1;
      for(int level_i = 1; level_i <= power + 1; ++level_i) {
        for (int i = level_i-1; i > 0; i--) {
          table[i] = table[i] + table[i - 1];
        }
      }
          
      // for (int i = 0; i < power + 1; ++i) {
      //   System.out.println(table[i]);
      // }
      
      return table;
    }
    
    //IGroupElement[]
    public IGroupElement[] get_g_pow_betas() {
      BigInteger x0 = BigInteger.valueOf(-this.x_star); //TO CHECK
      //minus x_star is in x0;
      IGroupElement[] g_beta_table = new IGroupElement[list_size]; //table[0] is g
      g_beta_table[0] = this.generator;
      
      for (int i = 1; i < list_size; ++i) { //i <= this.q
        //var poly_order_i = new SimplePolynomial(this.p, 2 ,4);
        int[] bin_coefs = get_binof_coef(i);
        IGroupElement g_beta_pow_i = this.e;
        for (int j = i; j > -1; --j) { //j>= 0; get g^a^j
          BigInteger x0_power_j = x0.pow(i - j);
          BigInteger exponent = x0_power_j.multiply(BigInteger.valueOf(bin_coefs[j]));
          g_beta_pow_i = g_beta_pow_i.multiply(this.challenge.get(j).power(exponent));
        }
        g_beta_table[i] = g_beta_pow_i;
      }
      return g_beta_table;
    }
    
    public BigInteger[] c_coef_list() {
      
      SimplePolynomial res_f = new SimplePolynomial(this.p, 1);
      SimplePolynomial temp;
      for (int w = 0; w < this.q; w++) {
        if (w != x_star) {
          temp = new SimplePolynomial(this.p, 0, 1).shift(w); //since x_star from Zp, ring modulo p
          res_f = res_f.multiply(temp);
          // System.out.print(w);
          // System.out.print(" ");
        }
      }
      //System.out.println();
      this.f = res_f;
      int deg = this.f.degree;
      // System.out.print("degree = ");
      // System.out.println(deg);
      
      BigInteger[] c_coef = new BigInteger[deg + 1];
      
      for (int d = 0; d <= deg; d++) {
        c_coef[d] = this.f.get(d);
      }
      return c_coef;
    }
    
    @Override
    public DY05_PK getPK() {
        // Write Code here!
        if (this.debugging) {
          System.out.println("getPK");
        }
        
        this.list_g_pow_betas = get_g_pow_betas();
        BigInteger[] c_coef = c_coef_list();
        
        if (this.debugging) {
          if (this.list_g_pow_betas.length == c_coef.length + 1) { //sanity check
            System.out.println("OKM"); //is correct
          }
        }
        
        IGroupElement h = this.e;
        for(int j = 0; j < this.q; j++) { //j <= q - q
          h = h.multiply(this.list_g_pow_betas[j].power(c_coef[j]));
        }
        
        //this.generator = h;
        
        IGroupElement h_beta = this.e;
        for(int j = 1; j <= this.q; j++) {
          h_beta = h_beta.multiply(this.list_g_pow_betas[j].power(c_coef[j-1]));
        }

        return new DY05_PK(h, h_beta);
    }
}
