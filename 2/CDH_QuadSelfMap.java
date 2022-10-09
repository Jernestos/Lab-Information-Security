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
		
		public IGroupElement g;
		public IGroupElement gx;
		public IGroupElement gy;
		
		public IGroupElement e;
		public BigInteger p;
		
		public void store_other_group_para(CDH_Challenge<IGroupElement> challenge) {
			this.p = challenge.generator.getGroupOrder();
			this.e = challenge.generator.power(this.p);
		}
		
		public void set(CDH_Challenge<IGroupElement> challenge) {
			this.g = challenge.generator;
			this.gx = challenge.x;
			this.gy = challenge.y;
		}
		
		public IGroupElement quad_map(IGroupElement g, IGroupElement a, IGroupElement b) {
			CDH_Challenge<IGroupElement> cdh_challenge = new CDH_Challenge<IGroupElement>(g, a, b);
			set(cdh_challenge);
			return adversary.run(this);
		}
		
		public IGroupElement solve(CDH_Challenge<IGroupElement> challenge) {
			
			/**
			 BigInteger getGroupOrder();
				IGroupElement multiply(IGroupElement otherElement);
				IGroupElement power(BigInteger exponent);
				IGroupElement invert();
				IGroupElement clone();
				boolean equals(IGroupElement otherElement);
			**/
			
			IGroupElement gd = quad_map(this.g, this.e, this.e);
			IGroupElement gd_inv = gd.invert();
			
			IGroupElement g_c_plus_d = quad_map(this.g, this.e, this.g);
			IGroupElement gc = g_c_plus_d.multiply(gd_inv);
			IGroupElement gc_inv = gc.invert();
			
			IGroupElement g_b_plus_d = quad_map(this.g, this.g, this.e);
			IGroupElement gb = g_b_plus_d.multiply(gd_inv);
			IGroupElement gb_inv = gb.invert();
			
			IGroupElement g_a_plus_b_plus_c_plus_d = quad_map(this.g, this.g, this.g);
			IGroupElement g_a_plus_b_plus_c = g_a_plus_b_plus_c_plus_d.multiply(gd_inv);
			IGroupElement g_a_plus_b = g_a_plus_b_plus_c.multiply(gc_inv);
			IGroupElement ga = g_a_plus_b.multiply(gb_inv);
			IGroupElement ga_inv = ga.invert();
			
			IGroupElement g_bx_plus_d = quad_map(this.g, challenge.x, this.e);
			IGroupElement g_bx = g_bx_plus_d.multiply(gd_inv);
			IGroupElement g_bx_inv = g_bx.invert();
			
			IGroupElement g_cy_plus_d = quad_map(this.g, this.e, challenge.y);
			IGroupElement g_cy = g_cy_plus_d.multiply(gd_inv);
			IGroupElement g_cy_inv = g_cy.invert();
			
			//sum of coef in exponent
			IGroupElement g_poly = quad_map(this.g, challenge.x, challenge.y);
			IGroupElement g_axy = g_poly.multiply(gd_inv).multiply(g_cy_inv).multiply(g_bx_inv);
			
			BigInteger two = BigInteger.valueOf(2);
			BigInteger p_minus_2 = this.p.subtract(two);
			IGroupElement g_xy = g_axy.power(p_minus_2);
			
			// //abxy + d in exponent
			// IGroupElement g_some_poly = quad_map(this.g, g_axy, this.e);
			// IGroupElement g_abxy = g_some_poly.multiply(gd_inv);
			// IGroupElement g_abxy_inv = g_abxy.invert();
			
			// //a^2xy + abxy + c + d in exponent
			// IGroupElement g_other_poly = quad_map(this.g, g_axy, this.g);
			// IGroupElement g_a2bxy = g_other_poly.multiply(gd_inv).multiply(gc_inv).multiply(g_abxy_inv);
			
			// BigInteger three = BigInteger.valueOf(3);
			// BigInteger p_minus_3 = this.p.subtract(three);
			
			
			// IGroupElement g_xy = g_a2bxy.power(p_minus_3);
			
			return this.g;
		} 
		
		@Override
		public IGroupElement run(I_CDH_Challenger<IGroupElement> challenger) {
				// This is one of the both methods you need to implement.

				// By the following call you will receive a DLog challenge.
				CDH_Challenge<IGroupElement> challenge = challenger.getChallenge();
				//System.out.println(challenge); //not null
				//Init.
				set(challenge);
				store_other_group_para(challenge);
				//IGroupElement test = adversary.run(this);
				//System.out.println(test);//not null
				// System.out.println(test);
				// System.out.println(test.invert().invert());
				return solve(challenge);
				
				//Prime most likely odd
				//System.out.println(this.p);
		
				// System.out.println(challenge.x);
				// System.out.println(this.gx);
				
				
				
				//BigInteger p = challenge.generator.getGroupOrder();
				//System.out.println(p);
				//IGroupElement test = adversary.run(challenger);
				//System.out.println(test);

				

				// your reduction does not need to be tight. I.e., you may call
				// adversary.run(this) multiple times.

				// Remember that this is a group of prime order p.
				// In particular, we have a^(p-1) = 1 mod p for each a != 0.

				//return solve(challenge);
		}

		@Override
		public CDH_Challenge<IGroupElement> getChallenge() {

				// This is the second method you need to implement.
				// You need to create a CDH challenge here which will be given to your CDH
				// adversary.

				IGroupElement generator = this.g;
				IGroupElement x = this.gx;
				IGroupElement y = this.gy;
				// Instead of null, your cdh challenge should consist of meaningful group
				// elements.
				CDH_Challenge<IGroupElement> cdh_challenge = new CDH_Challenge<IGroupElement>(this.g, this.gx, this.gy);
				return cdh_challenge;
		}
}
