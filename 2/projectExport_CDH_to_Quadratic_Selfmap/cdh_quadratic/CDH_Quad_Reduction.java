package cdh_quadratic;

import java.math.BigInteger;
import cdh.CDH_Challenge;
import cdh.I_CDH_Challenger;
import genericGroups.IGroupElement;

/**
 * This is the file you need to implement.
 * 
 * Implement the methods {@code run} and {@code getChallenge} of this class.
 * Do not change the constructor of this class.
 */
public class CDH_Quad_Reduction extends A_CDH_Quad_Reduction<IGroupElement> {

    /**
     * Do NOT change or remove this constructor. When your reduction can not provide
     * a working standard constructor, the TestRunner will not be able to test your
     * code and you will get zero points.
     */
    public CDH_Quad_Reduction() {
        // Do not add any code here!
    }
    
    BigInteger p;
  
    IGroupElement g;
    IGroupElement gx;
    IGroupElement gy;
    
    IGroupElement e;
    
    public void setup(CDH_Challenge<IGroupElement> challenge) {
      this.g = challenge.generator;
      this.gx = challenge.x;
      this.gy = challenge.y;
      this.p = challenge.generator.getGroupOrder();
      this.e = challenge.generator.power(BigInteger.ZERO);
    }
    
    public IGroupElement quad_map(IGroupElement g, IGroupElement x, IGroupElement y) {
      IGroupElement backup_g = this.g;
      IGroupElement backup_gx = this.gx;
      IGroupElement backup_gy = this.gy;
      
      this.g = g;
      this.gx = x;
      this.gy = y;
      
      IGroupElement ret_value = adversary.run(this);
      
      this.g = backup_g;
      this.gx = backup_gx;
      this.gy = backup_gy;
      
      return ret_value;
    }
 
    @Override
    public IGroupElement run(I_CDH_Challenger<IGroupElement> challenger) {
        // This is one of the both methods you need to implement.

        // By the following call you will receive a DLog challenge.
        CDH_Challenge<IGroupElement> challenge = challenger.getChallenge();
        setup(challenge);
        
        //System.out.println(challenge);
        // your reduction does not need to be tight. I.e., you may call
        // adversary.run(this) multiple times.

        // Remember that this is a group of prime order p.
        // In particular, we have a^(p-1) = 1 mod p for each a != 0.
        
        
        // IGroupElement g_whole_square_poly = quad_map(this.g, this.gx, this.gy);
      
        // IGroupElement gd = quad_map(this.g, this.e, this.e);
        // IGroupElement gd_inv = gd.invert();
        
        // IGroupElement g_whole_square_poly_no_d = g_whole_square_poly.multiply(gd_inv);
        
        // IGroupElement g_cy_d = quad_map(this.g, this.e, this.gy);
        // IGroupElement g_cy = g_cy_d.multiply(gd_inv);
        // IGroupElement g_cy_inv = g_cy.invert();
        
        // IGroupElement g_bx_d = quad_map(this.g, this.gx, this.e);
        // IGroupElement g_bx = g_bx_d.multiply(gd_inv);
        // IGroupElement g_bx_inv = g_bx.invert();
        
        // IGroupElement g_axy = g_whole_square_poly_no_d.multiply(g_cy_inv).multiply(g_bx_inv);
        
        Boolean debugging = false;
        
        IGroupElement g_d = quad_map(this.g, this.e, this.e);
        IGroupElement g_c_d = quad_map(this.g, this.e, this.g);
        IGroupElement g_b_d = quad_map(this.g, this.g, this.e);
        IGroupElement g_a_b_c_d = quad_map(this.g, this.g, this.g);
        IGroupElement g_a = g_a_b_c_d.multiply(g_c_d.invert()).multiply(g_b_d.invert()).multiply(g_d);
        
        IGroupElement g_c = g_c_d.multiply(g_d.invert());
        
        //testing
        //g_a = this.g.power(BigInteger.valueOf(3)); //a == 3
        
        IGroupElement g_a2_poly = quad_map(this.g, g_a, this.g);
        IGroupElement g_ab_d = quad_map(this.g, g_a, this.e);
        IGroupElement g_a2 = g_a2_poly.multiply(g_ab_d.invert()).multiply(g_c.invert());
        
        
        
        // if (g_a2.equals(this.g.power(BigInteger.valueOf(9)))) {
        //   System.out.println("2 - OK");
        // }
        
        IGroupElement g_ab = g_ab_d.multiply(g_d.invert());
        
        IGroupElement g_a3_poly = quad_map(this.g, g_a, g_a);
        IGroupElement g_ac_d = quad_map(this.g, this.e, g_a);
        IGroupElement g_a3 = g_a3_poly.multiply(g_ac_d.invert()).multiply(g_ab.invert());
        
        IGroupElement g_ad = quad_map(g_a, this.e, this.e);
        
        if (debugging) {
          IGroupElement temp = quad_map(g_a, g_a, g_a);
          IGroupElement test_g_a2 = temp.multiply(quad_map(g_a, this.e, g_a).invert()).multiply(g_ab.invert());
          if(test_g_a2.equals(g_a2)) {
            System.out.println("OK2"); //a^2 correct
          }
          
          temp = quad_map(g_a, test_g_a2, g_a);
          IGroupElement g_ac = g_ac_d.multiply(g_d.invert());
          IGroupElement aux = quad_map(g_a, test_g_a2, this.e);
          
          IGroupElement test_g_a3 = temp.multiply(aux.invert()).multiply(g_ac.invert());
          if(test_g_a3.equals(g_a3)) {
            System.out.println("OK3"); //a^3 correct
          }
          
        }
        
        
        IGroupElement g_axy_poly = quad_map(this.g, this.gx, this.gy);
        IGroupElement g_bx_d = quad_map(this.g, this.gx, this.e);
        IGroupElement g_cy_d = quad_map(this.g, this.e, this.gy);
        IGroupElement g_axy = g_axy_poly.multiply(g_bx_d.invert()).multiply(g_cy_d.invert()).multiply(g_d); //correct
        
        //INSERT here ingenious trickery
      
        //BigInteger p_minus_3 = BigInteger.valueOf(7).subtract(BigInteger.valueOf(2));
        BigInteger p_minus_3 = this.p.subtract(BigInteger.valueOf(3));
        String bitstring = p_minus_3.toString(2);
        var string_length = bitstring.length();
        
        if (debugging) {
          System.out.println(bitstring); //first bit is always 1
        }
        
        IGroupElement target;
        char curr_bit = bitstring.charAt(1); //init, second bit
        
        //IGroupElement[] list = new IGroupElement[2];
        //IGroupElement[] temp_list = new IGroupElement[2];
        //int prev_b;
        //int curr_b;
        
        //list[0] = g_a2;
        //list[1] = g_a3;
        
        if (curr_bit == '0') {
          target = g_a2;
        }
        else {
          target = g_a3;
        }
        
        // IGroupElement[] list = new IGroupElement[string_length];
        // list[0] = g_a;
        // list[1] = target;
        
        for (int i = 2; i < string_length; i++) { //already handled bit 0 and 1 (from left to right to read), begin with bit 3
          curr_bit = bitstring.charAt(i);
          
          IGroupElement g_a_double_poly = quad_map(g_a, target, target);
          IGroupElement g_ca_ad_part = quad_map(g_a, this.e, target);
          IGroupElement g_ba_ad_part = quad_map(g_a, target, this.e);
          IGroupElement g_a_double = g_a_double_poly.multiply(g_ca_ad_part.invert()).multiply(g_ba_ad_part.invert()).multiply(g_ad);
          
          target = g_a_double;
          
          if (curr_bit == '1') {
            IGroupElement g_a_double_plus_one_poly = quad_map(g_a, g_a_double, g_a);
            IGroupElement g_ca_ad_part_ = quad_map(g_a, this.e, g_a);
            IGroupElement g_ba_ad_part_ = quad_map(g_a, target, this.e);
            IGroupElement g_a_double_plus_one = g_a_double_plus_one_poly.multiply(g_ca_ad_part_.invert()).multiply(g_ba_ad_part_.invert()).multiply(g_ad);
            
            target = g_a_double_plus_one;
          }
          
          //list[i] = target;
          
        }
        
        // IGroupElement g_a4_poly = quad_map(g_a, g_a3, g_a);
        // IGroupElement temp1 = quad_map(g_a, this.e, g_a3);
        // IGroupElement temp2 = quad_map(g_a, target, this.e);
        
        
        
        //target = g^{a^-2}
        
        // if (target.equals(this.g)) {
        //   System.out.println("OK");
        // }
        
        //okay
        IGroupElement g_xy_some_poly = quad_map(this.g, g_axy, target);
        IGroupElement g_baxy_plus_d = quad_map(this.g, g_axy, this.e);
        IGroupElement g_target_plus_d = quad_map(this.g, this.e, target);
        IGroupElement g_xy = g_xy_some_poly.multiply(g_baxy_plus_d.invert()).multiply(g_target_plus_d.invert()).multiply(g_d); //g^xy
        
        return g_xy;
    }

    @Override
    public CDH_Challenge<IGroupElement> getChallenge() {

        // This is the second method you need to implement.
        // You need to create a CDH challenge here which will be given to your CDH
        // adversary.
        IGroupElement generator = null;
        IGroupElement x = null;
        IGroupElement y = null;
        // Instead of null, your cdh challenge should consist of meaningful group
        // elements.
        CDH_Challenge<IGroupElement> cdh_challenge = new CDH_Challenge<IGroupElement>(this.g, this.gx, this.gy);

        return cdh_challenge;
    }
}
